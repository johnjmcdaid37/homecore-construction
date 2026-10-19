# Progress Stories preview (local only) — revised

**Do not push until JJ OKs.** Branch: `preview/progress-stories`.

## How to preview

```bash
cd /workspace/site/repo
python3 -m http.server 8765
```

Open:

- Hub: http://127.0.0.1:8765/projects/progress-stories/
- Projects hub (3 cards): http://127.0.0.1:8765/projects/
- Homepage Our Work: http://127.0.0.1:8765/

- custom-home-1: http://127.0.0.1:8765/projects/progress-stories/custom-home-1.html
- custom-home-2: http://127.0.0.1:8765/projects/progress-stories/custom-home-2.html
- whole-home-1: http://127.0.0.1:8765/projects/progress-stories/whole-home-1.html
- whole-home-2: http://127.0.0.1:8765/projects/progress-stories/whole-home-2.html
- kitchen-1: http://127.0.0.1:8765/projects/progress-stories/kitchen-1.html
- bathroom-1: http://127.0.0.1:8765/projects/progress-stories/bathroom-1.html
- driveway-1: http://127.0.0.1:8765/projects/progress-stories/driveway-1.html
- garage-opening-1: http://127.0.0.1:8765/projects/progress-stories/garage-opening-1.html

Local Python server needs `.html` on story URLs (Netlify pretty paths later).

## Hub cover (why it is not the PIP look)

**Cover:** `images/projects/progress-stories/custom-home-1/06-underpinning-numbers.jpg`

Spray painted numbered underpinning walls inside the deepened basement. Reads as a documented build story, not an open-field framing house (the Projects in Progress cover look). Same image is used on the Projects hub Progress Stories card and the homepage Our Work Progress Stories tile.

## Photo counts

| Public name | Internal | Count |
|-------------|----------|------:|
| Custom Home | Goulard | 22 |
| Custom Home | Bridgehampton | 20 |
| Whole Home | Billy's rental | 26 |
| Whole Home | Eric Cook | 20 |
| Kitchen | Nonna's Dream Kitchen | 18 |
| Bathroom | master-bath website sequence | 21 |
| Driveway | Jennifer driveway | 19 |
| Garage Opening | Cara's garage | 17 |
| **Total** | | **163** |

## Per-job notes (befores and sources)

### Custom Home (Goulard) — 22
Befores: original bath + gutted interior. Then steel, numbered underpinning (not footing dig-out), foundation pour, GMX Ultra-Shield waterproofing, rear floor deck, framing, sheathing. Rear/interior orientation only (no front dumpster / garage-left brick mix). Sources: website `addition-*`, `/workspace/bf1016/final/`.

### Custom Home (Bridgehampton) — 20
Early footing dig as before-ish, then pour, foundation, waterproofing, framing, ZIP System wrap, roofing. Sources: GBP Bridgehampton + verified ground-up website `custom-home-*` (avoided Oct 15 Goulard remaps).

### Whole Home (Billy rental) — 26
Befores available: dated kitchen, bath, stair, exterior (Jul 29 band). Then demo, roofing, drywall, flooring, kitchen, finished rooms. Source: `/workspace/portfolio/icloud/billys-rental` sorted by capture date.

### Whole Home (Eric Cook) — 20
Befores scarce as pristine pre-touch exteriors; earliest set is already mid-gut / open framing. Sequence uses earliest gutted rooms as the start, then paint, tile, finished rooms. Source: `/workspace/portfolio/icloud/eric-cook` by date. **True untouched before photos were scarce.**

### Kitchen — 18
Three before angles, demo, studs, rough-in, cabinets, finished. BA slider kept. Sources: `nonnas-dream-kitchen/*` + website `kitchen-*`.

### Bathroom — 21
Full website `master-bath-*` sequence (gut through near finished shower). Strong before (gutted). Single room, no cross-job mix.

### Driveway (Jennifer) — 19
Clear before (`driveway-01-before`), excavator/demo, drainage, forms, concrete, pavers, finished. Source: website `driveway-*` (already curated build order).

### Garage Opening (Cara) — 17
Befores: sealed garage wall / interior before cut. Then opening, framing, wiring. Sources: `/workspace/portfolio/icloud/cara-garage` (11) + website `garage-*` (6). Same-day shoot; filename order used for before-first.

## Files touched

- `projects/progress-stories/` (hub + 8 story pages)
- `images/projects/progress-stories/` (all job folders rebuilt)
- `projects/index.html`, `index.html` (Progress Stories card cover + copy)
- `assets/site.js` (lightbox includes story carousel frames)
- `PREVIEW-progress-stories.md`, `PREVIEW-progress-stories-manifest.json`

Nothing pushed to GitHub or Netlify.
