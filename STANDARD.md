# Agadir three-site build — binding standard (all agents read this first)

Three real Agadir businesses, three speculative but COMPLETE, deployed, owner-showable websites.
A local Peashoot rep (Fadwa) will show them to the real owners, often from her phone.
Quality bar: outrageous — for THAT business. Not maximum code. Not a shared template.

| slug | business | repo | live URL |
|---|---|---|---|
| hala-tours | Hala Tours Agadir | github.com/sugarglider7/hala-tours | https://hala-tours.peashoot.io/ |
| hotel-lynx | Hôtel Lynx | github.com/sugarglider7/hotel-lynx | https://hotel-lynx.peashoot.io/ |
| line-up-surf-house | Line Up Surf House | github.com/sugarglider7/line-up-surf-house | https://line-up-surf-house.peashoot.io/ |

Workspace: `/home/agent/agadir-pilot/sites/<slug>/` (git repo). Site brief: `sites/<slug>/BRIEF.md` (the client's words — binding).

---------------------------------------------------------------------
## 0. RESOURCE SAFETY (a previous run crashed this VM — obey literally)

The VM has **3.8 GB RAM and 2 vCPUs**. The last run died after several agents launched their own Chromium instances.

- **NEVER launch your own browser process**: no `chrome`/`chromium` CLI, no puppeteer/playwright scripts, no `--user-data-dir` profiles. Use ONLY the omp eval `browser` global (one shared Chromium). **At most ONE tab per agent**, never `persist: true`, and `await tab.close()` as soon as a check is done (and always before you finish).
- **NEVER spawn subagents** (no `task`, `agent()`, `workpool()`). The orchestrator controls concurrency.
- No npm/node_modules/frameworks/bundlers. Python 3 stdlib + Pillow (installed) only. `curl` OK.
- Image work: one image at a time, sequential loop, no multiprocessing. Never open images > 8000 px without `Image.draft`/thumbnail.
- Long-running local server: `python3 -m http.server <PORT> --directory site` as a NAMED bash service (unique name `<slug>-preview`); stop it (`proc://<name>/kill`) before finishing. Ports: hala-tours 8701, hotel-lynx 8702, line-up-surf-house 8703.
- Before a heavy step (browser session, bulk image processing), run `free -m`. If `available` < 700 MB: do not start it; wait 60 s and re-check; if still low, write state to BUILD_STATUS.md and report back.
- Do not dump huge content into your own context: grep/slice raw HTML, summarise into files. Keep tool outputs small.

## 1. CRASH RECOVERY (mandatory)

Repo root of every site holds (keep them current — another agent must be able to resume from them alone):
`BRIEF.md` (client brief, do not edit) · `SOURCE_OF_TRUTH.md` · `CONTENT_INVENTORY.md` · `ASSET_INVENTORY.md` · `BRAND_NOTES.md` · `BUILD_STATUS.md` · `QA_CHECKLIST.md` · (`LEGACY_CONTENT_INVENTORY.md` for Hala — existing website).
- `research/` = committed concise notes (`research/notes-*.md`); `research/raw/` = gitignored raw dumps & original image downloads (stay on disk).
- `site/` = the public web root (Cloudflare Pages output dir). Nothing outside `site/` is published.
- `BUILD_STATUS.md` sections: Research · Design · Pages implemented · Pages remaining · Factual uncertainties · QA status · Deployment URL · Outstanding problems · Log (timestamped one-liners). Update after EVERY milestone.
- Commit in your own repo at each milestone: `git add -A && git commit -m "<milestone>" && git push`. Only touch your own repo.

## 2. RESEARCH & FACTUAL INTEGRITY

Sources in priority: official website · official Instagram/Facebook · Google Business listing · Booking/Hostelworld · Tripadvisor/Viator/GetYourGuide · public reviews · other credible sources. Use `read` on URLs and `web_search`; the browser only when a page truly needs JS.

`SOURCE_OF_TRUTH.md` = every fact the site may state, each tagged:
- `[VERIFIED: S#]` — stated by an official/first-party or listing source (S# = row in its Sources table with URL + date checked). Use freely.
- `[PROBABLE: S#]` — consistent but secondary/old/review-derived → soften ("on request", "ask us").
- `[CONFLICT: S#,S#]` — sources disagree → pick only if one is clearly authoritative; else omit/neutralise.
- `[STALE]` — old prices/products/pages → never show as current.
- `[UNVERIFIED]` → do not publish.

NEVER invent: services, tours, rooms, prices, staff, owners, roles, amenities, pickup zones, hours, policies, languages, testimonials, booking conditions, distances/times.
Uncertain → omit, soften, "ask us", or design around it. Old prices → "Ask for today's price" / "Check today's price on WhatsApp".
Human names: use only first names publicly attached to the business; roles only when stated by the business itself or consistently and unambiguously across many independent reviews — then phrase as what guests experience ("Zouhair is often the one in the water with beginners"), never invented job titles or biographies.
Reviews: quote only real text (short excerpt, unedited meaning), attributed exactly as the platform shows it (first name/country if shown + platform). No fabricated or composite quotes. Ratings: exact verified figure + platform, no dates ("9.6 on Booking.com").

**Owner embarrassment test** — for every specific claim: could the owner, standing next to Fadwa, say "where the hell did you get that?" If yes → verify or remove.

## 3. COPY (write as the business; human, specific, no sludge)

Write in the business's own voice ("we"), short sentences, concrete nouns (place names, times, objects).
BANNED (hard): unforgettable · memories that last · embark · elevate · discover excellence · gateway to · where X meets Y · nestled · hidden gem · breathtaking · immerse yourself · escape the ordinary · once-in-a-lifetime · world-class · unparalleled · curated · seamless · bespoke · oasis — and their French twins (inoubliable, niché, à couper le souffle, plongez…). Soft (only if truly natural): discover, journey, authentic, magical, stunning, vibrant, paradise (except "Paradise Valley").
NEVER expose research method: no "mentioned in N reviews", "review-backed", "publicly verified", "according to Google reviewers", "guests often mention", rating dates, "verified guests".
Languages: **English (root) + French (`/fr/`) full mirrors**, hand-written natural French (not literal translation), `hreflang` pairs, language switch that keeps the current page. Arabic not required.

## 4. DESIGN (outrageously good for THIS business)

Before coding, `BRAND_NOTES.md` must contain: what the business sells emotionally · who the customer is · primary conversion action · visual thesis · typography direction (exact families + why) · palette (hex, derived from the business's own photos/signage/logo) · photographic direction · motion direction · what the site must NOT look like · ONE distinctive creative concept unique to this site.
Do NOT default to: SaaS look, glassmorphism, black-luxury template, giant gradients, gradient text, generic beige Morocco, interchangeable white card grids, stock icon grids as storytelling, generic wave/palm/surfboard SVGs, the same navbar/hero as a sibling site.
Fonts: ≤2 families (+mono/label face only if essential), self-hosted latin(+latin-ext for FR) woff2 subsets or Google Fonts with `display=swap`. **Banned families** (used by sibling Peashoot sites/overused): Fraunces, Inter, Playfair Display, Poppins, Montserrat, Karla, Archivo, Marcellus, Roboto, Open Sans, Lato. The three sites must not share any family — record your choice in `/home/agent/agadir-pilot/FONTS.md` (append a row; read it first).
Sibling Peashoot sites in Agadir to stay clearly distinct from: https://hyle-surfhouse.peashoot.io/ (surf house, warm/host-centred), https://agadir-trip.peashoot.io/ and https://agadir-camel-horse.peashoot.io/ (tour/activity sellers).

## 5. ASSETS

Priority: business-owned public assets → official social → official booking-profile imagery → existing-site imagery → limited clearly non-deceptive supporting imagery (place context only, e.g. Anza beach, Essaouira ramparts — never presented as the business's rooms/vehicles/staff/tours).
NEVER use a competitor's rooms/vehicles/tours/staff/property. Watch for template/stock images reused across agencies (reverse-check suspicious ones) — if provenance is doubtful, classify DO-NOT-USE or CONTEXT-ONLY.
`ASSET_INVENTORY.md`: one row per candidate image: file · source URL · what it shows · owner/provenance · quality (1–5) · status USE / CONTEXT-ONLY / DO-NOT-USE · intended placement.
Look at the actual pixels (build labelled contact sheets with Pillow and `read` them) — never pick images by filename.
Optimised outputs in `site/assets/img/`: WebP (q≈72–80), hero ≤1920w & ≤300 KB plus a ≈800w mobile variant via `srcset`/`sizes`; content ≤1200w; thumbs ≤640w; every file ≤ 450 KB. Mediocre-but-real beats gorgeous-but-fake: crop, frame, treat (duotone/grain/grids) weak photos rather than replace them.

## 6. MOBILE (first-class — Fadwa hands over her phone)

Design at 390 px first; verify 360/390/430 and 1440. Check hero crops, text clipping, nav open/close (aria-expanded, Esc, closes on link tap, focus), ≥44 px targets, galleries (swipe/lightbox), forms (correct input types, no zoom-on-focus: inputs ≥16px), WhatsApp links, sticky CTA that never covers form submit buttons or footer content, no horizontal overflow at 360 px, image weight.

## 7. PERFORMANCE (tourists on mobile data)

Per page first load (mobile): ≤ ~900 KB transferred before scrolling, LCP image ≤ 200 KB at mobile width with `fetchpriority="high"` and NOT lazy; everything below the fold `loading="lazy" decoding="async"`. Every `<img>` has width/height (or aspect-ratio box) and a dominant-colour/LQIP background. JS ≤ 30 KB/page, vanilla, `defer`. CSS ≤ 60 KB. No libraries, no icon fonts (inline SVG sprites), no autoplay video unless it is real footage ≤ 2 MB with poster. Animations: CSS + IntersectionObserver, `prefers-reduced-motion` respected, content visible if JS fails. Global `[hidden]{display:none!important}`. `site/_headers` with long cache for `/assets/*`.

## 8. CONVERSION (one obvious action per site)

`tel:` and `https://wa.me/<digits>?text=<urlencoded>` ONLY with the VERIFIED number. Inquiry/booking forms: client-side validation → readable prefilled WhatsApp message (in the page language) → open wa.me; success state with "Didn't open? Tap here" + tel/mailto fallback. Verified Booking.com / marketplace links may be secondary CTAs. No fake payments, carts, availability engines, live prices or live surf data.

## 9. SEO & HYGIENE

Unique title + meta description per page, exactly one h1, semantic landmarks, JSON-LD (TravelAgency/TouristTrip, Hotel, Hostel/LodgingBusiness…; aggregateRating only with verified numbers), OG/Twitter tags with a real og:image (1200×630 webp/jpg), canonical `https://<slug>.peashoot.io/...`, `sitemap.xml`, `robots.txt`, self-contained `404.html`, favicon (SVG + 180px apple-touch PNG) derived from the brand. Folder-per-page clean URLs (`site/rooms/index.html`). Links may be relative or root-absolute (site is served at domain root).
Optional generator: a stdlib-Python `tools/build.py` rendering `site/` from data + templates is encouraged for catalogue/bilingual sites; the generated `site/` is committed (no build on Cloudflare).

## 10. VERIFICATION before reporting

1. `python3 /home/agent/agadir-pilot/tools/check_site.py <repo>` → must print `check_site: OK`; review every WARN and the contact-target list.
2. Preview server (named service), ONE browser tab: every page at 390×844 and 1440×900; scroll through before full-page shots; inspect shots like a demanding art director; fix; repeat (≥2 rounds for new work). Save screenshots to `/home/agent/agadir-pilot/qa/<slug>/<phase>/` (gitignored, outside repo).
3. Functional: zero console errors, no failed requests, no horizontal overflow at 360, nav/menu/lang switch, form validation → decoded wa.me text correct (no undefined/NaN/empty fields), all links resolve.
4. Close tab, stop preview, update BUILD_STATUS.md, commit + push. Report back ≤ 250 words (state, decisions, uncertainties, anything the orchestrator must decide).
