# HomeCore Construction website

Marketing site for HomeCore Construction, a remodeling and construction company on Long Island, NY. Live at https://homecoregc.com.

## How it works

- Plain HTML and CSS with no build step. Each page carries its own styles and a small script for the menu.
- Every push to `main` deploys automatically on Netlify.
- `_redirects` sends the old homecore-construction.com domain and legacy paths to homecoregc.com.

## Pages

| File | Page |
|---|---|
| `index.html` | Homepage: quick quote form, Our Work, About, Contact |
| `services.html` | Services, linked from the Services menu |
| `projects/index.html` | Recent Projects listing |
| `projects/past-projects.html` | Finished work gallery |
| `projects/projects-in-progress.html` | Job site progress, grouped by project |
| `projects/nonnas-dream-kitchen.html` | Kitchen project story (not currently listed) |
| `privacy.html` | Privacy policy |

## Images

- `images/brand/`: full-color master logos
- `images/projects/all-past-projects/`: finished work photos, named `<category>-<description>.jpg`
- `images/projects/projects-in-progress/`: progress photos, named `<group>-NN-<description>.jpg`
- `images/projects/nonnas-dream-kitchen/`: kitchen story photos

Keep each photo under about 200KB. Never add `width` or `height` attributes to the Projects in Progress gallery images; that gallery's CSS stretches them.

## Quote form

The quick quote form posts to a Google Form. That form requires first name, last name, phone, address, city, and project type, so the quick form fills the fields it does not ask for with a "(quick quote form)" marker. Check a test submission in the responses sheet after any form change.
