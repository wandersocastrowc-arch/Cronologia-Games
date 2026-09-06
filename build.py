# -*- coding: utf-8 -*-
"""Gera o site estático multilíngue em ./dist"""
import os, json, shutil, urllib.parse
from data import LANGS, DEFAULT, HTML_LANG, UI, LANG_NAME, ERAS, GAMES, STORES, LANG_COUNTRY

BASE = "https://SEU-DOMINIO.com"          # trocar pelo domínio real
OUT  = os.path.join(os.path.dirname(__file__), "dist")

CSS = """
:root{
  --ground:#0A0B0D;--surface:#131519;--surface-2:#1A1D22;--line:#262A31;
  --ink:#EDEFF2;--ink-2:#9AA1AC;--ink-3:#6B7280;--accent:#FF3B1F;
  --display:"Archivo Black","Arial Black",system-ui,sans-serif;
  --cond:"Barlow Condensed","Arial Narrow",Impact,sans-serif;
  --body:"Barlow","Helvetica Neue",Arial,system-ui,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--body);
  -webkit-font-smoothing:antialiased;line-height:1.55}
a{color:inherit}
.wrap{max-width:1220px;margin:0 auto;padding:0 clamp(16px,4vw,36px)}

/* ---------- barra de controles ---------- */
.bar{position:sticky;top:0;z-index:50;background:rgba(10,11,13,.93);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:11px;padding-bottom:11px}
.brand{font-family:var(--cond);font-weight:700;font-size:20px;letter-spacing:.06em;
  text-transform:uppercase;margin-right:auto;text-decoration:none}
.ctl{display:flex;align-items:center;gap:8px}
.ctl label{font-size:10.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.langs{display:flex;gap:2px;background:var(--line);padding:2px;border-radius:5px}
.langs a{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
  padding:5px 11px;border-radius:3px;text-decoration:none;color:var(--ink-2)}
.langs a[aria-current="true"]{background:var(--ink);color:var(--ground)}
.langs a:hover:not([aria-current="true"]){background:var(--surface-2);color:var(--ink)}
select{font-family:var(--body);font-size:13px;font-weight:500;color:var(--ink);
  background:var(--surface-2);border:1px solid var(--line);border-radius:5px;padding:6px 9px}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* ---------- topo ---------- */
header{padding:clamp(40px,7vw,84px) 0 clamp(28px,4vw,44px)}
.kick{font-size:11.5px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);margin-bottom:16px}
h1{font-family:var(--display);font-size:clamp(42px,9vw,92px);line-height:.92;
  letter-spacing:-.03em;margin:0 0 20px}
.sub{font-size:clamp(15.5px,1.8vw,19px);color:var(--ink-2);max-width:56ch;margin:0}

/* ---------- eras ---------- */
h2{font-family:var(--display);font-size:clamp(19px,2.4vw,26px);letter-spacing:-.01em;margin:0 0 20px}
.eras{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:2px;
  background:var(--line);border:2px solid var(--line);margin-bottom:clamp(44px,6vw,72px)}
.era{background:var(--surface);padding:15px 17px 17px}
.era i{display:block;width:22px;height:3px;border-radius:2px;margin-bottom:10px}
.era b{display:block;font-family:var(--cond);font-weight:700;font-size:20px;line-height:1;
  text-transform:uppercase;margin-bottom:5px}
.era span{font-size:12px;color:var(--ink-3);font-variant-numeric:tabular-nums}

/* ---------- jogos ---------- */
.games{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));
  gap:clamp(14px,2vw,22px);margin-bottom:56px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:6px;
  overflow:hidden;display:flex;flex-direction:column}
.art{position:relative;aspect-ratio:4/3;overflow:hidden;container-type:inline-size;
  background:linear-gradient(158deg,var(--c1),var(--c2));color:var(--ti);
  display:flex;flex-direction:column;justify-content:flex-end}
.art .motif{position:absolute;inset:0}
.art .scrim{position:absolute;inset:0;
  background:linear-gradient(to top,color-mix(in srgb,var(--c2) 85%,#000),transparent 66%)}
.art .band{position:absolute;top:0;left:0;right:0;height:4px;background:var(--era)}
.art .yr{position:absolute;top:14px;right:14px;z-index:3;font-weight:600;font-size:13px;
  letter-spacing:.06em;opacity:.75;font-variant-numeric:tabular-nums}
.art .tx{position:relative;z-index:3;padding:16px 18px}
.art .pre{font-size:9.5px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;
  opacity:.8;margin-bottom:4px}
.art .nm{font-family:var(--cond);font-weight:700;font-size:30px;line-height:.9;
  text-transform:uppercase}
.info{padding:16px 18px 18px;display:flex;flex-direction:column;gap:11px;flex:1}
.hook{font-size:13.5px;color:var(--ink-2);margin:0;flex:1}
.studio{font-size:11px;color:var(--ink-3);letter-spacing:.04em}
.studio b{color:var(--ink-2);font-weight:600}
.buy{display:flex;align-items:center;justify-content:space-between;gap:10px;
  font-family:var(--cond);font-weight:700;font-size:16px;letter-spacing:.05em;
  text-transform:uppercase;text-decoration:none;color:var(--ground);
  background:var(--accent);padding:10px 14px;border-radius:4px}
.buy:hover{filter:brightness(1.1)}
.buy span{font-family:var(--body);font-size:11px;font-weight:600;letter-spacing:.02em;
  text-transform:none;opacity:.82}

/* ---------- motivos ---------- */
.m-horizon{background:radial-gradient(58cqi 30cqi at 50% 78%,color-mix(in srgb,var(--gl) 60%,transparent),transparent 72%)}
.m-neon{inset:auto 0 -14% 0;height:70%;opacity:.5;transform:perspective(34cqi) rotateX(64deg);transform-origin:50% 100%;
  background:repeating-linear-gradient(90deg,transparent 0 8cqi,var(--gl) 8cqi 8.6cqi),
             repeating-linear-gradient(0deg,transparent 0 10cqi,var(--gl) 10cqi 10.6cqi)}
.m-pursuit{background:linear-gradient(112deg,var(--p1) 0 44%,transparent 44% 56%,var(--p2) 56%);opacity:.6}
.m-halftone{background-image:radial-gradient(var(--gl) 1cqi,transparent 1.1cqi);background-size:6cqi 6cqi;opacity:.4}
.m-scan{background:repeating-linear-gradient(0deg,var(--gl) 0 .5cqi,transparent .5cqi 3cqi);opacity:.32}
.m-track{background:repeating-radial-gradient(circle at 84% 14%,transparent 0 6.4cqi,var(--gl) 6.4cqi 7cqi);opacity:.42}
.m-stripe{background:repeating-linear-gradient(74deg,var(--gl) 0 3.4cqi,transparent 3.4cqi 12cqi);opacity:.4}
.m-shard{background:var(--gl);clip-path:polygon(0 56%,100% 16%,100% 44%,0 88%);opacity:.7}

/* ---------- carrossel ---------- */
.carousel{margin:0 0 clamp(44px,6vw,68px)}
.chead{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:14px}
.chead h2{margin:0}
.cnav{display:flex;gap:8px}
.cnav button{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);
  background:var(--surface-2);color:var(--ink);font-size:17px;line-height:1;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:border-color .15s,background .15s}
.cnav button:hover{border-color:var(--accent);background:var(--surface)}
.cnav button[disabled]{opacity:.32;cursor:default;border-color:var(--line);background:var(--surface-2)}
.track{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
  scroll-behavior:smooth;scrollbar-width:none;padding-bottom:4px}
.track::-webkit-scrollbar{display:none}
.slide{scroll-snap-align:start;flex:0 0 clamp(210px,26vw,286px);text-decoration:none;
  border-radius:6px;overflow:hidden;border:1px solid var(--line);position:relative;
  transition:border-color .15s,transform .15s}
.slide:hover,.slide:focus-visible{border-color:var(--accent);transform:translateY(-3px)}
.slide .art{aspect-ratio:1}
.slide .art .nm{font-size:clamp(24px,4.6cqi,34px)}
.dots{display:flex;gap:5px;justify-content:center;margin-top:16px;flex-wrap:wrap}
.dots i{width:5px;height:5px;border-radius:50%;background:var(--line);display:block;transition:background .2s,width .2s}
.dots i.on{background:var(--accent);width:18px;border-radius:3px}
@media (prefers-reduced-motion:reduce){.track{scroll-behavior:auto}.slide{transition:none}}

/* ---------- rodapé ---------- */
footer{border-top:1px solid var(--line);padding:26px 0 60px;font-size:12.5px;
  color:var(--ink-3);display:flex;flex-direction:column;gap:10px}
.note{background:var(--surface);border-left:2px solid var(--accent);padding:11px 14px;
  border-radius:0 5px 5px 0;color:var(--ink-2);max-width:78ch}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo+Black&family=Barlow+Condensed:wght@600;700&'
         'family=Barlow:wght@400;500;600&display=swap">')


def hreflangs(cur):
    out = [f'<link rel="alternate" hreflang="{HTML_LANG[l]}" href="{BASE}/{l}/">' for l in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return "\n  ".join(out)


def card(g, lang, i):
    c1, c2, ti, motif, gl, p2 = g["st"]
    style = f'--c1:{c1};--c2:{c2};--ti:{ti};--era:{ERAS[g["era"]]["color"]};'
    style += f'--p1:{gl};--p2:{p2};' if motif == "m-pursuit" else f'--gl:{gl};'
    return f'''      <article class="card" id="g{i}">
        <div class="art" style="{style}">
          <div class="motif {motif}"></div><div class="scrim"></div><div class="band"></div>
          <div class="yr">{g["y"]}</div>
          <div class="tx"><div class="pre">{g["pre"]}</div><div class="nm">{g["nm"]}</div></div>
        </div>
        <div class="info">
          <p class="hook">{g["hook"][lang]}</p>
          <div class="studio">{UI[lang]["studio"]}: <b>{g["studio"]}</b></div>
          <a class="buy" href="#" data-q="{urllib.parse.quote(g["q"])}" rel="nofollow sponsored noopener"
             target="_blank">{UI[lang]["buy"]} <span class="store"></span></a>
        </div>
      </article>'''


def slide(g, lang, i):
    c1, c2, ti, motif, gl, p2 = g["st"]
    style = f'--c1:{c1};--c2:{c2};--ti:{ti};--era:{ERAS[g["era"]]["color"]};'
    style += f'--p1:{gl};--p2:{p2};' if motif == "m-pursuit" else f'--gl:{gl};'
    return f'''      <a class="slide" href="#g{i}" aria-label="{UI[lang]["gotogame"]}: {g["name"]}, {g["y"]}">
        <div class="art" style="{style}">
          <div class="motif {motif}"></div><div class="scrim"></div><div class="band"></div>
          <div class="yr">{g["y"]}</div>
          <div class="tx"><div class="pre">{g["pre"]}</div><div class="nm">{g["nm"]}</div></div>
        </div>
      </a>'''


def page(lang):
    t = UI[lang]
    eras = "\n".join(
        f'      <div class="era"><i style="background:{e["color"]}"></i>'
        f'<b>{e[lang]}</b><span>{e["span"]}</span></div>'
        for e in ERAS.values())
    langs = "\n".join(
        f'        <a href="{BASE if False else ""}/{l}/" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}"'
        + (' aria-current="true"' if l == lang else "")
        + f'>{LANG_NAME[l]}</a>' for l in LANGS)
    stores = "\n".join(
        f'          <option value="{k}">{v["name"]}</option>' for k, v in STORES.items())
    games = "\n".join(card(g, lang, i) for i, g in enumerate(GAMES))
    slides = "\n".join(slide(g, lang, i) for i, g in enumerate(GAMES))
    dots = "".join("<i></i>" for _ in GAMES)

    return f'''<!doctype html>
<html lang="{HTML_LANG[lang]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["meta"]}">
  <link rel="canonical" href="{BASE}/{lang}/">
  {hreflangs(lang)}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{HTML_LANG[lang].replace("-", "_")}">
  <meta property="og:url" content="{BASE}/{lang}/">
  <meta property="og:title" content="{t["title"]}">
  <meta property="og:description" content="{t["meta"]}">
  <meta property="og:image" content="{BASE}/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  {FONTS}
  <style>{CSS}</style>
</head>
<body>

<nav class="bar">
  <div class="wrap">
    <a class="brand" href="/{lang}/">NFS</a>
    <div class="ctl">
      <label>{t["langlabel"]}</label>
      <div class="langs">
{langs}
      </div>
    </div>
    <div class="ctl">
      <label for="store">{t["storelabel"]}</label>
      <select id="store">
{stores}
      </select>
    </div>
  </div>
</nav>

<div class="wrap">
  <header>
    <div class="kick">{t["kicker"]}</div>
    <h1>{t["h1"]}</h1>
    <p class="sub">{t["sub"]}</p>
  </header>

  <section class="carousel" aria-roledescription="carousel" aria-label="{t["carousel"]}">
    <div class="chead">
      <h2>{t["carousel"]}</h2>
      <div class="cnav">
        <button type="button" id="cprev" aria-label="{t["prev"]}">&#8592;</button>
        <button type="button" id="cnext" aria-label="{t["next"]}">&#8594;</button>
      </div>
    </div>
    <div class="track" id="track" tabindex="0">
{slides}
    </div>
    <div class="dots" id="dots" aria-hidden="true">{dots}</div>
  </section>

  <h2>{t["eras_h"]}</h2>
  <div class="eras">
{eras}
  </div>

  <h2>{t["games_h"]}</h2>
  <div class="games">
{games}
  </div>

  <footer>
    <p class="note">{t["disclosure"]}</p>
    <p>{t["trademark"]}</p>
  </footer>
</div>

<script>
(function () {{
  var STORES = {json.dumps(STORES)};
  var LANGC  = {json.dumps(LANG_COUNTRY)};
  var sel = document.getElementById('store');

  // país presumido: preferência salva > região do idioma do navegador > idioma da página
  function guessCountry() {{
    try {{
      var saved = localStorage.getItem('nfs_country');
      if (saved && STORES[saved]) return saved;
    }} catch (e) {{}}
    var list = navigator.languages || [navigator.language || ''];
    for (var i = 0; i < list.length; i++) {{
      var p = String(list[i]).split('-');
      if (p.length > 1) {{
        var c = p[1].toUpperCase();
        if (STORES[c]) return c;
      }}
    }}
    return LANGC['{lang}'] || 'US';
  }}

  function apply(country) {{
    var s = STORES[country] || STORES['US'];
    document.querySelectorAll('.buy').forEach(function (a) {{
      a.href = s.base + a.dataset.q + '&tag=' + s.tag;
      a.querySelector('.store').textContent = s.name;
    }});
  }}

  var c = guessCountry();
  sel.value = c;
  apply(c);

  sel.addEventListener('change', function () {{
    try {{ localStorage.setItem('nfs_country', sel.value); }} catch (e) {{}}
    apply(sel.value);
  }});

  // ---------- carrossel ----------
  var track = document.getElementById('track');
  var dots  = document.getElementById('dots');
  var prev  = document.getElementById('cprev');
  var next  = document.getElementById('cnext');
  var slides = track ? track.querySelectorAll('.slide') : [];

  if (track && slides.length) {{
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function step() {{
      var r = slides[0].getBoundingClientRect();
      return r.width + 12;                      // largura do slide + gap
    }}
    function maxScroll() {{
      return track.scrollWidth - track.clientWidth;
    }}
    function index() {{
      return Math.round(track.scrollLeft / step());
    }}
    function sync() {{
      var i = index(), d = dots.children;
      for (var k = 0; k < d.length; k++) d[k].className = (k === i ? 'on' : '');
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= maxScroll() - 2;
    }}
    function go(dir) {{
      track.scrollBy({{ left: dir * step(), behavior: reduce ? 'auto' : 'smooth' }});
    }}

    prev.addEventListener('click', function () {{ stop(); go(-1); }});
    next.addEventListener('click', function () {{ stop(); go(1); }});

    var t = null;
    function start() {{
      if (reduce || t) return;
      t = setInterval(function () {{
        if (track.scrollLeft >= maxScroll() - 2) track.scrollTo({{ left: 0, behavior: 'smooth' }});
        else go(1);
      }}, 4000);
    }}
    function stop() {{ if (t) {{ clearInterval(t); t = null; }} }}

    // para de girar assim que a pessoa interage, e não volta a girar sozinho
    ['pointerdown', 'wheel', 'touchstart', 'keydown'].forEach(function (ev) {{
      track.addEventListener(ev, stop, {{ passive: true }});
    }});
    track.addEventListener('mouseenter', stop);
    track.addEventListener('focusin', stop);

    var ticking = false;
    track.addEventListener('scroll', function () {{
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {{ sync(); ticking = false; }});
    }}, {{ passive: true }});

    window.addEventListener('resize', sync);
    sync();

    // só começa a girar quando o carrossel está visível na tela
    if ('IntersectionObserver' in window) {{
      new IntersectionObserver(function (es) {{
        es[0].isIntersecting ? start() : stop();
      }}, {{ threshold: .35 }}).observe(track);
    }} else {{ start(); }}
  }}

  // grava o idioma quando a pessoa troca na mão, para a raiz respeitar depois
  document.querySelectorAll('.langs a').forEach(function (a) {{
    a.addEventListener('click', function () {{
      try {{ localStorage.setItem('nfs_lang', a.getAttribute('href').replace(/\\//g, '')); }} catch (e) {{}}
    }});
  }});
}})();
</script>

</body>
</html>
'''


ROOT = f'''<!doctype html>
<html lang="{HTML_LANG[DEFAULT]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{UI[DEFAULT]["title"]}</title>
  <meta name="description" content="{UI[DEFAULT]["meta"]}">
  <link rel="canonical" href="{BASE}/">
  {hreflangs(DEFAULT)}
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE}/">
  <meta property="og:title" content="{UI[DEFAULT]["title"]}">
  <meta property="og:description" content="{UI[DEFAULT]["meta"]}">
  <meta property="og:image" content="{BASE}/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  {FONTS}
  <style>{CSS}
  .pick{{min-height:70vh;display:flex;flex-direction:column;justify-content:center;gap:26px;
        padding:60px 0}}
  .pick .opts{{display:flex;flex-wrap:wrap;gap:12px}}
  .pick .opts a{{font-family:var(--cond);font-weight:700;font-size:22px;letter-spacing:.04em;
        text-transform:uppercase;text-decoration:none;background:var(--surface);
        border:1px solid var(--line);border-radius:6px;padding:14px 24px}}
  .pick .opts a:hover{{border-color:var(--accent)}}
  </style>
  <script>
  // Redireciona só pessoas. Robôs que não executam JS recebem a lista de idiomas
  // abaixo em HTML, com hreflang, e indexam cada versão separadamente.
  (function () {{
    var LANGS = {json.dumps(LANGS)}, DEF = "{DEFAULT}", pick = null;
    try {{ var s = localStorage.getItem('nfs_lang'); if (LANGS.indexOf(s) > -1) pick = s; }} catch (e) {{}}
    if (!pick) {{
      var list = navigator.languages || [navigator.language || ''];
      for (var i = 0; i < list.length && !pick; i++) {{
        var base = String(list[i]).toLowerCase().split('-')[0];
        if (LANGS.indexOf(base) > -1) pick = base;
      }}
    }}
    location.replace('/' + (pick || DEF) + '/');
  }})();
  </script>
</head>
<body>
<div class="wrap pick">
  <div>
    <div class="kick">Need for Speed</div>
    <h1>{UI[DEFAULT]["h1"]}</h1>
  </div>
  <div class="opts">
''' + "\n".join(
    f'    <a href="/{l}/" hreflang="{HTML_LANG[l]}" lang="{HTML_LANG[l]}">{LANG_NAME[l]}</a>'
    for l in LANGS) + '''
  </div>
</div>
</body>
</html>
'''

if __name__ == "__main__":
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(ROOT)
    for l in LANGS:
        os.makedirs(os.path.join(OUT, l))
        open(os.path.join(OUT, l, "index.html"), "w", encoding="utf-8").write(page(l))
    for l in LANGS:
        p = os.path.join(OUT, l, "index.html")
        print(f"{l}/index.html  {os.path.getsize(p)//1024} KB")
    print("index.html   ", os.path.getsize(os.path.join(OUT, "index.html")) // 1024, "KB")
