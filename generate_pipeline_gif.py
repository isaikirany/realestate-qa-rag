import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

# ── Colors ────────────────────────────────────────────────────────────────────
BG           = '#1A1A1A'
ORANGE       = '#E8632A'
ORANGE_DIM   = '#7A3010'
NODE_BG      = '#242424'
NODE_ACTIVE  = '#2E1608'
BORDER_DIM   = '#3A3A3A'
WHITE        = '#F0F0F0'
GREY         = '#888888'

# ── Layout ────────────────────────────────────────────────────────────────────
FIG_W, FIG_H = 13, 7.5
NW, NH       = 2.05, 0.95   # node width / height

# (label_line1, label_line2, cx, cy)
NODES = [
    ("User",         "",              1.5,  5.6),
    ("Streamlit",    "UI",            4.0,  5.6),
    ("URL",          "Scraper",       6.5,  5.6),
    ("Text",         "Splitter",      9.0,  5.6),
    ("HuggingFace",  "Embeddings",    9.0,  3.0),
    ("ChromaDB",     "Vector Store",  6.5,  3.0),
    ("Groq",         "LLM",           4.0,  3.0),
    ("Answer",       "+ Sources",     1.5,  3.0),
]

# ── Arrow path segments (x0,y0 → x1,y1) ──────────────────────────────────────
def arrow_endpoints():
    segs = []
    for i in range(len(NODES) - 1):
        _, _, x0, y0 = NODES[i]
        _, _, x1, y1 = NODES[i + 1]
        if abs(y0 - y1) < 0.01:          # horizontal
            gap = NW / 2 + 0.05
            if x1 > x0:
                segs.append((x0 + gap, y0, x1 - gap, y1))
            else:
                segs.append((x0 - gap, y0, x1 + gap, y1))
        else:                              # vertical (turn)
            gap = NH / 2 + 0.05
            if y1 < y0:
                segs.append((x0, y0 - gap, x1, y1 + gap))
            else:
                segs.append((x0, y0 + gap, x1, y1 - gap))
    return segs

ARROWS = arrow_endpoints()
N_SEGS = len(ARROWS)

# ── Animation timing ──────────────────────────────────────────────────────────
TRAVEL   = 22   # frames per segment travel
PAUSE    = 10   # frames pause at each node
TOTAL_F  = TRAVEL * N_SEGS + PAUSE * (N_SEGS + 1)

# ── Drawing helpers ───────────────────────────────────────────────────────────
def draw_node(ax, x, y, line1, line2, active):
    ec  = ORANGE       if active else BORDER_DIM
    fc  = NODE_ACTIVE  if active else NODE_BG
    lw  = 2.2          if active else 1.0
    tc  = WHITE        if active else '#AAAAAA'
    fw  = 'bold'       if active else 'normal'

    box = mpatches.FancyBboxPatch(
        (x - NW / 2, y - NH / 2), NW, NH,
        boxstyle="round,pad=0.08",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=3
    )
    ax.add_patch(box)

    if line2:
        ax.text(x, y + 0.19, line1, color=tc, ha='center', va='center',
                fontsize=12.5, fontweight=fw, zorder=4)
        ax.text(x, y - 0.19, line2, color=tc, ha='center', va='center',
                fontsize=11.5, fontweight=fw, zorder=4)
    else:
        ax.text(x, y, line1, color=tc, ha='center', va='center',
                fontsize=13, fontweight=fw, zorder=4)


def draw_arrow(ax, x0, y0, x1, y1, active):
    color = ORANGE if active else BORDER_DIM
    lw    = 2.2    if active else 1.2
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=lw,
                    mutation_scale=18
                ), zorder=2)


def draw_dot(ax, x, y):
    ax.plot(x, y, 'o', color=ORANGE, markersize=11, zorder=6)
    for r, a in [(20, 0.25), (28, 0.10)]:
        ax.plot(x, y, 'o', color=ORANGE, markersize=r, alpha=a, zorder=5)


# ── Frame mapper ──────────────────────────────────────────────────────────────
def frame_state(frame):
    """Return (seg_idx, t) where t in [0,1] is dot progress, t=None if pausing."""
    cursor = 0
    cursor += PAUSE   # initial pause before anything moves
    for seg in range(N_SEGS):
        if frame < cursor:
            return seg, None          # pausing at node before this seg
        if frame < cursor + TRAVEL:
            t = (frame - cursor) / TRAVEL
            return seg, t             # dot traveling segment
        cursor += TRAVEL
        if frame < cursor + PAUSE:
            return seg + 1, None      # pausing at node after seg
        cursor += PAUSE
    return N_SEGS, None


# ── Main draw ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor(BG)

def animate(frame):
    ax.clear()
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(1.8, 7.5)
    ax.axis('off')

    seg_idx, t = frame_state(frame)
    nodes_lit = seg_idx   # nodes 0..nodes_lit-1 are fully lit; nodes_lit is being reached

    # Title
    ax.text(FIG_W / 2, 7.1,
            "RAG Pipeline  —  Real Estate Research Tool",
            color=WHITE, fontsize=14.5, fontweight='bold',
            ha='center', va='center', fontfamily='DejaVu Sans')

    # Row labels
    ax.text(0.15, 5.6, "①", color=GREY, fontsize=9, va='center')
    ax.text(0.15, 3.0, "②", color=GREY, fontsize=9, va='center')

    # Draw arrows
    for i, (x0, y0, x1, y1) in enumerate(ARROWS):
        active = i < nodes_lit or (i == nodes_lit - 1 and t is None)
        draw_arrow(ax, x0, y0, x1, y1, active=active)

    # Draw nodes
    for i, (l1, l2, x, y) in enumerate(NODES):
        active = i < nodes_lit or (i == nodes_lit and t is None)
        draw_node(ax, x, y, l1, l2, active=active)

    # Traveling dot
    if t is not None and seg_idx < N_SEGS:
        x0, y0, x1, y1 = ARROWS[seg_idx]
        dx = x0 + t * (x1 - x0)
        dy = y0 + t * (y1 - y0)
        draw_dot(ax, dx, dy)

    # Footer
    ax.text(FIG_W / 2, 2.0,
            "LangChain  ·  Groq LLM  ·  ChromaDB  ·  HuggingFace  ·  Streamlit",
            color=GREY, fontsize=8.5, ha='center', va='center')


anim = FuncAnimation(fig, animate, frames=TOTAL_F, interval=50)
writer = PillowWriter(fps=20)
output = "rag_pipeline.gif"
anim.save(output, writer=writer, dpi=130)
plt.close()
print(f"Saved: {output}")
