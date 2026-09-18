#!/usr/bin/env python3
"""Generates dark_mode.svg / light_mode.svg for the GitHub profile README.

Every glyph is given its own x coordinate, so the layout does not depend on
which monospace font the viewer's browser happens to pick.

    python gen_svg.py        # reads art.json, writes both SVGs
"""
import json

# ---------------------------------------------------------------- EDIT ME ----
STATS = {
    "repos": "18",
    "stars": "0",
    "commits": "1,204",
    "followers": "1",
    "loc": "0",
}
# ------------------------------------------------------------------------------

ART = json.load(open("art.json"))
art_chars, art_shade = ART["chars"], ART["shade"]

AW, GUT, RW = 44, 3, 55        # art cols, gutter, info cols
FS, LH, PAD = 15.0, 20.0, 24.0
CW = 10.2                      # cell width: wider than any monospace advance
                               # at FS=15, so glyphs never collide

THEMES = {
    "dark": dict(
        bg="#0d1117", border="#1f2d24",
        art=["#4ade80", "#2fb765", "#1c8248", "#155e35"],
        head="#ff9e4f", rule="#274036", label="#4ade80",
        dots="#24382e", value="#ffa657",
    ),
    "light": dict(
        bg="#ffffff", border="#d4e2d8",
        art=["#14532d", "#1a7a45", "#37a468", "#9ed6b4"],
        head="#c2410c", rule="#cfe3d6", label="#15803d",
        dots="#dbe9e0", value="#ea580c",
    ),
}

FONT = ("Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', "
        "'Liberation Mono', 'Courier New', monospace")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row(label, value, width=RW):
    lab = label + " "
    return lab + "." * max(width - len(lab) - len(value) - 1, 3) + " " + value


def rule(title, width=RW):
    t = title + " "
    return t + "\u2500" * max(width - len(t), 3)


INFO = [
    rule("egan@renjiroegan"),
    row("Uptime:", "3 years"),
    row("Host:", "Engineer Every Now and Then"),
    "",
    row("Languages.Programming:", "Python, JavaScript, Java, SQL"),
    row("Focus:", "AI / Web Development"),
    row("Languages.Real:", "Indonesian, English, Malay"),
    "",
    row("Hobbies.Software:", "Cooking, Music"),
    row("Hobbies.Hardware:", "Photography, Travel"),
    "",
    rule("Contact"),
    row("Email:", "muhammadeganrenjiro@gmail.com"),
    row("LinkedIn:", "linkedin.com/in/jiroegan"),
    row("GitHub:", "github.com/RenjiroEgan"),
    row("Location:", "Jakarta"),
    "",
    rule("GitHub Stats"),
    row("Repos:", f"{STATS['repos']}   |   Stars: {STATS['stars']}"),
    row("Commits:", f"{STATS['commits']}   |   Followers: {STATS['followers']}"),
    row("Lines of Code:", STATS["loc"]),
]

ROWS = max(len(art_chars), len(INFO))
OFFSET = max((len(art_chars) - len(INFO)) // 2, 0)     # vertically centre info


def span(text, col, fill, bold=False):
    """One tspan with an explicit x for every character it contains."""
    if not text.strip():
        return ""
    xs = " ".join(f"{PAD + (col + k) * CW:.1f}" for k in range(len(text)))
    b = ' font-weight="bold"' if bold else ""
    return f'<tspan x="{xs}" fill="{fill}"{b}>{esc(text)}</tspan>'


def art_spans(i, c):
    """Colour the portrait by character density."""
    if i >= len(art_chars):
        return ""
    line, sh = art_chars[i], art_shade[i]
    out, x = [], 0
    while x < AW:
        if x >= len(line) or line[x] == " ":
            x += 1
            continue
        s_i, run, start = sh[x], "", x
        while x < AW and x < len(line) and line[x] != " " and sh[x] == s_i:
            run += line[x]
            x += 1
        out.append(span(run, start, c["art"][max(s_i, 0)]))
    return "".join(out)


def info_spans(i, c):
    j = i - OFFSET
    if not (0 <= j < len(INFO)) or not INFO[j]:
        return ""
    t, col0 = INFO[j], AW + GUT
    if "\u2500" in t:                                   # section rule
        head, _, dashes = t.partition("\u2500")
        return (span(head, col0, c["head"], bold=True)
                + span("\u2500" + dashes, col0 + len(head), c["rule"]))
    lab, _, rest = t.partition(" ")
    k = 0
    while k < len(rest) and rest[k] == ".":
        k += 1
    dots, val = rest[:k], rest[k:]
    d0 = col0 + len(lab) + 1
    return (span(lab, col0, c["label"])
            + span(dots, d0, c["dots"])
            + span(val, d0 + len(dots), c["value"]))


def build(theme):
    c = THEMES[theme]
    w = PAD * 2 + (AW + GUT + RW) * CW
    h = PAD * 2 + ROWS * LH
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" '
        f'height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
        f'font-family="{FONT}" font-size="{FS:.0f}px">',
        f'<style>text{{font-family:{FONT};font-size:{FS:.0f}px;'
        f'white-space:pre}}</style>',
        f'<rect x="0.5" y="0.5" width="{w-1:.0f}" height="{h-1:.0f}" rx="12" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]
    for i in range(ROWS):
        body = art_spans(i, c) + info_spans(i, c)
        if body:
            out.append(f'<text y="{PAD + FS + i * LH:.1f}">{body}</text>')
    out.append("</svg>")
    open(f"/mnt/user-data/outputs/{theme}_mode.svg", "w").write("\n".join(out))
    return int(w), int(h)


print("dark", build("dark"), "light", build("light"))
