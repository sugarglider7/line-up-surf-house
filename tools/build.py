#!/usr/bin/env python3
"""Render site/ for Line Up Surf House from per-language content + partials (stdlib only).

    python3 tools/build.py

Content: tools/content/en.py (and fr.py — same keys — once phase 3 adds it).
Images:  tools/img_manifest.json (written by tools/images.py).
Pages:   PAGES below. A page is rendered only if its renderer exists in RENDER; links to
         pages that are not built yet fall back to the matching homepage chapter anchor,
         so navigation never points at a missing file.
"""
import html
import importlib.util
import json
import os
from urllib.parse import quote

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
SITE = os.path.join(REPO, "site")
ORIGIN = "https://line-up-surf-house.peashoot.io"

PHONE_INTL = "+212 6 41 23 67 58"
PHONE_TEL = "tel:+212641236758"
WA = "https://wa.me/212641236758"
BOOKING = "https://www.booking.com/hotel/ma/line-up-surf-house.html"
MAPS = "https://www.google.com/maps/place/?q=place_id:ChIJnd03JgCzsw0Ryl0nJC4wElE"
ADDRESS = ("NR 33 Projet Social Anza", "80090 Agadir, Morocco")

# page key -> URL per language. Fallback anchor (on the homepage) while the page is not built.
PAGES = {
    "home": {"en": "/", "fr": "/fr/", "anchor": ""},
    "rooms": {"en": "/rooms/", "fr": "/fr/chambres/", "anchor": "#rooms"},
    "surf": {"en": "/surf/", "fr": "/fr/surf/", "anchor": "#surf"},
    "house": {"en": "/house/", "fr": "/fr/la-maison/", "anchor": "#family"},
    "anza": {"en": "/anza/", "fr": "/fr/anza/", "anchor": "#anza"},
    "book": {"en": "/book/", "fr": "/fr/reserver/", "anchor": "#ask"},
}

MANIFEST = json.load(open(os.path.join(TOOLS, "img_manifest.json")))
FONT_FILES = ["anybody-latin.woff2", "newsreader-400-latin.woff2"]  # preloaded (italic loads on demand)


def ver(rel):
    """Short content hash for cache-busting (assets are served immutable)."""
    import hashlib
    with open(os.path.join(SITE, "assets", rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def load_content(lang):
    path = os.path.join(TOOLS, "content", f"{lang}.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(f"content_{lang}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def a(s):
    """Escape for attribute values."""
    return html.escape(str(s), quote=True)


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------- built-page registry
BUILT = set()  # (page_key, lang) pairs rendered in this run; filled before rendering


def href(key, lang):
    if (key, lang) in BUILT:
        return PAGES[key][lang]
    home = PAGES["home"][lang] if ("home", lang) in BUILT else "/"
    return home + PAGES[key]["anchor"]


def wa_link(text):
    return f"{WA}?text={quote(text)}"


# ---------------------------------------------------------------- images
def srcset(name):
    return ", ".join(f"/assets/img/{v['file']} {v['w']}w" for v in MANIFEST[name]["variants"])


def img(name, alt, sizes, cls="", eager=False, fill=False):
    m = MANIFEST[name]
    v = m["variants"]
    big = v[-1]
    attrs = [
        f'src="/assets/img/{v[0]["file"] if len(v) > 1 else big["file"]}"',
        f'srcset="{srcset(name)}"' if len(v) > 1 else "",
        f'sizes="{sizes}"' if len(v) > 1 else "",
        f'width="{big["w"]}" height="{big["h"]}"',
        f'alt="{a(alt)}"',
        'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"',
        f'class="{cls}"' if cls else "",
        f'style="background-color:{m["color"]}"',
    ]
    return "<img " + " ".join(x for x in attrs if x) + ">"


# ---------------------------------------------------------------- partials
SVG_SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
<symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/></symbol>
<symbol id="i-out" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M7 17 17 7M9 7h8v8"/></symbol>
</svg>"""


def head(c, key, lang, extra_ld=None):
    meta = c.PAGES_META[key]
    url = ORIGIN + (PAGES[key][lang] if key in PAGES else "/404.html")
    alts = ""
    if key in PAGES and all((key, l) in BUILT for l in ("en", "fr")):
        alts = "".join(
            f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{PAGES[key][l]}">' for l in ("en", "fr")
        ) + f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{PAGES[key]["en"]}">'
    preload = "".join(
        f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>' for f in FONT_FILES
    )
    og_img = f"{ORIGIN}/assets/img/{MANIFEST['og']['variants'][0]['file']}"
    ld = f'<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>' if extra_ld else ""
    robots = '<meta name="robots" content="noindex">' if key == "404" else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{a(meta['title'])}</title>
<meta name="description" content="{a(meta['description'])}">
{robots}<link rel="canonical" href="{url}">{alts}
<meta name="theme-color" content="#0f2533">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Line Up Surf House">
<meta property="og:locale" content="{c.LOCALE}">
<meta property="og:title" content="{a(meta.get('og_title', meta['title']))}">
<meta property="og:description" content="{a(meta['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The LINE UP mural on the house in Anza: accommodation, Surf School, Shop">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{preload}
<link rel="stylesheet" href="/assets/css/site.css?v={ver('css/site.css')}">
<script src="/assets/js/site.js?v={ver('js/site.js')}" defer></script>
{ld}
</head>"""


def brand(c, home_href):
    return f"""<a class="brand" href="{home_href}" aria-label="Line Up Surf House — home">
<span class="brand__word">Line Up</span><span class="brand__sub">{c.UI['brand_sub']}</span></a>"""


def lang_switch(c, key, lang):
    other = "fr" if lang == "en" else "en"
    if (key, other) not in BUILT:
        return ""
    return f'<a class="lang" href="{PAGES[key][other]}" hreflang="{other}" lang="{other}">{c.UI["lang_switch_short"]}<span class="vh"> — {c.UI["lang_switch"]}</span></a>'


def header(c, key, lang):
    ui = c.UI
    links = "".join(f'<li><a href="{href(k, lang)}">{label}</a></li>' for k, label in c.NAV)
    home = href("home", lang)
    return f"""<a class="skip" href="#main">{ui['skip']}</a>
<header class="hd" data-header>
<div class="hd__in">
{brand(c, home)}
<nav class="hd__nav" aria-label="{ui['nav_label']}"><ul>{links}</ul></nav>
<div class="hd__end">
{lang_switch(c, key, lang)}
<a class="btn btn--sun hd__cta" href="{href('book', lang)}">{ui['cta_ask']}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="sheet" data-nav-toggle><span class="burger__lines" aria-hidden="true"></span><span class="burger__t">{ui['menu']}</span></button>
</div>
</div>
</header>"""


def sheet(c, key, lang):
    ui = c.UI
    items = [(k, label) for k, label in c.NAV] + [("book", ui["cta_ask"])]
    links = "".join(
        f'<li><a href="{href(k, lang)}" data-close><span class="sheet__n">0{i + 1}</span>{label}</a></li>'
        for i, (k, label) in enumerate(items)
    )
    return f"""<div class="sheet" id="sheet" hidden data-sheet>
<div class="sheet__top">{brand(c, href('home', lang))}<button class="sheet__close" type="button" data-nav-close>{ui['close']}</button></div>
<nav aria-label="{ui['nav_label']}"><ul class="sheet__list">{links}</ul></nav>
<div class="sheet__horizon" aria-hidden="true"><span class="sun"></span></div>
<div class="sheet__acts">
<a class="btn btn--sun" href="{wa_link(ui['wa_hello'])}" rel="noopener" target="_blank"><svg class="ic"><use href="#i-wa"/></svg>{ui['cta_whatsapp_long']}</a>
<a class="btn btn--line-light" href="{PHONE_TEL}"><svg class="ic"><use href="#i-phone"/></svg>{PHONE_INTL}</a>
<a class="sheet__bk" href="{BOOKING}" rel="noopener" target="_blank">{ui['cta_booking_long']} <svg class="ic ic--s"><use href="#i-out"/></svg></a>
</div>
{lang_switch(c, key, lang)}
</div>"""


def dock(c, lang):
    ui = c.UI
    return f"""<div class="dock" data-dock>
<button class="dock__menu" type="button" aria-expanded="false" aria-controls="sheet" data-nav-toggle><span class="burger__lines" aria-hidden="true"></span>{ui['menu']}</button>
<a class="dock__wa" href="{wa_link(ui['wa_hello'])}" rel="noopener" target="_blank"><svg class="ic"><use href="#i-wa"/></svg>{ui['cta_whatsapp_long']}</a>
<a class="dock__call" href="{PHONE_TEL}" aria-label="{ui['cta_call']} {PHONE_INTL}"><svg class="ic"><use href="#i-phone"/></svg></a>
</div>"""


def footer(c, key, lang):
    f, ui = c.FOOTER, c.UI
    links = "".join(f'<li><a href="{href(k, lang)}">{label}</a></li>' for k, label in c.NAV)
    stay = "".join(f"<li>{x}</li>" for x in f["stay_lines"])
    return f"""<footer class="ft" data-footer>
<div class="ft__horizon" aria-hidden="true"><span class="sun sun--set"></span></div>
<div class="wrap ft__grid">
<div class="ft__brand">
<p class="ft__word">Line Up</p>
<p class="ft__mural">{f['mural']}</p>
</div>
<div>
<h2 class="ft__h">{f['address_label']}</h2>
<address>Line Up Surf House<br>{ADDRESS[0]}<br>{ADDRESS[1]}</address>
<a class="ft__link" href="{MAPS}" rel="noopener" target="_blank">{f['maps']} <svg class="ic ic--s"><use href="#i-out"/></svg></a>
</div>
<div>
<h2 class="ft__h">{f['contact_label']}</h2>
<ul class="ft__list">
<li><a href="{wa_link(ui['wa_hello'])}" rel="noopener" target="_blank">WhatsApp {PHONE_INTL}</a></li>
<li><a href="{PHONE_TEL}">{ui['cta_call']} {PHONE_INTL}</a></li>
<li><a href="{BOOKING}" rel="noopener" target="_blank">{ui['cta_booking']}</a></li>
</ul>
<p class="ft__small">{f['langs']}</p>
</div>
<div>
<h2 class="ft__h">{f['stay_label']}</h2>
<ul class="ft__list ft__list--plain">{stay}</ul>
</div>
<nav aria-label="{f['explore_label']}"><h2 class="ft__h">{f['explore_label']}</h2><ul class="ft__list">{links}<li><a href="{href('book', lang)}">{ui['cta_ask']}</a></li></ul>{lang_switch(c, key, lang)}</nav>
</div>
</footer>"""


def marker(ch, pos):
    """Chapter marker: a horizon rule with the sun at this chapter's place in the day (pos 0..4)."""
    x, sy = (6, 28, 50, 72, 94)[pos], (-15, 2, 13, 2, -15)[pos]
    return f"""<div class="mk" data-reveal style="--x:{x}%;--sy:{sy}px">
<div class="mk__sky" aria-hidden="true"><span class="sun"></span></div>
<div class="mk__sea" aria-hidden="true"></div>
<p class="mk__label"><span class="mk__n">{ch['n']}</span> {ch['label']}</p>
</div>"""


def quote_block(text, by, src, cls=""):
    return f"""<figure class="q {cls}"><blockquote><p>“{text}”</p></blockquote><figcaption>{by} <span>· {src}</span></figcaption></figure>"""


# ---------------------------------------------------------------- form
def ask_form(c, lang):
    F = c.FORM
    rooms = "".join(f'<option value="{v}">{t}</option>' for v, t in F["room_opts"])
    extras = "".join(
        f'<label class="chk"><input type="checkbox" name="extras" value="{v}" data-label="{a(t)}"><span>{t}</span></label>'
        for v, t in F["extra_opts"]
    )
    adults = "".join(f'<option{" selected" if n == 2 else ""}>{n}</option>' for n in range(1, 11))
    kids = "".join(f"<option>{n}</option>" for n in range(0, 7))
    i18n = {"errors": F["errors"], "msg": F["msg"], "lang": c.LOCALE.replace("_", "-"), "wa": WA}
    return f"""<form class="ask" id="ask-form" novalidate data-ask>
<script type="application/json" data-i18n>{json.dumps(i18n, ensure_ascii=False)}</script>
<p class="ask__summary" role="alert" hidden data-summary></p>
<div class="ask__row ask__row--2">
<div class="fld"><label for="f-in">{F['checkin']}</label><input id="f-in" name="checkin" type="date" required autocomplete="off" aria-describedby="e-in"><p class="fld__err" id="e-in" hidden></p></div>
<div class="fld"><label for="f-out">{F['checkout']}</label><input id="f-out" name="checkout" type="date" required autocomplete="off" aria-describedby="e-out"><p class="fld__err" id="e-out" hidden></p></div>
</div>
<div class="ask__row ask__row--3">
<div class="fld"><label for="f-ad">{F['adults']}</label><select id="f-ad" name="adults">{adults}</select></div>
<div class="fld"><label for="f-ch">{F['children']}</label><select id="f-ch" name="children">{kids}</select></div>
<div class="fld fld--room"><label for="f-room">{F['room']}</label><select id="f-room" name="room">{rooms}</select></div>
</div>
<fieldset class="ask__extras"><legend>{F['extras']}</legend>{extras}</fieldset>
<div class="ask__row ask__row--2">
<div class="fld"><label for="f-name">{F['name']} <span class="opt">({F['optional']})</span></label><input id="f-name" name="name" type="text" autocomplete="name"></div>
<div class="fld"><label for="f-note">{F['note']} <span class="opt">({F['optional']})</span></label><textarea id="f-note" name="note" rows="2" placeholder="{a(F['note_ph'])}"></textarea></div>
</div>
<button class="btn btn--ink ask__go" type="submit"><svg class="ic"><use href="#i-wa"/></svg>{F['submit']}</button>
</form>
<div class="ask__done" hidden data-done tabindex="-1">
<p class="ask__done-t">{F['done_title']}</p>
<p>{F['done_text']}</p>
<p><a class="btn btn--ink" href="{WA}" rel="noopener" target="_blank" data-retry><svg class="ic"><use href="#i-wa"/></svg>{F['done_retry']}</a></p>
<p class="ask__alts"><a href="{PHONE_TEL}">{F['done_call']}: {PHONE_INTL}</a><a href="{BOOKING}" rel="noopener" target="_blank">{F['done_booking']}</a><button type="button" class="linkbtn" data-edit>{F['done_edit']}</button></p>
</div>"""


# ---------------------------------------------------------------- pages
def ld_hostel(c):
    return {
        "@context": "https://schema.org",
        "@type": "Hostel",
        "name": "Line Up Surf House",
        "url": ORIGIN + "/",
        "image": [f"{ORIGIN}/assets/img/{MANIFEST['og']['variants'][0]['file']}",
                  f"{ORIGIN}/assets/img/{MANIFEST['hero-d']['variants'][-1]['file']}"],
        "description": c.PAGES_META["home"]["description"],
        "telephone": PHONE_INTL,
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS[0], "postalCode": "80090",
                    "addressLocality": "Agadir", "addressCountry": "MA"},
        "geo": {"@type": "GeoCoordinates", "latitude": 30.44686, "longitude": -9.659849},
        "hasMap": MAPS,
        "sameAs": [BOOKING],
        "checkinTime": "14:00",
        "checkoutTime": "12:00",
        "petsAllowed": False,
        "numberOfRooms": 8,
        "knowsLanguage": ["ar", "fr", "en"],
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in ("Breakfast included", "Free Wi-Fi", "Free public parking", "Terrace", "Surf school and board rental")
        ],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 9.6, "bestRating": 10, "worstRating": 1,
                            "reviewCount": 208},
    }


def page_home(c, lang):
    H, ui = c.HOME, c.UI
    cv, c1, c2, c3, c4, c5, ask = (H[k] for k in ("cover", "ch1", "ch2", "ch3", "ch4", "ch5", "ask"))
    hm, hd = MANIFEST["hero-m"], MANIFEST["hero-d"]

    cover = f"""<section class="cover" aria-labelledby="h1" data-cover style="--hz-m:{hm['horizon']};--hz-d:{hd['horizon']};--ar-m:{hm['w']}/{hm['h']};--ar-d:{hd['w']}/{hd['h']};--r-m:{hm['h'] / hm['w']:.4f};--r-d:{hd['h'] / hd['w']:.4f}">
<div class="cover__media">
<picture>
<source media="(min-width: 700px)" srcset="{srcset('hero-d')}" sizes="100vw" width="{hd['variants'][-1]['w']}" height="{hd['variants'][-1]['h']}">
{img('hero-m', cv['img_alt'], '100vw', 'cover__img', eager=True)}
</picture>
<div class="cover__hz" aria-hidden="true"><span>{cv['horizon']}</span></div>
<p class="cover__cap">{cv['caption']}</p>
<div class="cover__title wrap">
<p class="cover__kicker">{cv['kicker']}</p>
<h1 id="h1">{cv['h1']}</h1>
</div>
</div>
<div class="cover__band">
<div class="wrap cover__band-in">
<p class="cover__lead">{cv['lead']}</p>
<div class="cover__acts">
<a class="btn btn--sun" href="{href('book', lang)}">{ui['cta_ask']}</a>
</div>
<p class="cover__rating"><span class="cover__score">{cv['rating_score']}</span> {cv['rating_on']}<a href="{BOOKING}" rel="noopener" target="_blank">{cv['rating_link']} <svg class="ic ic--s"><use href="#i-out"/></svg><span class="vh"> ({ui['ext']})</span></a></p>
</div>
</div>
</section>"""

    bf_items = "\n".join(f"<li>{x}</li>" for x in c1["bf_items"])
    ch1 = f"""<section class="ch ch--dawn" id="{c1['id']}" aria-labelledby="t1">
<div class="wrap">
{marker(c1, 0)}
<div class="ch1">
<div class="ch1__text">
<h2 class="h2" id="t1">{c1['title']}</h2>
<p class="lead">{c1['lead']}</p>
</div>
<figure class="ch1__fig frame">{img('window', c1['img_alt'], '(min-width: 960px) 40vw, 100vw')}<figcaption>{c1['caption']}</figcaption></figure>
<div class="ch1__bf">
<h3 class="h3">{c1['bf_title']}</h3>
<p>{c1['bf_text']}</p>
<p class="maybe__label">{c1['bf_maybe']}</p>
<ul class="maybe">{bf_items}</ul>
<p class="small">{c1['bf_note']}</p>
</div>
{quote_block(c1['quote'], c1['quote_by'], c1['quote_src'], 'q--ch1')}
</div>
</div>
</section>"""

    items = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in c2["items"])
    sets = "".join(
        f'<figure class="set__f set__f--{i + 1}">{img(n, alt, "(min-width: 960px) 30vw, 80vw")}<figcaption>{cap}</figcaption></figure>'
        for i, (n, alt, cap) in enumerate(c2["set"])
    )
    ch2 = f"""<section class="ch ch--sky" id="{c2['id']}" aria-labelledby="t2">
<div class="wrap">
{marker(c2, 1)}
<div class="ch2">
<div class="ch2__text">
<h2 class="h2" id="t2">{c2['title']}</h2>
<p class="lead">{c2['lead']}</p>
<dl class="specs">{items}</dl>
</div>
<div class="ch2__who">
<p class="who">{c2['who']}</p>
{quote_block(c2['quote'], c2['quote_by'], c2['quote_src'], 'q--light')}
</div>
</div>
</div>
<div class="set" role="group" aria-label="{c2['set_label']}">{sets}</div>
</section>"""

    rows = []
    for i, r in enumerate(c3["rooms"]):
        facts = "".join(f"<li>{x}</li>" for x in r["facts"])
        plaques = "".join(f'<span class="plaque">{p}</span>' for p in r.get("plaques", []))
        rows.append(f"""<li class="room">
<span class="room__n">0{i + 1}</span>
<div class="room__img">{img(r['img'], r['alt'], '(min-width: 960px) 220px, 34vw')}</div>
<div class="room__body">
<p class="room__kind">{r['kind']}</p>
<h4 class="room__name">{r['name']}</h4>
<ul class="room__facts">{facts}</ul>
{f'<p class="room__plaques">{plaques}</p>' if plaques else ''}
</div>
<span class="room__count">{r['count']}</span>
</li>""")
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in c3["facts"])
    ch3 = f"""<section class="ch ch--noon" id="{c3['id']}" aria-labelledby="t3">
<div class="wrap">
{marker(c3, 2)}
<h2 class="h2 h2--wide" id="t3">{c3['title']}</h2>
<div class="rooms" id="{c3['rooms_id']}">
<div class="rooms__head">
<h3 class="h3 h3--big">{c3['rooms_title']}</h3>
<p>{c3['rooms_lead']}</p>
</div>
<ol class="rooms__list">{''.join(rows)}</ol>
<p class="rooms__note">{c3['rooms_note']}</p>
</div>
<div class="noon">
<div class="noon__lunch">
<h3 class="h3">{c3['lunch_title']}</h3>
<p>{c3['lunch_text']}</p>
</div>
<div class="noon__anza" id="{c3['anza_id']}">
<h3 class="h3">{c3['anza_title']}</h3>
<p>{c3['anza_text']}</p>
</div>
<aside class="noon__facts" aria-labelledby="t3f">
<h3 class="kicker" id="t3f">{c3['facts_title']}</h3>
<dl class="specs specs--ink">{facts}</dl>
</aside>
</div>
</div>
</section>"""

    qs = "".join(quote_block(t, by, src, f"q--set q--s{i + 1}") for i, (t, by, src) in enumerate(c4["quotes"]))
    ch4 = f"""<section class="ch ch--sea" id="{c4['id']}" aria-labelledby="t4">
<div class="wrap">
{marker(c4, 3)}
<div class="ch4">
<div class="ch4__text">
<h2 class="h2" id="t4">{c4['title']}</h2>
<p class="lead">{c4['lead']}</p>
<h3 class="h3">{c4['fam_title']}</h3>
<p>{c4['fam_text']}</p>
</div>
<div class="stat">
<p class="stat__n">{c4['stat']}</p>
<p class="stat__l">{c4['stat_label']}</p>
<p class="stat__note">{c4['stat_note']}</p>
</div>
</div>
<div class="qset">{qs}</div>
</div>
</section>"""

    roof_lines = "".join(f"<li>{x}</li>" for x in c5["roof_lines"])
    ch5 = f"""<section class="ch ch--dusk" id="{c5['id']}" aria-labelledby="t5">
<div class="wrap">
{marker(c5, 4)}
<div class="ch5">
<div class="ch5__text">
<h2 class="h2" id="t5">{c5['title']}</h2>
<p class="lead">{c5['lead']}</p>
</div>
<div class="roof" aria-hidden="true" data-reveal>
<p class="roof__word">{c5['roof_word']}</p>
<span class="roof__sun"></span>
<span class="roof__line"></span>
<ul class="roof__lines">{roof_lines}</ul>
</div>
<figure class="ch5__fig">{img('late-light', c5['img_alt'], '(min-width: 960px) 40vw, 100vw')}<figcaption>{c5['caption']}</figcaption></figure>
</div>
</div>
</section>"""

    asks = f"""<section class="ch ch--sun" id="{ask['id']}" aria-labelledby="t6">
<div class="wrap askw">
<div class="askw__head">
<h2 class="h2" id="t6">{ask['title']}</h2>
<p class="lead">{ask['lead']}</p>
<p class="askw__alt"><a href="{BOOKING}" rel="noopener" target="_blank">{ask['alt']} <svg class="ic ic--s"><use href="#i-out"/></svg></a></p>
</div>
<div class="askw__form">{ask_form(c, lang)}</div>
</div>
</section>"""

    body = f"""<body class="home">
{SVG_SPRITE}
{header(c, 'home', lang)}
{sheet(c, 'home', lang)}
<main id="main">
{cover}
{ch1}
{ch2}
{ch3}
{ch4}
{ch5}
{asks}
</main>
{footer(c, 'home', lang)}
{dock(c, lang)}
</body>
</html>"""
    return head(c, "home", lang, ld_hostel(c)) + "\n" + body


def page_404(c, lang):
    n = c.NOT_FOUND
    body = f"""<body class="nf">
{SVG_SPRITE}
<main id="main" class="nf__main">
<div class="nf__sky"><span class="sun sun--set"></span></div>
<div class="wrap nf__in">
<p class="nf__word">Line Up</p>
<h1 class="h2">{n['title']}</h1>
<p class="lead">{n['text']}</p>
<p class="nf__acts"><a class="btn btn--sun" href="/">{n['back']}</a>
<a class="btn btn--line-light" href="{wa_link(c.UI['wa_hello'])}" rel="noopener" target="_blank"><svg class="ic"><use href="#i-wa"/></svg>{c.UI['cta_whatsapp_long']}</a></p>
</div>
</main>
</body>
</html>"""
    return head(c, "404", lang) + "\n" + body


RENDER = {
    ("home", "en"): page_home,
}


def out_path(key, lang):
    url = PAGES[key][lang]
    return os.path.join(SITE, url.strip("/"), "index.html")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    contents = {l: load_content(l) for l in ("en", "fr")}
    BUILT.update(k for k in RENDER if contents.get(k[1]))
    for (key, lang), fn in RENDER.items():
        c = contents.get(lang)
        if not c:
            continue
        write(out_path(key, lang), fn(c, lang))
        print("built", PAGES[key][lang])
    write(os.path.join(SITE, "404.html"), page_404(contents["en"], "en"))
    print("built /404.html")
    urls = sorted(PAGES[k][l] for k, l in BUILT)
    sm = "".join(f"<url><loc>{ORIGIN}{u}</loc></url>" for u in urls)
    write(os.path.join(SITE, "sitemap.xml"),
          f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    write(os.path.join(SITE, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
    write(os.path.join(SITE, "_headers"),
          "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
    print("built sitemap.xml robots.txt _headers")


if __name__ == "__main__":
    main()
