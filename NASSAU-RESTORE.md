# Nassau restore point

This branch is `main` as of commit d8eb4dd (Oct 23 2026), the last version with the Nassau County town pages. It exists so the Nassau content can go back up in one push once the Nassau County Home Improvement license is issued. Do not deploy this branch as is: it predates later changes.

What was taken down on branch `nassau-scrub` (commit on top of d8eb4dd):

- Town pages: `areas-we-serve/garden-city.html`, `areas-we-serve/rockville-centre.html`, `areas-we-serve/wantagh.html`
- Hub cards and the "More Nassau Towns We Serve" section on `areas-we-serve/index.html`
- Nassau entries in schema `areaServed` (Nassau County, Garden City, Rockville Centre, Wantagh, Oyster Bay) on every page
- "Nassau and Suffolk" wording in titles, meta descriptions, service page copy, FAQs and the footer line
- `sitemap.xml` entries for the three town pages
- `llms.txt` Nassau town lines and the Garden City and Wantagh job lines
- `_redirects`: six 301s from the three town URLs to `/areas-we-serve/` (remove these when restoring)

How to restore (on the box):

1. `cd /workspace/seo/gen` and copy back `areas_v3_before_nassau_scrub.py` over `areas.py`, and take the Nassau parts of `common_v2_before_nassau_scrub.py` and `services_pages_v2_before_nassau_scrub.py` (keep the STYLE_BASE fix in the current `common.py`).
2. Run `python3 services_pages.py && python3 areas.py && python3 optimize.py`, then restore the hand edited files from this branch: `git checkout nassau-restore -- llms.txt sitemap.xml` and revert the `nassau_scrub.py` replacements on index, services and the project pages.
3. Delete the six Nassau lines at the bottom of `_redirects`, check, and push once.

Copies of the removed pages and the old generators are also in `/workspace/site/nassau-restore/` on the box.
