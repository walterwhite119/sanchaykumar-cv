# sanchaykumar-cv

Modeling portfolio site for Sanchay Kumar Sivakumar: book, digitals, measurements, contact.
Plain HTML/CSS/JS, no build step.

## Updating it

1. **Text and measurements:** edit `content.js` only.
2. **Photos:** drop them into `images/` using the filenames referenced in `content.js`
   (`hero.jpg`, `book-01.jpg` … `book-08.jpg`, `digital-front.jpg`, etc.). Missing images show a placeholder.
   Export at ~2000px on the long edge, JPG quality ~80, so the site stays fast on mobile.
3. **Comp card:** add `compcard.pdf` at the repo root (or set `compCard: ""` in `content.js` to hide the button).

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Publish (free)

GitHub repo → **Settings → Pages** → Source: *Deploy from a branch* → `main` / root.
The site will be live at `https://walterwhite119.github.io/sanchaykumar-cv/`.
