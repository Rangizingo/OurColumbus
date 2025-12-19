"""
OurColumbus Database Module
Supabase client wrapper for CRUD operations on reports.
"""
import logging
from typing import List, Set, Optional
from datetime import datetime, timedelta

from supabase import create_client, Client

from config import SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_ANON_KEY
from models import Report, Source

logger = logging.getLogger(__name__)

# Global client instances
_service_client: Optional[Client] = None
_anon_client: Optional[Client] = None


def get_service_client() -> Client:
    """Get Supabase client with service role (full access)."""
    global _service_client
    if _service_client is None:
        _service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _service_client


def get_anon_client() -> Client:
    """Get Supabase client with anon key (read-only via RLS)."""
    global _anon_client
    if _anon_client is None:
        _anon_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _anon_client


def get_seen_ids(source: Optional[Source] = None) -> Set[str]:
    """
    Get set of already-seen report IDs for deduplication.

    Args:
        source: Optional filter by source ('reddit' or 'facebook')

    Returns:
        Set of (source, source_id) composite keys as strings
    """
    client = get_service_client()

    query = client.table("reports").select("source, source_id")

    if source:
        query = query.eq("source", source.value)

    response = query.execute()

    # Create composite keys for deduplication
    seen = set()
    for row in response.data:
        key = f"{row['source']}:{row['source_id']}"
        seen.add(key)

    logger.debug(f"Found {len(seen)} existing reports in database")
    return seen


def store_reports(reports: List[Report]) -> int:
    """
    Store new reports in the database.

    Args:
        reports: List of Report objects to store

    Returns:
        Number of reports successfully stored
    """
    if not reports:
        return 0

    client = get_service_client()
    stored = 0

    # Convert to dicts for insertion
    rows = [report.to_dict() for report in reports]

    try:
        # Upsert to handle any duplicates gracefully
        response = client.table("reports").upsert(
            rows,
            on_conflict="source,source_id"
        ).execute()

        stored = len(response.data)
        logger.info(f"Stored {stored} reports in database")

    except Exception as e:
        logger.error(f"Error storing reports: {e}")
        # Try inserting one by one to save what we can
        for report in reports:
            try:
                client.table("reports").upsert(
                    report.to_dict(),
                    on_conflict="source,source_id"
                ).execute()
                stored += 1
            except Exception as inner_e:
                logger.warning(f"Failed to store report {report.source_id}: {inner_e}")

    return stored


def get_reports(
    limit: int = 50,
    offset: int = 0,
    source: Optional[Source] = None,
    hours: Optional[int] = None,
    verified_only: bool = False,
) -> List[Report]:
    """
    Fetch reports from the database.

    Args:
        limit: Maximum number of reports to return
        offset: Number of reports to skip (for pagination)
        source: Optional filter by source
        hours: Optional filter to last N hours
        verified_only: If True, only return verified reports

    Returns:
        List of Report objects
    """
    client = get_anon_client()

    query = client.table("reports").select("*")

    if source:
        query = query.eq("source", source.value)

    if hours:
        cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        query = query.gte("scraped_at", cutoff)

    if verified_only:
        query = query.eq("is_verified", True)

    # Order by most recent first
    query = query.order("scraped_at", desc=True)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()

    reports = [Report.from_dict(row) for row in response.data]
    logger.debug(f"Fetched {len(reports)} reports from database")

    return reports


def get_reports_in_radius(
    center_lat: float,
    center_lng: float,
    radius_miles: float,
    limit: int = 100,
) -> List[Report]:
    """
    Fetch reports within a radius of a point.

    Args:
        center_lat: Center latitude
        center_lng: Center longitude
        radius_miles: Radius in miles
        limit: Maximum reports to return

    Returns:
        List of Report objects within the radius
    """
    client = get_anon_client()

    # Convert miles to meters for PostGIS
    radius_meters = radius_miles * 1609.34

    # Use PostGIS ST_DWithin for efficient radius query
    # Note: This requires the latitude/longitude to be indexed
    response = client.rpc(
        "get_reports_in_radius",
        {
            "center_lat": center_lat,
            "center_lng": center_lng,
            "radius_meters": radius_meters,
            "max_results": limit,
        }
    ).execute()

    if response.data:
        return [Report.from_dict(row) for row in response.data]
    return []


def get_report_count(source: Optional[Source] = None) -> int:
    """Get total count of reports."""
    client = get_anon_client()

    query = client.table("reports").select("id", count="exact")

    if source:
        query = query.eq("source", source.value)

    response = query.execute()
    return response.count or 0


def delete_old_reports(days: int = 90) -> int:
    """
    Delete reports older than specified days.

    Args:
        days: Delete reports older than this many days

    Returns:
        Number of reports deleted
    """
    client = get_service_client()

    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

    response = client.table("reports").delete().lt("scraped_at", cutoff).execute()

    deleted = len(response.data)
    logger.info(f"Deleted {deleted} reports older than {days} days")

    return deleted
