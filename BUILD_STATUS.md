# BUILD STATUS — line-up-surf-house

_Last updated: 2026-10-02 (phase 3 complete: all pages EN + FR, inquiry flow, QA, live check) by BuildLineUp_

## Recovered state (resume of crashed run "agadir-batch2")
- Prior run left ONLY raw material (no repo, no status files, no code, no deployment):
  raw page dumps + downloaded images, now in `research/raw/` (gitignored; on disk at /home/agent/agadir-pilot/sites/line-up-surf-house/research/raw/). Original copy still at /tmp/sites2/line-up-surf-house/.
- Confirmed on 2026-10-02: no GitHub repo, no Cloudflare Pages project, no live line-up-surf-house.peashoot.io before this run.

## Orchestrator review (phase 2 → phase 3, binding)
- Homepage proof approved: "A day on the line", Anybody + Newsreader, horizon rules with the sun's position, yellow board-colour CTA. Keep it.
- Keep claims about Saïd/Zohair exactly as soft as now (guest-experience phrasing, no titles). "Zohair is often the one in the water with you" and "Saïd is usually the one sorting out taxis, trips and tips" are the ceiling — do not go further.
- Phase 3: build the dedicated pages from the page map (rooms/stay, surf school & shop, the house incl. roof + food + family, Anza, ask for dates) + full FR mirror; homepage sections stay as chapters linking to them, not duplicates.
- 404 must be checked on the live site (local http.server doesn't serve it).
- Live: https://line-up-surf-house.peashoot.io/ (Cloudflare Pages project line-up-surf-house, output dir site/, auto-deploys on push to main).

## Research
- SOURCE_OF_TRUTH.md — DONE (S1–S9; contact block; facts by topic; ratings; people; 12 quotes; owner questions)
- CONTENT_INVENTORY.md — DONE (per page/section, ✓/~/✗ markers)
- ASSET_INVENTORY.md — DONE (92 images described from contact sheets; Best 12; gaps)
- research/notes-reviews.md, notes-surf-food-people.md, notes-rooms-house.md, notes-neighbourhood.md — DONE
- Raw (gitignored): booking_main.html, booking_reviews.json (208), booking_responses.json (73 first-party replies), google_reviews.json (91), gmaps_tbm.json, images/ (81 Booking + 11 Google-owner + 15 hires)
- Contact sheets: /home/agent/agadir-pilot/qa/line-up-surf-house/sheets/

## Design
- BRAND_NOTES.md — DONE: concept "A day on the line" (5 chapters, sun moves along a horizon rule; cover headline stands on the photo's real horizon), palette sampled from their photos, fonts Anybody + Newsreader (registered in FONTS.md, 3 self-hosted woff2, 104 KB), nav/dock/sheet, CTA + form spec, page map + per-page section plans, conversion flow EN+FR, must-not-look-like.
- Tooling: `tools/images.py` (Pillow, sequential, declarative SPEC → site/assets/img/*.webp + tools/img_manifest.json with sizes, dominant colour, detected horizon; favicons), `tools/build.py` (stdlib; content in `tools/content/en.py`, FR = parallel `fr.py` with the same keys; links to unbuilt pages fall back to homepage anchors; writes sitemap/robots/_headers/404).
- Design system: `site/assets/css/site.css` (40 KB, 9 KB gzip), `site/assets/js/site.js` (8.6 KB, deferred), favicon.svg + favicon-32.png + apple-touch-icon.png. Phase 3 added the inner-page system (day-strip masthead, chapter markers per page, ask band, "The day goes on" band, Anza cross-section) — see BRAND_NOTES §7.

## Pages implemented
- EN: `/` · `/rooms/` · `/surf/` · `/house/` · `/anza/` · `/book/`
- FR: `/fr/` · `/fr/chambres/` · `/fr/surf/` · `/fr/la-maison/` · `/fr/anza/` · `/fr/reserver/`
- `/404.html` (EN + FR text) · sitemap.xml (hreflang pairs) · robots.txt · _headers (cache + security headers)

## Pages remaining
- none

## Factual uncertainties
- WhatsApp: only phone found is 06 41 23 67 58 (+212 6 41 23 67 58) on the Google listing. ORCHESTRATOR DECISION (phase 2): use it for tel: AND wa.me/212641236758. **Open item: confirm with the owner that this number is on WhatsApp.**
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
- Phase 2: check_site OK (2 pages); 3 screenshot rounds (qa/line-up-surf-house/p2/).
- Phase 3: check_site OK (13 pages, 0 WARN); 2 screenshot rounds over every template at 390×844 + 1440×900, plus 360 px, menu open, 404, form filled + success EN/FR (qa/line-up-surf-house/p3/); 0 console errors, 0 failed requests on all 13 pages; no horizontal overflow at 360/390/1440; lang switch keeps page; form validation + decoded wa.me text EN/FR verified; dock never covers submit/footer; perf at 390: 166–241 KB before scroll, 6–9 requests, CLS 0. Details + claim table in QA_CHECKLIST.md.

## Deployment URL
- https://line-up-surf-house.peashoot.io/ (Cloudflare Pages project "line-up-surf-house", output dir `site/`, no build command). **Note: GitHub pushes did NOT auto-deploy in phase 3** (latest deployment stayed on 73baae3 after two pushes); deployments were triggered with `tools/cf-static-deploy.sh line-up-surf-house deploy`. Live = b962376, verified.

## Outstanding problems
- Image gaps: no rooftop, breakfast/food, people or surf-action photos; ask owner via Fadwa. The rooftop is carried by a typographic panel; replace/add photos when supplied.
- Hero desktop image is the 1536-px Booking upload scaled to 1396 px (slightly soft on 2× screens); a larger original from the owner would help.
- Owner questions still open (SOURCE_OF_TRUTH §g): WhatsApp on 06 41 23 67 58; brothers' spellings + OK to be named; lesson formats/prices; R8 "Reef room" bathroom; roof/breakfast/family/lesson photos.

## Log
- 05:08 recovery: workspace created from prior raw research; brief + standard written.
- research: parsed Booking JSON (8 rooms, facilities, policies, 9.6/208 + subscores, AR/EN/FR); captured all 208 Booking reviews + 73 property responses and all 91 Google reviews (one browser tab, closed); Google listing data (4.9/91, phone, Hostel + Surf school); 11 Google owner photos downloaded.
- research: contact sheets built and reviewed; asset inventory + Best 12 + gaps written.
- research: SOURCE_OF_TRUTH, CONTENT_INVENTORY, notes committed and pushed.
- phase 2: read contracts/inputs, looked at full-size photos, sampled palette with Pillow, registered Anybody + Newsreader in FONTS.md, self-hosted 3 woff2 files.
- phase 2: images.py (13 outputs, all ≤115 KB; horizon detection 0.725/0.725) + build.py + content/en.py + site.css + site.js + favicons; check_site OK.
- round 1 (390 + 1440): Newsreader files were swapped (italic served as roman) → fixed; mobile H1 broke into 4 lines → resized; Booking button wrapped under primary; desktop hero box shrank (aspect-ratio + max-height) leaving a white strip and misaligning the horizon → width:100%; hero copy sat over the white building → moved left; "Today, maybe" dots started lines → nbsp separators; rooms rows too tall on desktop → 180 px square thumbs; sepia late-light duotone looked vintage → slate/haze tone, frame edge cropped; submit label wrapped → "Continue in WhatsApp".
- round 2 (390 + 1440): mobile H1 too timid (2 small lines, empty sky) → 12.3vw / 110 % width, 3 lines standing on the horizon; "Ask for dates" wrapped beside the Booking button → single full-width primary + "9.6 on Booking.com · Book there" link line; spec labels column too wide on mobile → 6em.
- round 3 (390 + 1440 + 360): fold verified on both; ch1 window photo now sticky on desktop; breakfast items no longer break mid-item; en-GB date format in the WhatsApp text; nav sheet + form + success state screenshots saved; tab closed, preview stopped.
- phase 3: inner pages built from the page map (rooms, surf, house, anza, book) + full FR mirror (`tools/content/fr.py`, same keys, French review quotes from the captured corpus); masthead "day strip" (five hours on one horizon, sun at the page's hour), time-of-day markers inside pages, "The day goes on" band linking pages in day order; 8 new image outputs (Anza band levelled −2.69° so the line-up hairline sits on the real horizon); book form prefill (`?room=`, `?extra=`), robust date parsing, FR spacing (NBSP before : ; ! ? »).
- phase 3 QA round 1 → 2: house breakfast list overflow fixed; desktop mast H1 clamp; Anza band levelled + horizon re-measured; Anza mast H1/lead side by side on desktop; FR NBSP pass; "×2" + footer phone kept on one line; guest selects aligned; aria-current in nav; compact dock at <380 px; claims softened ("one staircase away", "LINE UP towels" in every room). QA_CHECKLIST, BRAND_NOTES §7, ASSET_INVENTORY phase-3 outputs written.
- deploy: pushes to main not picked up by Cloudflare → triggered production deploys via cf-static-deploy.sh (8b2c3ec, then b962376).
- live check (390, one tab): home, /rooms/, /book/, /fr/, /fr/la-maison/, 404 (custom page, HTTP 404, EN + FR) — first pass showed the Cloudflare Web Analytics beacon blocked by the new CSP (failed request) → CSP allows static.cloudflareinsights.com / cloudflareinsights.com; second pass: 0 failed requests, 0 console errors, 0 broken images, canonicals correct; live home 185 KB / 10 requests at 390. Tab closed, preview stopped.
