# BRAND_NOTES — Line Up Surf House (Anza, Agadir)

Phase 2 design direction. Facts referenced as SoT tags (SOURCE_OF_TRUTH.md). Build: `python3 tools/images.py` → `python3 tools/build.py` → `python3 /home/agent/agadir-pilot/tools/check_site.py .`

## 1. Positioning
- **What it sells emotionally:** being *right there*. The surf is the reason you came to Agadir; Line Up lets you check the water from your window, walk across the car park to the sand, and come home to a family who feeds you and sorts out the rest.
- **Customer:** surfers and would-be surfers (first-timers, improvers, families with kids over 5, couples, friends in a triple) who want a clean private room steps from Anza beach at a fair price, not a party hostel and not a resort. Mostly European + Moroccan travellers on phones, coming from Booking.com.
- **Primary conversion:** "Ask for dates" → a form that writes a WhatsApp message to +212 6 41 23 67 58 (orchestrator decision; WhatsApp on that number still to be confirmed with the owner). Secondary: Booking.com listing. Tertiary: `tel:`.
- **Visual thesis:** a surf publication about one day by one break. Crisp white and Atlantic blue, heavy horizon-wide type, thin horizon rules, the yellow of their soft-tops. Rhythmic, graphic, clean, energetic.

## 2. The creative concept (unique to this site): "A day on the line"
The homepage is one day at Line Up, told in five chapters — **01 First light → 02 First session → 03 Midday → 04 Second session → 05 Sunset** — then "Ask for dates".
- Every chapter opens on a **horizon marker**: a full-width rule with two thinner "swell" lines under it and a yellow sun sitting at that chapter's place in the day (rising half-disc at the left → low → overhead → lower → setting half-disc at the right). Scrolling the page plays the sun's arc. It is storytelling, never a schedule: no clock times, no forecast, no live data.
- Each chapter's background is that hour's flat colour, taken from their own photos: dawn (pale low sky) → Anza sky blue → noon white/sand → deep sea → night ink → board-yellow for the ask band. Flat bands, no gradients.
- **The cover sits on the real horizon.** The hero is the actual view from upstairs at Line Up. A hairline is drawn exactly on the photograph's horizon (detected by `tools/images.py`, aligned in CSS with container-query maths, so it holds at every width), labelled "the line-up". The headline and the hero copy stand on that line, like surfers sitting in the line-up.
- **"Sets":** images and quotes come in sets of three that grow in size (wave 1, 2, 3): the shop photo set in chapter 02, the review set in chapter 04.
- **The rooftop without a photo:** no rooftop photo exists, so the roof is a typographic panel — "THE ROOF" set horizon-wide, a yellow sun setting on a haze line over thin swell lines — next to a real (toned) window photo of late light over Anza, captioned honestly. No fake imagery.
- **The line-up glyph** (sun on a horizon over two swell lines) is the favicon, the menu-sheet divider, the footer top edge and the 404.

## 3. Palette (sampled with Pillow from the business's own photos)
| token | hex | source |
|---|---|---|
| `--ink` | #0f2533 | deep Atlantic band just below the horizon in the upstairs view (bk-03 sampled #2f5166, darkened for text) |
| `--sea` | #1f4257 | same sea band, mid-dark — chapter 04 background |
| `--sky` | #3d6cb9 | Anza sky high in the upstairs view (bk-03 sampled #4172c0, deepened 3 % for 4.8:1 with white) — chapter 02, links, room labels |
| `--dawn` | #e4eef7 | low sky at the horizon (bk-03 sampled #8dc2ec), lifted — chapter 01 |
| `--mural` | #7aa4cb | painted sea of the LINE UP mural (gm-owner-06) — reserve |
| `--board` | #ecd03c | yellow soft-tops by the mural (gm-owner-01 sampled #e0ca51) and Line Up tees/logo board (#c39f23 in shade) — primary buttons, suns, the "10" |
| `--pine` | #d6b27e | pine doors and oval room-name plaques (bk-80 / bk-26) — plaque badges |
| `--sand` | #f1ebe1 / `--sand-2` #bfa084 | Anza sand in the upstairs view (sampled #bfa084), lifted for panels |
| `--haze` | #f0debe | hazy late light over the sea (bk-17 sampled #e8dcc5) — text on night ink, duotone highlight |
| `--err` | #a3260f | form errors (4.9:1 on board yellow) |
Contrast: white on `--sky` 4.8:1; ink on `--board` 11:1; `--board` on `--sky` used only for ≥24 px bold display text.

## 4. Typography
Registered in `/home/agent/agadir-pilot/FONTS.md` (no overlap). Self-hosted woff2 in `site/assets/fonts/`, **3 files, 104 KB total**, `font-display:swap`, 2 preloaded. Google's *latin* subset already covers all French characters (é è à ç ô ï œ « » €), so no latin-ext file is needed for /fr/; unicode-range declared.
- **Anybody** (variable: width 50–150 %, weight 100–900; `anybody-latin.woff2`, 57 KB) — display + UI. Pushed to 120–150 % width and 820–900 weight it goes *horizon-wide*: the line-up as letterforms; at 100–112 % it is a clean sporty grotesk for nav, buttons, labels, form fields. No monospace anywhere (reserved for Hôtel Lynx).
- **Newsreader** 400 roman + 400 italic (static, 22 + 24 KB) — running text, leads, quotes: the editorial serif of a surf magazine. It is the inverse of Hyle (serif display + sans body).
- Scale (390 px → 1440 px): H1 cover 48 px / 110 % width → 90 px / 130 % (line-height .92) · H2 chapter 34 px → 74 px, 122 % · H3 21 px → 27 px, 112 % · H3 big 28 px → 46 px · lead 20 px → 26 px Newsreader · body 18 px → 19 px · labels 12.5 px Anybody 110 %, caps, +0.1em · room name 22 → 37 px · stat "10" 112 px → 224 px, 150 %.

## 5. Grid, spacing, imagery, motion
- **Grid:** 12 columns ≥960 px, max 1320 px content, gutters 24 px; side padding 20 px (<700) / 40 px. Spacing scale 4·8·12·16·24·32·48·64·96·128. Chapter padding clamp(48→112 / 64→136 px).
- **Image treatment:** their phone photos, cropped hard: horizon-led crops for views (sky = room for type), 4:5 portraits for rooms, the shop "set" bottom-aligned at growing heights. No filters except one honest slate/haze duotone on the hazy late-light window photo (sunset chapter). Every `<img>` has width/height + dominant-colour background; WebP q72–80; hero 31 KB (640w) / 48 KB (900w) / 42 KB (desktop). Captions in small caps say what and where ("Anza beach from upstairs at Line Up").
- **Motion:** CSS + IntersectionObserver only. Cover horizon line draws left→right on load; each chapter marker's rule draws and its sun rises into place; the roof panel's sun sinks onto the line. Content is fully visible without JS; `prefers-reduced-motion` disables all of it.

## 6. Navigation, CTAs, sticky action, forms
- **Desktop nav:** wordmark "LINE UP / SURF HOUSE · ANZA" left, four text links centred (Rooms · Surf school · The house · Anza), yellow "Ask for dates" right. Transparent white-on-sky over the cover; turns solid white once the cover is passed.
- **Mobile nav:** top bar shows wordmark + "Menu" (two-line horizon icon). It slides away once you leave the cover and is replaced by the **bottom dock** (Menu · WhatsApp us · Call). Both Menu buttons open a full-screen ink sheet: numbered links 01–05 set large in Anybody on hairline rules, a horizon with the setting sun, then WhatsApp / phone / Booking.com. aria-expanded synced, Esc closes and returns focus, link tap closes, focus trapped, body scroll locked.
- The dock hides while the Ask band or the footer is on screen (never covers the submit button or footer content; footer has 96 px bottom padding <960 px).
- **CTA treatment:** square-cornered, uppercase Anybody 112 % — `btn--sun` (board yellow, primary), `btn--ink` (form submit), `btn--line` / `btn--line-light` (secondary). Booking.com is always a quieter link or outline, never yellow.
- **Form styling:** on the board-yellow band; 2 px ink borders, square, 52 px tall, 17 px text (no iOS zoom), labels in Anybody caps; extras are ink-bordered chips that invert when checked; inline errors in `--err` + an ink summary bar.

## 7. Page map (EN root + FR mirror)
| page | EN | FR | status |
|---|---|---|---|
| Home | `/` | `/fr/` | EN built (phase 2) · FR phase 3 |
| Rooms | `/rooms/` | `/fr/chambres/` | phase 3 |
| Surf school & shop | `/surf/` | `/fr/surf/` | phase 3 |
| The house (family, breakfast, home cooking, rooftop, reviews) | `/house/` | `/fr/la-maison/` | phase 3 |
| Anza (place, practical bit, day trips) | `/anza/` | `/fr/anza/` | phase 3 |
| Ask for dates (full form) | `/book/` | `/fr/reserver/` | phase 3 |
| 404 | `/404.html` | — | built |
Rooftop and Reviews are folded into The house (no rooftop photos; reviews work better beside the family story). Until a page exists, `build.py` points its links at the matching homepage chapter (`#rooms`, `#surf`, `#family`, `#anza`, `#ask`).

### Section plans
**Home (built)**
1. Cover — kicker "Surf house · Anza beach, Agadir"; H1 "Stay beside the break."; lead (8 private rooms, a few steps from Anza beach [VERIFIED S1]; breakfast made by the family [VERIFIED S1 included / PROBABLE family]; own surf school + shop [VERIFIED S5,S2b]); Ask for dates; 9.6 on Booking.com [VERIFIED S1] + link. Image: `hero-m` / `hero-d` (bk-03 upstairs view).
2. 01 First light — "Check the water before breakfast." 4 of 8 rooms sea view [VERIFIED S1]; breakfast included, vegetarian & halal, changes daily, examples ("Today, maybe") [VERIFIED/PROBABLE S1,S2]; dietary needs / early flights [VERIFIED S2b]; quote Katharina (rooftop breakfast). Image: `window` (bk-47).
3. 02 First session — "Downstairs: the surf school." School + shop on the ground floor; lessons first-timers/improvers, private or small group, ask us [PROBABLE S2,S4]; board + wetsuit rental [VERIFIED S5]; prices → WhatsApp; "Zohair is often the one in the water with you" [PROBABLE, 3 independent]; quote Youness. Set: `shopfront` (gm-03, banner quoted), `boards` (gm-01), `wetsuits` (gm-05).
4. 03 Midday — "Midday: eat, rest, wander." Rooms: 8 private, no dorms, 4 types ×2 with beds/guests/bathroom facts [VERIFIED S1; R8 bathroom CONFLICT → "ask us about the bathroom set-up"], door plaques "Open face"/"Reef room" [VERIFIED photos]; policy line [VERIFIED S1]. Lunch at home on request, paid, not a restaurant [PROBABLE S2,S2b]. Anza: quiet local surf town, dinosaur footprints, fried fish, Saïd sorts taxis/trips [PROBABLE]. Practical bit: beach, free public parking [VERIFIED], bus few minutes [PROBABLE S6], airport taxi help [PROBABLE S2b], Paradise Valley trips — ask [PROBABLE], languages [VERIFIED]. Images: `room-seaview` (bk-73), `room-triple` (bk-46), `room-private` (bk-55), `room-compact` (bk-80).
5. 04 Second session — "Back out. Then back to the family." Some evenings a brother paddles out [PROBABLE]; family house, Saïd & Zohair brothers [VERIFIED S2b]; "10 — Staff score on Booking.com" [VERIFIED S1]; quote set Garig · Piekarec · Zoe.
6. 05 Sunset — "Sunset from the roof." Roof terrace, sun over the Atlantic [PROBABLE S2,S2b; terrace VERIFIED S1]; "Some evenings everyone ends up at the same table" [PROBABLE]. Typographic roof panel; image `late-light` (bk-17, duotone, captioned).
7. Ask for dates — compact WhatsApp form (spec §8) + Booking.com alternative.
8. Footer — wordmark, mural line "accommodation · Surf School · Shop" [VERIFIED S5], address, Maps, WhatsApp/tel/Booking, languages, check-in/out, kids over 5, no pets/parties.

**Rooms** — intro (8 private rooms, no dorms, new + very clean, towels, Wi-Fi) · the 4 types in detail, 2–4 photos each (bk-73/34/44 sea-view twin; bk-46/29/66 triple; bk-55/06 private; bk-80/26/22/23 compact) · door names (only the two seen) · what's in every room / what we don't have (no cribs/extra beds) · check-in/out · Ask for dates (room preselected via `?room=`).
**Surf** — school + shop downstairs (gm-03, gm-04, gm-05, gm-01, gm-07 logo board) · lessons (levels, private/small group, kids — ask) · who teaches (brothers; Zohair often) + Youness, Gildo, Piekarec quotes · rental (soft-tops, hard boards, wetsuits; non-guests ask) · prices → WhatsApp · Anza beach in front (window views bk-03/45/32). No forecast, packages, trips, prices.
**The house** — family-run (Saïd & Zohair, family breakfast) · breakfast detail + Safae/Katharina quotes · home cooking on request (tajines, lubya; order ahead, paid) · the roof (typographic panel; replace with real photo when the owner sends one) · help: taxis, airport taxi, day trips, SIM/tips · reviews: 9.6 / staff 10 / value 9.8 / Google 4.9 + 6 quotes · house rules.
**Anza** — quiet local surf town, beach in front, dinosaur footprints, cafés/fried fish, bus stop, free parking, day trips (Paradise Valley — ask), "real, not polished". Optional CONTEXT-ONLY Anza beach imagery clearly captioned as the beach, never as the house. No distances/times to airport/Taghazout.
**Book** — full form (§8) + Booking.com + tel + address/map link.

## 8. Conversion flow (verified channels only)
Channels: WhatsApp `https://wa.me/212641236758` and `tel:+212641236758` (number VERIFIED S3; WhatsApp use = orchestrator decision, confirm with owner) · Booking.com `https://www.booking.com/hotel/ma/line-up-surf-house.html` [VERIFIED S1]. No email exists.
- **Fields:** check-in (date, required, ≥ today) · check-out (date, required, > check-in; auto-set to +1 night) · adults (1–10, default 2) · children over 5 (0–6) · room (any / sea view double-twin / sea-view triple / private bathroom double-twin / compact double-twin) · also interested in (surf lessons · board & wetsuit rental · help with an airport taxi · home-cooked lunch or dinner) · name (optional) · anything else (optional textarea: level, arrival time, dietary needs). Book page (phase 3) may add: arrival time select.
- **Validation:** client-side on submit; inline messages (`aria-invalid`, `aria-describedby`), summary bar with `role=alert`, focus to first bad field. Strings come from the page language (JSON in the form).
- **Compose → open:** `wa.me/212641236758?text=<encodeURIComponent(message)>` in a new tab; the form is replaced by a success panel: "Your message is ready in WhatsApp…" + **Didn't open? Tap here** (same URL) + call link + Booking.com + "Change something". Empty optional fields are omitted (never "undefined").
- **Message EN** (dates via `toLocaleDateString('en-GB')`):
```
Hello Line Up! I'd like to ask about a stay.

• Check-in: Sat, 14 Nov 2026
• Check-out: Tue, 17 Nov 2026 (3 nights)
• Guests: 2 adults, 1 child (over 5)
• Room: Sea view · double or twin
• Also interested in: surf lessons, board & wetsuit rental
• Note: Beginner, arriving late

Name: Ana

Sent from line-up-surf-house.peashoot.io
```
- **Message FR** (fr.py `FORM.msg`, dates `fr-FR`):
```
Bonjour Line Up ! J'aimerais avoir des infos pour un séjour.

• Arrivée : sam. 14 nov. 2026
• Départ : mar. 17 nov. 2026 (3 nuits)
• Voyageurs : 2 adultes, 1 enfant (plus de 5 ans)
• Chambre : Vue mer · double ou twin
• Intéressé·e aussi par : cours de surf, location planche et combinaison
• Note : débutante, arrivée tard

Nom : Ana

Envoyé depuis line-up-surf-house.peashoot.io
```
- **Fallbacks:** no JS → "Ask for dates" anchors still reach the band, and the dock / menu sheet / footer carry plain wa.me (generic hello), `tel:` and Booking.com links. WhatsApp not installed → wa.me web page; call and Booking.com links sit in the success panel.

## 9. Must NOT look like
- **Hyle Surfhouse** (hyle-surfhouse.peashoot.io): cream paper, Fraunces + Karla, teal/clay, warm host-centred intimacy, one man's story. Line Up: cool white + Atlantic blue + yellow, expanded grotesk over serif, family as a team, the day/horizon system leads.
- **Agadir Trip / Agadir Camel Horse** (sibling Peashoot tour sellers): no tour-card grids, prices, activity catalogues.
- **Hala Tours** (this batch): no multicolour travel-guide styling, mood tiles, photographic joy-collages.
- **Hôtel Lynx** (this batch): no monospace/label face, no wayfinding/transit-map signage, no room-number grids.
- Generic surf clichés: turquoise gradients, palm icons, surfboard/wave clip-art, "good vibes only", fake swell/forecast widgets, GoPro-barrel stock, sunset stock.
- Generic templates: white card grids, glassmorphism, black luxury, gradient text, icon-row "amenities", testimonial carousels, booking-engine fakery.
