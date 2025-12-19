"""
OurColumbus Data Models
Dataclasses for reports and related entities.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class Source(str, Enum):
    """Supported data sources."""
    REDDIT = "reddit"
    FACEBOOK = "facebook"


class LocationConfidence(str, Enum):
    """Confidence level for extracted location."""
    EXACT = "exact"        # Street address or precise coordinates
    APPROXIMATE = "approximate"  # Neighborhood or general area
    NONE = "none"          # No location could be determined


@dataclass
class Report:
    """
    Represents an ICE activity report from social media.
    """
    source: Source
    source_id: str
    source_url: str
    content: str
    id: Optional[str] = None
    author: Optional[str] = None
    image_urls: List[str] = field(default_factory=list)
    location_text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_confidence: LocationConfidence = LocationConfidence.NONE
    matched_keywords: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    scraped_at: Optional[datetime] = None
    is_verified: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for database insertion."""
        return {
            "source": self.source.value if isinstance(self.source, Source) else self.source,
            "source_id": self.source_id,
            "source_url": self.source_url,
            "content": self.content,
            "author": self.author,
            "image_urls": self.image_urls,
            "location_text": self.location_text,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_confidence": (
                self.location_confidence.value
                if isinstance(self.location_confidence, LocationConfidence)
                else self.location_confidence
            ),
            "matched_keywords": self.matched_keywords,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else datetime.utcnow().isoformat(),
            "is_verified": self.is_verified,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Report":
        """Create Report from database row."""
        return cls(
            id=data.get("id"),
            source=Source(data["source"]),
            source_id=data["source_id"],
            source_url=data["source_url"],
            content=data["content"],
            author=data.get("author"),
            image_urls=data.get("image_urls", []),
            location_text=data.get("location_text"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            location_confidence=LocationConfidence(data["location_confidence"]) if data.get("location_confidence") else LocationConfidence.NONE,
            matched_keywords=data.get("matched_keywords", []),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            scraped_at=datetime.fromisoformat(data["scraped_at"]) if data.get("scraped_at") else None,
            is_verified=data.get("is_verified", False),
        )
