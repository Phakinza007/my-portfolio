# Portfolio Cover Gallery

A static HTML portfolio gallery that collects six standalone front-end projects into one cover page. The root `index.html` works as the portfolio entry point, with separate links for viewing each live page and opening its source file.

Live site: <https://phakinza007.github.io/my-portfolio/>

![Portfolio cover](assets/screenshots/cover.png)
![Social preview](assets/social-preview.png)

## Projects

| Project | Live page | Source file | Preview |
| --- | --- | --- | --- |
| PulseBoard | [`PulseBoard.html`](PulseBoard.html) | [`PulseBoard.html`](https://github.com/Phakinza007/my-portfolio/blob/main/PulseBoard.html) | ![PulseBoard screenshot](assets/screenshots/pulseboard.png) |
| DevLaunch Academy | [`intern_landing_page_html_css.html`](intern_landing_page_html_css.html) | [`intern_landing_page_html_css.html`](https://github.com/Phakinza007/my-portfolio/blob/main/intern_landing_page_html_css.html) | ![DevLaunch Academy screenshot](assets/screenshots/devlaunch.png) |
| Brew & Co. | [`Brew & Co..html`](Brew%20%26%20Co..html) | [`Brew & Co..html`](https://github.com/Phakinza007/my-portfolio/blob/main/Brew%20%26%20Co..html) | ![Brew and Co screenshot](assets/screenshots/brew-co.png) |
| NOIR Coffee | [`coffee-landing.html`](coffee-landing.html) | [`coffee-landing.html`](https://github.com/Phakinza007/my-portfolio/blob/main/coffee-landing.html) | ![NOIR Coffee screenshot](assets/screenshots/noir-coffee.png) |
| DRIP Coffee Bar | [`DRIP.html`](DRIP.html) | [`DRIP.html`](https://github.com/Phakinza007/my-portfolio/blob/main/DRIP.html) | ![DRIP Coffee Bar screenshot](assets/screenshots/drip.png) |
| Cozy Coffee Shop | [`coffee_shop_landing_page.html`](coffee_shop_landing_page.html) | [`coffee_shop_landing_page.html`](https://github.com/Phakinza007/my-portfolio/blob/main/coffee_shop_landing_page.html) | ![Cozy Coffee Shop screenshot](assets/screenshots/cozy-coffee.png) |

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

## GitHub Pages

This repository is deployed from the `main` branch and root folder:

```text
https://phakinza007.github.io/my-portfolio/
```

The launch setup includes SEO metadata, Open Graph/Twitter preview tags, a custom favicon, a web manifest, and a GitHub Pages `404.html` fallback.

## Contact

Phakin Chawanpunya

- GitHub: <https://github.com/Phakinza007>
- Email: <273589474+Pakkihaveuni@users.noreply.github.com>

## Structure

```text
.
├── index.html
├── 404.html
├── site.webmanifest
├── PulseBoard.html
├── intern_landing_page_html_css.html
├── Brew & Co..html
├── coffee-landing.html
├── DRIP.html
├── coffee_shop_landing_page.html
└── assets/
    ├── favicon.svg
    ├── social-preview.png
    ├── screenshots/
    └── thumbs/
```
