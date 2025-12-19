# Project Planning and Discovery Q and A

## 1. Business Requirements
Q: What problem does this solve and for whom?
A: There have been a lot of cases of reports of ICE across my city. I want to build some sort of web hosted map based tracker that aggregates any reports of ICE activity from various sources like reddit.com/r/columbus, facebook posts in the local area, groups, and anything else, that way I can keep people alert.

Q: What are your success metrics?
A: Success metrics are something that is a map that shows a chronological list of any posts, comments or alerts, and a pin on the map if location data can be gathered, and any pics included if possible. Success metrics are having the site live.

Q: Timeline and resource constraints?
A: Timeline is as soon as I can, resource constraints are it must be free. We can develop it ourselves.

## 2. Technical Scale and Performance
Q: Expected users or traffic (roughly: daily visitors, spikes during alerts)?
A: Unsure but it should be able to handle spikes.

Q: Data volume (how many reports per day or week; how long should data be retained)?
A: Also unsure reports, probably 10-100 per day if I had to randomly guess. Data should be retained indefinitely.

Q: Performance requirements (map load time, update frequency, real time vs periodic)?
A: As smoothly and efficiently as possible.

Q: Must integrate with existing systems or data sources (APIs, webhooks, RSS, scrapers)?
A: Look at how I have the couchfinder project working for scraping. There is a good scraping system in there for facebook and craigslist, I think we could utilize that to scrape sites.

## 3. Security and Compliance
Q: What sensitive data will you handle (e.g., names, exact locations, photos, user submitted tips)?
A: All we need to do is provide a link to the post, comment, etc. and the contents of it. No need to include the user who reported it in the map. Exact locations or reports are important.

Q: Any regulatory requirements (GDPR or CCPA, local privacy laws)?
A: No regulatory requirements except for making sure this is a secure program.

Q: Authentication or authorization approach (public access vs accounts; who can submit or edit)?
A: Only my bot that will scrape will submit, and I can edit it. No one is posting to it, just the bot is gathering data.

Q: Do you need safeguards for data accuracy, abuse, or compliance with source site terms (e.g., Reddit or Facebook ToS, scraping limits)?
A: No safeguards. This is not anything against any ToS.

## 4. Technology Stack
Q: Language or framework preferences?
A: Whatever works best, I am open to any language.

Q: Hosting preferences (AWS, Azure, self hosted, etc.)?
A: Whatever will allow me to host for free, be publicly accessible and secure. I do not care what the final URL is as long as I can somewhat customize it, for example iceout.hostingservicedomain.io. I made up iceout as the name; I do not know what it will be.

Q: Database requirements (SQL vs NoSQL, geo query support)?
A: Database, whatever is free and secure. Would likely need to be cloud hosted. Supabase?

Q: Mapping library preference (Mapbox, Leaflet, Google Maps)?
A: Whatever is most accurate, secure, scalable, free, and most applicable for this project.

## 5. Development and Operations
Q: Team size and experience level?
A: You and I, master level.

Q: CI or CD and testing strategy (even minimal is fine)?
A: Explain.

Q: Monitoring or alerting requirements (uptime checks, error logging)?
A: Industry standard.
