"""Helpers for the bilingual AVS deck. Every visible string is authored as an (en, fr) pair."""
import html as _html

SLIDES = []

SECTIONS = [
    ("intro", "Why AVS", "Pourquoi AVS"),
    ("connect", "Connect", "Connecter"),
    ("migrate", "Migrate", "Migrer"),
    ("operate", "Operate", "Exploiter"),
    ("troubleshoot", "Troubleshoot", "Dépanner"),
    ("perform", "Performance", "Performance"),
    ("adopt", "Adopt", "Adopter"),
]

LAYERS = {
    "exec": ("Executive summary", "Sommaire pour la direction"),
    "eli5": ("ELI5", "En termes simples"),
    "deep": ("Deep dive", "Plongée technique"),
    "arch": ("Architecture", "Architecture"),
    "decide": ("Decision guide", "Guide de décision"),
    "plan": ("Plan", "Plan"),
    "appendix": ("Appendix", "Annexe"),
}


def esc(s):
    return _html.escape(s, quote=False)


def t(en, fr):
    """Inline bilingual text."""
    return f'<span class="l-en">{en}</span><span class="l-fr">{fr}</span>'


def tb(tag, en, fr, cls="", attrs=""):
    """Block-level bilingual pair: two sibling elements, one per language."""
    c = f" {cls}" if cls else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} class="l-en{c}"{a}>{en}</{tag}><{tag} class="l-fr{c}"{a}>{fr}</{tag}>'


def ul(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{t(en, fr)}</li>" for en, fr in items) + "</ul>"


def ol(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ol{c}>" + "".join(f"<li>{t(en, fr)}</li>" for en, fr in items) + "</ol>"


def link(url, en, fr=None):
    fr = fr or en
    return f'<a href="{url}" target="_blank" rel="noopener">{t(en, fr)}</a>'


def refs(*pairs):
    """Footer reference strip: pairs of (url, en, fr)."""
    items = []
    for p in pairs:
        url, en = p[0], p[1]
        fr = p[2] if len(p) > 2 else en
        items.append(link(url, en, fr))
    return '<div class="refs">' + t("Learn more: ", "En savoir plus&nbsp;: ") + " <span class=\"sep\">|</span> ".join(items) + "</div>"


def table(head, rows, cls="", colw=None):
    """head: list of (en, fr); rows: list of lists of (en, fr) or raw html str."""
    def cell(c, tag):
        if isinstance(c, tuple):
            return f"<{tag}>{t(c[0], c[1])}</{tag}>"
        return f"<{tag}>{c}</{tag}>"
    cg = ""
    if colw:
        cg = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in colw) + "</colgroup>"
    h = "<thead><tr>" + "".join(cell(c, "th") for c in head) + "</tr></thead>"
    b = "<tbody>" + "".join("<tr>" + "".join(cell(c, "td") for c in r) + "</tr>" for r in rows) + "</tbody>"
    return f'<table class="{cls}">{cg}{h}{b}</table>'


def panel(title_en, title_fr, body, cls=""):
    return f'<div class="panel {cls}"><h3>{t(title_en, title_fr)}</h3>{body}</div>'


def callout(kind, title_en, title_fr, body_en, body_fr):
    return (f'<div class="callout {kind}"><strong>{t(title_en, title_fr)}</strong> '
            f'{t(body_en, body_fr)}</div>')


def code(s):
    return f'<pre class="code"><code>{esc(s)}</code></pre>'


# ---------------- notes (talk track) -----------------
NL = {
    "en": {"time": "Time", "say": "Say", "qa": "Likely questions", "trans": "Transition", "tip": "Presenter tip", "q": "Q", "a": "A"},
    "fr": {"time": "Durée", "say": "À dire", "qa": "Questions probables", "trans": "Transition", "tip": "Conseil", "q": "Q", "a": "R"},
}


def notes(time, say, trans=None, qa=(), tip=None):
    out = []
    for i, lang in enumerate(("en", "fr")):
        L = NL[lang]
        tm = time[i] if isinstance(time, tuple) else time
        h = f'<p class="n-time"><b>{L["time"]}</b> {tm}</p>'
        if tip:
            h += f'<p class="n-tip"><b>{L["tip"]}</b> {tip[i]}</p>'
        h += f'<h4>{L["say"]}</h4><ul>' + "".join(f"<li>{s[i]}</li>" for s in say) + "</ul>"
        if qa:
            h += f'<h4>{L["qa"]}</h4><dl>'
            for q, a in qa:
                h += f'<dt>{L["q"]}&nbsp;: {q[i]}</dt><dd>{L["a"]}&nbsp;: {a[i]}</dd>' if lang == "fr" else f'<dt>{L["q"]}: {q[i]}</dt><dd>{L["a"]}: {a[i]}</dd>'
            h += "</dl>"
        if trans:
            h += f'<h4>{L["trans"]}</h4><p>{trans[i]}</p>'
        out.append(f'<div class="l-{lang}">{h}</div>')
    return "".join(out)


def add(id, section, title, body, note, layer=None, kind="content", skip=False, lede=None):
    SLIDES.append(dict(id=id, section=section, title=title, body=body, notes=note,
                       layer=layer, kind=kind, skip=skip, lede=lede))


# ---------------- SVG helpers -----------------

def svg(w, h, inner, aria_en, aria_fr, cls="dg", uid="d"):
    defs = (f'<defs>'
            f'<marker id="{uid}-a" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0B2545"/></marker>'
            f'<marker id="{uid}-b" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0078D4"/></marker>'
            f'<marker id="{uid}-w" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9A5B00"/></marker>'
            f'<marker id="{uid}-g" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1E7B3A"/></marker>'
            f'</defs>')
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria_en)}" '
            f'data-aria-en="{esc(aria_en)}" data-aria-fr="{esc(aria_fr)}">{defs}{inner}</svg>')


def _lines(x, y, lines, size, lh, attrs):
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    y0 = y - (n - 1) * lh / 2
    spans = "".join(f'<tspan x="{x}" y="{y0 + k * lh:.1f}">{ln}</tspan>' for k, ln in enumerate(lines))
    return spans


def st(x, y, en, fr, size=18, weight=400, anchor="middle", fill=None, cls="", lh=None, italic=False):
    """Bilingual SVG text; en/fr may be str or list of lines (vertically centred on y)."""
    lh = lh or size * 1.25
    f = f' fill="{fill}"' if fill else ""
    it = ' font-style="italic"' if italic else ""
    out = ""
    for lang, val in (("en", en), ("fr", fr)):
        out += (f'<text class="l-{lang} {cls}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
                f'text-anchor="{anchor}" dominant-baseline="central"{f}{it}>{_lines(x, y, val, size, lh, "")}</text>')
    return out


def rect(x, y, w, h, cls="bx", rx=6, extra=""):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {extra}/>'


def box(x, y, w, h, en, fr, cls="bx", size=18, weight=500, fill=None, sub=None, subsize=15, rx=6):
    """Rect with centred bilingual label; optional sub-label (en, fr) under it."""
    out = rect(x, y, w, h, cls, rx)
    if sub:
        out += st(x + w / 2, y + h / 2 - subsize * 0.75, en, fr, size, weight, fill=fill)
        out += st(x + w / 2, y + h / 2 + size * 0.7, sub[0], sub[1], subsize, 400, fill=fill or "#42566E")
    else:
        out += st(x + w / 2, y + h / 2, en, fr, size, weight, fill=fill)
    return out


def line(x1, y1, x2, y2, cls="ln", marker="a", uid="d", both=False, dash=False):
    m = f' marker-end="url(#{uid}-{marker})"' if marker else ""
    if both and marker:
        m += f' marker-start="url(#{uid}-{marker})"'
    d = ' stroke-dasharray="8 6"' if dash else ""
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{m}{d}/>'


def path(d, cls="ln", marker="a", uid="d", both=False, dash=False):
    m = f' marker-end="url(#{uid}-{marker})"' if marker else ""
    if both and marker:
        m += f' marker-start="url(#{uid}-{marker})"'
    ds = ' stroke-dasharray="8 6"' if dash else ""
    return f'<path class="{cls}" d="{d}" fill="none"{m}{ds}/>'


def pill(x, y, en, fr, w=None, size=15, cls="pill", fill="#0B2545"):
    w = w or 140
    h = size * 1.7
    return rect(x - w / 2, y - h / 2, w, h, cls, rx=h / 2) + st(x, y, en, fr, size, 500, fill=fill)


def figure(svg_html, cap_en, cap_fr, cls=""):
    return f'<figure class="{cls}">{svg_html}<figcaption>{t(cap_en, cap_fr)}</figcaption></figure>'
