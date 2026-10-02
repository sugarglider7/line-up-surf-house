# BUILD STATUS — line-up-surf-house

_Last updated: 2026-10-02 (research phase complete) by ResearchLineUp_

## Recovered state (resume of crashed run "agadir-batch2")
- Prior run left ONLY raw material (no repo, no status files, no code, no deployment):
  raw page dumps + downloaded images, now in `research/raw/` (gitignored; on disk at /home/agent/agadir-pilot/sites/line-up-surf-house/research/raw/). Original copy still at /tmp/sites2/line-up-surf-house/.
- Confirmed on 2026-10-02: no GitHub repo, no Cloudflare Pages project, no live line-up-surf-house.peashoot.io before this run.

## Research
- SOURCE_OF_TRUTH.md — DONE (S1–S9; contact block; facts by topic; ratings; people; 12 quotes; owner questions)
- CONTENT_INVENTORY.md — DONE (per page/section, ✓/~/✗ markers)
- ASSET_INVENTORY.md — DONE (92 images described from contact sheets; Best 12; gaps)
- research/notes-reviews.md, notes-surf-food-people.md, notes-rooms-house.md, notes-neighbourhood.md — DONE
- Raw (gitignored): booking_main.html, booking_reviews.json (208), booking_responses.json (73 first-party replies), google_reviews.json (91), gmaps_tbm.json, images/ (81 Booking + 11 Google-owner + 15 hires)
- Contact sheets: /home/agent/agadir-pilot/qa/line-up-surf-house/sheets/

## Design
- BRAND_NOTES.md — not started

## Pages implemented
- none

## Pages remaining
- all

## Factual uncertainties
- WhatsApp: only phone found is 06 41 23 67 58 (+212 6 41 23 67 58) on the Google listing. Family uses WhatsApp with guests, but WhatsApp on this number is UNVERIFIED → orchestrator decision before using wa.me.
- No Instagram/Facebook/email/own website found (searched; Instagram blocks curl).
- Rooftop exists per 2026 reviews + business replies, but NO photo of it.
- "Reef room" (cheapest twin) bathroom: Booking text says private, facility list says shared; reviews: in-room shower+basin, WC in corridor → CONFLICT.
- Lunch/dinner = on-request home cooking (PROBABLE, ~10 guests + business replies), not a restaurant; no prices.
- Surf: own school + shop + board/wetsuit rental VERIFIED; levels/formats/who teaches PROBABLE; no trips to other breaks, no prices, no packages.
- People: Saïd + Zohair (business's own spellings; brief's "Zouhair" is a guest spelling) — brothers, named by the business itself. Parents unnamed. "Rachid" (owner?) and "Ali" (instructor?) single-source → do not publish.
- Airport distance conflicting on Booking (16 vs 17 mi) → no distances/times to airport.
- Opening date conflicting → don't state.
- Booking prices seen are STALE (never show).
- Name collision: "THE LINE UP surf house & hostel" in Mirleft (Airbnb) is a different business.

## QA status
- not started (see QA_CHECKLIST.md)

## Deployment URL
- target: https://line-up-surf-house.peashoot.io/ (Cloudflare Pages project "line-up-surf-house", output dir `site/`, no build command) — not yet created

## Outstanding problems
- Image gaps: no rooftop, breakfast/food, people or surf-action photos; ask owner via Fadwa.

## Log
- 05:08 recovery: workspace created from prior raw research; brief + standard written.
- research: parsed Booking JSON (8 rooms, facilities, policies, 9.6/208 + subscores, AR/EN/FR); captured all 208 Booking reviews + 73 property responses and all 91 Google reviews (one browser tab, closed); Google listing data (4.9/91, phone, Hostel + Surf school); 11 Google owner photos downloaded.
- research: contact sheets built and reviewed; asset inventory + Best 12 + gaps written.
- research: SOURCE_OF_TRUTH, CONTENT_INVENTORY, notes committed and pushed.
