"""Original blocky-display alphabet for the John's Sessions marks.

Every glyph is built from axis-aligned rectangles plus thick line "bars",
drawn on a 100 x 140 cap-height grid.  Straight-edged forms on purpose: the
mark gets its energy from slant + torn edges, not from curves.
"""
import math

H = 140.0           # cap height
W = 28.0            # stroke weight


def rect(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def bar(p1, p2, t=W):
    """Thick line segment from p1 to p2 as a quad."""
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L * t / 2, dx / L * t / 2
    return [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]


# each entry: (advance width, [polygons])
G = {}

G["A"] = (100, [bar((50, 0), (6, H)), bar((50, 0), (94, H)), rect(16, 82, 84, 110)])
G["B"] = (96, [rect(0, 0, 30, H), rect(0, 0, 80, 28), rect(0, 56, 84, 84),
               rect(0, 112, 88, H), rect(56, 28, 84, 56), rect(60, 84, 88, 112)])
G["C"] = (98, [rect(0, 0, 100, 28), rect(0, 0, 30, H), rect(0, 112, 100, H)])
G["D"] = (100, [rect(0, 0, 30, H), rect(0, 0, 74, 28), rect(0, 112, 74, H), rect(70, 14, 100, 126)])
G["E"] = (94, [rect(0, 0, 30, H), rect(0, 0, 96, 28), rect(0, 56, 84, 84), rect(0, 112, 96, H)])
G["F"] = (92, [rect(0, 0, 30, H), rect(0, 0, 96, 28), rect(0, 56, 84, 84)])
G["G"] = (100, [rect(0, 0, 100, 28), rect(0, 0, 30, H), rect(0, 112, 100, H),
                rect(70, 70, 100, H), rect(52, 70, 100, 96)])
G["H"] = (100, [rect(0, 0, 30, H), rect(70, 0, 100, H), rect(0, 56, 100, 84)])
G["I"] = (34, [rect(0, 0, 32, H)])
G["J"] = (100, [rect(70, 0, 100, 112), rect(8, 112, 100, H), rect(0, 76, 30, H)])
G["K"] = (100, [rect(0, 0, 30, H), bar((26, 70), (100, 0)), bar((26, 70), (100, H))])
G["L"] = (92, [rect(0, 0, 30, H), rect(0, 112, 94, H)])
G["M"] = (110, [rect(0, 0, 30, H), rect(80, 0, 110, H), bar((14, 4), (55, 92)), bar((96, 4), (55, 92))])
G["N"] = (102, [rect(0, 0, 30, H), rect(72, 0, 102, H), bar((14, 0), (88, H), 32)])
G["O"] = (100, [rect(0, 0, 100, 30), rect(0, 110, 100, H), rect(0, 0, 30, H), rect(70, 0, 100, H)])
G["P"] = (96, [rect(0, 0, 30, H), rect(0, 0, 84, 28), rect(0, 56, 84, 84), rect(56, 28, 84, 56)])
G["Q"] = (104, [rect(0, 0, 100, 30), rect(0, 110, 100, H), rect(0, 0, 30, H), rect(70, 0, 100, H),
                bar((62, 96), (104, 150), 26)])
G["R"] = (100, [rect(0, 0, 30, H), rect(0, 0, 84, 28), rect(0, 56, 84, 84), rect(56, 28, 84, 56),
                bar((52, 80), (98, H))])
G["S"] = (98, [rect(0, 0, 98, 28), rect(0, 0, 30, 70), rect(0, 56, 98, 84),
               rect(68, 70, 98, H), rect(0, 112, 98, H)])
G["T"] = (100, [rect(0, 0, 100, 28), rect(36, 0, 64, H)])
G["U"] = (100, [rect(0, 0, 30, H), rect(70, 0, 100, H), rect(0, 112, 100, H)])
G["V"] = (100, [bar((6, 0), (50, H)), bar((94, 0), (50, H))])
G["W"] = (118, [bar((6, 0), (32, H)), bar((32, H), (59, 44)), bar((59, 44), (86, H)), bar((86, H), (112, 0))])
G["X"] = (100, [bar((4, 0), (96, H)), bar((96, 0), (4, H))])
G["Y"] = (100, [bar((6, 0), (50, 76)), bar((94, 0), (50, 76)), rect(36, 70, 64, H)])
G["Z"] = (98, [rect(0, 0, 98, 28), rect(0, 112, 98, H), bar((80, 24), (18, 116), 32)])
G["'"] = (38, [[(0, 0), (30, 0), (20, 52), (0, 52)]])
G["."] = (40, [rect(0, 108, 30, H)])
G["-"] = (60, [rect(0, 58, 56, 82)])
G[" "] = (44, [])
G["/"] = (70, [bar((56, -6), (6, 146), 24)])
G["&"] = (100, [rect(0, 0, 30, 84), rect(0, 0, 84, 28), rect(0, 56, 84, 84),
                rect(0, 112, 100, H), bar((20, 70), (96, H))])
G["0"] = G["O"]
G["1"] = (52, [rect(18, 0, 48, H), bar((0, 30), (24, 6), 24)])
G["2"] = (96, [rect(0, 0, 96, 28), rect(66, 0, 96, 70), rect(0, 56, 96, 84),
               rect(0, 70, 30, H), rect(0, 112, 96, H)])
G["8"] = G["B"]


def text_polys(s, tracking=16.0):
    """Lay out a string; returns (polygons, total advance)."""
    out, x = [], 0.0
    for ch in s.upper():
        adv, polys = G.get(ch, G[" "])
        for p in polys:
            out.append([(px + x, py) for px, py in p])
        x += adv + tracking
    return out, max(0.0, x - tracking)


def path_d(polys):
    return " ".join(
        "M " + " L ".join(f"{px:.2f} {py:.2f}" for px, py in p) + " Z" for p in polys
    )
