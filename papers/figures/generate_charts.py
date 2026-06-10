import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
import os

# ── Global style (tuned for standard paper sizing) ────────────────────────
plt.style.use('seaborn-v0_8-white')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'Liberation Serif', 'DejaVu Serif', 'Nimbus Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = SCRIPT_DIR
JSON_PATH = os.path.join(SCRIPT_DIR, "..", "verification_data", "abstract_corpus_analysis.json")

def load_data():
    with open(JSON_PATH, "r") as f:
        return json.load(f)

data = load_data()

def cleanup_axes(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ══════════════════════════════════════════════════════════════════════════
# Chart 1: Publication Volume
# ══════════════════════════════════════════════════════════════════════════
def chart1():
    by_year = data["by_year"]
    years = sorted([int(y) for y in by_year.keys()])
    counts = [by_year[str(y)] for y in years]
    
    # Compute YoY growth (skip 2013 and 2026)
    yoy = [None]  # No growth for first year
    for i in range(1, len(counts)):
        yoy.append((counts[i] - counts[i-1]) / counts[i-1] * 100)
    
    fig, ax1 = plt.subplots(figsize=(5.5, 3.5))
    
    # Phase shading
    ax1.axvspan(2012.5, 2016.5, alpha=0.08, color='#4393c3', zorder=0)
    ax1.axvspan(2016.5, 2022.5, alpha=0.08, color='#2166ac', zorder=0)
    ax1.axvspan(2022.5, 2026.5, alpha=0.08, color='#b2182b', zorder=0)
    
    # Phase labels at top
    ax1.text(2014.5, max(counts)*0.55, 'Phase 1', ha='center', fontsize=7, color='#4393c3', fontweight='bold')
    ax1.text(2019.5, max(counts)*1.02, 'Phase 2', ha='center', fontsize=7, color='#2166ac', fontweight='bold')
    ax1.text(2024.5, max(counts)*1.02, 'Phase 3', ha='center', fontsize=7, color='#b2182b', fontweight='bold')
    
    # Primary axis: publication volume line
    ax1.plot(years[:-1], counts[:-1], 'o-', color='#2166ac', linewidth=2, markersize=4, zorder=3, label='Publications')
    ax1.plot(years[-1], counts[-1], 's', color='#92c5de', markersize=5, zorder=3)  # partial year marker
    ax1.plot([years[-2], years[-1]], [counts[-2], counts[-1]], '--', color='#92c5de', linewidth=1.5, zorder=3)
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Publications', color='#2166ac')
    ax1.tick_params(axis='y', labelcolor='#2166ac')
    ax1.set_xticks(years)
    ax1.set_xticklabels([str(y) for y in years], rotation=45)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
    ax1.set_ylim(0, max(counts) * 1.12)
    
    # Secondary axis: YoY growth rate
    ax2 = ax1.twinx()
    yoy_years = [y for y, g in zip(years, yoy) if g is not None and y < 2026]
    yoy_vals = [g for y, g in zip(years, yoy) if g is not None and y < 2026]
    ax2.plot(yoy_years, yoy_vals, '^--', color='#d6604d', linewidth=1.2, markersize=3.5, alpha=0.85, zorder=2, label='YoY Growth')
    ax2.set_ylabel('YoY Growth (%)', color='#d6604d')
    ax2.tick_params(axis='y', labelcolor='#d6604d')
    ax2.set_ylim(0, 50)
    
    # Combined legend
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    legend_elements = [
        Line2D([0], [0], color='#2166ac', marker='o', markersize=4, linewidth=2, label='Publications (Full Year)'),
        Line2D([0], [0], color='#92c5de', marker='s', markersize=5, linestyle='--', linewidth=1.5, label='Publications (Partial Year)'),
        Line2D([0], [0], color='#d6604d', marker='^', markersize=3.5, linestyle='--', linewidth=1.2, label='YoY Growth Rate (%)'),
    ]
    ax1.legend(handles=legend_elements, frameon=True, fancybox=True, shadow=False, fontsize=7, loc='upper left')
    
    cleanup_axes(ax1)
    ax2.spines['top'].set_visible(False)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_publication_volume.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 1 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 2: Established Methods
# ══════════════════════════════════════════════════════════════════════════
def chart2():
    timelines = data["timelines"]
    years_full = list(range(2013, 2027))
    
    neural = [timelines["neural network"].get(str(y), 0) for y in years_full]
    deep =   [timelines["deep learning"].get(str(y), 0) for y in years_full]
    rl =     [timelines["reinforcement learning"].get(str(y), 0) for y in years_full]
    
    years_trans = list(range(2017, 2027))
    transformer = [timelines["transformer"].get(str(y), 0) for y in years_trans]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(years_full, neural, marker='o', markersize=4, linewidth=1.5, label='Neural Network', color='#2166ac')
    ax.plot(years_full, deep,   marker='s', markersize=4, linewidth=1.5, label='Deep Learning',  color='#d6604d')
    ax.plot(years_full, rl,     marker='^', markersize=4, linewidth=1.5, label='Reinforcement Learning', color='#4daf4a')
    ax.plot(years_trans, transformer, marker='D', markersize=4, linewidth=1.5, label='Transformer', color='#ff7f00', linestyle='--')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years_full)
    labels = [str(y) for y in years_full]
    labels[-1] = '2026\n(Jun)'
    ax.set_xticklabels(labels, rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=9)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_established_methods.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 2 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 3: LLM Explosion
# ══════════════════════════════════════════════════════════════════════════
def chart3():
    timelines = data["timelines"]
    years = list(range(2018, 2027))
    counts = [timelines["large language model"].get(str(y), 0) for y in years]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    ax.plot(years, counts, marker='o', markersize=5, linewidth=2, color='#1a5276', zorder=5)
    ax.fill_between(years, counts, alpha=0.15, color='#2980b9')

    ax.axvline(x=2022.5, color='#c0392b', linestyle='--', linewidth=1.2, alpha=0.8)
    ax.annotate('ChatGPT\nrelease', xy=(2022.5, max(counts) * 0.85),
                xytext=(2020.0, max(counts) * 0.90),
                fontsize=9, color='#c0392b', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.0))

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years)
    labels = [str(y) for y in years]
    labels[-1] = '2026\n(upto June)'
    ax.set_xticklabels(labels)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_llm_explosion.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 3 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 4: Rising Methods
# ══════════════════════════════════════════════════════════════════════════
def chart4():
    timelines = data["timelines"]
    years_diff = list(range(2019, 2027))
    diffusion = [timelines["diffusion model"].get(str(y), 0) for y in years_diff]

    years_fed = list(range(2017, 2027))
    federated = [timelines["federated learning"].get(str(y), 0) for y in years_fed]

    years_gnn = list(range(2017, 2027))
    gnn = [timelines["graph neural"].get(str(y), 0) for y in years_gnn]

    years_kg = list(range(2013, 2027))
    knowledge = [timelines["knowledge graph"].get(str(y), 0) for y in years_kg]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(years_diff, diffusion, marker='o', markersize=4, linewidth=1.5, label='Diffusion Model', color='#e41a1c')
    ax.plot(years_fed, federated,  marker='s', markersize=4, linewidth=1.5, label='Federated Learning', color='#377eb8')
    ax.plot(years_gnn, gnn,        marker='^', markersize=4, linewidth=1.5, label='Graph Neural Network', color='#4daf4a')
    ax.plot(years_kg, knowledge,   marker='D', markersize=4, linewidth=1.5, label='Knowledge Graph', color='#984ea3')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    all_years = sorted(set(years_diff + years_fed + years_gnn + years_kg))
    ax.set_xticks(all_years)
    labels = [str(y) for y in all_years]
    labels[-1] = '2026\n(upto June)'
    ax.set_xticklabels(labels, rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=9)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_rising_methods.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 4 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 5: Top 10 Countries
# ══════════════════════════════════════════════════════════════════════════
def chart5():
    raw_countries = data["countries"]
    
    # Map long names to standard display names
    name_mapping = {
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
        "Korea, Republic of": "South Korea",
        "Russian Federation": "Russia"
    }
    
    mapped_countries = []
    for name, count in raw_countries.items():
        display_name = name_mapping.get(name, name)
        mapped_countries.append((display_name, count))
        
    # Sort and take Top 10
    mapped_countries = sorted(mapped_countries, key=lambda x: x[1], reverse=True)[:10]
    
    countries = [x[0] for x in mapped_countries]
    counts = [x[1] for x in mapped_countries]

    # Reverse for horizontal bar (top at top)
    countries = countries[::-1]
    counts = counts[::-1]

    # Sequential blue palette
    cmap = plt.cm.Blues
    norm_vals = np.linspace(0.4, 0.9, len(countries))
    colors = [cmap(v) for v in norm_vals]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bars = ax.barh(countries, counts, color=colors, edgecolor='white', height=0.7)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 15000, bar.get_y() + bar.get_height() / 2,
                f'{count:,}', va='center', fontsize=9)

    ax.set_xlabel('Number of Publications')
    ax.set_xlim(0, max(counts) * 1.15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_countries.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 5 (Top 10 Countries) saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 6: Citation Distribution
# ══════════════════════════════════════════════════════════════════════════
def chart6():
    citation_dist = data["citation_dist"]
    categories = ['0', '1–10', '11–50', '51–100', '101–500', '501–1000', '1000+']
    counts = [
        citation_dist.get("0", 0),
        citation_dist.get("1-10", 0),
        citation_dist.get("11-50", 0),
        citation_dist.get("51-100", 0),
        citation_dist.get("101-500", 0),
        citation_dist.get("501-1000", 0),
        citation_dist.get("1001+", 0)
    ]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bars = ax.bar(categories, counts, color='#2166ac', edgecolor='white', width=0.65)

    ax.set_yscale('log')
    ax.set_xlabel('Citation Count')
    ax.set_ylabel('Number of Papers (log scale)')

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.15,
                f'{count:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylim(1e3, 1e7)
    cleanup_axes(ax)
    ax.yaxis.set_minor_locator(plt.NullLocator())
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_citation_dist.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 6 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 7: China vs United States (Overall)
# ══════════════════════════════════════════════════════════════════════════
def chart7():
    years = list(range(2013, 2026))
    china = [12074, 11897, 11766, 12229, 17125, 27353, 41011, 53743,
             71273, 90485, 112646, 144452, 187887]
    us =    [13829, 14551, 16713, 18988, 23991, 33567, 45404, 58622,
             64931, 64486, 77664, 90915, 122449]

    fig, ax = plt.subplots(figsize=(5.5, 3.8))

    ax.plot(years, china, marker='o', markersize=4, linewidth=1.8, color='#c0392b', label='China', zorder=4)
    ax.plot(years, us, marker='s', markersize=4, linewidth=1.8, color='#2166ac', label='United States', zorder=4)

    # Endpoint labels
    ax.annotate(f'{china[-1]:,}', xy=(2025, china[-1]),
                xytext=(2025.3, china[-1] + 3000),
                fontsize=8, fontweight='bold', color='#c0392b', va='bottom')
    ax.annotate(f'{us[-1]:,}', xy=(2025, us[-1]),
                xytext=(2025.3, us[-1] - 3000),
                fontsize=8, fontweight='bold', color='#2166ac', va='top')

    ax.grid(axis='y', alpha=0.12, linewidth=0.4, color='#999999')
    ax.set_axisbelow(True)

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:,.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=9, loc='upper left')
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_china_vs_us.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 7 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 8: LLM Papers — China vs United States
# ══════════════════════════════════════════════════════════════════════════
def chart8():
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    china = [568, 831, 1010, 2270, 6218, 15008]
    us =    [1342, 1491, 1574, 4068, 8014, 14735]

    x = np.arange(len(years))
    width = 0.35

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bars_cn = ax.bar(x - width/2, china, width, label='China', color='#c0392b', edgecolor='white')
    bars_us = ax.bar(x + width/2, us, width, label='United States', color='#2166ac', edgecolor='white')


    # Value labels on bars — all centered on top
    for bar, val in zip(bars_cn, china):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{val:,}', ha='center', va='bottom', fontsize=7, color='#c0392b', fontweight='bold')
    for bar, val in zip(bars_us, us):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{val:,}', ha='center', va='bottom', fontsize=7, color='#2166ac', fontweight='bold')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years])
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=9)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_llm_china_us.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 8 saved")

# ══════════════════════════════════════════════════════════════════════════
# Chart 9: Gartner-style Hype Cycle
# ══════════════════════════════════════════════════════════════════════════
def chart9():
    """
    Gartner-style hype cycle curve with methods placed along the lifecycle
    based on their growth trajectories in the corpus data.
    """
    # Define control points for a smooth hype cycle shape
    cx = np.array([0.0, 0.8, 1.6, 2.4, 3.0, 3.5, 4.2, 5.0, 5.8, 6.5, 7.5, 8.5, 9.5, 10.0])
    cy = np.array([0.0, 0.08, 0.25, 0.65, 1.0, 0.82, 0.40, 0.32, 0.38, 0.48, 0.58, 0.64, 0.68, 0.70])

    # Cubic Hermite interpolation for perfectly smooth curve
    h = np.diff(cx)
    delta = np.diff(cy) / h
    m = np.zeros_like(cy)
    m[0] = delta[0]
    m[-1] = delta[-1]
    for i in range(1, len(cx) - 1):
        if delta[i-1] * delta[i] > 0:
            m[i] = (delta[i-1] + delta[i]) / 2
        else:
            m[i] = 0
    # Override slopes at key points for artistic smoothness
    m[4] = 0.0    # peak: flat
    m[7] = 0.0    # trough: flat

    t = np.linspace(cx[0], cx[-1], 800)
    y = np.zeros_like(t)
    for j in range(len(t)):
        idx = min(np.searchsorted(cx, t[j], side='right') - 1, len(cx) - 2)
        idx = max(idx, 0)
        s = (t[j] - cx[idx]) / h[idx]
        h00 = 2*s**3 - 3*s**2 + 1
        h10 = s**3 - 2*s**2 + s
        h01 = -2*s**3 + 3*s**2
        h11 = s**3 - s**2
        y[j] = (h00 * cy[idx] + h10 * h[idx] * m[idx] +
                h01 * cy[idx+1] + h11 * h[idx] * m[idx+1])

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.plot(t, y, color='#34495e', linewidth=2.5, zorder=2)
    ax.fill_between(t, 0, y, alpha=0.04, color='#34495e')

    # Phase labels along bottom
    phases = [
        (1.0, 'Innovation\nTrigger'),
        (3.0, 'Peak of Inflated\nExpectations'),
        (4.6, 'Trough of\nDisillusionment'),
        (6.2, 'Slope of\nEnlightenment'),
        (8.5, 'Plateau of\nProductivity'),
    ]
    for px, plabel in phases:
        ax.text(px, -0.10, plabel, ha='center', va='top', fontsize=7.5,
                color='#222222', linespacing=1.1)

    # Place methods along the curve based on corpus data patterns
    # Colors encode lifecycle category:
    #   Green (#27ae60) = Foundational/mature
    #   Blue  (#2471a3) = Growth phase
    #   Red   (#c0392b) = Hype peak
    #   Gray  (#7f8c8d) = Declining
    methods = [
        (0.7, 'Agentic', '#c0392b', 0.16),
        (1.4, 'Federated\nLearning', '#2471a3', 0.18),
        (1.9, 'RAG', '#c0392b', -0.14),
        (2.5, 'LLM', '#c0392b', 0.20),
        (2.8, 'Diffusion\nModel', '#c0392b', 0.14),
        (3.2, 'Graph\nNeural', '#2471a3', -0.16),
        (4.0, 'Multimodal', '#2471a3', -0.16),
        (4.5, 'Transformer', '#2471a3', 0.28),
        (5.2, 'BERT', '#7f8c8d', -0.14),
        (5.8, 'GAN', '#7f8c8d', 0.15),
        (6.8, 'Reinforcement\nLearning', '#27ae60', 0.16),
        (7.8, 'Deep\nLearning', '#27ae60', 0.15),
        (8.5, 'CNN', '#27ae60', -0.13),
        (8.8, 'Neural\nNetwork', '#27ae60', 0.15),
        (9.5, 'Knowledge\nGraph', '#27ae60', -0.13),
    ]

    for mx, mlabel, mcolor, mdy in methods:
        my = np.interp(mx, t, y)
        ax.plot(mx, my, 'o', color=mcolor, markersize=6, zorder=5,
                markeredgecolor='white', markeredgewidth=0.8)
        ax.annotate(mlabel, xy=(mx, my), xytext=(mx, my + mdy),
                    fontsize=6.5, fontweight='bold', color=mcolor,
                    ha='center', va='bottom' if mdy > 0 else 'top',
                    linespacing=0.85,
                    arrowprops=dict(arrowstyle='-', color='#cccccc', lw=0.5),
                    zorder=6)

    ax.set_xlim(-0.3, 10.5)
    ax.set_ylim(-0.22, 1.30)
    ax.set_ylabel('Expectations', fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_hype_cycle.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 9 (Hype Cycle) saved")


# ── Run all ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    chart1()
    chart2()
    chart3()
    chart4()
    chart5()
    chart6()
    chart7()
    chart8()
    chart9()
    print("\n✅ All 9 charts generated successfully.")
