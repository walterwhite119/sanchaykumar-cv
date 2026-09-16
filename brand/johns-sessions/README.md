# John's Sessions — logo set

Nine files, all built from vector geometry. The `.svg` files are the masters
(scale to anything — shirt print, court banner, website header); the `.png`
files are the ready-to-send versions for WhatsApp.

## Files

| File | Use |
| --- | --- |
| `johns-sessions-primary` | Main stacked mark, transparent background |
| `johns-sessions-primary-dark` | Same on the deep charcoal panel |
| `johns-sessions-horizontal` | One-line lockup — website header, email footer |
| `johns-sessions-horizontal-dark` | Same on charcoal |
| `johns-sessions-badge` | Circular — WhatsApp group icon, profile picture, sticker |
| `johns-sessions-mono-black` | Single colour, for a fax-quality print or a light shirt |
| `johns-sessions-mono-white` | Single colour reversed, for a dark shirt |
| `johns-academy-primary` | Same lockup with the lower line swapped to ACADEMY |
| `johns-academy-badge` | Circular Academy variant |

## Palette

| Role | Hex |
| --- | --- |
| Lime (primary) | `#8CC63F` |
| Deep charcoal (keyline, extrude, dark panel) | `#12160F` |
| Shuttle red (accent only — never for type) | `#E8342B` |
| Off-white | `#F5F7F1` |
| Lime shade (motion streaks) | `#4F7A18` |

## Why the lower line is a separate line

The lockup is built so the bottom word is swappable. Today it reads
**SESSIONS**, which is honest about what the thing currently is. The same
geometry reads **ACADEMY** without redrawing anything — see the academy
files. If the sessions ever become a coached academy or an affiliated club,
the brand upgrades with it instead of being thrown away, and nobody has to
re-print shirts.

"Sessions" is deliberately the starting point, not the destination: you
cannot put the word Sessions on a junior squad or a league team shirt.

## Source note

The reference sent over was a watermarked pngtree stock illustration. That
file cannot be used for a real business — it is someone else's copyrighted
artwork and the licence has not been bought. Nothing here is traced from it.
The alphabet, the shuttlecock and the brush streaks in these files are all
drawn from scratch in `src/`, so the marks are yours to print, register and
put on a shirt.

## Rebuilding

```sh
pip install shapely cairosvg
python3 src/build.py                       # writes the SVGs
python3 -c "import cairosvg,glob; [cairosvg.svg2png(url=f, write_to=f[:-4]+'.png') for f in glob.glob('*.svg')]"
```

Editing text, colour, slant or the amount of torn-edge distress all happens
in `src/build.py`. `src/glyphs.py` holds the letterform grid.
