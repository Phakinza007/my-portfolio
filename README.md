# Portfolio Cover Gallery

A static HTML portfolio gallery that collects five standalone landing-page projects into one cover page. The root `index.html` works as the portfolio entry point, and every project card opens the real full-page website.

![Portfolio cover](assets/screenshots/cover.png)

## Projects

| Project | File | Preview |
| --- | --- | --- |
| DevLaunch Academy | [`intern_landing_page_html_css.html`](intern_landing_page_html_css.html) | ![DevLaunch Academy screenshot](assets/screenshots/devlaunch.png) |
| Brew & Co. | [`Brew & Co..html`](Brew%20%26%20Co..html) | ![Brew and Co screenshot](assets/screenshots/brew-co.png) |
| NOIR Coffee | [`coffee-landing.html`](coffee-landing.html) | ![NOIR Coffee screenshot](assets/screenshots/noir-coffee.png) |
| DRIP Coffee Bar | [`DRIP.html`](DRIP.html) | ![DRIP Coffee Bar screenshot](assets/screenshots/drip.png) |
| Cozy Coffee Shop | [`coffee_shop_landing_page.html`](coffee_shop_landing_page.html) | ![Cozy Coffee Shop screenshot](assets/screenshots/cozy-coffee.png) |

## How To Open

### Open directly

Open `index.html` in a browser.

### Run locally

From this folder:

```bash
python -m http.server 4173 --bind 127.0.0.1
```

Then visit:

```text
http://127.0.0.1:4173/index.html
```

## Deploy With GitHub Pages

After pushing this repository to GitHub:

1. Open the repository on GitHub.
2. Go to `Settings` -> `Pages`.
3. Under `Build and deployment`, choose `Deploy from a branch`.
4. Select the `main` branch and `/ (root)` folder.
5. Save, then wait for GitHub Pages to publish the site.

The public URL will usually look like:

```text
https://YOUR-USERNAME.github.io/my-portfolio/
```

## Structure

```text
.
├── index.html
├── intern_landing_page_html_css.html
├── Brew & Co..html
├── coffee-landing.html
├── DRIP.html
├── coffee_shop_landing_page.html
└── assets/
    └── screenshots/
```

