"""Statik portfolio generatori: data.py -> HTML sahifalar.

  python build.py

Natija repo ildiziga yoziladi: index.html, loyihalar/<slug>/, blog/, blog/<slug>/,
404.html, sitemap.xml, robots.txt. GitHub Pages ularni to'g'ridan-to'g'ri beradi.
"""
import html
import json
import os
import re

from data import FAQ, POSTS, PROJECTS, SERVICES, SITE, SKILL_LEVELS, SKILLS, SUPPORT

ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

ICON_TG = '<svg class="brand tg" viewBox="0 0 24 24" aria-hidden="true"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>'
ICON_GH = '<svg class="brand" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>'

ICON_WA = '<svg class="brand wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'


def second_contact(label_wa="WhatsApp", label_gh="GitHub", icon=True):
    """WhatsApp raqami berilgan bo'lsa — WhatsApp, aks holda GitHub."""
    if SITE.get("whatsapp"):
        return (f'<a class="btn" href="https://wa.me/{SITE["whatsapp"]}" target="_blank" rel="noopener">'
                f'{ICON_WA if icon else ""} {label_wa}</a>')
    return (f'<a class="btn" href="{SITE["github_url"]}" target="_blank" rel="noopener">'
            f'{ICON_GH if icon else ""} {label_gh}</a>')


def ld(*objs):
    """schema.org JSON-LD — Google va AI qidiruvlar sahifani tushunishi uchun."""
    data = {"@context": "https://schema.org", "@graph": list(objs)}
    text = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'  <script type="application/ld+json">\n{text}\n  </script>\n'


PERSON_ID = SITE["url"] + "/#person"


def person():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": SITE["full_name"],
        "givenName": SITE["first_name"],
        "familyName": SITE["last_name"],
        "alternateName": [SITE["name"], f"{SITE['last_name']} {SITE['first_name']}", SITE["telegram"]],
        "jobTitle": SITE["role"],
        "description": f"{SITE['full_name']} — O‘zbekistonlik full-stack dasturchi. Biznes uchun tizimlar quradi: "
                       "CRM, hisob-kitob va ombor, to‘lov qabul qilish, Telegram botlar, veb-ilovalar; "
                       "ishga tushirishdan keyin qo‘llab-quvvatlaydi. O‘zbek tilida bepul dasturlash darsliklari muallifi.",
        "url": SITE["url"] + "/",
        "mainEntityOfPage": SITE["url"] + "/",
        "image": SITE["url"] + "/assets/dinmuhammad-760.jpg",
        "sameAs": [SITE["telegram_url"], SITE["telegram_channel_url"], SITE["github_url"], SITE["linkedin_url"]],
        "address": {"@type": "PostalAddress", "addressLocality": SITE["city"], "addressCountry": "UZ"},
        "nationality": {"@type": "Country", "name": SITE["country"]},
        "knowsLanguage": ["uz", "ru", "en"],
        "hasOccupation": {"@type": "Occupation", "name": SITE["role"],
                          "occupationLocation": {"@type": "Country", "name": SITE["country"]},
                          "skills": "NestJS, Node.js, TypeScript, Next.js, React, PostgreSQL, Redis, Docker"},
        "knowsAbout": ["Full-stack dasturlash", "Biznesni avtomatlashtirish", "CRM", "ERP", "SaaS", "JavaScript"]
                      + [n for g in SKILLS for n, lvl in g["items"] if lvl != "learn"],
    }


def breadcrumbs(*items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n, "name": name, "item": SITE["url"] + path}
        for n, (name, path) in enumerate(items, 1)]}


def verification_tags():
    tags = [("google-site-verification", SITE.get("google_verification")),
            ("msvalidate.01", SITE.get("bing_verification")),
            ("yandex-verification", SITE.get("yandex_verification"))]
    return "".join(f'  <meta name="{n}" content="{E(v)}" />\n' for n, v in tags if v)


def page(title, description, body, path, og_image="/assets/og.png", schema="", keywords=None):
    url = SITE["url"] + path
    kw = ", ".join(keywords or SITE["keywords"][:12])
    return f"""<!doctype html>
<html lang="uz">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{E(title)}</title>
  <meta name="description" content="{E(description)}" />
  <meta name="author" content="{E(SITE['full_name'])}" />
  <meta name="keywords" content="{E(kw)}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1" />
  <meta name="geo.region" content="UZ" />
  <meta name="geo.placename" content="{E(SITE['city'])}" />
{verification_tags()}  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{E(SITE['full_name'])}" />
  <meta property="og:locale" content="uz_UZ" />
  <meta property="og:title" content="{E(title)}" />
  <meta property="og:description" content="{E(description)}" />
  <meta property="og:image" content="{SITE['url']}{og_image}" />
  <meta property="og:url" content="{url}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="/assets/avatar.jpg" />
  <script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
  <link rel="stylesheet" href="/style.min.css" />
  <link rel="alternate" type="text/markdown" href="/llms.txt" title="llms.txt" />
{schema}</head>
<body>
  <header class="nav">
    <div class="wrap nav-in">
      <a class="brand" href="/" aria-label="Bosh sahifa">
        <img src="/assets/avatar-96.webp" alt="" width="32" height="32" />
        <span>{E(SITE['name'])}</span>
      </a>
      <nav class="nav-links" aria-label="Bo'limlar">
        <a href="/#xizmatlar">Xizmatlar</a>
        <a href="/#loyihalar">Loyihalar</a>
        <a href="/konikmalar/">Ko‘nikmalar</a>
        <a href="/blog/">Blog</a>
        <a href="/#aloqa">Aloqa</a>
      </nav>
      <button class="theme" type="button" aria-label="Rangli rejimni almashtirish" title="Yorug‘ / qorong‘i">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9z" /></svg>
      </button>
    </div>
  </header>
{body}
  <aside class="nudge" id="nudge" aria-live="polite" hidden>
    <button class="nudge-x" type="button" aria-label="Yopish">×</button>
    <img src="/assets/avatar-96.webp" alt="" loading="lazy" decoding="async" width="44" height="44" />
    <div>
      <b>Loyihangiz bormi yoki biznesingizni avtomatlashtirish kerakmi?</b>
      <p>Vazifani yozing — qanday qilish mumkinligini birga ko‘ramiz.</p>
      <span class="nudge-cta">
        <a class="btn primary" href="{SITE['telegram_url']}" target="_blank" rel="noopener">{ICON_TG} Telegram</a>
        {second_contact()}
      </span>
    </div>
  </aside>
  <footer class="wrap foot">
    <span>© <span id="y">2026</span> {E(SITE['name'])}</span>
    <span class="foot-links">
      <a href="/blog/">Blog</a>
      <a href="{SITE['telegram_url']}" target="_blank" rel="noopener">Telegram</a>
      <a href="{SITE['telegram_channel_url']}" target="_blank" rel="noopener">Kanal</a>
      <a href="{SITE['github_url']}" target="_blank" rel="noopener">GitHub</a>
      <a href="{SITE['linkedin_url']}" target="_blank" rel="noopener">LinkedIn</a>
    </span>
  </footer>
  <script>
    (function () {{
      var root = document.documentElement;
      document.querySelector(".theme").addEventListener("click", function () {{
        var dark = root.dataset.theme ? root.dataset.theme === "dark"
          : window.matchMedia("(prefers-color-scheme: dark)").matches;
        root.dataset.theme = dark ? "light" : "dark";
        try {{ localStorage.setItem("theme", root.dataset.theme); }} catch (e) {{}}
      }});
      document.getElementById("y").textContent = new Date().getFullYear();

      // Eslatma: bir marta, sahifaning yarmidan keyin yoki 25 soniyadan keyin.
      // Yopilsa — 1 kun ko‘rsatilmaydi. Aloqa bo'limi ko'rinib turganda chiqmaydi.
      var nudge = document.getElementById("nudge");
      var KEY = "nudge-closed";
      var closedAt = 0, shown = false, contactVisible = false;
      try {{ closedAt = +localStorage.getItem(KEY) || 0; if (sessionStorage.getItem("nudge-shown")) shown = true; }} catch (e) {{}}
      if (Date.now() - closedAt < 864e5) shown = true;
      var contact = document.getElementById("aloqa");
      if (contact && "IntersectionObserver" in window) {{
        new IntersectionObserver(function (es) {{
          contactVisible = es[0].isIntersecting;
          if (contactVisible) nudge.classList.remove("show");
        }}).observe(contact);
      }}
      function show() {{
        if (shown || contactVisible) return;
        shown = true;
        try {{ sessionStorage.setItem("nudge-shown", "1"); }} catch (e) {{}}
        nudge.hidden = false;
        requestAnimationFrame(function () {{ nudge.classList.add("show"); }});
        window.removeEventListener("scroll", onScroll);
      }}
      function onScroll() {{
        var max = document.documentElement.scrollHeight - innerHeight;
        if (max > 0 && scrollY / max > 0.5) show();
      }}
      window.addEventListener("scroll", onScroll, {{ passive: true }});
      setTimeout(show, 25000);
      nudge.querySelector(".nudge-x").addEventListener("click", function () {{
        nudge.classList.remove("show");
        try {{ localStorage.setItem(KEY, String(Date.now())); }} catch (e) {{}}
        setTimeout(function () {{ nudge.hidden = true; }}, 250);
      }});
    }})();
  </script>
</body>
</html>
"""


def stack(items):
    return "<ul class=\"stack\">" + "".join(f"<li>{E(s)}</li>" for s in items) + "</ul>"


def site_link(p, cls="site"):
    if p.get("site"):
        href, label = p["site"]
        return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{E(label)} ↗</a>'
    return f'<span class="{cls} plain">{E(p.get("site_label", ""))}</span>'


def project_card(p):
    cls = "card clickable compact" + (" featured" if p.get("featured") else "")
    chips = p["stack"][:4] + ([f"+{len(p['stack']) - 4}"] if len(p["stack"]) > 4 else [])
    return f"""        <article class="{cls}">
          <div class="card-top">
            <span class="tag">{E(p['tag'])}</span>
            {site_link(p)}
          </div>
          <h3><a class="stretch" href="/loyihalar/{p['slug']}/">{E(p['title'])}</a></h3>
          <p class="who">{E(p['role'])}</p>
          <p class="clamp">{p['summary']}</p>
          {stack(chips)}
          <span class="open">Batafsil →</span>
        </article>"""


SERVICE_ICONS = {
    "workflow": '<rect x="3" y="3" width="7" height="6" rx="1.5"/><rect x="14" y="15" width="7" height="6" rx="1.5"/><rect x="14" y="3" width="7" height="6" rx="1.5"/><path d="M10 6h4M17.5 9v6M6.5 9v5a2 2 0 0 0 2 2H14"/>',
    "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 8V4.5M9.5 4.5h5"/><circle cx="9" cy="13.5" r="1.2"/><circle cx="15" cy="13.5" r="1.2"/><path d="M2 12.5v2M22 12.5v2"/>',
    "layers": '<path d="M12 3 3 7.5l9 4.5 9-4.5z"/><path d="m3 12 9 4.5 9-4.5"/><path d="m3 16.5 9 4.5 9-4.5"/>',
    "support": '<path d="M12 3 4.5 6v5.5c0 4.3 3.1 8.2 7.5 9.5 4.4-1.3 7.5-5.2 7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    "card": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/>',
}


def service_card(x):
    by_slug = {p["slug"]: p for p in PROJECTS}
    ex = ", ".join(f'<a href="/loyihalar/{sl}/">{E(by_slug[sl]["name"])}</a>' for sl in x["examples"])
    items = "".join(f"<li>{E(i)}</li>" for i in x["items"])
    cls = "service accent" if x.get("accent") else "service"
    return f"""        <div class="{cls}">
          <span class="service-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{SERVICE_ICONS[x['icon']]}</svg></span>
          <h3>{E(x['title'])}</h3>
          <p>{E(x['text'])}</p>
          <ul>{items}</ul>
          <p class="examples">Misollar: {ex}</p>
        </div>"""


def post_card(post):
    return f"""        <article class="card clickable post-card">
          <span class="tag">Darslik</span>
          <h3><a class="stretch" href="/blog/{post['slug']}/">{E(post['title'])}</a></h3>
          <p class="muted">{E(post['excerpt'])}</p>
          <span class="open">O‘qish →</span>
        </article>"""


def slugify(text):
    text = text.lower().replace("’", "").replace("‘", "")
    for a, b in (("o‘", "o"), ("g‘", "g"), ("’", ""), ("sun", "sun")):
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def build_skills():
    groups = []
    for g in SKILLS:
        chips = "".join(
            f'<li class="lvl-{lvl}" title="{E(SKILL_LEVELS[lvl])}">{E(n)}</li>' for n, lvl in g["items"])
        groups.append(f"""      <section class="skill-group" id="{slugify(g['title'])}">
        <div class="skill-group-head">
          <h2>{E(g['title'])}</h2>
          <p class="muted">{E(g['text'])}</p>
        </div>
        <ul class="chips">{chips}</ul>
      </section>""")
    legend = "".join(f'<li class="lvl-{k}">{E(v)}</li>' for k, v in SKILL_LEVELS.items())
    total = sum(len(g["items"]) for g in SKILLS)
    core = sum(1 for g in SKILLS for _, lvl in g["items"] if lvl == "core")
    body = f"""  <main>
    <article class="wrap detail skills-page">
      <a class="back" href="/">← Bosh sahifa</a>
      <header class="detail-head">
        <p class="eyebrow">Ko‘nikmalar</p>
        <h1>Nimalarni bilaman</h1>
        <p class="lead">Backendga urg‘u bergan full-stack dasturchiman. Quyida {total} ta texnologiya 7 guruhda —
          qaysi birini har kuni ishlatishim, qaysi birini kerak bo‘lganda olishim va hozir nimani o‘rganayotganim bilan.</p>
        <div class="numbers">
          <div><b>{core}</b><span>har kuni ishlatadigan</span></div>
          <div><b>{total}</b><span>jami texnologiya</span></div>
          <div><b>{len(PROJECTS)}</b><span>ishlab turgan loyihada sinalgan</span></div>
        </div>
        <ul class="chips legend" aria-label="Belgilar">{legend}</ul>
      </header>
{chr(10).join(groups)}
      <section class="block">
        <h2>Bularni qayerda ishlatganman?</h2>
        <p>Har bir texnologiya haqiqiy loyihada sinalgan — <a href="/#loyihalar">loyihalar</a> sahifasida har birining
          arxitekturasi va muhim qarorlari yozilgan. Tizim dizayni bo‘yicha esa <a href="/blog/">o‘zbek tilida kurslar</a> yozganman.</p>
      </section>
    </article>
{contact()}
  </main>
"""
    names = [n for g in SKILLS for n, _ in g["items"]]
    desc = (f"{SITE['full_name']} — full-stack dasturchi ko‘nikmalari: NestJS, Node.js, TypeScript, PostgreSQL, "
            "Next.js, React, Redis, Docker, LLM integratsiyalari, Payme va Click to‘lovlari va boshqalar.")
    return page(f"Ko‘nikmalar va texnologiyalar — {SITE['full_name']}", desc, body, "/konikmalar/",
                keywords=[SITE["full_name"], "full-stack dasturchi ko‘nikmalari", "NestJS dasturchi", "Node.js dasturchi"] + names[:20],
                schema=ld({"@type": "ItemList", "name": "Texnologiyalar", "url": SITE["url"] + "/konikmalar/",
                           "numberOfItems": total,
                           "itemListElement": [{"@type": "ListItem", "position": i, "name": n}
                                               for i, n in enumerate(names, 1)]},
                          person(), breadcrumbs(("Bosh sahifa", "/"), ("Ko‘nikmalar", "/konikmalar/"))))


def build_index():
    cards = "\n".join(project_card(p) for p in PROJECTS)
    posts = "\n".join(post_card(p) for p in POSTS[:3])
    services_html = "\n".join(service_card(x) for x in SERVICES)
    support_items = "".join(f"<li>{E(i)}</li>" for i in SUPPORT["items"])
    total = sum(len(g["items"]) for g in SKILLS)
    skill_cards = "\n".join(
        f"""        <a class="skill" href="/konikmalar/#{slugify(g['title'])}"><h3>{E(g['title'])}</h3>"""
        f"""<p>{E(', '.join(n for n, lvl in g['items'] if lvl == 'core'))}</p></a>""" for g in SKILLS[:6])
    faq_html = "\n".join(
        f"""        <details class="faq-item"><summary>{E(q)}</summary><p>{E(a)}</p></details>""" for q, a in FAQ)
    support_html = f"""      <div class="support">
        <div class="support-head">
          <span class="service-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{SERVICE_ICONS['support']}</svg></span>
          <div>
            <h3>{E(SUPPORT['title'])}</h3>
            <p>{E(SUPPORT['text'])}</p>
          </div>
        </div>
        <ul>{support_items}</ul>
      </div>"""
    body = f"""  <main id="top">
    <section class="hero wrap">
      <div class="hero-text">
        <p class="kicker"><span class="dot"></span> Biznesni avtomatlashtirish · Veb-ilovalar · Telegram botlar · Qo‘llab-quvvatlash</p>
        <h1>{E(SITE['full_name'])}</h1>
        <p class="role">{E(SITE['role'])} · {E(SITE['city'])}, {E(SITE['country'])}</p>
        <p class="lead">
          Biznesingiz uchun ishlaydigan tizimlar quraman: <strong>buyurtma va mijozlarni yuritish</strong>,
          <strong>hisob-kitob va ombor</strong>, <strong>to‘lov qabul qilish</strong>, Telegram orqali
          xizmat ko‘rsatish. Qo‘lda, qog‘ozda yoki Excel’da qilinadigan ishlarni dasturga topshiraman —
          xodimlar vaqti tejaladi, xatolar kamayadi, raqamlar har doim ko‘z oldingizda bo‘ladi.
          Loyihani boshidan oxirigacha o‘zim olib boraman: g‘oyadan ishga tushirishgacha, keyin esa
          qo‘llab-quvvatlayman. Texnik tafsilotlar — <a href="/konikmalar/">ko‘nikmalar sahifasida</a>.
        </p>
        <div class="cta">
          <a class="btn primary" href="{SITE['telegram_url']}" target="_blank" rel="noopener">{ICON_TG} Telegramda yozish</a>
          {second_contact()}
          <a class="btn ghost" href="#loyihalar">Loyihalarni ko‘rish ↓</a>
        </div>
        <ul class="facts">
          <li><b>{len(PROJECTS)}</b><span>asosiy loyiha</span></li>
          <li><b>{SITE['other_projects']}</b><span>boshqa loyihalar</span></li>
          <li><b>{len(POSTS)}</b><span>o‘zbekcha darslik</span></li>
        </ul>
      </div>
      <figure class="hero-photo">
        <picture>
          <source type="image/webp" srcset="/assets/dinmuhammad-480.webp 480w, /assets/dinmuhammad-760.webp 760w" sizes="(max-width: 960px) min(420px, 100vw), 400px" />
          <img src="/assets/dinmuhammad-760.jpg" srcset="/assets/dinmuhammad-480.jpg 480w, /assets/dinmuhammad-760.jpg 760w"
               sizes="(max-width: 960px) min(420px, 100vw), 400px" alt="{E(SITE['full_name'])} — full-stack dasturchi" width="760" height="1140" fetchpriority="high" decoding="async" />
        </picture>
      </figure>
    </section>

    <section id="xizmatlar" class="wrap section">
      <div class="section-head">
        <p class="eyebrow">Xizmatlar</p>
        <h2>Nima qila olaman</h2>
        <p class="muted">Har bir yo‘nalish bo‘yicha ishlab turgan loyihalar bor — misollarni bosib ko‘ring.</p>
      </div>
      <div class="services">
{services_html}
      </div>
{support_html}
    </section>

    <section id="loyihalar" class="wrap section">
      <div class="section-head">
        <p class="eyebrow">Loyihalar</p>
        <h2>Nimalar qurganman</h2>
        <p class="muted">Ko‘p loyihalar mijozlar uchun, shuning uchun kodlari yopiq. Kartani bosib, har
          birining ichiga kiring: muammo, mening rolim, arxitektura va muhim qarorlar.</p>
      </div>
      <div class="grid projects">
{cards}
      </div>
    </section>

    <section id="blog" class="wrap section">
      <div class="section-head row">
        <div>
          <p class="eyebrow">Blog</p>
          <h2>Darsliklarim</h2>
          <p class="muted">O‘zbek tilida yozgan darslik va kurslarim — qisqacha va havolalari bilan.</p>
        </div>
        <a class="btn" href="/blog/">Barcha yozuvlar →</a>
      </div>
      <div class="grid three">
{posts}
      </div>
    </section>

    <section id="konikmalar" class="wrap section">
      <div class="section-head row">
        <div>
          <p class="eyebrow">Ko‘nikmalar</p>
          <h2>Ish qurollarim</h2>
          <p class="muted">Har kuni ishlatadigan asosiy texnologiyalar. To‘liq ro‘yxat — {total} ta texnologiya, 7 guruhda.</p>
        </div>
        <a class="btn" href="/konikmalar/">Barcha ko‘nikmalar →</a>
      </div>
      <div class="skills">
{skill_cards}
      </div>
    </section>

    <section id="savol-javob" class="wrap section">
      <div class="section-head">
        <p class="eyebrow">Savol-javob</p>
        <h2>Ko‘p so‘raladigan savollar</h2>
      </div>
      <div class="faq">
{faq_html}
      </div>
    </section>

{contact()}
  </main>
"""
    return page(f"{SITE['full_name']} — {SITE['role']} | Biznesni avtomatlashtirish, veb-ilovalar, Telegram botlar",
                f"{SITE['full_name']} — O‘zbekistonlik full-stack dasturchi. Biznes uchun tizimlar: "
                "buyurtma va mijozlarni yuritish (CRM), hisob-kitob va ombor, to‘lov qabul qilish, Telegram botlar, "
                "veb-ilovalar. Ishga tushirishdan keyin qo‘llab-quvvatlash. O‘zbek tilida bepul dasturlash darsliklari.",
                body, "/", schema=ld(
                    person(),
                    {"@type": "FAQPage", "mainEntity": [
                        {"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
                    {"@type": "WebSite", "@id": SITE["url"] + "/#website", "url": SITE["url"] + "/",
                     "name": SITE["full_name"], "alternateName": SITE["name"], "inLanguage": "uz",
                     "publisher": {"@id": PERSON_ID}},
                    {"@type": "ProfilePage", "url": SITE["url"] + "/", "inLanguage": "uz",
                     "mainEntity": {"@id": PERSON_ID},
                     "hasPart": [{"@type": "CreativeWork", "name": p["title"],
                                  "url": f"{SITE['url']}/loyihalar/{p['slug']}/"} for p in PROJECTS]}))


def contact():
    return f"""    <section id="aloqa" class="wrap section contact">
      <div class="contact-card">
        <img src="/assets/avatar-96.webp" alt="" loading="lazy" decoding="async" width="72" height="72" />
        <div>
          <h2>Loyihangiz bormi yoki biznesingizni avtomatlashtirish kerakmi?</h2>
          <p class="muted">CRM, ERP, SaaS, Telegram bot, SMS eslatmalar, to‘lov integratsiyasi yoki mavjud loyihani qo‘llab-quvvatlash — vazifani yozing, qanday avtomatlashtirish mumkinligini birga ko‘ramiz.</p>
        </div>
        <div class="cta">
          <a class="btn primary" href="{SITE['telegram_url']}" target="_blank" rel="noopener">{ICON_TG} {E(SITE['telegram'])}</a>
          {second_contact()}
        </div>
      </div>
    </section>"""


def build_project(i, p):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    prv = PROJECTS[i - 1]
    feats = "".join(
        f'<div class="feat"><h3>{E(title)}</h3><ul>' + "".join(f"<li>{E(x)}</li>" for x in items) + "</ul></div>"
        for title, items in p["features"])
    arch = "".join(
        f'<div class="layer"><span class="layer-name">{E(name)}</span><div class="boxes">'
        + "".join(f'<span class="box">{E(b)}</span>' for b in boxes) + "</div></div>"
        for name, boxes in p["arch"])
    decisions = "".join(
        f'<div class="decision"><span class="num">{n}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>'
        for n, (t, d) in enumerate(p["decisions"], 1))
    numbers = ""
    if p.get("numbers"):
        numbers = '<div class="numbers">' + "".join(
            f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in p["numbers"]) + "</div>"
    visit = ""
    if p.get("site"):
        href, label = p["site"]
        text = p.get("visit_label") or f"{label} saytini ochish"
        visit = f'<a class="btn primary" href="{href}" target="_blank" rel="noopener">{E(text)} ↗</a>'
    body = f"""  <main>
    <article class="wrap detail">
      <a class="back" href="/#loyihalar">← Barcha loyihalar</a>
      <header class="detail-head">
        <div class="card-top"><span class="tag">{E(p['tag'])}</span>{site_link(p)}</div>
        <h1>{E(p['title'])}</h1>
        <p class="who">{E(p['role'])}</p>
        <p class="lead">{p['summary']}</p>
        {stack(p['stack'])}
        <div class="cta">{visit}<a class="btn" href="{SITE['telegram_url']}" target="_blank" rel="noopener">{ICON_TG} Loyiha haqida so‘rash</a></div>
        {numbers}
      </header>

      <section class="block">
        <h2>Muammo</h2>
        <p>{E(p['problem'])}</p>
      </section>

      <section class="block">
        <h2>Mening rolim</h2>
        <p>{E(p['my_role'])}</p>
      </section>

      <section class="block">
        <h2>Imkoniyatlar</h2>
        <div class="feats">{feats}</div>
      </section>

      <section class="block">
        <h2>Arxitektura</h2>
        <div class="arch">{arch}</div>
      </section>

      <section class="block">
        <h2>Muhim muhandislik qarorlari</h2>
        <div class="decisions">{decisions}</div>
      </section>

      <nav class="pager" aria-label="Loyihalar">
        <a href="/loyihalar/{prv['slug']}/"><span>← Oldingi</span><b>{E(prv['name'])}</b></a>
        <a class="next" href="/loyihalar/{nxt['slug']}/"><span>Keyingi →</span><b>{E(nxt['name'])}</b></a>
      </nav>
    </article>
{contact()}
  </main>
"""
    desc = html.unescape(p["summary"].replace("<b>", "").replace("</b>", ""))
    url = f"{SITE['url']}/loyihalar/{p['slug']}/"
    work = {"@type": "CreativeWork", "name": p["title"], "url": url, "description": desc,
            "inLanguage": "uz", "genre": p["tag"], "keywords": ", ".join(p["stack"]),
            "creator": {"@id": PERSON_ID}}
    if p.get("site"):
        work["sameAs"] = p["site"][0]
    return page(f"{p['title']} — {SITE['full_name']}", desc, body, f"/loyihalar/{p['slug']}/",
                keywords=[p["title"], p["tag"], SITE["full_name"]] + p["stack"] + SITE["keywords"][:6],
                schema=ld(work, person(), breadcrumbs(("Bosh sahifa", "/"), ("Loyihalar", "/#loyihalar"),
                                                      (p["name"], f"/loyihalar/{p['slug']}/"))))


def build_blog_index():
    cards = "\n".join(post_card(p) for p in POSTS)
    body = f"""  <main>
    <section class="wrap section">
      <a class="back" href="/">← Bosh sahifa</a>
      <div class="section-head">
        <p class="eyebrow">Blog</p>
        <h1 class="h1">Darsliklarim</h1>
        <p class="muted">O‘zbek tilida dasturlash va tizim dizayni bo‘yicha yozgan darslik va kurslarim.
          Har birida — nima haqida, kim uchun va qanday qurilgani.</p>
      </div>
      <div class="grid">
{cards}
      </div>
    </section>
  </main>
"""
    return page(f"Blog — o‘zbek tilida tizim dizayni va JavaScript darsliklari | {SITE['full_name']}",
                f"{SITE['full_name']}ning o‘zbek tilidagi bepul darslik va kurslari: tizim dizayni (system design), JavaScript, backend, NestJS.",
                body, "/blog/", schema=ld(
                    {"@type": "Blog", "name": f"Blog — {SITE['full_name']}", "url": SITE["url"] + "/blog/",
                     "inLanguage": "uz", "author": {"@id": PERSON_ID},
                     "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                                   "url": f"{SITE['url']}/blog/{p['slug']}/"} for p in POSTS]},
                    person(), breadcrumbs(("Bosh sahifa", "/"), ("Blog", "/blog/"))))


def build_post(i, post):
    paras = "".join(f"<p>{E(x)}</p>" for x in post["body"])
    stats = "".join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in post.get("stats", []))
    others = "".join(
        f'<li><a href="/blog/{o["slug"]}/">{E(o["title"])}</a></li>' for o in POSTS if o is not post)
    body = f"""  <main>
    <article class="wrap detail post">
      <a class="back" href="/blog/">← Blog</a>
      <header class="detail-head">
        <span class="tag">Darslik</span>
        <h1>{E(post['title'])}</h1>
        <p class="lead">{E(post['excerpt'])}</p>
        <div class="numbers">{stats}</div>
        <div class="cta"><a class="btn primary" href="{post['url']}" target="_blank" rel="noopener">{E(post['cta'])} ↗</a></div>
      </header>
      <div class="prose">{paras}</div>
      <div class="cta"><a class="btn primary" href="{post['url']}" target="_blank" rel="noopener">{E(post['cta'])} ↗</a></div>
      <section class="block">
        <h2>Boshqa yozuvlar</h2>
        <ul class="others">{others}</ul>
      </section>
    </article>
  </main>
"""
    url = f"{SITE['url']}/blog/{post['slug']}/"
    return page(f"{post['title']} — {SITE['full_name']}", post["excerpt"], body, f"/blog/{post['slug']}/",
                keywords=post.get("keywords"),
                schema=ld({"@type": "BlogPosting", "headline": post["title"], "url": url,
                           "keywords": ", ".join(post.get("keywords") or []),
                           "mainEntityOfPage": url, "description": post["excerpt"], "inLanguage": "uz",
                           "author": {"@id": PERSON_ID}, "image": SITE["url"] + "/assets/og.png",
                           "about": {"@type": "Course", "name": post["title"], "url": post["url"],
                                     "description": post["excerpt"], "inLanguage": "uz",
                                     "provider": {"@id": PERSON_ID}}},
                          person(), breadcrumbs(("Bosh sahifa", "/"), ("Blog", "/blog/"),
                                                (post["title"], f"/blog/{post['slug']}/"))))


def build_404():
    body = """  <main class="wrap section notfound">
    <h1 class="h1">Sahifa topilmadi</h1>
    <p class="muted">Havola eskirgan yoki xato yozilgan bo‘lishi mumkin.</p>
    <div class="cta"><a class="btn primary" href="/">Bosh sahifaga</a><a class="btn" href="/blog/">Blog</a></div>
  </main>
"""
    return page(f"Topilmadi — {SITE['full_name']}", "Sahifa topilmadi", body, "/404.html")


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def minify_css():
    css = open(os.path.join(ROOT, "style.css"), encoding="utf-8").read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    write("style.min.css", css.strip())


def plain(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def build_llms(full=False):
    """llms.txt — AI yordamchilar (ChatGPT, Claude, Perplexity...) uchun saytning markdown xulosasi."""
    u = SITE["url"]
    out = [f"# {SITE['full_name']} — {SITE['role']}", "",
           f"> {SITE['full_name']} ({SITE['name']}, {SITE['telegram']}) — O‘zbekistonlik ({SITE['city']}) full-stack "
           "dasturchi (NestJS, Next.js, PostgreSQL). Biznesni avtomatlashtirish (CRM, ERP), SaaS va veb-ilovalar, "
           "Telegram botlar va to‘lov tizimlari integratsiyasi. O‘zbek tilida tizim dizayni (system design) va "
           f"JavaScript darsliklari muallifi. Rasmiy sayt: {u}/", "",
           "## Savol-javob", ""] + [f"**{q}** {a}" for q, a in FAQ] + ["",
           "## Aloqa", "",
           f"- Telegram: [{SITE['telegram']}]({SITE['telegram_url']})"]
    if SITE.get("whatsapp"):
        out.append(f"- WhatsApp: [+{SITE['whatsapp']}](https://wa.me/{SITE['whatsapp']})")
    out += [f"- Telegram kanal: [{SITE['telegram_channel']}]({SITE['telegram_channel_url']})",
            f"- GitHub: [{SITE['github_url'].rsplit('/', 1)[-1]}]({SITE['github_url']})",
            f"- LinkedIn: {SITE['linkedin_url']}", "",
            "## Xizmatlar", ""]
    for x in SERVICES + [SUPPORT]:
        out.append(f"- **{x['title']}** — {x['text']} ({'; '.join(x['items'])})")
    out += ["", f"## Ko‘nikmalar ({u}/konikmalar/)", ""]
    for g in SKILLS:
        out.append(f"- **{g['title']}**: " + ", ".join(
            n + (" (o‘rganyapman)" if lvl == "learn" else "") for n, lvl in g["items"]))
    out += ["", "## Loyihalar", ""]
    for p in PROJECTS:
        site = f" Sayt: {p['site'][0]}" if p.get("site") else ""
        out.append(f"- [{p['title']}]({u}/loyihalar/{p['slug']}/): {plain(p['summary'])}{site}")
        if full:
            out += ["", f"### {p['title']}", "", f"Rol: {p['role']}", f"Texnologiyalar: {', '.join(p['stack'])}", "",
                    f"**Muammo.** {p['problem']}", "", f"**Mening rolim.** {p['my_role']}", ""]
            for title, items in p["features"]:
                out += [f"**{title}:**"] + [f"- {i}" for i in items] + [""]
            out += ["**Arxitektura:**"] + [f"- {n}: {', '.join(b)}" for n, b in p["arch"]] + [""]
            out += ["**Muhim qarorlar:**"] + [f"- {t}: {d}" for t, d in p["decisions"]] + [""]
    out += ["", "## Blog (o‘zbek tilidagi darsliklar)", ""]
    for post in POSTS:
        out.append(f"- [{post['title']}]({u}/blog/{post['slug']}/): {post['excerpt']} Kurs: {post['url']}")
        if full:
            out += [""] + post["body"] + [""]
    if not full:
        out += ["", "## Optional", "", f"- [To‘liq matn]({u}/llms-full.txt): barcha loyihalar va darsliklar batafsil"]
    return "\n".join(out) + "\n"


AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot",
           "YandexBot", "meta-externalagent", "CCBot"]


def main():
    minify_css()
    write("index.html", build_index())
    for i, p in enumerate(PROJECTS):
        write(f"loyihalar/{p['slug']}/index.html", build_project(i, p))
    write("konikmalar/index.html", build_skills())
    write("blog/index.html", build_blog_index())
    for i, post in enumerate(POSTS):
        write(f"blog/{post['slug']}/index.html", build_post(i, post))
    write("404.html", build_404())
    urls = ["/", "/konikmalar/", "/blog/"] + [f"/loyihalar/{p['slug']}/" for p in PROJECTS] + [f"/blog/{p['slug']}/" for p in POSTS]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("llms.txt", build_llms())
    write("llms-full.txt", build_llms(full=True))
    # "*" hammasiga ruxsat beradi; AI botlar aniq sanab o'tilgan — ular uchun ochiq ekani ko'rinib tursin.
    write("robots.txt", "".join(f"User-agent: {b}\n" for b in AI_BOTS) + "Allow: /\n\n"
          f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n"
          # Darslik shu domenning ichki yo'lida; qidiruv tizimlari faqat ildizdagi
          # robots.txt ni o'qiydi, shuning uchun uning sitemap'i ham shu yerda.
          f"Sitemap: {SITE['url']}/15-case-studiesfo-software-engineers/sitemap.xml\n"
          f"Sitemap: {SITE['url']}/computer-qanday-ishlaydi/sitemap.xml\n"
          f"Sitemap: {SITE['url']}/javascript-info/sitemap.xml\n"
          f"Sitemap: {SITE['url']}/system-design/sitemap.xml\n"
          f"Sitemap: {SITE['url']}/sys_design_44/sitemap.xml\n"
          f"Sitemap: {SITE['url']}/claude-code/sitemap.xml\n")
    print(f"tayyor: {len(urls)} sahifa")


if __name__ == "__main__":
    main()
