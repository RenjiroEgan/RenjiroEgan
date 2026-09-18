#!/usr/bin/env python3
"""Generates dark_mode.svg / light_mode.svg for the GitHub profile README."""
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

AW, GUT, RW = 44, 4, 60
FS, LH, PAD = 15.0, 19.0, 26.0
CW = FS * 0.6

THEMES = {
    "dark": dict(
        bg="#0d1117", border="#1f2d24",
        art=["#4ade80", "#2fb765", "#1c8248", "#155e35"],
        head="#ff9e4f", rule="#274036", label="#4ade80",
        dots="#24382e", value="#ffa657", accent="#ffd089",
    ),
    "light": dict(
        bg="#ffffff", border="#d4e2d8",
        art=["#14532d", "#1a7a45", "#37a468", "#9ed6b4"],
        head="#c2410c", rule="#cfe3d6", label="#15803d",
        dots="#dbe9e0", value="#ea580c", accent="#b45309",
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def row(label, value, width=RW):
    lab = label + " "
    dots = width - len(lab) - len(value) - 1
    return lab + "." * max(dots, 3) + " " + value


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
OFFSET = max((len(art_chars) - len(INFO)) // 2, 0)   # vertically centre info


def X(col):
    return f"{PAD + col * CW:.2f}"


def art_spans(i, c):
    """Colour the portrait by character density. Each run is pinned to an
    explicit x so columns line up in any monospace font."""
    if i >= len(art_chars):
        return ""
    line, sh = art_chars[i], art_shade[i]
    out = []
    x = 0
    while x < AW:
        ch = line[x] if x < len(line) else " "
        if ch == " ":
            x += 1
            continue
        s_i = sh[x] if x < len(sh) else 0
        run, start = "", x
        while x < AW:
            ch = line[x] if x < len(line) else " "
            s_j = sh[x] if x < len(sh) else -1
            if ch == " " or s_j != s_i:
                break
            run += ch
            x += 1
        out.append(f'<tspan x="{X(start)}" xml:space="preserve" '
                   f'fill="{c["art"][s_i]}">{esc(run)}</tspan>')
    return "".join(out)


def info_spans(i, c):
    j = i - OFFSET
    if j < 0 or j >= len(INFO):
        return ""
    t = INFO[j]
    if not t:
        return ""
    col0 = AW + GUT
    if "\u2500" in t:                                   # section rule
        head, _, dashes = t.partition("\u2500")
        return (f'<tspan x="{X(col0)}" xml:space="preserve" fill="{c["head"]}" '
                f'font-weight="bold">{esc(head)}</tspan>'
                f'<tspan x="{X(col0 + len(head))}" xml:space="preserve" '
                f'fill="{c["rule"]}">{"\u2500" + dashes}</tspan>')
    lab, _, rest = t.partition(" ")
    k = 0
    while k < len(rest) and rest[k] == ".":
        k += 1
    dots, val = rest[:k], rest[k:]
    dstart = col0 + len(lab) + 1
    return (f'<tspan x="{X(col0)}" xml:space="preserve" '
            f'fill="{c["label"]}">{esc(lab)}</tspan>'
            f'<tspan x="{X(dstart)}" xml:space="preserve" '
            f'fill="{c["dots"]}">{esc(dots)}</tspan>'
            f'<tspan x="{X(dstart + len(dots))}" xml:space="preserve" '
            f'fill="{c["value"]}">{esc(val)}</tspan>')


def plain(i):
    """The row as plain text -- used to compute textLength."""
    a = art_chars[i] if i < len(art_chars) else ""
    a = a.ljust(AW)
    j = i - OFFSET
    b = INFO[j] if 0 <= j < len(INFO) else ""
    return (a + " " * GUT + b).rstrip()


def build(theme):
    c = THEMES[theme]
    w = PAD * 2 + (AW + GUT + RW) * CW
    h = PAD * 2 + ROWS * LH
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}" font-family="Consolas, \'DejaVu Sans Mono\', '
        f'\'Courier New\', monospace" font-size="{FS}">',
        f'<rect x="0.5" y="0.5" width="{w-1:.0f}" height="{h-1:.0f}" rx="10" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]
    for i in range(ROWS):
        y = PAD + FS + i * LH
        n = len(plain(i))
        if n < 2:
            continue
        # textLength pins every row to exact monospace metrics, so the columns
        # stay aligned whatever monospace font the viewer's browser picks.
        tl = f' textLength="{n * CW:.2f}" lengthAdjust="spacing"'
        lines.append(
            f'<text x="{PAD:.0f}" y="{y:.1f}" xml:space="preserve"{tl}>'
            + art_spans(i, c)
            + info_spans(i, c)
            + "</text>"
        )
    lines.append("</svg>")
    out = "\n".join(lines)
    open(f"/mnt/user-data/outputs/{theme}_mode.svg", "w").write(out)
    return w, h


print(build("dark"), build("light"))
