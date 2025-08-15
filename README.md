# Purrfect Picks — Landing Page

A lightweight, responsive landing page for a pet shop brand. Built with semantic HTML, vanilla CSS, and a dash of JS.

## Structure

- `index.html` — the page markup, SEO meta, JSON‑LD, and sections
- `styles.css` — theme variables, layout, and components
- `script.js` — nav, accordion, carousel, and email capture
- `assets/` — images (add/replace with your own)
- `icons/` — inline SVG icons used in Benefits

## Local preview

You can open `index.html` directly in a browser, or run a simple server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Customize

- Branding: replace `assets/logo.png` and update colors in `styles.css` under `:root`
- Copy: edit section headings and text in `index.html`
- Images: drop your images into `assets/` and update the `src` paths
- Icons: swap SVGs in `icons/`

## Accessibility & Performance

- Keyboard accessible nav, carousel, and accordion
- Visible focus styles and AA color contrast
- Lazy‑loaded images and minimal JS

## Deploy to GitHub Pages

1. Push this folder to a repo, e.g., `purrfect-picks-site`
2. In GitHub, open Settings → Pages → Deploy from `main` branch → `/root` (or `docs/` if you move files there)
3. Update the canonical URL in `<head>` once your site is live

## Notes

- Cart buttons are demo only. Integrate with your cart later.
- Replace Open Graph image at `assets/og-image.jpg` for rich sharing.