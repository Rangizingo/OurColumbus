"""
OurColumbus Configuration
Loads environment variables and defines constants.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Location Configuration - Columbus, OH (zip 43215)
CENTER_LATITUDE = float(os.getenv("CENTER_LATITUDE", "39.9612"))
CENTER_LONGITUDE = float(os.getenv("CENTER_LONGITUDE", "-82.9988"))
SEARCH_RADIUS_MILES = float(os.getenv("SEARCH_RADIUS_MILES", "50"))

# Scraper Configuration
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SCRAPE_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "15"))
BROWSER_DATA_DIR = Path(os.getenv("BROWSER_DATA_DIR", "./browser_data"))

# API Configuration
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# User agent for scraping
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Reddit Configuration
REDDIT_SUBREDDIT = "Columbus"
REDDIT_URL = f"https://www.reddit.com/r/{REDDIT_SUBREDDIT}"

# Facebook Configuration
FACEBOOK_SEARCH_LOCATION = "Columbus, Ohio"


def validate_config():
    """Validate that required configuration is present."""
    missing = []
    if not SUPABASE_URL:
        missing.append("SUPABASE_URL")
    if not SUPABASE_ANON_KEY:
        missing.append("SUPABASE_ANON_KEY")
    if not SUPABASE_SERVICE_KEY:
        missing.append("SUPABASE_SERVICE_KEY")

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return True
