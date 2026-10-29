#!/usr/bin/env python3
"""Build HomeCore Construction Videos page and wire embeds from assets/data/videos.json.

Run: python3 scripts/build_videos.py
Only visibility=public videos with a youtube_id are rendered.
Scheduled entries stay in the JSON as a hook for their publish date.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/videos.json"
TODAY_PUBLIC_ONLY = True

YT_CHANNEL = "https://www.youtube.com/@HomeCoreConstruction"
YT_SAMEAS_LINE = '    "https://www.youtube.com/@HomeCoreConstruction"'

YOUTUBE_SVG = (
    '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.8 15.5v-7l6.3 3.5-6.3 3.5z"/>'
    "</svg>"
)

VIDEOS_CSS = """
    .videos-intro { max-width: 720px; margin: 0 auto 36px; text-align: center; color: var(--gray); font-size: 1.05rem; line-height: 1.65; }
    .videos-intro a { color: var(--accent); font-weight: 700; }
    .videos-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 28px;
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 24px 64px;
    }
    @media (max-width: 900px) {
      .videos-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
    }
    @media (max-width: 560px) {
      .videos-grid { grid-template-columns: 1fr; }
    }
    .video-card {
      background: var(--white);
      border: 1px solid var(--rule);
      border-radius: 6px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 8px 24px rgba(13,35,64,0.06);
    }
    .video-card h3 {
      color: var(--navy);
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1.35;
      margin: 16px 16px 8px;
    }
    .video-card .video-blurb {
      color: var(--gray);
      font-size: 0.92rem;
      line-height: 1.5;
      margin: 0 16px 18px;
      flex: 1;
    }
    .yt-lite {
      position: relative;
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      background: var(--navy);
      cursor: pointer;
      border: 0;
      padding: 0;
      overflow: hidden;
    }
    .yt-lite img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .yt-lite .yt-play {
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(13,35,64,0.28);
      transition: background 0.2s;
    }
    .yt-lite:hover .yt-play,
    .yt-lite:focus-visible .yt-play { background: rgba(13,35,64,0.42); }
    .yt-lite .yt-play-btn {
      width: 68px;
      height: 48px;
      border-radius: 14px;
      background: #16579E;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 20px rgba(13,35,64,0.35);
    }
    .yt-lite .yt-play-btn svg { width: 22px; height: 22px; fill: #fff; margin-left: 3px; }
    .yt-lite.is-playing { cursor: default; }
    .yt-lite iframe {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }
    .yt-lite.yt-portrait { aspect-ratio: 9 / 16; max-height: 520px; margin: 0 auto; }
    .home-videos { padding: 72px 24px 64px; background: var(--light); }
    .home-videos .section-head { margin-bottom: 36px; }
    .home-videos-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      max-width: 1100px;
      margin: 0 auto 36px;
    }
    @media (max-width: 800px) {
      .home-videos-grid { grid-template-columns: 1fr; max-width: 420px; }
    }
    .home-videos-card {
      background: var(--white);
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid var(--rule);
      display: flex;
      flex-direction: column;
    }
    .home-videos-card h3 {
      color: var(--navy);
      font-size: 1.05rem;
      font-weight: 700;
      margin: 14px 16px 6px;
      line-height: 1.35;
    }
    .home-videos-card p {
      color: var(--gray);
      font-size: 0.9rem;
      line-height: 1.5;
      margin: 0 16px 18px;
    }
    .home-videos-actions { text-align: center; }
    .page-videos-embed {
      max-width: 900px;
      margin: 0 auto;
      padding: 56px 24px;
    }
    .page-videos-embed .section-head { margin-bottom: 28px; text-align: center; }
    .page-videos-embed .embed-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 22px;
    }
    .page-videos-embed .video-card { box-shadow: none; }
    .social-youtube { background: #ff0000; }
"""

PLAY_ICON = (
    '<span class="yt-play" aria-hidden="true"><span class="yt-play-btn">'
    '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 5v14l11-7z"/></svg>'
    "</span></span>"
)


def load_data():
    data = json.loads(DATA.read_text())
    public = [
        v
        for v in data["videos"]
        if v.get("visibility") == "public" and v.get("youtube_id")
    ]
    return data, public


def thumb_url(youtube_id: str) -> str:
    return f"https://i.ytimg.com/vi/{youtube_id}/hqdefault.jpg"


def content_url(youtube_id: str) -> str:
    return f"https://www.youtube.com/watch?v={youtube_id}"


def embed_url(youtube_id: str) -> str:
    return f"https://www.youtube-nocookie.com/embed/{youtube_id}"


def facade_html(v: dict, portrait: bool = False) -> str:
    yid = v["youtube_id"]
    title = v["title"]
    cls = "yt-lite yt-portrait" if portrait and v.get("shorts") else "yt-lite"
    return (
        f'<button type="button" class="{cls}" data-yt-id="{yid}" '
        f'data-yt-title="{html_esc(title)}" aria-label="Play {html_esc(title)}">'
        f'<img src="{thumb_url(yid)}" alt="" width="480" height="360" loading="lazy" decoding="async">'
        f"{PLAY_ICON}"
        f"</button>"
    )


def card_html(v: dict) -> str:
    return (
        '<article class="video-card">\n'
        f"  {facade_html(v)}\n"
        f"  <h3>{html_esc(v['title'])}</h3>\n"
        f'  <p class="video-blurb">{html_esc(v["blurb"])}</p>\n'
        "</article>\n"
    )


def html_esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def video_object_ld(v: dict) -> dict:
    return {
        "@type": "VideoObject",
        "name": v["title"],
        "description": v["description"],
        "thumbnailUrl": [thumb_url(v["youtube_id"]), f"https://i.ytimg.com/vi/{v['youtube_id']}/maxresdefault.jpg"],
        "uploadDate": v["upload_date"],
        "duration": v.get("duration"),
        "embedUrl": embed_url(v["youtube_id"]),
        "contentUrl": content_url(v["youtube_id"]),
        "publisher": {
            "@type": "Organization",
            "name": "HomeCore Construction",
            "url": "https://homecoregc.com",
            "logo": {
                "@type": "ImageObject",
                "url": "https://homecoregc.com/images/og-homecore.png",
            },
        },
    }


def build_videos_page(data: dict, public: list[dict]) -> None:
    template = (ROOT / "projects/index.html").read_text()
    # Start from projects page chrome
    head_match = re.search(r"<head>([\s\S]*?)</head>", template)
    head = head_match.group(1)

    # Replace title/meta/canonical/og
    title = "Videos | HomeCore Construction | Long Island, NY"
    desc = (
        "Watch HomeCore Construction at work on Long Island: custom homes, "
        "kitchen renovations, millwork and job site walkthroughs. See our YouTube videos."
    )
    canonical = "https://homecoregc.com/videos/"

    def repl_meta(src: str) -> str:
        src = re.sub(r"<title>[\s\S]*?</title>", f"<title>{title}</title>", src, count=1)
        src = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{html_esc(desc)}">',
            src,
            count=1,
        )
        src = re.sub(
            r'<link rel="canonical" href="[^"]*"\s*/?>',
            f'<link rel="canonical" href="{canonical}" />',
            src,
            count=1,
        )
        src = re.sub(
            r'<meta property="og:url" content="[^"]*"\s*/?>',
            f'<meta property="og:url" content="{canonical}" />',
            src,
            count=1,
        )
        src = re.sub(
            r'<meta property="og:title" content="[^"]*"\s*/?>',
            f'<meta property="og:title" content="{html_esc(title)}" />',
            src,
            count=1,
        )
        src = re.sub(
            r'<meta property="og:description" content="[^"]*"\s*/?>',
            f'<meta property="og:description" content="{html_esc(desc)}" />',
            src,
            count=1,
        )
        src = re.sub(
            r'<meta name="twitter:title" content="[^"]*"\s*/?>',
            f'<meta name="twitter:title" content="{html_esc(title)}" />',
            src,
            count=1,
        )
        src = re.sub(
            r'<meta name="twitter:description" content="[^"]*"\s*/?>',
            f'<meta name="twitter:description" content="{html_esc(desc)}" />',
            src,
            count=1,
        )
        # Ensure Videos CSS is in style block
        if ".videos-grid" not in src:
            src = src.replace("</style>", VIDEOS_CSS + "\n  </style>", 1)
        # Ensure yt-lite.js
        if "yt-lite.js" not in src:
            src = src.replace(
                '<script src="/assets/site.js" defer>',
                '<script src="/assets/js/yt-lite.js" defer></script>\n  <script src="/assets/site.js" defer>',
                1,
            )
        return src

    head = repl_meta(head)

    nav = re.search(r"<nav id=\"top\">[\s\S]*?</nav>", template).group(0)
    # Ensure Videos link present (patch_all_nav will also do this, but generate clean)
    if 'href="/videos/"' not in nav:
        nav = nav.replace(
            '<a href="/projects/">Our Work</a>\n    <a href="/areas-we-serve/">Areas</a>',
            '<a href="/projects/">Our Work</a>\n    <a href="/videos/">Videos</a>\n    <a href="/areas-we-serve/">Areas</a>',
        )

    footer = re.search(r"<footer>[\s\S]*?</footer>", template).group(0)
    schema = re.search(
        r'<script type="application/ld\+json">[\s\S]*?</script>', template
    ).group(0)
    # Patch sameAs in schema
    if YT_CHANNEL not in schema:
        schema = schema.replace(
            '"https://www.linkedin.com/company/homecore-construction/"\n  ]',
            '"https://www.linkedin.com/company/homecore-construction/",\n'
            + YT_SAMEAS_LINE
            + "\n  ]",
        )
        schema = schema.replace(
            '"https://www.linkedin.com/company/homecore-construction/"\n   ]',
            '"https://www.linkedin.com/company/homecore-construction/",\n'
            + YT_SAMEAS_LINE
            + "\n   ]",
        )

    cards = "\n".join(card_html(v) for v in public)

    item_list = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": "https://homecoregc.com/videos/#page",
        "url": "https://homecoregc.com/videos/",
        "name": "Watch HomeCore Construction at work",
        "description": desc,
        "isPartOf": {"@id": "https://homecoregc.com/#website"},
        "about": {"@id": "https://homecoregc.com/#business"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "item": video_object_ld(v),
                }
                for i, v in enumerate(public)
            ],
        },
    }
    video_ld = json.dumps(item_list, indent=2)

    body = f"""
<header class="page-hero">
  <span class="hero-eyebrow">Videos</span>
  <h1>Watch HomeCore Construction at work</h1>
  <p>Custom homes, renovations and millwork across Long Island. See the work on our job sites and in our shop, then talk with us about your project.</p>
</header>

<section class="videos" id="videos">
  <p class="videos-intro">
    New videos land on our
    <a href="{YT_CHANNEL}" target="_blank" rel="noopener">YouTube channel</a>
    first. Prefer a call?
    <a href="tel:5165093289">(516) 509-3289</a>
    or
    <a href="/#quote">request a free estimate</a>.
  </p>
  <div class="videos-grid">
{cards}  </div>
</section>

<section class="services-cta alt-bg">
  <h2>Ready to Build With Us?</h2>
  <p>Call or send us a message and we will set up a time to come out. Estimates are always free and always honest.</p>
  <div class="services-cta-actions">
    <a href="tel:5165093289" class="btn-solid">Call (516) 509-3289</a>
    <a href="/#quote" class="btn-outline-navy">Get a Free Estimate</a>
  </div>
</section>
"""

    # Need services-cta styles from a service page if not in projects
    if ".services-cta" not in head:
        cta_css = """
    .services-cta { text-align: center; padding: 72px 24px; }
    .services-cta h2 { color: var(--navy); font-size: clamp(1.4rem, 2.4vw, 1.85rem); font-weight: 700; margin-bottom: 12px; }
    .services-cta p { color: var(--gray); max-width: 560px; margin: 0 auto 24px; line-height: 1.6; }
    .services-cta-actions { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
    .alt-bg { background: var(--light); }
    .btn-solid {
      display: inline-flex; align-items: center; justify-content: center;
      background: var(--navy); color: var(--white); font-weight: 700;
      padding: 14px 22px; border-radius: 4px; text-decoration: none;
    }
    .btn-solid:hover { background: var(--deep-navy); }
    .btn-outline-navy {
      display: inline-flex; align-items: center; justify-content: center;
      border: 1.5px solid var(--navy); color: var(--navy); font-weight: 700;
      padding: 13px 22px; border-radius: 4px; text-decoration: none; background: transparent;
    }
    .btn-outline-navy:hover { background: var(--navy); color: var(--white); }
"""
        head = head.replace("</style>", cta_css + "\n  </style>", 1)

    # Keep projects page chrome after the footer (nav JS, action bar, site.js)
    foot_end = template.find("</footer>") + len("</footer>")
    body_end = template.rfind("</body>")
    tail = template[foot_end:body_end]

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
</head>
<body>
{nav}
{body}
{footer}

{schema}
<script type="application/ld+json">
{video_ld}
</script>
{tail}
  <script src="/assets/js/yt-lite.js" defer></script>
</body>
</html>
"""
    out = ROOT / "videos/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print(f"wrote {out.relative_to(ROOT)} ({len(public)} public videos)")


def patch_nav_and_sameas() -> None:
    yt_link = '    <a href="/videos/">Videos</a>\n'
    replacements = [
        (
            '<a href="#our-work">Our Work</a>\n    <a href="/areas-we-serve/">Areas</a>',
            '<a href="#our-work">Our Work</a>\n'
            + yt_link
            + '    <a href="/areas-we-serve/">Areas</a>',
        ),
        (
            '<a href="/projects/">Our Work</a>\n    <a href="/areas-we-serve/">Areas</a>',
            '<a href="/projects/">Our Work</a>\n'
            + yt_link
            + '    <a href="/areas-we-serve/">Areas</a>',
        ),
    ]
    same_a = (
        '"https://www.linkedin.com/company/homecore-construction/"\n  ]',
        '"https://www.linkedin.com/company/homecore-construction/",\n'
        + YT_SAMEAS_LINE
        + "\n  ]",
    )
    same_b = (
        '"https://www.linkedin.com/company/homecore-construction/"\n   ]',
        '"https://www.linkedin.com/company/homecore-construction/",\n'
        + YT_SAMEAS_LINE
        + "\n   ]",
    )

    count_nav = count_same = 0
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text()
        orig = text
        if 'href="/videos/"' not in text:
            for a, b in replacements:
                if a in text:
                    text = text.replace(a, b, 1)
                    count_nav += 1
                    break
        if YT_CHANNEL not in text and '"sameAs"' in text:
            if same_a[0] in text:
                text = text.replace(same_a[0], same_a[1], 1)
                count_same += 1
            elif same_b[0] in text:
                text = text.replace(same_b[0], same_b[1], 1)
                count_same += 1
        if text != orig:
            path.write_text(text)
    print(f"nav patched on {count_nav} pages; sameAs patched on {count_same} pages")


def ensure_videos_css_on_page(text: str) -> str:
    if ".yt-lite" in text and ".home-videos" in text:
        return text
    if "</style>" in text and ".yt-lite" not in text:
        text = text.replace("</style>", VIDEOS_CSS + "\n  </style>", 1)
    elif ".yt-lite" in text and ".home-videos" not in text:
        text = text.replace("</style>", VIDEOS_CSS + "\n  </style>", 1)
    if "yt-lite.js" not in text:
        if '<script src="/assets/site.js" defer></script>' in text:
            text = text.replace(
                '<script src="/assets/site.js" defer></script>',
                '<script src="/assets/js/yt-lite.js" defer></script>\n  <script src="/assets/site.js" defer></script>',
                1,
            )
        elif '<script src="/assets/site.js" defer>' in text:
            text = text.replace(
                '<script src="/assets/site.js" defer>',
                '<script src="/assets/js/yt-lite.js" defer></script>\n  <script src="/assets/site.js" defer>',
                1,
            )
        else:
            text = text.replace(
                "</body>",
                '  <script src="/assets/js/yt-lite.js" defer></script>\n</body>',
                1,
            )
    return text


def patch_home_strip(public: list[dict]) -> None:
    path = ROOT / "index.html"
    text = path.read_text()
    featured = [v for v in public if v.get("featured")][:3]
    if len(featured) < 3:
        featured = public[:3]

    cards = []
    for v in featured:
        cards.append(
            '<article class="home-videos-card">\n'
            f"  {facade_html(v)}\n"
            f"  <h3>{html_esc(v['title'])}</h3>\n"
            f"  <p>{html_esc(v['blurb'])}</p>\n"
            "</article>"
        )
    section = f"""
<!-- VIDEOS -->
<section class="home-videos" id="videos">
  <div class="section-head">
    <p class="section-eyebrow">Videos</p>
    <h2>See the Work</h2>
    <p class="section-sub">Job site walkthroughs, kitchen renovations and builds across Long Island, filmed as the work happens.</p>
  </div>
  <div class="home-videos-grid">
    {chr(10).join(cards)}
  </div>
  <div class="home-videos-actions">
    <a href="/videos/" class="btn-solid">View all videos</a>
  </div>
</section>

"""
    if 'id="videos"' in text and "home-videos" in text:
        text = re.sub(
            r"<!-- VIDEOS -->\s*<section class=\"home-videos\"[\s\S]*?</section>\s*",
            section,
            text,
            count=1,
        )
    else:
        text = text.replace(
            "<!-- ABOUT -->",
            section + "<!-- ABOUT -->",
            1,
        )

    # YouTube social icon next to other socials in work-social
    if "social-youtube" not in text:
        yt_a = (
            '      <a href="https://www.youtube.com/@HomeCoreConstruction" '
            'class="social-link social-youtube" '
            'aria-label="HomeCore Construction on YouTube" target="_blank" rel="noopener">\n'
            f"        {YOUTUBE_SVG}\n"
            "      </a>\n"
        )
        text = text.replace(
            'aria-label="HomeCore Construction on LinkedIn" target="_blank" rel="noopener">\n'
            ,
            'aria-label="HomeCore Construction on LinkedIn" target="_blank" rel="noopener">\n',
            1,
        )
        # Insert after LinkedIn block
        text = re.sub(
            r'(aria-label="HomeCore Construction on LinkedIn"[\s\S]*?</a>\n)',
            r"\1" + yt_a,
            text,
            count=1,
        )

    # Footer note: social icons live in Our Work; also add a compact footer YouTube text link if missing
    # Footer YouTube link (social icon row is in Our Work; footer gets a text+icon link too)
    foot = text.split("<footer>", 1)[1] if "<footer>" in text else ""
    if "youtube.com/@HomeCoreConstruction" not in foot[:900]:
        yt_icon = YOUTUBE_SVG.replace(
            'viewBox="0 0 24 24"',
            'width="18" height="18" viewBox="0 0 24 24"',
            1,
        )
        yt_footer = (
            '<p style="margin-bottom:10px">'
            '<a href="https://www.youtube.com/@HomeCoreConstruction" '
            'aria-label="HomeCore Construction on YouTube" '
            'style="display:inline-flex;align-items:center;gap:8px;color:rgba(255,255,255,0.85)">'
            + yt_icon
            + " YouTube</a></p>\n  "
        )
        text = text.replace(
            "<footer>\n  <p><strong>HomeCore Construction</strong>",
            "<footer>\n  " + yt_footer + "<p><strong>HomeCore Construction</strong>",
            1,
        )

    text = ensure_videos_css_on_page(text)
    path.write_text(text)
    print("patched home videos strip + YouTube social")


def patch_projects_index() -> None:
    path = ROOT / "projects/index.html"
    text = path.read_text()
    card = """
    <a href="/videos/" class="project-card">
      <div class="project-cover" style="background:#0D2340;display:flex;align-items:center;justify-content:center;min-height:220px;">
        <span style="color:#fff;font-size:1.1rem;font-weight:700;letter-spacing:0.4px;">Watch on YouTube</span>
        <span class="project-cat">Videos</span>
      </div>
      <div class="project-body">
        <h3>Videos</h3>
        <p>Job site walkthroughs, kitchen renovations and millwork from HomeCore Construction across Long Island.</p>
        <span class="project-link">View Videos &rarr;</span>
      </div>
    </a>
"""
    if 'href="/videos/"' in text and "View Videos" in text:
        text = re.sub(
            r'\s*<a href="/videos/" class="project-card">[\s\S]*?</a>\n',
            "\n" + card,
            text,
            count=1,
        )
    else:
        # Insert before closing projects-grid
        text = text.replace(
            "  </div>\n</section>",
            card + "  </div>\n</section>",
            1,
        )
    path.write_text(text)
    print("patched projects index Videos card")


def embed_section_for(page_key: str, videos: list[dict]) -> str:
    matched = [v for v in videos if page_key in (v.get("pages") or [])]
    if not matched:
        return ""
    cards = "\n".join(
        '<article class="video-card">\n'
        f"  {facade_html(v)}\n"
        f"  <h3>{html_esc(v['title'])}</h3>\n"
        f'  <p class="video-blurb">{html_esc(v["blurb"])}</p>\n'
        "</article>"
        for v in matched
    )
    heading = "Watch Related Videos"
    return f"""
<section class="page-videos-embed alt-bg" id="related-videos">
  <div class="section-head">
    <p class="section-eyebrow">Videos</p>
    <h2>{heading}</h2>
    <p class="section-sub">See HomeCore Construction at work. <a href="/videos/" style="color:var(--accent);font-weight:700;">View all videos</a></p>
  </div>
  <div class="embed-grid">
{cards}
  </div>
</section>
"""


def patch_page_embeds(public: list[dict]) -> None:
    # Map page key -> file path
    mapping = {
        "kitchen-remodeling": ROOT / "kitchen-remodeling.html",
        "custom-homes": ROOT / "custom-homes.html",
        "custom-millwork": ROOT / "custom-millwork.html",
        "whole-home-renovation": ROOT / "whole-home-renovation.html",
        "roofing-siding-windows": ROOT / "roofing-siding-windows.html",
        "projects/progress-stories/driveway-1": ROOT
        / "projects/progress-stories/driveway-1.html",
        "projects/progress-stories/custom-home-2": ROOT
        / "projects/progress-stories/custom-home-2.html",
        "projects/progress-stories/custom-home-1": ROOT
        / "projects/progress-stories/custom-home-1.html",
    }
    for key, path in mapping.items():
        if not path.exists():
            print(f"skip missing {path}")
            continue
        section = embed_section_for(key, public)
        if not section:
            # Remove prior embed if no public videos match
            text = path.read_text()
            if 'id="related-videos"' in text:
                text = re.sub(
                    r'\s*<section class="page-videos-embed[\s\S]*?</section>\s*',
                    "\n",
                    text,
                    count=1,
                )
                path.write_text(text)
                print(f"cleared embed on {path.relative_to(ROOT)}")
            continue
        text = path.read_text()
        text = ensure_videos_css_on_page(text)
        if 'id="related-videos"' in text:
            text = re.sub(
                r'<section class="page-videos-embed[\s\S]*?</section>',
                section.strip(),
                text,
                count=1,
            )
        elif '<section class="services-cta' in text:
            text = text.replace(
                '<section class="services-cta',
                section + '<section class="services-cta',
                1,
            )
        elif "<footer>" in text:
            text = text.replace("<footer>", section + "\n<footer>", 1)
        else:
            print(f"could not find insert point on {path}")
            continue
        # VideoObject JSON-LD for embedded videos
        matched = [v for v in public if key in (v.get("pages") or [])]
        ld = {
            "@context": "https://schema.org",
            "@graph": [video_object_ld(v) for v in matched],
        }
        ld_script = (
            '<script type="application/ld+json" id="related-videos-ld">\n'
            + json.dumps(ld, indent=2)
            + "\n</script>"
        )
        if 'id="related-videos-ld"' in text:
            text = re.sub(
                r'<script type="application/ld\+json" id="related-videos-ld">[\s\S]*?</script>',
                ld_script,
                text,
                count=1,
            )
        else:
            text = text.replace("</body>", ld_script + "\n</body>", 1)
        path.write_text(text)
        print(f"embedded {len(matched)} video(s) on {path.relative_to(ROOT)}")


def patch_sitemap(public: list[dict]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text()
    entry = """  <url>
    <loc>https://homecoregc.com/videos/</loc>
    <lastmod>2026-10-29</lastmod>
    <priority>0.9</priority>
  </url>
"""
    if "homecoregc.com/videos/" not in text:
        text = text.replace("</urlset>", entry + "</urlset>")
        path.write_text(text)
        print("added /videos/ to sitemap.xml")
    else:
        print("sitemap.xml already has /videos/")

    # Video sitemap
    ns = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"'
    urls = []
    for v in public:
        urls.append(
            f"""  <url>
    <loc>https://homecoregc.com/videos/</loc>
    <video:video>
      <video:thumbnail_loc>{thumb_url(v['youtube_id'])}</video:thumbnail_loc>
      <video:title>{html_esc(v['title'])}</video:title>
      <video:description>{html_esc(v['description'][:2048])}</video:description>
      <video:content_loc>{content_url(v['youtube_id'])}</video:content_loc>
      <video:player_loc>{embed_url(v['youtube_id'])}</video:player_loc>
      <video:publication_date>{v['upload_date']}</video:publication_date>
      <video:family_friendly>yes</video:family_friendly>
      <video:live>no</video:live>
    </video:video>
  </url>"""
        )
    vsm = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"<urlset {ns}>\n"
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "video-sitemap.xml").write_text(vsm)
    print(f"wrote video-sitemap.xml ({len(public)} entries)")

    # Reference video sitemap from main sitemap as sitemap index? Keep simple: add comment-free second file
    # Also add to robots.txt if present
    robots = ROOT / "robots.txt"
    if robots.exists():
        r = robots.read_text()
        if "video-sitemap.xml" not in r:
            if not r.endswith("\n"):
                r += "\n"
            r += "Sitemap: https://homecoregc.com/video-sitemap.xml\n"
            robots.write_text(r)
            print("added video-sitemap to robots.txt")


def patch_llms() -> None:
    path = ROOT / "llms.txt"
    text = path.read_text()
    line = "- [Videos](https://homecoregc.com/videos/): YouTube videos of HomeCore Construction custom homes, renovations and millwork on Long Island\n"
    if "homecoregc.com/videos/" not in text:
        # Add under Work section
        if "## Work" in text:
            text = text.replace("## Work\n", "## Work\n\n" + line, 1)
        else:
            text += "\n## Videos\n\n" + line
        path.write_text(text)
        print("added Videos to llms.txt")
    else:
        print("llms.txt already has Videos")


def main() -> None:
    data, public = load_data()
    print(f"public videos: {len(public)}")
    build_videos_page(data, public)
    patch_nav_and_sameas()
    patch_home_strip(public)
    patch_projects_index()
    patch_page_embeds(public)
    patch_sitemap(public)
    patch_llms()
    print("done")


if __name__ == "__main__":
    main()
