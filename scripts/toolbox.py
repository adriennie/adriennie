#!/usr/bin/env python3
"""Generate toolbox.svg, the toolbox card in the profile README.

Edit TOOLS below, then run from the repo root:

    python3 scripts/toolbox.py

Logo paths come from scripts/toolbox_icons.json (Simple Icons, CC0).
A tool without an icon gets a monogram tile instead.
"""
import json
import math
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "toolbox.svg")
ICONS = json.load(open(os.path.join(HERE, "toolbox_icons.json")))["icons"]

# (group, [(name, icon slug or None, brand colour, note), ...])
# Brand colours that vanish on a dark background are swapped for a light tint.
TOOLS = [
    ("languages", [
        ("Python", "python", "#FFD43B", "daily driver"),
        ("Rust", "rust", "#F74C00", "Sentinel-cli"),
        ("C++", "cplusplus", "#659AD2", "graphics, numerics"),
        ("TypeScript", "typescript", "#3178C6", "apps & tooling"),
        ("SQL", "postgresql", "#7C9CF0", "queries & schemas"),
        ("Bash", "gnubash", "#4EAA25", "glue & CI"),
    ]),
    ("ml-and-llms", [
        ("PyTorch", "pytorch", "#EE4C2C", "training & eval"),
        ("Hugging Face", "huggingface", "#FFD21E", "models & datasets"),
        ("vLLM", None, "#38bdf8", "PagedAttention ablations"),
        ("PEFT / LoRA", None, "#a855f7", "adapter serving"),
        ("scikit-learn", "scikitlearn", "#F7931E", "baselines first"),
        ("LangChain", "langchain", "#7dd3fc", "RAG pipelines"),
        ("RAGAS", None, "#f472b6", "RAG evaluation"),
    ]),
    ("systems-and-observability", [
        ("FastAPI", "fastapi", "#009688", "model APIs"),
        ("OpenTelemetry", "opentelemetry", "#F5A800", "traces & telemetry"),
        ("Docker", "docker", "#2496ED", "containers"),
        ("PostgreSQL", "postgresql", "#7C9CF0", "+ PostGIS"),
        ("Google Cloud", "googlecloud", "#4285F4", "Cloud Run, Vertex AI"),
        ("Azure AI", None, "#0ea5e9", "AI-102 certified"),
        ("GitHub Actions", "githubactions", "#2088FF", "CI that runs"),
        ("W&B", "weightsandbiases", "#FFBE00", "experiment tracking"),
    ]),
]

W = 1000
PAD = 28
COLS = 4
GAP = 12
TILE_W = (W - 2 * PAD - (COLS - 1) * GAP) / COLS
TILE_H = 62
HEAD_H = 40
PANEL_GAP = 14
TOP = 62
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',sans-serif"


def monogram(name):
    a, b = [c for c in name if c.isalnum()][:2]
    return a + (b.lower() if a.isupper() and b.isupper() else b)


def tile(x, y, name, slug, colour, note, delay):
    chip = 38
    cx, cy = x + 12, y + (TILE_H - chip) / 2
    out = [f'<g class="t" style="animation-delay:{delay:.2f}s">']
    out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{TILE_W:.1f}" height="{TILE_H}" rx="12" '
               f'fill="#111827" stroke="#1f2a44"/>')
    out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{chip}" height="{chip}" rx="10" '
               f'fill="{colour}" fill-opacity=".14" stroke="{colour}" stroke-opacity=".35"/>')
    if slug and slug in ICONS:
        s = 22 / 24
        out.append(f'<path transform="translate({cx + 8:.1f} {cy + 8:.1f}) scale({s:.4f})" '
                   f'fill="{colour}" d="{ICONS[slug]}"/>')
    else:
        out.append(f'<text x="{cx + chip / 2:.1f}" y="{cy + 25:.1f}" text-anchor="middle" '
                   f'font-family="{MONO}" font-size="14" font-weight="800" fill="{colour}">'
                   f'{escape(monogram(name))}</text>')
    tx = cx + chip + 12
    out.append(f'<text x="{tx:.1f}" y="{y + 27:.1f}" font-family="{SANS}" font-size="15" '
               f'font-weight="700" fill="#f5f3ff">{escape(name)}</text>')
    out.append(f'<text x="{tx:.1f}" y="{y + 46:.1f}" font-family="{MONO}" font-size="11.5" '
               f'fill="#94a3b8">{escape(note)}</text>')
    out.append('</g>')
    return "".join(out)


def build():
    body, y, i = [], TOP + 10, 0
    for group, tools in TOOLS:
        body.append(f'<text x="{PAD}" y="{y + 24}" font-family="{MONO}" font-size="14" font-weight="700">'
                    f'<tspan fill="#a855f7">▸ </tspan><tspan fill="#7dd3fc">{escape(group)}/</tspan>'
                    f'<tspan fill="#64748b">  {len(tools)} items</tspan></text>')
        y += HEAD_H
        for n, (name, slug, colour, note) in enumerate(tools):
            r, c = divmod(n, COLS)
            body.append(tile(PAD + c * (TILE_W + GAP), y + r * (TILE_H + GAP),
                             name, slug, colour, note, 0.15 + i * 0.05))
            i += 1
        y += math.ceil(len(tools) / COLS) * (TILE_H + GAP) - GAP + PANEL_GAP
    H = int(y + PAD - PANEL_GAP + 4)
    total = sum(len(t) for _, t in TOOLS)

    label = escape("Toolbox. " + " ".join(
        f"{g.replace('-', ' ')}: {', '.join(t[0] for t in tools)}." for g, tools in TOOLS), {'"': "&quot;"})
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{label}">
<style>
.t{{animation:in .4s ease-out both}}
@keyframes in{{from{{opacity:0;transform:translateY(6px)}}}}
.sheen{{animation:sh 7s ease-in-out infinite}}
@keyframes sh{{0%{{transform:translateX(-400px)}}60%,100%{{transform:translateX(1300px)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
<linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".35" stop-color="#22d3ee"/><stop offset=".65" stop-color="#4ade80"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
<radialGradient id="glow" cx=".1" cy="0" r=".8"><stop offset="0" stop-color="#22d3ee" stop-opacity=".12"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
<linearGradient id="sg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="card"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16"/></clipPath>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#foil)"/>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="#0a0e1a"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<rect x="0" y="0" width="{W}" height="46" fill="#111827"/>
<line x1="0" y1="46" x2="{W}" y2="46" stroke="#1f2937"/>
<circle cx="28" cy="23" r="6.5" fill="#f472b6"/><circle cx="50" cy="23" r="6.5" fill="#fbbf24"/><circle cx="72" cy="23" r="6.5" fill="#4ade80"/>
<text x="{W / 2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#64748b">adrika@usi: ~/toolbox — tree -L 2 · {total} tools</text>
'''
    tail = '<g class="sheen"><rect x="0" y="-40" width="220" height="2000" fill="url(#sg)" transform="skewX(-20)"/></g>\n</g>\n</svg>\n'
    with open(OUT, "w") as f:
        f.write(head + "\n".join(body) + "\n" + tail)
    print(f"wrote {os.path.normpath(OUT)} ({W}x{H}, {total} tools)")


if __name__ == "__main__":
    build()
