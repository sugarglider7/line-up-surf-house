#!/usr/bin/env python3
"""Render site/ for Line Up Surf House from per-language content + partials (stdlib only).

    python3 tools/build.py

Content: tools/content/en.py and tools/content/fr.py (same keys; FR = parallel copy, not a translation).
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

PHONE_INTL = "+212\u00a06\u00a041\u00a023\u00a067\u00a058"  # displayed number; NBSPs keep it on one line
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
{robots}{'' if key == '404' else f'<link rel="canonical" href="{url}">'}{alts}
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
<meta property="og:image:alt" content="{a(c.UI['og_alt'])}">
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
    cur = lambda k: ' aria-current="page"' if k == key else ""
    links = "".join(f'<li><a href="{href(k, lang)}"{cur(k)}>{label}</a></li>' for k, label in c.NAV)
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
        f'<li><a href="{href(k, lang)}"{" aria-current=page" if k == key else ""} data-close><span class="sheet__n">0{i + 1}</span>{label}</a></li>'
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


def sun_at(t):
    """Sun position for a time of day t (0 = first light, 1 = sunset): x along the rule, height of the arc."""
    import math
    return round(6 + 88 * t, 1), round(-15 + 28 * math.sin(math.pi * t))


def marker(ch, pos=None, t=None):
    """Chapter marker: a horizon rule with the sun at this chapter's place in the day.
    pos = homepage chapter index 0..4; t = any time of day 0..1 (inner pages)."""
    x, sy = sun_at(pos / 4 if t is None else t)
    n = f'<span class="mk__n">{ch["n"]}</span> ' if ch.get("n") else ""
    return f"""<div class="mk" data-reveal style="--x:{x}%;--sy:{sy}px">
<div class="mk__sky" aria-hidden="true"><span class="sun"></span></div>
<div class="mk__sea" aria-hidden="true"></div>
<p class="mk__label">{n}{ch['label']}</p>
</div>"""


def quote_block(text, by, src, cls="", ql=None, lang="en"):
    """A real review quote, never translated. ql = language of the quote; lang = page language."""
    ql = ql or lang
    la = f' lang="{ql}"' if ql != lang else ""
    o, cl = ("« ", " »") if ql == "fr" else ("“", "”")
    return f"""<figure class="q {cls}"><blockquote{la}><p>{o}{text}{cl}</p></blockquote><figcaption>{by} <span>· {src}</span></figcaption></figure>"""


def quotes(items, lang, cls=""):
    """items: (text, by, src[, quote_lang]) tuples."""
    return "".join(quote_block(*q[:3], cls=cls, ql=q[3] if len(q) > 3 else None, lang=lang) for q in items)


def more(ch, lang, cls="", key="more"):
    """'Read more' link from a homepage chapter (or any block) to its dedicated page: (page, label[, #frag])."""
    spec = ch.get(key)
    if not spec:
        return ""
    page, label = spec[0], spec[1]
    frag = spec[2] if len(spec) > 2 else ""
    return f'<p class="more {cls}"><a href="{href(page, lang)}{frag}">{label}<span aria-hidden="true"> →</span></a></p>'


def specs(items, cls=""):
    rows = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in items)
    return f'<dl class="specs {cls}">{rows}</dl>'


DAY_ORDER = ["house", "surf", "rooms", "anza", "book"]  # inner pages in the order of the day


def day_strip(c, t):
    """Masthead strip: the day as one horizon rule — five chapter ticks, the sun at this page's hour."""
    x, sy = sun_at(t)
    now = round(t * 4) if abs(t * 4 - round(t * 4)) < .15 else -1
    ticks = "".join(
        f'<li style="--tx:{6 + 22 * i}%"{" class=is-now" if i == now else ""}>{lab}</li>' for i, lab in enumerate(c.DAY)
    )
    return f"""<div class="day" aria-hidden="true" data-reveal style="--x:{x}%;--sy:{sy}px">
<div class="day__sky"><span class="sun"></span></div>
<ol class="day__ticks">{ticks}</ol>
</div>"""


def masthead(c, lang, M, eager_img=True):
    """Inner-page cover: the day strip, the hour, the H1, a lead and one real photo.
    M['wide'] → full-width horizon band (photo with the line-up drawn on its real horizon)."""
    fig = ""
    if M.get("img") and M.get("wide"):
        m = MANIFEST[M["img"]]
        r_img = m["w"] / m["h"]
        r_d, p = 2.4, .42  # desktop band ratio + object-position y
        k = r_d / r_img
        hz_d = m["horizon"] * k - (k - 1) * p
        fig = f"""<figure class="band" style="--hz-m:{m['horizon']};--hz-d:{hz_d:.4f};--ar:{m['w']}/{m['h']};--py:{p * 100:.0f}%">
{img(M['img'], M['img_alt'], '100vw', 'band__img', eager=eager_img)}
<div class="band__hz" aria-hidden="true"><span>{c.HOME['cover']['horizon']}</span></div>
<figcaption class="band__cap">{M['caption']}</figcaption>
</figure>"""
    elif M.get("img"):
        fig = f"""<figure class="mast__fig">{img(M['img'], M['img_alt'], '(min-width: 960px) 38vw, 100vw', eager=eager_img)}<figcaption>{M['caption']}</figcaption></figure>"""
    wide = M.get("wide")
    return f"""<section class="mast mast--{M['tone']}{' mast--wide' if wide else ''}{'' if M.get('img') else ' mast--bare'}" aria-labelledby="h1" data-cover>
<div class="wrap">
{day_strip(c, M['t'])}
<div class="mast__grid">
<div class="mast__text">
<p class="mast__kicker"><span class="mk__n">{M['hour']}</span> · {M['kicker']}</p>
<h1 id="h1">{M['h1']}</h1>
<p class="lead mast__lead">{M['lead']}</p>
</div>
{'' if wide else fig}
</div>
</div>
{fig if wide else ''}
</section>"""


def book_href(lang, room=None, extra=None):
    q = "&".join(x for x in (f"room={room}" if room else "", f"extra={extra}" if extra else "") if x)
    return href("book", lang) + (f"?{q}" if q else "")


def ask_band(c, lang, title, room=None, extra=None):
    """Yellow 'ask for dates' band closing every inner page (the full form lives on /book/)."""
    A, ui = c.ASK_BAND, c.UI
    return f"""<section class="ch ch--sun cta" aria-labelledby="t-cta" data-nodock>
<div class="wrap cta__in">
<div>
<h2 class="h2" id="t-cta">{title}</h2>
<p class="lead">{A['text']}</p>
</div>
<div class="cta__acts">
<a class="btn btn--ink" href="{book_href(lang, room, extra)}">{ui['cta_ask']}</a>
<a class="cta__link" href="{wa_link(ui['wa_hello'])}" rel="noopener" target="_blank"><svg class="ic"><use href="#i-wa"/></svg>{A['wa']}</a>
<a class="cta__link" href="{BOOKING}" rel="noopener" target="_blank">{A['booking']} <svg class="ic ic--s"><use href="#i-out"/></svg></a>
</div>
</div>
</section>"""


def next_band(c, key, lang):
    """'The day goes on': link to the next inner page in the order of the day, sun at its hour."""
    i = DAY_ORDER.index(key)
    nxt = DAY_ORDER[(i + 1) % len(DAY_ORDER)] if i + 1 < len(DAY_ORDER) else "home"
    lab = c.NEXT[nxt]
    t = getattr(c, nxt.upper(), {}).get("mast", {}).get("t", 0) if nxt != "home" else 0
    x, sy = sun_at(t)
    return f"""<nav class="next" aria-label="{c.NEXT['label']}">
<div class="wrap">
<div class="mk next__mk" data-reveal style="--x:{x}%;--sy:{sy}px"><div class="mk__sky" aria-hidden="true"><span class="sun"></span></div><div class="mk__sea" aria-hidden="true"></div></div>
<p class="next__label">{c.NEXT['label']}</p>
<a class="next__a" href="{href(nxt, lang)}"><span class="next__hour">{lab[0]}</span><span class="next__t">{lab[1]}<span aria-hidden="true"> →</span></span></a>
</div>
</nav>"""


def ld_breadcrumb(c, key, lang):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Line Up Surf House", "item": ORIGIN + PAGES["home"][lang]},
            {"@type": "ListItem", "position": 2, "name": strip_tags(c.PAGES_META[key]["crumb"]),
             "item": ORIGIN + PAGES[key][lang]},
        ],
    }


def page(c, key, lang, main, ld=None):
    """Shell shared by every inner page."""
    body = f"""<body class="inner p-{key}">
{SVG_SPRITE}
{header(c, key, lang)}
{sheet(c, key, lang)}
<main id="main">
{main}
</main>
{next_band(c, key, lang) if key != 'book' else ''}
{footer(c, key, lang)}
{dock(c, lang)}
</body>
</html>"""
    return head(c, key, lang, ld or ld_breadcrumb(c, key, lang)) + "\n" + body


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
<p class="ask__alts"><a href="{PHONE_TEL}">{F['done_call']}{F['msg']['sep']}{PHONE_INTL}</a><a href="{BOOKING}" rel="noopener" target="_blank">{F['done_booking']}</a><button type="button" class="linkbtn" data-edit>{F['done_edit']}</button></p>
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
        "telephone": "+212641236758",
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
<a class="btn btn--sun" href="#{ask['id']}">{ui['cta_ask']}</a>
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
{more(c1, lang)}
</div>
{quote_block(c1['quote'], c1['quote_by'], c1['quote_src'], 'q--ch1', c1.get('quote_lang'), lang)}
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
{more(c2, lang, "more--light")}
</div>
<div class="ch2__who">
<p class="who">{c2['who']}</p>
{quote_block(c2['quote'], c2['quote_by'], c2['quote_src'], 'q--light', c2.get('quote_lang'), lang)}
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
{more(c3, lang)}
</div>
<div class="noon">
<div class="noon__lunch">
<h3 class="h3">{c3['lunch_title']}</h3>
<p>{c3['lunch_text']}</p>
</div>
<div class="noon__anza" id="{c3['anza_id']}">
<h3 class="h3">{c3['anza_title']}</h3>
<p>{c3['anza_text']}</p>
{more(c3, lang, key="more_anza")}
</div>
<aside class="noon__facts" aria-labelledby="t3f">
<h3 class="kicker" id="t3f">{c3['facts_title']}</h3>
<dl class="specs specs--ink">{facts}</dl>
</aside>
</div>
</div>
</section>"""

    qs = "".join(quote_block(q[0], q[1], q[2], f"q--set q--s{i + 1}", q[3] if len(q) > 3 else None, lang)
                 for i, q in enumerate(c4["quotes"]))
    ch4 = f"""<section class="ch ch--sea" id="{c4['id']}" aria-labelledby="t4">
<div class="wrap">
{marker(c4, 3)}
<div class="ch4">
<div class="ch4__text">
<h2 class="h2" id="t4">{c4['title']}</h2>
<p class="lead">{c4['lead']}</p>
<h3 class="h3">{c4['fam_title']}</h3>
<p>{c4['fam_text']}</p>
{more(c4, lang, "more--light")}
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
{more(c5, lang, "more--light")}
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

    asks = f"""<section class="ch ch--sun" id="{ask['id']}" aria-labelledby="t6" data-nodock>
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


def fig(name, alt, cap, sizes, cls=""):
    return f'<figure class="{cls}">{img(name, alt, sizes)}<figcaption>{cap}</figcaption></figure>'


def page_rooms(c, lang):
    R = c.ROOMS
    arts = []
    for i, r in enumerate(R["types"]):
        figs = "".join(
            fig(n, alt, cap, "(min-width: 960px) 26vw, 46vw", f"rt__f rt__f--{j + 1}") for j, (n, alt, cap) in enumerate(r["imgs"])
        )
        plaques = "".join(f'<span class="plaque">{p}</span>' for p in r.get("plaques", []))
        arts.append(f"""<article class="rt{' rt--flip' if i % 2 else ''}" id="{r['id']}" aria-labelledby="rt-{r['id']}">
<div class="wrap">
{marker({'n': f'0{i + 1}', 'label': r['kind']}, t=.3 + i * .1)}
<div class="rt__grid">
<div class="rt__text">
<h2 class="rt__name" id="rt-{r['id']}">{r['name']}&nbsp;<span class="rt__count">{r['count']}</span></h2>
<p class="rt__blurb">{r['blurb']}</p>
{specs(r['specs'], 'specs--ink')}
{f'<p class="room__plaques">{plaques}</p>' if plaques else ''}
<p class="more"><a href="{book_href(lang, room=r['room'])}">{R['ask_room']}<span aria-hidden="true"> →</span></a></p>
</div>
<div class="rt__set">{figs}</div>
</div>
</div>
</article>""")
    E = R["every"]
    has = "".join(f"<li>{x}</li>" for x in E["has"])
    hasnt = "".join(f"<li>{x}</li>" for x in E["not"])
    plaques = "".join(f'<span class="plaque plaque--big">{p}</span>' for p in E["plaques"])
    every = f"""<section class="ch ch--dawn" aria-labelledby="t-every">
<div class="wrap">
{marker({'label': E['label']}, t=.75)}
<h2 class="h2" id="t-every">{E['title']}</h2>
<div class="every">
<div><h3 class="kicker">{E['has_title']}</h3><ul class="lines">{has}</ul></div>
<div><h3 class="kicker">{E['not_title']}</h3><ul class="lines lines--not">{hasnt}</ul></div>
<div class="every__doors"><h3 class="h3">{E['doors_title']}</h3><p>{E['doors_text']}</p><p class="room__plaques">{plaques}</p></div>
</div>
<div class="every__arrive">
<h3 class="h3">{E['arrive_title']}</h3>
{specs(E['arrive'], 'specs--ink specs--wide')}
</div>
{quotes([R['quote']], lang, 'q--rule')}
</div>
</section>"""
    main = masthead(c, lang, R["mast"]) + "\n" + "\n".join(arts) + "\n" + every + "\n" + ask_band(c, lang, R["cta_title"])
    return page(c, "rooms", lang, main)


def page_surf(c, lang):
    S = c.SURF
    L, Rn, W = S["lessons"], S["rental"], S["water"]
    sets = "".join(
        fig(n, alt, cap, "(min-width: 960px) 30vw, 80vw", f"set__f set__f--{i + 1}") for i, (n, alt, cap) in enumerate(Rn["set"])
    )
    main = f"""{masthead(c, lang, S['mast'])}
<section class="ch ch--noon" id="lessons" aria-labelledby="t-les">
<div class="wrap">
{marker({'label': L['label']}, t=.2)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-les">{L['title']}</h2>
<p class="lead">{L['lead']}</p>
{specs(L['specs'], 'specs--ink')}
</div>
<div class="split__b">
<p class="who who--ink">{L['who']}</p>
{quotes(L['quotes'], lang, 'q--rule')}
</div>
</div>
</div>
</section>
<section class="ch ch--sky" id="rental" aria-labelledby="t-rent">
<div class="wrap">
{marker({'label': Rn['label']}, t=.4)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-rent">{Rn['title']}</h2>
<p class="lead">{Rn['lead']}</p>
<p>{Rn['text']}</p>
</div>
<div class="split__b">{quotes(Rn['quotes'], lang, 'q--light')}</div>
</div>
</div>
<div class="set" role="group" aria-label="{Rn['set_label']}">{sets}</div>
</section>
<section class="ch ch--dawn" id="water" aria-labelledby="t-wat">
<div class="wrap">
{marker({'label': W['label']}, t=.6)}
<div class="split split--fig">
<div class="split__a">
<h2 class="h2" id="t-wat">{W['title']}</h2>
<p class="lead">{W['lead']}</p>
<p>{W['text']}</p>
{quotes(W['quotes'], lang, 'q--rule')}
</div>
{fig(W['img'], W['img_alt'], W['caption'], '(min-width: 960px) 38vw, 100vw', 'split__b split__fig')}
</div>
</div>
</section>
{ask_band(c, lang, S['cta_title'], extra='lessons')}"""
    return page(c, "surf", lang, main)


def page_house(c, lang):
    H = c.HOUSE
    B, F, K, R, Q, X = H["breakfast"], H["family"], H["cooking"], H["roof"], H["scores"], H["rules"]
    bf_items = "\n".join(f"<li>{x}</li>" for x in B["items"])  # newline = break opportunity between nowrap items
    asks = "".join(f"<li>{x}</li>" for x in F["ask_items"])
    roof_lines = "".join(f"<li>{x}</li>" for x in R["lines"])
    scores = "".join(f'<div class="score"><p class="score__n">{n}</p><p class="score__l">{l}</p></div>' for n, l in Q["items"])
    qs = "".join(quote_block(q[0], q[1], q[2], f"q--set q--s{i + 1}", q[3] if len(q) > 3 else None, lang)
                 for i, q in enumerate(Q["quotes"]))
    main = f"""{masthead(c, lang, H['mast'])}
<section class="ch ch--dawn" id="breakfast" aria-labelledby="t-bf">
<div class="wrap">
{marker({'label': B['label']}, t=0)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-bf">{B['title']}</h2>
<p class="lead">{B['lead']}</p>
<p class="maybe__label">{B['maybe']}</p>
<ul class="maybe">{bf_items}</ul>
<p class="small">{B['note']}</p>
</div>
<div class="split__b">{quotes(B['quotes'], lang, 'q--rule')}</div>
</div>
</div>
</section>
<section class="ch ch--noon" id="family" aria-labelledby="t-fam">
<div class="wrap">
{marker({'label': F['label']}, t=.3)}
<h2 class="h2 h2--wide" id="t-fam">{F['title']}</h2>
<div class="split">
<div class="split__a">
<p class="lead">{F['lead']}</p>
<p class="who who--ink">{F['said']}</p>
<p class="who who--ink">{F['zohair']}</p>
</div>
<div class="split__b panel">
<h3 class="kicker">{F['ask_title']}</h3>
<ul class="lines">{asks}</ul>
<p class="small">{F['ask_note']}</p>
</div>
</div>
</div>
</section>
<section class="ch ch--sand" id="food" aria-labelledby="t-food">
<div class="wrap">
{marker({'label': K['label']}, t=.7)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-food">{K['title']}</h2>
<p class="lead">{K['lead']}</p>
<p>{K['text']}</p>
</div>
<div class="split__b">{quotes(K['quotes'], lang, 'q--rule')}</div>
</div>
</div>
</section>
<section class="ch ch--dusk" id="roof" aria-labelledby="t-roof">
<div class="wrap">
{marker({'label': R['label']}, t=1)}
<div class="ch5">
<div class="ch5__text">
<h2 class="h2" id="t-roof">{R['title']}</h2>
<p class="lead">{R['lead']}</p>
{quotes(R['quotes'], lang, 'q--dusk')}
</div>
<div class="roof" aria-hidden="true" data-reveal>
<p class="roof__word">{R['word']}</p>
<span class="roof__sun"></span>
<span class="roof__line"></span>
<ul class="roof__lines">{roof_lines}</ul>
</div>
</div>
</div>
</section>
<section class="ch ch--sea" id="reviews" aria-labelledby="t-rev">
<div class="wrap">
<h2 class="h2" id="t-rev">{Q['title']}</h2>
<div class="scores">{scores}</div>
<p class="stat__note">{Q['note']}</p>
<div class="qset">{qs}</div>
</div>
</section>
<section class="ch ch--noon ch--tight" id="rules" aria-labelledby="t-rules">
<div class="wrap split">
<div class="split__a"><h2 class="h3 h3--big" id="t-rules">{X['title']}</h2><p>{X['text']}</p></div>
<div class="split__b">{specs(X['items'], 'specs--ink')}</div>
</div>
</section>
{ask_band(c, lang, H['cta_title'])}"""
    return page(c, "house", lang, main)


def page_anza(c, lang):
    A = c.ANZA
    O, W, G = A["front"], A["wander"], A["around"]
    xs = "".join(
        f'<li class="xs__i xs__i--{k}"><span class="xs__shape" aria-hidden="true"></span><b>{t}</b><span>{s}</span></li>'
        for k, t, s in O["xs"]
    )
    main = f"""{masthead(c, lang, A['mast'])}
<section class="ch ch--noon" id="front" aria-labelledby="t-front">
<div class="wrap">
{marker({'label': O['label']}, t=.55)}
<h2 class="h2 h2--wide" id="t-front">{O['title']}</h2>
<ol class="xs" aria-label="{O['xs_label']}">{xs}</ol>
<div class="split">
<div class="split__a"><p class="lead">{O['lead']}</p></div>
<div class="split__b">{quotes(O['quotes'], lang, 'q--rule')}</div>
</div>
</div>
</section>
<section class="ch ch--sand" id="wander" aria-labelledby="t-wan">
<div class="wrap">
{marker({'label': W['label']}, t=.65)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-wan">{W['title']}</h2>
<p class="lead">{W['lead']}</p>
<p>{W['text']}</p>
</div>
<div class="split__b">
<h3 class="h3">{W['fp_title']}</h3>
<p>{W['fp_text']}</p>
{quotes(W['quotes'], lang, 'q--rule')}
</div>
</div>
</div>
</section>
<section class="ch ch--dawn" id="around" aria-labelledby="t-around">
<div class="wrap">
{marker({'label': G['label']}, t=.8)}
<div class="split">
<div class="split__a">
<h2 class="h2" id="t-around">{G['title']}</h2>
{specs(G['specs'], 'specs--ink')}
</div>
<div class="split__b">
<p class="who who--ink">{G['who']}</p>
<h3 class="h3">{G['trips_title']}</h3>
<p>{G['trips_text']}</p>
<div class="findus">
<h3 class="kicker">{G['find_title']}</h3>
<address>Line Up Surf House<br>{ADDRESS[0]}<br>{ADDRESS[1]}</address>
<a class="btn btn--line" href="{MAPS}" rel="noopener" target="_blank">{c.FOOTER['maps']} <svg class="ic ic--s"><use href="#i-out"/></svg></a>
</div>
</div>
</div>
</div>
</section>
{ask_band(c, lang, A['cta_title'])}"""
    return page(c, "anza", lang, main)


def page_book(c, lang):
    B, ui = c.BOOK, c.UI
    steps = "".join(f"<li>{x}</li>" for x in B["steps"])
    main = f"""{masthead(c, lang, B['mast'])}
<section class="ch ch--sun book" id="ask" aria-label="{B['form_label']}" data-nodock>
<div class="wrap book__in">
<div class="book__form">{ask_form(c, lang)}{quotes([B['quote']], lang, 'q--rule book__q')}</div>
<aside class="book__aside" aria-labelledby="t-how">
<h2 class="kicker" id="t-how">{B['how_title']}</h2>
<ol class="steps">{steps}</ol>
<h2 class="kicker">{B['other_title']}</h2>
<ul class="book__other">
<li><a href="{wa_link(ui['wa_hello'])}" rel="noopener" target="_blank"><svg class="ic"><use href="#i-wa"/></svg>WhatsApp {PHONE_INTL}</a></li>
<li><a href="{PHONE_TEL}"><svg class="ic"><use href="#i-phone"/></svg>{ui['cta_call']} {PHONE_INTL}</a></li>
<li><a href="{BOOKING}" rel="noopener" target="_blank">{ui['cta_booking_long']} <svg class="ic ic--s"><use href="#i-out"/></svg></a></li>
</ul>
<h2 class="kicker">{B['know_title']}</h2>
{specs(B['know'], 'specs--ink')}
<h2 class="kicker">{B['find_title']}</h2>
<address>Line Up Surf House<br>{ADDRESS[0]}<br>{ADDRESS[1]}</address>
<p><a class="book__map" href="{MAPS}" rel="noopener" target="_blank">{c.FOOTER['maps']} <svg class="ic ic--s"><use href="#i-out"/></svg></a></p>
</aside>
</div>
</section>"""
    return page(c, "book", lang, main)


def page_404(c, lang, fr=None):
    """Self-contained 404 (Cloudflare serves it for any missing path): English first, French below."""
    n = c.NOT_FOUND
    frb = ""
    if fr:
        f = fr.NOT_FOUND
        frb = f"""<div class="nf__fr" lang="fr">
<p class="nf__frt">{f['title']}</p>
<p>{f['text']}</p>
<p><a class="btn btn--line-light" href="/fr/">{f['back']}</a></p>
</div>"""
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
{frb}
</div>
</main>
</body>
</html>"""
    return head(c, "404", lang) + "\n" + body


RENDER = {
    (key, lang): fn
    for key, fn in (("home", page_home), ("rooms", page_rooms), ("surf", page_surf), ("house", page_house),
                    ("anza", page_anza), ("book", page_book))
    for lang in ("en", "fr")
}

HEADERS = """/assets/*
  Cache-Control: public, max-age=31536000, immutable
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Content-Security-Policy: default-src 'self'; script-src 'self' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://cloudflareinsights.com; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'
"""


def fr_typo(s):
    """French spacing: no line break before : ; ! ? » or after « (URLs are percent-encoded, so untouched)."""
    import re
    return re.sub(r" ([:;!?»])", "\u00a0\\1", s).replace("« ", "«\u00a0")


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
        out = fn(c, lang)
        write(out_path(key, lang), fr_typo(out) if lang == "fr" else out)
        print("built", PAGES[key][lang])
    write(os.path.join(SITE, "404.html"), page_404(contents["en"], "en", contents.get("fr")))
    print("built /404.html")
    sm = []
    for key in PAGES:
        langs = [l for l in ("en", "fr") if (key, l) in BUILT]
        alts = ""
        if len(langs) == 2:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{ORIGIN}{PAGES[key][l]}"/>' for l in langs)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{PAGES[key]["en"]}"/>'
        sm += [f"<url><loc>{ORIGIN}{PAGES[key][l]}</loc>{alts}</url>" for l in langs]
    write(os.path.join(SITE, "sitemap.xml"),
          '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(sm) + "\n</urlset>\n")
    write(os.path.join(SITE, "robots.txt"), f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
    write(os.path.join(SITE, "_headers"), HEADERS)
    print("built sitemap.xml robots.txt _headers")


if __name__ == "__main__":
    main()
