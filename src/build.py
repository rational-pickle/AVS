import re, sys, html
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lib import SLIDES, SECTIONS, LAYERS, t, tb, st, esc
import s_intro, s_connect, s_migrate, s_ops, s_perf  # noqa: F401  (registers slides)

OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE.parent / "avs-gen2-client-deck.html")
SEC_IDX = {s[0]: i for i, s in enumerate(SECTIONS)}


# ------------------------------------------------------------ transit graphics
def transit_small(section):
    cur = SEC_IDX.get(section, len(SECTIONS))
    h = '<nav class="transit" aria-hidden="true">'
    for i, (sid, en, fr) in enumerate(SECTIONS):
        cls = "on" if i == cur else ("done" if i < cur else "")
        h += f'<span class="stn {cls}"><i></i>{t(en, fr)}</span>'
    if section == "appendix":
        h += f'<span class="stn on appx"><i></i>{t("Appendix", "Annexe")}</span>'
    return h + "</nav>"


def transit_big(cur, uid, title=False):
    """Large route line for title and divider slides. cur=None -> title (all stations equal)."""
    W, y = 1440, 70
    x0, x1 = 120, 1320
    n = len(SECTIONS)
    xs = [x0 + (x1 - x0) * (k + 1) / (n + 1) for k in range(n)]
    s = ""
    s += f'<line class="hl-base" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>'
    if cur is not None:
        s += f'<line class="hl-done" x1="{x0}" y1="{y}" x2="{xs[cur]:.0f}" y2="{y}"/>'
    else:
        s += f'<line class="hl-draw" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>'
    s += f'<rect class="hl-term" x="{x0 - 14}" y="{y - 14}" width="28" height="28" rx="4"/>'
    s += st(x0, y + 54, ["Your", "datacenter"], ["Votre centre", "de données"], 17, 600, fill="#CFE3F5", lh=20)
    s += f'<circle class="hl-term2" cx="{x1}" cy="{y}" r="16"/>'
    s += st(x1, y + 54, ["Azure VMware", "Solution"], ["Azure VMware", "Solution"], 17, 600, fill="#CFE3F5", lh=20)
    for k, (sid, en, fr) in enumerate(SECTIONS):
        x = xs[k]
        if cur is not None and k == cur:
            s += f'<circle class="hl-cur" cx="{x:.0f}" cy="{y}" r="20"/>'
            s += st(x, y - 44, en, fr, 22, 700, fill="#50E6FF")
        else:
            cls = "hl-stn-done" if (cur is not None and k < cur) else "hl-stn"
            s += f'<circle class="{cls}" cx="{x:.0f}" cy="{y}" r="11"/>'
            s += st(x, y + 44, en, fr, 17, 500, fill="#9FB8D2" if cur is not None else "#E6EEF7")
    aria_en = "Route from your datacenter to Azure through seven topics"
    aria_fr = "Trajet de votre centre de données vers Azure en sept sujets"
    return (f'<svg class="hero-svg" viewBox="0 0 {W} 150" role="img" aria-label="{aria_en}" data-aria-en="{aria_en}" '
            f'data-aria-fr="{aria_fr}">{s}</svg>')


# ------------------------------------------------------------ slides
def badge(layer):
    if not layer:
        return ""
    en, fr = LAYERS[layer]
    return f'<span class="badge b-{layer}">{t(en, fr)}</span>'


parts = []
total = len(SLIDES)
for i, s in enumerate(SLIDES):
    en, fr = s["title"]
    common = (f'id="s{i + 1}" data-id="{s["id"]}" data-section="{s["section"] or ""}" '
              f'data-skip="{1 if s["skip"] else 0}" data-title-en="{esc(re.sub("<[^>]+>|&nbsp;", " ", en))}" '
              f'data-title-fr="{esc(re.sub("<[^>]+>", "", fr).replace("&nbsp;", " "))}"')
    notes = f'<aside class="notes">{s["notes"]}</aside>'
    if s["kind"] == "title":
        body = s["body"].replace('<div class="hero-line" data-hero></div>', f'<div class="hero-line">{transit_big(None, "hero", True)}</div>')
        parts.append(f'<section class="slide s-title" {common}>{body}{notes}</section>')
    elif s["kind"] == "divider":
        cur = SEC_IDX[s["section"]]
        parts.append(
            f'<section class="slide s-divider" {common}>'
            f'<div class="div-wrap"><h2>{t(en, fr)}</h2>{s["body"]}</div>'
            f'<div class="div-line">{transit_big(cur, "dv" + str(i))}</div>'
            f'<span class="s-num">{i + 1}</span>{notes}</section>')
    else:
        parts.append(
            f'<section class="slide s-content" {common} data-layer="{s["layer"] or ""}">'
            f'<header class="s-top">{transit_small(s["section"])}</header>'
            f'<div class="s-head"><h2>{t(en, fr)}</h2>{badge(s["layer"])}</div>'
            f'<div class="s-body">{s["body"]}</div>'
            f'<span class="s-num">{i + 1}</span>{notes}</section>')

slides_html = "\n".join(parts)

# ------------------------------------------------------------ grid classes used
grids = sorted(set(re.findall(r'\bg-(\d+(?:-\d+)+)\b', slides_html)))
grid_css = "\n".join(
    f'.g-{g}{{grid-template-columns:{" ".join(x + "fr" for x in g.split("-"))};}}' for g in grids)

CSS = r"""
:root{
  --navy:#0B2545; --azure:#0078D4; --azure-d:#005A9E; --sky:#50E6FF; --ice:#EAF4FB; --paper:#F7FAFD;
  --slate:#42566E; --line:#C9D8E6; --amber:#9A5B00; --amber-bg:#FFF4DC; --green:#1E7B3A; --green-bg:#E8F5EC;
  --eli:#E7F9FD; --eli-b:#0E8FAE; --ink:#0B2545; --stagebg:#0A1626;
  --font:"Segoe UI Variable Text","Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif;
  --mono:"Cascadia Code","Cascadia Mono",Consolas,"SFMono-Regular",Menlo,monospace;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--stagebg);color:var(--ink);font-family:var(--font);}
html[data-lang="en"] .l-fr{display:none!important}
html[data-lang="fr"] .l-en{display:none!important}
a{color:var(--azure-d);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:3px solid var(--sky);outline-offset:2px}
code{font-family:var(--mono);font-size:.88em;background:#EEF3F8;padding:.05em .3em;border-radius:3px}

/* ---------- stage ---------- */
#stage{position:fixed;left:0;top:0;right:0;bottom:0;overflow:hidden}
body.notes-open #stage{bottom:36vh}
#slides{position:absolute;left:50%;top:50%;width:1600px;height:900px;transform-origin:center center}
.slide{position:absolute;inset:0;width:1600px;height:900px;display:none;overflow:hidden;background:var(--paper);color:var(--ink)}
.slide.active{display:block}
@media (prefers-reduced-motion:no-preference){
  .slide.active{animation:fadein .18s ease-out}
  @keyframes fadein{from{opacity:.4}to{opacity:1}}
  .s-title.active .hl-draw{stroke-dasharray:1300;stroke-dashoffset:1300;animation:draw 1.6s .2s ease-out forwards}
  @keyframes draw{to{stroke-dashoffset:0}}
}
.notes{display:none}

/* ---------- content slide frame ---------- */
.s-content{padding:0 80px}
.s-top{height:58px;display:flex;align-items:flex-end}
.transit{position:relative;display:flex;width:100%;justify-content:space-between;padding-top:6px}
.transit::before{content:"";position:absolute;left:6px;right:6px;top:12px;height:2px;background:#C9D8E6}
.stn{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;font-size:13.5px;color:#7A8CA1;flex:1;min-width:0;white-space:nowrap}
.stn:first-child{align-items:flex-start}.stn:last-child{align-items:flex-end}
.stn i{width:14px;height:14px;border-radius:50%;background:var(--paper);border:2px solid #9FB3C8;display:block;position:relative;z-index:1}
.stn.done i{background:#9FB3C8;border-color:#9FB3C8}
.stn.done{color:#5E7186}
.stn.on i{background:var(--azure);border-color:var(--azure);box-shadow:0 0 0 4px #CFE5F7}
.stn.on{color:var(--azure-d);font-weight:700}
.stn.appx{flex:0 0 auto;margin-left:18px}
.s-head{display:flex;align-items:flex-start;justify-content:space-between;gap:24px;margin-top:22px}
.s-head h2{margin:0;font-size:42px;line-height:1.12;font-weight:600;letter-spacing:-.012em;color:var(--navy);max-width:1220px}
.badge{flex:0 0 auto;margin-top:8px;font-size:15px;font-weight:600;padding:6px 14px;border-radius:999px;white-space:nowrap}
.b-exec{background:var(--navy);color:#fff}
.b-eli5{background:var(--eli);color:#065E73;border:1px solid #9EDDEB}
.b-deep{background:#fff;color:var(--azure-d);border:1.5px solid var(--azure)}
.b-arch{background:var(--ice);color:var(--azure-d);border:1px solid #B9D7F0}
.b-decide{background:var(--green-bg);color:var(--green);border:1px solid #B5DDC1}
.b-plan{background:#EEF1F5;color:var(--slate);border:1px solid #CFD8E2}
.b-appendix{background:#EEF1F5;color:var(--slate);border:1px dashed #9FB3C8}
.s-body{margin-top:24px;font-size:24px;line-height:1.4}
.s-num{position:absolute;right:40px;bottom:22px;font-size:15px;color:#7A8CA1;font-variant-numeric:tabular-nums}
.refs{position:absolute;left:80px;right:110px;bottom:20px;font-size:15px;color:var(--slate);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.refs .sep{color:#9FB3C8;margin:0 6px}

/* ---------- layout ---------- */
.grid{display:grid;gap:28px;align-items:start}
.stack{display:flex;flex-direction:column;gap:18px;min-width:0}
.grid>*{min-width:0}
.mt{margin-top:22px}
.grid .callout:first-child{margin-top:0}
figure{margin:0}
figure svg{display:block;width:100%;height:auto}
figcaption{font-size:18px;color:var(--slate);margin-top:8px;line-height:1.35}

/* ---------- panels and text ---------- */
.panel{background:#fff;border:1px solid var(--line);border-left:6px solid var(--slate);border-radius:4px;padding:20px 26px 20px 24px}
.panel h3{margin:0 0 12px;font-size:24px;font-weight:650;color:var(--navy);line-height:1.2}
.p-exec{border-left-color:var(--navy)}
.p-eli5{border-left-color:var(--eli-b);background:var(--eli)}
.p-deep{border-left-color:var(--azure)}
.p-note{border-left-color:#7A8CA1;background:#FBFCFE}
.p-warn{border-left-color:var(--amber);background:#FFFBF2}
.p-green{border-left-color:var(--green);background:#F6FBF7}
.p-blue{border-left-color:var(--azure);background:#F5FAFE}
.p-code{border-left-color:var(--navy);padding:16px 18px}
.p-code h3{font-size:20px;margin-bottom:10px}
.p-code.sm pre.code{font-size:15.5px}
ul,ol{margin:0;padding-left:1.15em}
li{margin:0 0 10px}
li:last-child{margin-bottom:0}
li::marker{color:var(--azure)}
ul.big li{font-size:25px;line-height:1.38;margin-bottom:16px}
ul.dense li{font-size:21px;line-height:1.36;margin-bottom:9px}
ul.cols2{columns:3;column-gap:36px;margin-top:16px}
ul.cols2 li{break-inside:avoid}
.eli5-text{margin:0;font-size:26px;line-height:1.5;color:#08394A}
.eli5-text.sm{font-size:22px;line-height:1.45}
h3.minor{margin:0 0 10px;font-size:22px;font-weight:650;color:var(--navy)}
b,strong{font-weight:650}

/* steps */
ol.steps{list-style:none;padding:0;margin:0;counter-reset:st;display:grid;gap:8px}
ol.steps li{counter-increment:st;position:relative;padding:8px 12px 8px 54px;font-size:20px;line-height:1.33;background:#fff;border:1px solid var(--line);border-radius:4px;margin:0}
ol.steps li::before{content:counter(st);position:absolute;left:10px;top:50%;transform:translateY(-50%);width:32px;height:32px;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center}

/* tables */
.tbl{width:100%;border-collapse:collapse;background:#fff;font-size:21px;line-height:1.32;table-layout:fixed}
.tbl th{background:var(--navy);color:#fff;text-align:left;font-weight:600;padding:10px 12px;font-size:18px;vertical-align:bottom}
.tbl td{overflow-wrap:anywhere;padding:10px 12px;border-bottom:1px solid #DCE5EE;vertical-align:top}
.tbl tbody tr:nth-child(even) td{background:#F6F9FC}
.tbl td:first-child{font-weight:600;color:var(--navy)}
.tbl-sm{font-size:19px}.tbl-sm th{font-size:17px;padding:8px 10px}.tbl-sm td{padding:8px 10px}
.tbl-md{font-size:18px;line-height:1.32}.tbl-md th{font-size:17px;padding:9px 10px}.tbl-md td{padding:9px 10px}
.tbl-lg{font-size:23px}.tbl-lg td{padding:14px 14px}.tbl-lg th{font-size:20px;padding:12px 14px}
.tbl-xs{font-size:15.5px;line-height:1.3}.tbl-xs th{font-size:15px;padding:8px 10px}.tbl-xs td{padding:7px 10px}
.tbl-tight td{padding:6px 10px}

/* callouts */
.callout{margin-top:20px;padding:14px 18px;border-left:6px solid var(--azure);background:#F1F7FD;font-size:21px;line-height:1.38;border-radius:3px}
.callout strong{margin-right:4px}
.callout.warn{border-left-color:var(--amber);background:var(--amber-bg)}
.callout.warn strong{color:var(--amber)}
.callout.tip strong{color:var(--azure-d)}
.callout.eli5{border-left-color:var(--eli-b);background:var(--eli);margin-top:0;font-size:22px}
.callout.cta{background:var(--navy);color:#fff;border-left-color:var(--sky);font-size:25px;padding:18px 24px;margin-top:28px}
.callout.cta strong{color:var(--sky)}

/* code */
pre.code{margin:0;background:var(--navy);color:#E6F1FB;font-family:var(--mono);font-size:17px;line-height:1.45;padding:14px 16px;border-radius:4px;white-space:pre;overflow:hidden}
pre.code code{background:none;padding:0;font-size:inherit;color:inherit}

/* specific blocks */
.facts{display:grid;gap:10px}
.facts>div{background:#fff;border:1px solid var(--line);border-radius:4px;padding:10px 16px;font-size:19px;line-height:1.35}
.facts b{display:block;color:var(--azure-d);font-size:15px;margin-bottom:2px}
.defs{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:10px}
.defs>div{font-size:19px;line-height:1.35;border-top:3px solid var(--azure);padding-top:8px}
.defs b{display:block;color:var(--navy);margin-bottom:2px}
.route{display:flex;align-items:center;gap:0;margin-top:30px;font-size:22px}
.route>span{padding:10px 18px;border:1.5px solid var(--line);background:#fff;border-radius:4px;font-weight:600;color:var(--navy)}
.route>span.on{border-color:var(--azure);background:var(--ice);color:var(--azure-d)}
.route i{flex:0 0 56px;height:2px;background:var(--navy);position:relative}
.route i::after{content:"";position:absolute;right:-2px;top:-6px;border:7px solid transparent;border-left:10px solid var(--navy);border-right:0}
.calc{margin-top:14px;background:var(--ice);border-radius:4px;padding:12px 14px;font-size:19px;line-height:1.4}
.formula{margin:0 0 14px;font-size:27px;color:var(--navy)}
.rhythm{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.rhythm>div{background:#fff;border:1px solid var(--line);border-top:4px solid var(--azure);border-radius:4px;padding:10px 14px;font-size:19px;line-height:1.35}
.rhythm b{display:block;color:var(--navy);font-size:20px;margin-bottom:2px}
h3.minor.mt{margin-top:24px}
.phase-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:6px}
.phase-grid>div{font-size:19px;line-height:1.35;border-top:3px solid var(--azure);padding-top:8px}
.phase-grid b{display:block;color:var(--navy);font-size:21px;margin-bottom:3px}
.faq{display:grid;grid-template-columns:1fr 1fr;gap:30px 44px}
.faq h3{margin:0 0 6px;font-size:26px;color:var(--navy)}
.faq p{margin:0;font-size:23px;line-height:1.4}
.faq>div{border-left:4px solid var(--azure);padding-left:16px}
.refgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:26px}
.refgrid h3{margin:0 0 12px;font-size:22px;color:var(--navy)}
.refgrid ul{padding-left:1em}
.refgrid li{font-size:19px;line-height:1.35;margin-bottom:10px}

/* agenda */
.g-agenda{grid-template-columns:1.32fr .68fr;gap:44px}
ol.agenda{list-style:none;margin:0;padding:0;counter-reset:ag}
ol.agenda li{counter-increment:ag;display:grid;grid-template-columns:44px 210px 1fr 76px;align-items:baseline;gap:8px;padding:13px 0;border-bottom:1px solid var(--line);margin:0}
ol.agenda li::before{content:counter(ag);font-weight:700;color:var(--azure);font-size:22px}
.ag-sec{font-weight:650;color:var(--navy);font-size:24px}
.ag-desc{font-size:20px;color:var(--slate)}
.ag-min{text-align:right;font-variant-numeric:tabular-nums;font-size:20px;color:var(--navy);font-weight:600}
.legend h3{margin:4px 0 16px;font-size:22px;color:var(--navy)}
.lg-item{margin-bottom:16px}
.lg-item .badge{display:inline-block;margin:0 0 6px}
.lg-item p{margin:0;font-size:18px;color:var(--slate)}

/* ---------- title + dividers ---------- */
.s-title,.s-divider{background:var(--navy);color:#fff}
.s-title{padding:150px 100px 0}
.s-title h1{margin:0;font-size:96px;line-height:1.02;font-weight:650;letter-spacing:-.02em}
.s-title .subtitle{margin:28px 0 0;font-size:31px;line-height:1.35;color:#CFE3F5;max-width:1180px}
.s-title .prepared{margin-top:40px;font-size:21px;color:#9FB8D2}
.s-title .prepared [data-cfg]{color:#fff;font-weight:600}
.cfg-sep:not(:empty){margin:0 12px;color:#5E7894}
.hero-line{position:absolute;left:80px;right:80px;bottom:70px}
.hero-svg{width:100%;height:auto;display:block}
.hl-base{stroke:#2C4A6E;stroke-width:6;stroke-linecap:round}
.hl-draw,.hl-done{stroke:var(--sky);stroke-width:6;stroke-linecap:round}
.hl-term{fill:#2C4A6E;stroke:#9FB8D2;stroke-width:2}
.hl-term2{fill:var(--azure);stroke:#fff;stroke-width:3}
.hl-stn{fill:var(--navy);stroke:#9FB8D2;stroke-width:3}
.hl-stn-done{fill:var(--sky);stroke:var(--sky);stroke-width:3}
.hl-cur{fill:var(--sky);stroke:#fff;stroke-width:5}
.s-title .hl-stn{stroke:var(--sky)}
.s-divider .div-wrap{position:absolute;left:100px;right:100px;top:220px}
.s-divider h2{margin:0;font-size:88px;line-height:1.04;font-weight:650;letter-spacing:-.02em}
.s-divider .promise{margin:26px 0 0;font-size:34px;line-height:1.35;color:var(--sky);max-width:1200px}
.s-divider .div-line{position:absolute;left:80px;right:80px;bottom:110px}
.s-divider .s-num,.s-title .s-num{color:#5E7894}

/* ---------- diagram styling ---------- */
.dg text{fill:var(--navy);font-family:var(--font)}
.bx{fill:#fff;stroke:var(--navy);stroke-width:1.5}
.bx-region{fill:none;stroke:#9FB3C8;stroke-width:1.5;stroke-dasharray:6 5}
.bx-vnet{fill:var(--ice);stroke:var(--azure);stroke-width:2}
.bx-pc{fill:#fff;stroke:var(--azure);stroke-width:1.5}
.bx-soft{fill:#F2F6FA;stroke:#9FB3C8;stroke-width:1.2}
.bx-svc{fill:#fff;stroke:#9FB3C8;stroke-width:1.2}
.bx-onprem,.bx-onprem-f{fill:#EEF1F5;stroke:var(--slate);stroke-width:1.5}
.bx-onprem{fill:#fff}
.bx-hub{fill:#F4F7FB;stroke:var(--navy);stroke-width:1.5}
.bx-fw{fill:var(--amber-bg);stroke:var(--amber);stroke-width:1.5}
.bx-nsx{fill:#DDEEFB;stroke:var(--azure);stroke-width:1.5}
.bx-seg{fill:#fff;stroke:var(--azure);stroke-width:1.2}
.bx-hcx{fill:#D6EAFA;stroke:var(--azure-d);stroke-width:1.8}
.bx-group{fill:none;stroke:#9FB3C8;stroke-width:1.2;stroke-dasharray:5 4}
.bx-underlay{fill:#FFFFFF;stroke:#C9D8E6;stroke-width:1.2;stroke-dasharray:3 4}
.bx-q{fill:#E3EEF8;stroke:var(--navy);stroke-width:1.5}
.bx-pick{fill:var(--green-bg);stroke:var(--green);stroke-width:2}
.bx-pick2{fill:#DDEEFB;stroke:var(--azure);stroke-width:2}
.bx-lane0{fill:var(--ice);stroke:var(--azure);stroke-width:1.5}
.bx-lane1{fill:var(--green-bg);stroke:var(--green);stroke-width:1.5}
.bx-span{fill:#F2F6FA;stroke:#C9D8E6;stroke-width:1}
.bx-fail{fill:#FFF4DC;stroke:#E2B86B;stroke-width:1.2}
.st-hw{fill:#BBD6EE;stroke:var(--azure-d);stroke-width:1}
.st-vsan{fill:#CBE0F3;stroke:var(--azure-d);stroke-width:1}
.st-vc{fill:#DAE9F7;stroke:var(--azure-d);stroke-width:1}
.st-nsx{fill:#E7F1FA;stroke:var(--azure-d);stroke-width:1}
.st-hcx{fill:#F3F8FD;stroke:var(--azure-d);stroke-width:1}
.srm-ms{fill:var(--azure)}
.srm-cu{fill:#fff;stroke:var(--navy);stroke-width:1.5}
.srm-pa{fill:#F2F6FA;stroke:#9FB3C8;stroke-width:1.5;stroke-dasharray:6 4}
.pill,.pill-net{fill:var(--green-bg);stroke:var(--green);stroke-width:1.5}
.ln{stroke:var(--navy);stroke-width:2;fill:none}
.ln-b{stroke:var(--azure);stroke-width:2.6;fill:none}
.ln-g{stroke:var(--green);stroke-width:2.6;fill:none}
.ln-w{stroke:var(--amber);stroke-width:2.8;fill:none}
.ln-er{stroke:var(--navy);stroke-width:4;fill:none}
.ln-tun{stroke:var(--azure);stroke-width:5;fill:none;opacity:.85}
.ln-time{stroke:var(--navy);stroke-width:3}
.ln-track{stroke:#9CCBF0;stroke-width:4}
.dot{fill:var(--azure)}
.dot-on{fill:var(--green);stroke:#fff;stroke-width:3}
.tick{stroke:#E1E8EF;stroke-width:1}
.bar{fill:var(--azure)}
.bar-soft{fill:#9CCBF0}
.bar-pick{fill:var(--green)}

/* ---------- chrome: toolbar, notes, overview ---------- */
#prog{position:fixed;left:0;top:0;height:3px;background:var(--sky);z-index:30;transition:width .2s}
#bar{position:fixed;right:14px;bottom:12px;z-index:40;display:flex;gap:6px;align-items:center;opacity:.28;transition:opacity .2s;background:rgba(10,22,38,.82);padding:6px 8px;border-radius:8px;font-family:var(--font)}
#bar:hover,#bar:focus-within{opacity:1}
body.idle #bar:not(:hover):not(:focus-within){opacity:0}
body.idle{cursor:none}
body.notes-open #bar{bottom:calc(36vh + 12px)}
#bar button{background:transparent;color:#DCE8F5;border:1px solid #33506F;border-radius:5px;padding:5px 9px;font-size:13px;cursor:pointer;font-family:inherit}
#bar button:hover{background:#18324F}
#bar button[aria-pressed="true"]{background:var(--azure);border-color:var(--azure);color:#fff}
#bar .cnt{color:#DCE8F5;font-size:13px;min-width:62px;text-align:center;font-variant-numeric:tabular-nums}
#bar .lang button{border-radius:0;padding:5px 8px}
#bar .lang button:first-child{border-radius:5px 0 0 5px}
#bar .lang button:last-child{border-radius:0 5px 5px 0;margin-left:-1px}
#notesPane{position:fixed;left:0;right:0;bottom:0;height:36vh;background:#0E1E33;color:#E6EEF7;z-index:35;display:none;overflow:auto;padding:16px 28px 22px;font-size:17px;line-height:1.5;border-top:3px solid var(--azure)}
body.notes-open #notesPane{display:block}
#notesPane .nh{display:flex;justify-content:space-between;gap:20px;color:#9FB8D2;font-size:14px;margin-bottom:6px}
#notesPane .nh b{color:#fff;font-size:16px}
#notesPane h4,.pw h4{margin:12px 0 4px;color:var(--sky);font-size:14px;font-weight:700}
#notesPane ul{margin:0;padding-left:1.1em}
#notesPane li{margin:0 0 6px}
#notesPane li::marker{color:var(--sky)}
#notesPane dt{font-weight:650;margin-top:6px}
#notesPane dd{margin:2px 0 6px 0;color:#CFE0F1}
#notesPane p{margin:4px 0}
.n-time b,.n-tip b{color:var(--sky);margin-right:6px}
.n-tip{background:#162C47;padding:8px 10px;border-radius:4px}
#overview{position:fixed;inset:0;background:rgba(7,16,28,.96);z-index:50;display:none;overflow:auto;padding:36px 48px;color:#E6EEF7;font-family:var(--font)}
#overview.open{display:block}
#overview h2{margin:0 0 18px;font-size:24px}
#overview .ov-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
#overview h3{margin:0 0 8px;font-size:15px;color:var(--sky);font-weight:700}
#overview button{display:block;width:100%;text-align:left;background:#10233B;border:1px solid #233F60;color:#E6EEF7;padding:7px 10px;margin-bottom:6px;border-radius:5px;font-size:14px;cursor:pointer;font-family:inherit}
#overview button.cur{border-color:var(--sky)}
#overview button.skipped{opacity:.45}
#overview button span.n{color:#7FA3C8;margin-right:8px;font-variant-numeric:tabular-nums}
#toast{position:fixed;left:50%;top:18px;transform:translateX(-50%);background:#0E1E33;color:#fff;border:1px solid var(--azure);padding:10px 16px;border-radius:6px;font-size:14px;z-index:60;display:none;font-family:var(--font)}

/* ---------- print ---------- */
@media print{
  @page{size:1600px 900px;margin:0}
  html,body{background:#fff;height:auto}
  #bar,#notesPane,#overview,#prog,#toast{display:none!important}
  #stage{position:static;overflow:visible}
  #slides{position:static;transform:none!important;width:1600px;height:auto}
  .slide{display:block!important;position:relative;break-after:page;page-break-after:always;animation:none!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .hl-draw{stroke-dasharray:none!important;stroke-dashoffset:0!important}
}
"""

JS = r"""
(function(){
  const cfg = Object.assign({client:"", presenter:"", date:""}, window.DECK_CONFIG || {});
  const root = document.documentElement;
  const slides = Array.from(document.querySelectorAll('.slide'));
  const wrap = document.getElementById('slides');
  const stage = document.getElementById('stage');
  const pane = document.getElementById('notesPane');
  const cnt = document.getElementById('cnt');
  const prog = document.getElementById('prog');
  const ov = document.getElementById('overview');
  const toast = document.getElementById('toast');
  const store = {
    get(k){ try { return localStorage.getItem('avsdeck.'+k); } catch(e){ return null; } },
    set(k,v){ try { localStorage.setItem('avsdeck.'+k, v); } catch(e){} }
  };
  const deck = { i:0, lang: store.get('lang') || 'en', deep: store.get('deep') !== '0', pw:null, t0:null };
  window.avsDeck = deck;

  // config into title slide
  document.querySelectorAll('[data-cfg]').forEach(el => { el.textContent = cfg[el.dataset.cfg] || ''; });
  const sep1 = document.querySelector('[data-cfg-sep]'); const sep2 = document.querySelector('[data-cfg-sep2]');
  if (sep1) sep1.textContent = (cfg.client && cfg.presenter) ? '|' : '';
  if (sep2) sep2.textContent = ((cfg.client || cfg.presenter) && cfg.date) ? '|' : '';
  if (!cfg.client) document.querySelectorAll('[data-cfg="client"]').forEach(el => el.textContent = '—');

  function title(s, lang){ return s.dataset['title' + (lang === 'fr' ? 'Fr' : 'En')]; }
  function skipped(k){ return !deck.deep && slides[k].dataset.skip === '1'; }

  function fit(){
    const W = stage.clientWidth, H = stage.clientHeight;
    const s = Math.min(W / 1600, H / 900);
    wrap.style.transform = 'translate(-50%,-50%) scale(' + s + ')';
  }

  function setLang(l){
    deck.lang = l; root.dataset.lang = l; root.lang = (l === 'fr' ? 'fr-CA' : 'en');
    store.set('lang', l);
    document.querySelectorAll('svg[data-aria-en]').forEach(sv => sv.setAttribute('aria-label', sv.dataset['aria' + (l === 'fr' ? 'Fr' : 'En')]));
    document.querySelectorAll('[data-lang-btn]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.langBtn === l)));
    document.title = (l === 'fr' ? 'AVS Gen 2 : rencontre client' : 'AVS Gen 2: client briefing');
    render(); buildOverview();
  }

  function render(){
    slides.forEach((s, k) => s.classList.toggle('active', k === deck.i));
    const s = slides[deck.i];
    cnt.textContent = (deck.i + 1) + ' / ' + slides.length;
    prog.style.width = ((deck.i + 1) / slides.length * 100) + '%';
    if (location.hash !== '#' + (deck.i + 1)) history.replaceState(null, '', '#' + (deck.i + 1));
    // notes pane
    let nx = deck.i + 1; while (nx < slides.length && skipped(nx)) nx++;
    const L = deck.lang === 'fr';
    const nextT = nx < slides.length ? title(slides[nx], deck.lang) : (L ? 'Fin' : 'End');
    pane.innerHTML = '<div class="nh"><span><b>' + (deck.i + 1) + '. ' + title(s, deck.lang) + '</b>' +
      (s.dataset.skip === '1' ? (L ? ' (plongée technique, peut être sautée)' : ' (deep dive, can be skipped)') : '') +
      '</span><span>' + (L ? 'Suivante : ' : 'Next: ') + nextT + '</span></div>' + (s.querySelector('.notes') ? s.querySelector('.notes').innerHTML : '');
    renderPresenter();
  }

  function go(k){ deck.i = Math.max(0, Math.min(slides.length - 1, k)); render(); }
  function next(){ let k = deck.i + 1; while (k < slides.length && skipped(k)) k++; if (k < slides.length) go(k); }
  function prev(){ let k = deck.i - 1; while (k > 0 && skipped(k)) k--; if (k >= 0) go(k); }
  deck.go = go; deck.next = next; deck.prev = prev;

  function toggleNotes(){ document.body.classList.toggle('notes-open'); document.getElementById('bNotes').setAttribute('aria-pressed', String(document.body.classList.contains('notes-open'))); fit(); }
  function toggleDeep(){ deck.deep = !deck.deep; store.set('deep', deck.deep ? '1' : '0'); document.getElementById('bDeep').setAttribute('aria-pressed', String(deck.deep)); say(deck.deep ? (deck.lang === 'fr' ? 'Plongées techniques affichées' : 'Deep dives shown') : (deck.lang === 'fr' ? 'Plongées techniques sautées' : 'Deep dives skipped')); buildOverview(); render(); }
  function toggleOverview(force){ const open = force !== undefined ? force : !ov.classList.contains('open'); ov.classList.toggle('open', open); if (open) { buildOverview(); const c = ov.querySelector('button.cur'); if (c) c.focus(); } }
  function fullscreen(){ if (!document.fullscreenElement) { (root.requestFullscreen || function(){}).call(root); } else { document.exitFullscreen(); } }
  function say(msg){ toast.textContent = msg; toast.style.display = 'block'; clearTimeout(say._t); say._t = setTimeout(() => toast.style.display = 'none', 1800); }
  deck.toggleNotes = toggleNotes; deck.toggleDeep = toggleDeep; deck.setLang = setLang;

  function buildOverview(){
    const secs = [];
    let cur = null;
    slides.forEach((s, k) => {
      const sec = s.dataset.section || 'intro';
      if (!cur || cur.sec !== sec) { cur = { sec, items: [] }; secs.push(cur); }
      cur.items.push(k);
    });
    const names = SECTION_NAMES;
    let h = '<h2>' + (deck.lang === 'fr' ? 'Diapositives' : 'Slides') + '</h2><div class="ov-grid">';
    secs.forEach(g => {
      const nm = names[g.sec] ? names[g.sec][deck.lang === 'fr' ? 1 : 0] : g.sec;
      h += '<div><h3>' + nm + '</h3>';
      g.items.forEach(k => {
        h += '<button data-k="' + k + '" class="' + (k === deck.i ? 'cur ' : '') + (skipped(k) ? 'skipped' : '') + '"><span class="n">' + (k + 1) + '</span>' + title(slides[k], deck.lang) + '</button>';
      });
      h += '</div>';
    });
    ov.innerHTML = h + '</div>';
    ov.querySelectorAll('button[data-k]').forEach(b => b.addEventListener('click', () => { go(+b.dataset.k); toggleOverview(false); }));
  }

  // ---------- presenter window ----------
  function openPresenter(){
    if (deck.pw && !deck.pw.closed) { deck.pw.focus(); return; }
    const w = window.open('', 'avs-presenter', 'width=1280,height=820');
    if (!w) { say(deck.lang === 'fr' ? 'Autorisez les fenêtres contextuelles pour ouvrir la vue présentateur' : 'Allow pop-ups to open the presenter window'); return; }
    const css = document.getElementById('deck-css').textContent;
    w.document.open();
    w.document.write('<!doctype html><html data-lang="' + deck.lang + '"><head><meta charset="utf-8"><title>Presenter</title><style>' + css + PW_CSS + '</style></head><body class="pw"><div class="pw-top"><div><span id="pwN"></span> <b id="pwT"></b></div><div class="pw-ctl"><button id="pwPrev">‹</button><button id="pwNext">›</button><button id="pwLang">EN / FR</button><span id="pwClock"></span><span id="pwTimer"></span><button id="pwReset">⟲</button></div></div><div class="pw-main"><div class="pw-left"><div class="pv pv-cur" id="pvCur"></div><div class="pw-nextlbl" id="pwNextLbl"></div><div class="pv pv-next" id="pvNext"></div></div><div class="pw-notes" id="pwNotes"></div></div></body></html>');
    w.document.close();
    deck.pw = w; deck.t0 = Date.now();
    w.document.getElementById('pwPrev').onclick = prev;
    w.document.getElementById('pwNext').onclick = next;
    w.document.getElementById('pwLang').onclick = () => setLang(deck.lang === 'fr' ? 'en' : 'fr');
    w.document.getElementById('pwReset').onclick = () => { deck.t0 = Date.now(); tick(); };
    w.document.addEventListener('keydown', onKey);
    w.addEventListener('resize', renderPresenter);
    renderPresenter();
  }
  function clonePreview(box, k){
    box.innerHTML = '';
    if (k == null || k >= slides.length) return;
    const c = slides[k].cloneNode(true);
    c.classList.add('active'); c.removeAttribute('id');
    const n = c.querySelector('.notes'); if (n) n.remove();
    const inner = deck.pw.document.createElement('div');
    inner.className = 'pv-in';
    inner.appendChild(deck.pw.document.importNode(c, true));
    box.appendChild(inner);
    const s = box.clientWidth / 1600;
    inner.style.transform = 'scale(' + s + ')';
    box.style.height = (900 * s) + 'px';
  }
  function renderPresenter(){
    const w = deck.pw; if (!w || w.closed) return;
    const d = w.document; d.documentElement.dataset.lang = deck.lang;
    const s = slides[deck.i];
    let nx = deck.i + 1; while (nx < slides.length && skipped(nx)) nx++;
    d.getElementById('pwN').textContent = (deck.i + 1) + ' / ' + slides.length;
    d.getElementById('pwT').textContent = title(s, deck.lang);
    d.getElementById('pwNotes').innerHTML = s.querySelector('.notes') ? s.querySelector('.notes').innerHTML : '';
    d.getElementById('pwNextLbl').textContent = (deck.lang === 'fr' ? 'Suivante : ' : 'Next: ') + (nx < slides.length ? title(slides[nx], deck.lang) : (deck.lang === 'fr' ? 'Fin' : 'End'));
    clonePreview(d.getElementById('pvCur'), deck.i);
    clonePreview(d.getElementById('pvNext'), nx < slides.length ? nx : null);
    tick();
  }
  function tick(){
    const w = deck.pw; if (!w || w.closed) return;
    const e = Math.floor((Date.now() - (deck.t0 || Date.now())) / 1000);
    const mm = String(Math.floor(e / 60)).padStart(2, '0'), ss = String(e % 60).padStart(2, '0');
    w.document.getElementById('pwTimer').textContent = mm + ':' + ss;
    w.document.getElementById('pwClock').textContent = new Date().toLocaleTimeString(deck.lang === 'fr' ? 'fr-CA' : 'en-CA', {hour:'2-digit', minute:'2-digit'});
  }
  setInterval(tick, 1000);
  deck.openPresenter = openPresenter;

  // ---------- input ----------
  function onKey(e){
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (ov.classList.contains('open') && k === 'Escape') { toggleOverview(false); return; }
    if (['ArrowRight', 'PageDown', ' ', 'ArrowDown'].includes(k)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp', 'ArrowUp', 'Backspace'].includes(k)) { e.preventDefault(); prev(); }
    else if (k === 'Home') { go(0); }
    else if (k === 'End') { go(slides.length - 1); }
    else if (k === 'n' || k === 'N') { toggleNotes(); }
    else if (k === 'l' || k === 'L') { setLang(deck.lang === 'fr' ? 'en' : 'fr'); }
    else if (k === 'd' || k === 'D') { toggleDeep(); }
    else if (k === 'o' || k === 'O') { toggleOverview(); }
    else if (k === 'p' || k === 'P') { openPresenter(); }
    else if (k === 'f' || k === 'F') { fullscreen(); }
  }
  document.addEventListener('keydown', onKey);
  let idleT = null;
  function wake(){ document.body.classList.remove('idle'); clearTimeout(idleT); idleT = setTimeout(() => document.body.classList.add('idle'), 2500); }
  document.addEventListener('mousemove', wake); wake();
  let tx = null;
  stage.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, {passive:true});
  stage.addEventListener('touchend', e => { if (tx == null) return; const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) { dx < 0 ? next() : prev(); } tx = null; });
  document.getElementById('bPrev').onclick = prev;
  document.getElementById('bNext').onclick = next;
  document.getElementById('bNotes').onclick = toggleNotes;
  document.getElementById('bPres').onclick = openPresenter;
  document.getElementById('bDeep').onclick = toggleDeep;
  document.getElementById('bOv').onclick = () => toggleOverview();
  document.getElementById('bFs').onclick = fullscreen;
  document.querySelectorAll('[data-lang-btn]').forEach(b => b.onclick = () => setLang(b.dataset.langBtn));
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => { const n = parseInt(location.hash.slice(1), 10); if (n >= 1 && n <= slides.length && n - 1 !== deck.i) go(n - 1); });

  const h = parseInt(location.hash.slice(1), 10);
  if (h >= 1 && h <= slides.length) deck.i = h - 1;
  document.getElementById('bDeep').setAttribute('aria-pressed', String(deck.deep));
  fit(); setLang(deck.lang);
})();
"""

PW_CSS = r"""
body.pw{background:#0A1626;color:#E6EEF7;font-family:var(--font);margin:0;padding:14px 18px;height:100vh;display:flex;flex-direction:column;box-sizing:border-box;overflow:hidden}
.pw-top{display:flex;justify-content:space-between;align-items:center;gap:16px;font-size:16px;margin-bottom:12px}
.pw-top b{font-size:18px;color:#fff}
.pw-ctl{display:flex;gap:8px;align-items:center}
.pw-ctl button{background:#10233B;border:1px solid #33506F;color:#E6EEF7;border-radius:5px;padding:6px 12px;font-size:15px;cursor:pointer}
#pwTimer{font-size:24px;font-weight:700;color:#50E6FF;font-variant-numeric:tabular-nums;min-width:80px;text-align:right}
#pwClock{font-size:16px;color:#9FB8D2}
.pw-main{display:grid;grid-template-columns:44% 56%;gap:18px;flex:1;min-height:0}
.pw-left{min-width:0}
.pv{position:relative;overflow:hidden;border:1px solid #33506F;border-radius:4px;background:#000}
.pv-in{position:absolute;left:0;top:0;width:1600px;height:900px;transform-origin:0 0}
.pv-in .slide{display:block;animation:none}
.pv-next{width:70%;opacity:.85}
.pw-nextlbl{margin:12px 0 6px;color:#9FB8D2;font-size:15px}
.pw-notes{overflow:auto;font-size:19px;line-height:1.5;padding-right:8px}
.pw-notes ul{padding-left:1.1em;margin:0}
.pw-notes li{margin-bottom:8px}
.pw-notes li::marker{color:#50E6FF}
.pw-notes dt{font-weight:650;margin-top:8px}
.pw-notes dd{margin:2px 0 8px;color:#CFE0F1}
.pw-notes p{margin:4px 0}
.pw h4{font-size:15px}
"""

names_js = "{" + ",".join(f'"{sid}":["{en}","{fr}"]' for sid, en, fr in SECTIONS) + ',"appendix":["Appendix","Annexe"]}'

page = f"""<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AVS Gen 2: client briefing</title>
<script id="deck-config">
/* ===== Edit before presenting =====
   client:    shown on the title slide ("Prepared for ...")
   presenter: your name (optional)
   date:      meeting date (optional)
   Keys: Left/Right navigate | L language EN/FR | N talk track | P presenter window
         D skip deep dives | O slide list | F full screen | Print to PDF from the browser */
window.DECK_CONFIG = {{ client: "Client name", presenter: "", date: "" }};
</script>
<style id="deck-css">{CSS}
{grid_css}</style>
</head>
<body>
<div id="prog"></div>
<main id="stage"><div id="slides">
{slides_html}
</div></main>
<div id="bar" role="toolbar" aria-label="Deck controls">
  <button id="bPrev" aria-label="Previous slide">‹</button><span class="cnt" id="cnt"></span><button id="bNext" aria-label="Next slide">›</button>
  <span class="lang"><button data-lang-btn="en" aria-pressed="true">EN</button><button data-lang-btn="fr" aria-pressed="false">FR</button></span>
  <button id="bNotes" aria-pressed="false" title="N">{t("Notes", "Notes")}</button>
  <button id="bPres" title="P">{t("Presenter", "Présentateur")}</button>
  <button id="bDeep" aria-pressed="true" title="D">{t("Deep dives", "Plongées")}</button>
  <button id="bOv" title="O">{t("Slides", "Diapos")}</button>
  <button id="bFs" title="F" aria-label="Full screen">⛶</button>
</div>
<section id="notesPane" aria-label="Talk track"></section>
<div id="overview" role="dialog" aria-label="Slide list"></div>
<div id="toast" role="status"></div>
<script>
const SECTION_NAMES = {names_js};
const PW_CSS = {PW_CSS!r};
{JS}
</script>
</body>
</html>
"""
# PW_CSS repr uses python quoting; make sure it is valid JS string
page = page.replace("const PW_CSS = " + repr(PW_CSS), "const PW_CSS = " + __import__("json").dumps(PW_CSS))
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, len(page) // 1024, "KB,", total, "slides")
