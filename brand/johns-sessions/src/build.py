"""Build the John's Sessions / John's Academy logo set.

Letterforms come from an original blocky alphabet (glyphs.py). Everything is
unioned with shapely first, so the torn edges, the dark keyline and the 3D
extrude are baked into real geometry -- the SVGs render identically in any
renderer, with no masks or clip paths to go wrong.
"""
import math, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glyphs import text_polys, H
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

OUT = os.environ.get("OUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.makedirs(OUT, exist_ok=True)

LIME, LIME_D, DEEP, RED, PAPER = "#8CC63F", "#4F7A18", "#12160F", "#E8342B", "#F5F7F1"
SKEW = 9.0          # degrees of lean


# ---------------------------------------------------------------- geometry ---
def mk_word(text, cap, tracking=18.0, skew=SKEW):
    polys, _ = text_polys(text, tracking)
    k = cap / H
    g = unary_union([Polygon([(x * k, y * k) for x, y in p]).buffer(0) for p in polys])
    if skew:
        g = affinity.skew(g, xs=-skew, origin=(0, cap))      # lean right at the top
    return affinity.translate(g, -g.bounds[0], -g.bounds[1])


def at(g, x, y):
    return affinity.translate(g, x, y)


def sliver(x, y, ln, th, drop, seed, steps=11):
    r = random.Random(seed)
    top = [(x + ln * i / steps, y + drop * i / steps + r.uniform(-.45, .45) * th)
           for i in range(steps + 1)]
    bot = [(x + ln * i / steps,
            y + drop * i / steps + th * (.15 + .85 * math.sin(math.pi * i / steps))
            + r.uniform(-.35, .35) * th)
           for i in range(steps, -1, -1)]
    return Polygon(top + bot).buffer(0)


def _pieces(g):
    return len(g.geoms) if hasattr(g, "geoms") else (0 if g.is_empty else 1)


def distress(g, seed, n=6, strength=1.0):
    """Rake thin angled slivers out of the wordmark.

    A candidate cut is kept only if it does not increase the number of
    connected pieces -- so it can nick a letter's edge but never sever a
    stroke. That keeps the mark readable at avatar size.
    """
    x0, y0, x1, y1 = g.bounds
    w, h = x1 - x0, y1 - y0
    r = random.Random(seed)
    base, area0 = _pieces(g), g.area
    kept, tries = 0, 0
    while kept < n and tries < n * 14:
        tries += 1
        ln = r.uniform(.22, .62) * w
        cut = sliver(x0 + r.uniform(-.06, .50) * w, y0 + r.uniform(.03, .99) * h, ln,
                     r.uniform(.007, .016) * h * strength,
                     -ln * math.tan(math.radians(r.uniform(5, 10))), seed * 97 + tries)
        cand = g.difference(cut.buffer(0))
        if _pieces(cand) > base or cand.area < area0 * .80:
            continue
        g, kept = cand, kept + 1
    return g


def shards(g, seed, n=7):
    """Detached fragments flung off the wordmark."""
    x0, y0, x1, y1 = g.bounds
    w, h = x1 - x0, y1 - y0
    r = random.Random(seed + 404)
    grown, out, tries = g.buffer(w * .006), [], 0
    while len(out) < n and tries < 300:
        tries += 1
        cx, cy = r.uniform(x0 - .05 * w, x1 + .07 * w), r.uniform(y0, y1)
        ln, th = r.uniform(.04, .13) * w, r.uniform(.008, .020) * h
        s = sliver(cx, cy, ln, th, -ln * math.tan(math.radians(8)), seed * 31 + tries)
        if not s.intersects(grown):
            out.append(s)
    return unary_union(out) if out else None


def d_of(g):
    if g is None or g.is_empty:
        return ""
    polys = g.geoms if isinstance(g, MultiPolygon) else [g]
    out = []
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = list(ring.coords)[:-1]
            if len(pts) < 3:
                continue
            out.append("M " + " L ".join(f"{a:.2f} {b:.2f}" for a, b in pts) + " Z")
    return " ".join(out)


# ------------------------------------------------------------------ drawing ---
def wordmark(g, ink=LIME, key=DEEP, extrude=DEEP, off=None, kw=None):
    """Dark extrude behind, flat face, dark keyline -- the reference's build."""
    x0, y0, x1, y1 = g.bounds
    off = off if off is not None else max(5.0, (y1 - y0) * .052)
    kw = kw if kw is not None else max(2.2, (y1 - y0) * .012)
    s = []
    if extrude:
        s.append('<path d="%s" fill="%s" fill-rule="evenodd"/>'
                 % (d_of(at(g, off, off)), extrude))
    s.append('<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="%.2f" '
             'stroke-linejoin="round"/>' % (d_of(g), ink, key or "none", kw if key else 0))
    return "\n".join(s)


def spray(x, y, w, h, seed, n=12, colour=LIME, op=.20, clip=None):
    r = random.Random(seed)
    out = []
    for i in range(n):
        ln = r.uniform(.25, 1.15) * w
        out.append(sliver(x + r.uniform(-.05, .40) * w, y + r.uniform(.02, .98) * h,
                          ln, r.uniform(.020, .065) * h,
                          -ln * math.tan(math.radians(r.uniform(4, 9))), seed * 7 + i))
    g = unary_union(out)
    if clip is not None:
        g = g.intersection(Polygon([(clip[0], clip[1]), (clip[2], clip[1]),
                                    (clip[2], clip[3]), (clip[0], clip[3])]))
    return '<path d="%s" fill="%s" fill-rule="evenodd" opacity="%.2f"/>' % (d_of(g), colour, op)


def shuttle(cx, cy, s, cork=RED, feather=PAPER, key=DEEP, tilt=-14, streak=None):
    u = s / 100.0
    def P(*pts):
        return "M " + " L ".join(f"{a*u:.2f} {b*u:.2f}" for a, b in pts) + " Z"
    g = ['<g transform="translate(%.2f %.2f) rotate(%d)">' % (cx, cy, tilt)]
    if streak:
        for i, (oy, ln) in enumerate(((-30, 76), (-8, 106), (16, 64))):
            g.append('<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="%.1f" '
                     'stroke-linecap="round" opacity="%.2f"/>'
                     % (-46 * u, oy * u, (-46 - ln) * u, oy * u, streak, 8 * u, .8 - i * .18))
    g.append('<g stroke="%s" stroke-width="%.2f" stroke-linejoin="round" '
             'stroke-linecap="round">' % (key, 3.6 * u))
    g.append('<path d="%s" fill="%s"/>' % (
        P((-17, 16), (17, 16), (36, -40), (30, -50), (-30, -50), (-36, -40)), feather))
    for i in range(1, 7):
        t = i / 7.0
        g.append('<path d="M %.2f %.2f L %.2f %.2f" stroke-width="%.2f"/>'
                 % ((-17 + 34 * t) * u, 16 * u, (-33 + 66 * t) * u, -46 * u, 2.4 * u))
    g.append('<path d="M %.2f %.2f L %.2f %.2f" stroke-width="%.2f"/>'
             % (-24 * u, -8 * u, 24 * u, -8 * u, 3.0 * u))
    g.append('<path d="%s" fill="%s"/>' % (
        P((-17, 16), (17, 16), (18, 27), (11, 38), (-11, 38), (-18, 27)), cork))
    g.append("</g></g>")
    return "\n".join(g)


def svg(w, h, body, bg=None):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">\n%s\n%s\n</svg>\n' % (w, h, w, h, b, body))


# ------------------------------------------------------------------ layouts ---
def stacked(top, bottom, size=(1200, 1010), bg=None, ink=LIME, sub=None,
            seed=7, mark=True, key=DEEP, extrude=DEEP):
    CW, CH = size
    gt = mk_word(top, 258, 20)
    gb = mk_word(bottom, 194, 18)
    wt, wb = gt.bounds[2], gb.bounds[2]
    sc = min(1.0, (CW * .84) / max(wt, wb))
    gt, gb = affinity.scale(gt, sc, sc, origin=(0, 0)), affinity.scale(gb, sc, sc, origin=(0, 0))
    ht, hb, wt, wb = gt.bounds[3], gb.bounds[3], gt.bounds[2], gb.bounds[2]
    gap = 26 * sc
    mark_h = 186.0 if mark else 0.0
    gs = mk_word(sub, 36, 62, skew=0) if sub else None
    sub_h = (gs.bounds[3] + 46) if sub else 0.0
    y = (CH - (mark_h + ht + gap + hb + sub_h)) / 2
    parts = []
    if mark:
        parts.append(shuttle(CW / 2 + 4, y + mark_h * .45, 196,
                             key=DEEP if not bg else "#090B07",
                             streak=(ink if bg else LIME_D)))
        y += mark_h
    block = unary_union([at(gt, (CW - wt) / 2, y), at(gb, (CW - wb) / 2, y + ht + gap)])
    x0, y0, x1, y1 = block.bounds
    parts.insert(0, spray(max(8, x0 - 70), y0 - 30,
                          min(CW - 16, (x1 - x0) + 150), (y1 - y0) + 70, seed,
                          colour=ink, op=.17 if bg else .22,
                          clip=(14, 14, CW - 14, CH - 14)))
    torn = distress(block, seed, n=6)
    parts.append(wordmark(torn, ink, key, extrude))
    sh = shards(block, seed)
    if sh is not None:
        parts.append('<path d="%s" fill="%s" fill-rule="evenodd" opacity="0.9"/>'
                     % (d_of(sh), ink))
    if sub:
        parts.append('<path d="%s" fill="%s" fill-rule="evenodd" opacity="0.92"/>'
                     % (d_of(at(gs, (CW - gs.bounds[2]) / 2, y + ht + gap + hb + 46)),
                        ink if bg else DEEP))
    return svg(CW, CH, "\n".join(parts), bg=bg)


def horizontal(text, w=1900, h=460, bg=None, ink=LIME, seed=11, mark=True,
               key=DEEP, extrude=DEEP, spray_on=True):
    g = mk_word(text, 212, 20)
    pad_l = 296 if mark else 90
    sc = min(1.0, (w - pad_l - 100) / g.bounds[2])
    g = affinity.scale(g, sc, sc, origin=(0, 0))
    gw, gh = g.bounds[2], g.bounds[3]
    g = at(g, pad_l + ((w - pad_l - 90) - gw) / 2, (h - gh) / 2)
    x0, y0, x1, y1 = g.bounds
    parts = []
    if spray_on:
        parts.append(spray(max(8, x0 - 60), y0 - 26, min(w - 16, (x1 - x0) + 130),
                           (y1 - y0) + 55, seed, n=10, colour=ink,
                           op=.16 if bg else .20, clip=(12, 12, w - 12, h - 12)))
    parts.append(wordmark(distress(g, seed, n=5), ink, key, extrude))
    sh = shards(g, seed, n=5) if spray_on else None
    if sh is not None:
        parts.append('<path d="%s" fill="%s" fill-rule="evenodd" opacity="0.9"/>'
                     % (d_of(sh), ink))
    if mark:
        parts.append(shuttle(174, h / 2, 262, key=DEEP if not bg else "#090B07",
                             streak=(ink if bg else LIME_D)))
    return svg(w, h, "\n".join(parts), bg=bg)


def badge(top, bottom, ring, d=1100, bg=DEEP, ink=LIME, seed=3):
    R = d / 2
    parts = ['<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (R, R, R - 4, bg),
             '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="18"/>'
             % (R, R, R - 32, ink),
             '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="5" '
             'opacity="0.45"/>' % (R, R, R - 66, ink)]
    g1 = mk_word(top, 138, 16)
    g1 = affinity.scale(g1, *(2 * [min(1.0, (d - 300) / g1.bounds[2])]), origin=(0, 0))
    g2 = mk_word(bottom, 108, 14)
    g2 = affinity.scale(g2, *(2 * [min(1.0, (d - 250) / g2.bounds[2])]), origin=(0, 0))
    gr = mk_word(ring, 32, 54, skew=0)
    gr = affinity.scale(gr, *(2 * [min(1.0, (d - 350) / gr.bounds[2])]), origin=(0, 0))
    mark_h = 230.0
    total = mark_h + g1.bounds[3] + 20 + g2.bounds[3] + gr.bounds[3] + 50
    y = (d - total) / 2 + 8
    parts.append(spray(96, y, d - 200, total, seed, n=9, colour=ink, op=.14,
                       clip=(R - (R - 80), R - (R - 80), R + (R - 80), R + (R - 80))))
    parts.append(shuttle(R + 4, y + mark_h * .44, 210, key="#090B07", streak=ink))
    y += mark_h
    parts.append(wordmark(distress(at(g1, (d - g1.bounds[2]) / 2, y), seed, n=3),
                          ink, DEEP, DEEP))
    y += g1.bounds[3] + 20
    parts.append('<path d="%s" fill="%s" fill-rule="evenodd"/>'
                 % (d_of(at(g2, (d - g2.bounds[2]) / 2, y)), PAPER))
    y += g2.bounds[3] + 44
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="%s" opacity="0.5"/>'
                 % ((d - gr.bounds[2]) / 2 - 26, y - 20, gr.bounds[2] + 52, ink))
    parts.append('<path d="%s" fill="%s" fill-rule="evenodd" opacity="0.9"/>'
                 % (d_of(at(gr, (d - gr.bounds[2]) / 2, y)), ink))
    return svg(d, d, "\n".join(parts))


files = {
    "johns-sessions-primary.svg":
        stacked("JOHN'S", "SESSIONS", sub="LIVERPOOL BADMINTON"),
    "johns-sessions-primary-dark.svg":
        stacked("JOHN'S", "SESSIONS", sub="LIVERPOOL BADMINTON", bg=DEEP, seed=9),
    "johns-sessions-horizontal.svg": horizontal("JOHN'S SESSIONS"),
    "johns-sessions-horizontal-dark.svg": horizontal("JOHN'S SESSIONS", bg=DEEP, seed=13),
    "johns-sessions-badge.svg": badge("JOHN'S", "SESSIONS", "LIVERPOOL - BADMINTON"),
    "johns-sessions-mono-black.svg":
        horizontal("JOHN'S SESSIONS", ink=DEEP, key=None, extrude=None, seed=17,
                   spray_on=False),
    "johns-sessions-mono-white.svg":
        horizontal("JOHN'S SESSIONS", ink=PAPER, key=None, extrude=None, bg=DEEP,
                   seed=19, spray_on=False),
    "johns-academy-primary.svg":
        stacked("JOHN'S", "ACADEMY", sub="BADMINTON LIVERPOOL", seed=23),
    "johns-academy-badge.svg": badge("JOHN'S", "ACADEMY", "BADMINTON - LIVERPOOL"),
}
for name, data in files.items():
    open(os.path.join(OUT, name), "w").write(data)
print("wrote", len(files), "svgs")
