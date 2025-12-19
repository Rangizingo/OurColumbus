# OurColumbus - Project Scope & Development Checklist

## Overview

**Project Name**: OurColumbus
**Purpose**: Community safety alert system that aggregates and displays ICE (Immigration and Customs Enforcement) activity reports from social media sources on an interactive map.

**Target Area**: 50-mile radius of zip code 43215 (Columbus, OH city center)

### Goals
- Scrape Reddit (r/Columbus) and Facebook for ICE-related posts
- Display reports on an interactive map with location pins
- Show chronological feed of all reports with links to original posts
- Provide accurate, timely information with minimal false negatives
- Host entirely for free

### Success Criteria
- [ ] Live, publicly accessible website
- [ ] Map displaying ICE activity reports with pins
- [ ] Chronological list of posts/comments/alerts
- [ ] Links to original source posts
- [ ] Images displayed when available
- [ ] Automated scraping every 15 minutes

---

## Architecture

### Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| **Backend/Scraper** | Python 3.11+ | Matches couchfinder pattern, Playwright support |
| **Web Scraping** | Playwright + BeautifulSoup | Anti-detection, proven pattern |
| **Database** | Supabase (PostgreSQL) | Free tier, geo queries, cloud-hosted |
| **Frontend** | Next.js / React | Free on Vercel, SSR for SEO |
| **Mapping** | Leaflet + OpenStreetMap | Free, accurate, no API key needed |
| **Backend Hosting** | Render | Free tier, cron jobs supported |
| **Frontend Hosting** | Vercel | Free tier, auto-deploy from Git |

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      OURCOLUMBUS SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Reddit     │    │   Facebook   │    │  (Future     │      │
│  │  r/Columbus  │    │  Local Groups│    │   Sources)   │      │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘      │
│         │                   │                                   │
│         ▼                   ▼                                   │
│  ┌─────────────────────────────────────┐                       │
│  │         SCRAPER SERVICE             │  ← Render (cron)      │
│  │  • Playwright + Stealth             │    Every 15 min       │
│  │  • Keyword matching                 │                       │
│  │  • Location extraction              │                       │
│  │  • Deduplication                    │                       │
│  └──────────────┬──────────────────────┘                       │
│                 │                                               │
│                 ▼                                               │
│  ┌─────────────────────────────────────┐                       │
│  │         SUPABASE DATABASE           │                       │
│  │  • reports table (with geo)         │                       │
│  │  • PostGIS for radius queries       │                       │
│  │  • Real-time subscriptions          │                       │
│  └──────────────┬──────────────────────┘                       │
│                 │                                               │
│                 ▼                                               │
│  ┌─────────────────────────────────────┐                       │
│  │         FRONTEND (Vercel)           │                       │
│  │  • Interactive Leaflet map          │                       │
│  │  • Chronological feed               │                       │
│  │  • Mobile responsive                │                       │
│  └─────────────────────────────────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Scraper** runs every 15 minutes on Render cron
2. **Fetches** new posts from Reddit and Facebook
3. **Filters** using keyword matching (broad capture)
4. **Extracts** location data when possible
5. **Stores** in Supabase with deduplication
6. **Frontend** fetches from Supabase API
7. **Displays** on map + chronological feed

---

## Keyword Strategy

### Tier 1 - High Confidence (Direct Match)
```
ICE raid, ICE agents, ICE officers, ICE spotted, ICE sighting,
ICE checkpoint, la migra, immigration raid, immigration enforcement,
immigration officers, deportation raid, federal immigration
```

### Tier 2 - Contextual (Requires Related Terms)
```
ICE + (spotted|seen|outside|near|at|parked|arrived|leaving)
unmarked + (SUV|vehicle|van|car) + (spotted|seen|agents)
federal agents + (detained|arrested|immigration)
checkpoint + (immigration|papers|ID)
```

### Tier 3 - Spanish Language
```
migra, redada, deportación, agentes de inmigración,
la migra está aquí, inmigración
```

### Tier 4 - Coded/Emoji
```
🧊 (ice emoji), "Hotel" (potential code)
```

### Exclusion Patterns (False Positive Reduction)
Posts containing these WITHOUT other indicators may be filtered:
```
weather, forecast, roads, driving conditions, hockey,
skating, freezer, ice cream, dry ice, ice cold
```

**Note**: Prefer false positives over false negatives. Collect broadly, refine later.

---

## Database Schema

### Table: `reports`

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `source` | TEXT | 'reddit' or 'facebook' |
| `source_id` | TEXT | Original post/comment ID |
| `source_url` | TEXT | Link to original post |
| `content` | TEXT | Post/comment text |
| `author` | TEXT | Original author (for dedup, not displayed) |
| `image_urls` | TEXT[] | Array of image URLs |
| `location_text` | TEXT | Raw location mentioned |
| `latitude` | FLOAT | Extracted/geocoded lat |
| `longitude` | FLOAT | Extracted/geocoded lng |
| `location_confidence` | TEXT | 'exact', 'approximate', 'none' |
| `matched_keywords` | TEXT[] | Which keywords triggered capture |
| `created_at` | TIMESTAMP | When post was created |
| `scraped_at` | TIMESTAMP | When we found it |
| `is_verified` | BOOLEAN | Manual verification flag |

### Indexes
- `idx_reports_location` - GiST index on (latitude, longitude)
- `idx_reports_created` - For chronological queries
- `idx_reports_source_id` - For deduplication

---

## Development Phases

### Phase 1: Foundation (Data Layer)
Setup project structure, database, and core models.

### Phase 2: Scraper Service
Build Reddit and Facebook scrapers using couchfinder patterns.

### Phase 3: API Layer
Create endpoints for frontend to fetch data.

### Phase 4: Frontend & Map
Build the user-facing website with interactive map.

### Phase 5: Deployment
Deploy all services to free hosting.

### Phase 6: Testing & Refinement
End-to-end testing, keyword tuning, bug fixes.

---

## Development Checklist

### Phase 1: Foundation

#### 1.1 Project Setup
- [ ] 1.1.1 Create project directory structure
- [ ] 1.1.2 Initialize Git repository
- [ ] 1.1.3 Create Python virtual environment
- [ ] 1.1.4 Create `requirements.txt` with dependencies
- [ ] 1.1.5 Create `.env.example` for environment variables
- [ ] 1.1.6 Create `.gitignore` (exclude .env, __pycache__, etc.)

#### 1.2 Supabase Setup
- [ ] 1.2.1 Create Supabase project (free tier)
- [ ] 1.2.2 Enable PostGIS extension for geo queries
- [ ] 1.2.3 Create `reports` table with schema above
- [ ] 1.2.4 Create indexes for performance
- [ ] 1.2.5 Set up Row Level Security (RLS) policies
- [ ] 1.2.6 Generate API keys and save to `.env`
- [ ] 1.2.7 Test connection from Python

#### 1.3 Core Models & Config
- [ ] 1.3.1 Create `config.py` with environment loading
- [ ] 1.3.2 Create `models.py` with Report dataclass
- [ ] 1.3.3 Create `database.py` with Supabase client wrapper
- [ ] 1.3.4 Implement `get_seen_ids()` for deduplication
- [ ] 1.3.5 Implement `store_reports()` for saving
- [ ] 1.3.6 Implement `get_reports()` for fetching
- [ ] 1.3.7 Write unit tests for database operations

**Phase 1 Acceptance**: Can connect to Supabase, CRUD operations work.

---

### Phase 2: Scraper Service

#### 2.1 Base Scraper Infrastructure
- [ ] 2.1.1 Create `scrapers/` directory
- [ ] 2.1.2 Create `scrapers/base.py` with abstract BaseScraper
- [ ] 2.1.3 Create `scrapers/keywords.py` with keyword lists
- [ ] 2.1.4 Implement keyword matching function (regex-based)
- [ ] 2.1.5 Test keyword matching with sample texts

#### 2.2 Reddit Scraper
- [ ] 2.2.1 Create `scrapers/reddit.py`
- [ ] 2.2.2 Implement Playwright browser initialization
- [ ] 2.2.3 Implement r/Columbus navigation
- [ ] 2.2.4 Implement post listing extraction
- [ ] 2.2.5 Implement comment extraction (expand threads)
- [ ] 2.2.6 Implement keyword filtering on content
- [ ] 2.2.7 Implement image URL extraction
- [ ] 2.2.8 Implement location text extraction (if mentioned)
- [ ] 2.2.9 Implement early-stop when hitting seen posts
- [ ] 2.2.10 Add rate limiting and delays
- [ ] 2.2.11 Test scraper manually

#### 2.3 Facebook Scraper
- [ ] 2.3.1 Create `scrapers/facebook.py` (adapt from couchfinder)
- [ ] 2.3.2 Implement persistent browser session
- [ ] 2.3.3 Implement login detection and manual login flow
- [ ] 2.3.4 Implement Columbus-area group/page navigation
- [ ] 2.3.5 Implement post extraction with keyword filtering
- [ ] 2.3.6 Implement image URL extraction
- [ ] 2.3.7 Implement location extraction
- [ ] 2.3.8 Implement deduplication with early-stop
- [ ] 2.3.9 Test scraper manually

#### 2.4 Location Processing
- [ ] 2.4.1 Create `location.py` for geo utilities
- [ ] 2.4.2 Implement Columbus area street/landmark detection
- [ ] 2.4.3 Implement geocoding (free service: Nominatim/OSM)
- [ ] 2.4.4 Implement 50-mile radius validation from 43215
- [ ] 2.4.5 Handle "no location found" gracefully
- [ ] 2.4.6 Test with sample location strings

#### 2.5 Scraper Orchestration
- [ ] 2.5.1 Create `main.py` scraper entry point
- [ ] 2.5.2 Implement scraper scheduling logic
- [ ] 2.5.3 Implement error handling and logging
- [ ] 2.5.4 Implement graceful shutdown
- [ ] 2.5.5 Test full scrape cycle locally

**Phase 2 Acceptance**: Scrapers run, find posts, store in Supabase.

---

### Phase 3: API Layer

#### 3.1 API Setup
- [ ] 3.1.1 Create `api/` directory
- [ ] 3.1.2 Set up FastAPI application
- [ ] 3.1.3 Configure CORS for frontend access
- [ ] 3.1.4 Add health check endpoint (`/health`)

#### 3.2 API Endpoints
- [ ] 3.2.1 `GET /api/reports` - List all reports (paginated)
- [ ] 3.2.2 `GET /api/reports/recent` - Last 24 hours
- [ ] 3.2.3 `GET /api/reports/geo` - Reports within radius
- [ ] 3.2.4 `GET /api/reports/:id` - Single report detail
- [ ] 3.2.5 Add query filters (source, date range, keyword)
- [ ] 3.2.6 Test all endpoints with curl/Postman

**Phase 3 Acceptance**: API returns data from Supabase correctly.

---

### Phase 4: Frontend & Map

#### 4.1 Frontend Setup
- [ ] 4.1.1 Initialize Next.js project in `frontend/`
- [ ] 4.1.2 Install dependencies (leaflet, react-leaflet, tailwind)
- [ ] 4.1.3 Configure environment variables for API URL
- [ ] 4.1.4 Set up basic layout and styling

#### 4.2 Map Component
- [ ] 4.2.1 Create Map component with Leaflet
- [ ] 4.2.2 Center on Columbus (39.9612, -82.9988)
- [ ] 4.2.3 Add 50-mile radius circle overlay
- [ ] 4.2.4 Implement report markers with popups
- [ ] 4.2.5 Color-code markers by recency (red=recent, yellow=older)
- [ ] 4.2.6 Add marker clustering for dense areas
- [ ] 4.2.7 Test map rendering and interactions

#### 4.3 Report Feed
- [ ] 4.3.1 Create ReportFeed component
- [ ] 4.3.2 Display chronological list of reports
- [ ] 4.3.3 Show: time, content preview, source icon, location
- [ ] 4.3.4 Link to original post (opens in new tab)
- [ ] 4.3.5 Display images in expandable gallery
- [ ] 4.3.6 Implement infinite scroll or pagination
- [ ] 4.3.7 Add "click to zoom on map" interaction

#### 4.4 UI Polish
- [ ] 4.4.1 Mobile responsive design
- [ ] 4.4.2 Dark mode support (optional)
- [ ] 4.4.3 Loading states and error handling
- [ ] 4.4.4 "Last updated" timestamp display
- [ ] 4.4.5 Add "Know Your Rights" resources link
- [ ] 4.4.6 Test on mobile devices

**Phase 4 Acceptance**: Website displays map with markers and feed.

---

### Phase 5: Deployment

#### 5.1 Backend Deployment (Render)
- [ ] 5.1.1 Create Render account
- [ ] 5.1.2 Create new Web Service from Git repo
- [ ] 5.1.3 Configure environment variables
- [ ] 5.1.4 Set up cron job for scraper (every 15 min)
- [ ] 5.1.5 Configure Playwright for headless Linux
- [ ] 5.1.6 Test scraper runs in cloud
- [ ] 5.1.7 Verify data appears in Supabase

#### 5.2 Frontend Deployment (Vercel)
- [ ] 5.2.1 Create Vercel account
- [ ] 5.2.2 Import Git repository
- [ ] 5.2.3 Configure environment variables (API URL)
- [ ] 5.2.4 Configure custom domain (if desired)
- [ ] 5.2.5 Test production build
- [ ] 5.2.6 Verify frontend loads and displays data

#### 5.3 DNS & Domain (Optional)
- [ ] 5.3.1 Choose subdomain (e.g., iceout.vercel.app)
- [ ] 5.3.2 Configure if custom domain purchased later

**Phase 5 Acceptance**: Site live, scraper running, data flowing.

---

### Phase 6: Testing & Refinement

#### 6.1 End-to-End Testing
- [ ] 6.1.1 Verify scraper finds real posts
- [ ] 6.1.2 Verify posts appear on map
- [ ] 6.1.3 Verify links to original posts work
- [ ] 6.1.4 Test on multiple devices/browsers
- [ ] 6.1.5 Load test with simulated traffic

#### 6.2 Keyword Tuning
- [ ] 6.2.1 Review captured posts for false positives
- [ ] 6.2.2 Identify missed posts (false negatives)
- [ ] 6.2.3 Adjust keyword lists based on real data
- [ ] 6.2.4 Add new coded language as discovered

#### 6.3 Monitoring
- [ ] 6.3.1 Set up uptime monitoring (UptimeRobot - free)
- [ ] 6.3.2 Configure error alerting
- [ ] 6.3.3 Monitor Supabase usage (stay in free tier)
- [ ] 6.3.4 Monitor Render usage

#### 6.4 Documentation
- [ ] 6.4.1 Update README with setup instructions
- [ ] 6.4.2 Document environment variables
- [ ] 6.4.3 Document how to add new scrapers

**Phase 6 Acceptance**: System stable, keywords tuned, monitoring active.

---

## Future Enhancements (Post-MVP)

- [ ] Push notifications for new alerts
- [ ] SMS/email alert subscriptions
- [ ] User-submitted reports (with moderation)
- [ ] Additional sources (Twitter/X, Nextdoor, news sites)
- [ ] Historical heatmap of activity
- [ ] Multi-city expansion
- [ ] Verification workflow for reports
- [ ] Mobile app (React Native)

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Reddit blocks scraping | High | Use stealth, respect rate limits, backup with API if needed |
| Facebook login required | Medium | Persistent session, manual login flow (like couchfinder) |
| Free tier limits exceeded | Medium | Monitor usage, optimize queries, cache aggressively |
| False positives overwhelm feed | Low | Keyword tuning, optional manual verification |
| Geocoding API limits | Low | Use free Nominatim, cache results, fallback to "no location" |
| Render cron job fails | Medium | Error logging, uptime monitoring, manual trigger option |

---

## File Structure

```
OurColumbus/
├── backend/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── reddit.py
│   │   ├── facebook.py
│   │   └── keywords.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── location.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map.tsx
│   │   │   ├── ReportFeed.tsx
│   │   │   └── ReportCard.tsx
│   │   ├── pages/
│   │   │   └── index.tsx
│   │   └── styles/
│   ├── package.json
│   └── .env.example
├── SCOPE.md
├── README.md
└── .gitignore
```

---

## Getting Started

After reviewing this scope:

1. Confirm scope is acceptable
2. Begin Phase 1.1 (Project Setup)
3. Work through checklist sequentially
4. Test each component before moving on
5. Deploy MVP after Phase 5
6. Refine in Phase 6

---

*Document created: 2025-12-19*
*Last updated: 2025-12-19*
