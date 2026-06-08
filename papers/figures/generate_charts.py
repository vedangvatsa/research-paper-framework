import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
import os

# ── Global style (tuned for standard paper sizing) ────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7.5,
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
    
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    colors = ['#2166ac'] * 13 + ['#92c5de']
    bars = ax.bar(years, counts, color=colors, edgecolor='white', width=0.75)
    
    ax.annotate('(Jan–Jun)', xy=(2026, counts[-1]), xytext=(2026, counts[-1] + 180000),
                ha='center', fontsize=8, color='#555555',
                arrowprops=dict(arrowstyle='->', color='#999999', lw=0.8))
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M' if x >= 1e6 else f'{x/1e3:.0f}K'))
    cleanup_axes(ax)
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
    ax.set_xticklabels([str(y) for y in years_full], rotation=45)
    fig.text(0.5, 0.95, 'Note: 2026 reflects Jan–Jun only (partial year)', ha='center', fontsize=8, fontstyle='italic', color='#666666')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=7.5)
    cleanup_axes(ax)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
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
    ax.fill_between(years, [c * 0.7 for c in counts], alpha=0.10, color='#2980b9')
    ax.fill_between(years, [c * 0.4 for c in counts], alpha=0.08, color='#2980b9')

    ax.axvline(x=2022.5, color='#c0392b', linestyle='--', linewidth=1.2, alpha=0.8)
    ax.annotate('ChatGPT\nrelease', xy=(2022.5, max(counts) * 0.85),
                xytext=(2020.0, max(counts) * 0.90),
                fontsize=8, color='#c0392b', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.0))

    ax.annotate('2026\n(Jan–Jun)', xy=(2026, counts[-1]), xytext=(2026, counts[-1] - 25000),
                fontsize=8, fontstyle='italic', color='#555555', ha='center',
                arrowprops=dict(arrowstyle='->', color='#999999', lw=0.8))

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years)
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
    ax.set_xticklabels([str(y) for y in all_years], rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=7.5)
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
                f'{count:,}', va='center', fontsize=8)

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
                f'{count:,}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax.set_ylim(1e3, 1e7)
    cleanup_axes(ax)
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

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(years, china, marker='o', markersize=4, linewidth=1.5, label='China', color='#c0392b')
    ax.plot(years, us, marker='s', markersize=4, linewidth=1.5, label='United States', color='#2166ac')

    # Annotate crossover
    ax.annotate('China overtakes US', xy=(2021, 71273), xytext=(2019.5, 95000),
                fontsize=8, color='#555555',
                arrowprops=dict(arrowstyle='->', color='#999999', lw=0.8))

    # Annotate endpoints
    ax.annotate(f'{china[-1]:,}', xy=(2025, china[-1]), xytext=(2025.2, china[-1]),
                fontsize=8, fontweight='bold', color='#c0392b', va='center')
    ax.annotate(f'{us[-1]:,}', xy=(2025, us[-1]), xytext=(2025.2, us[-1]),
                fontsize=8, fontweight='bold', color='#2166ac', va='center')

    # Annotate start points
    ax.annotate(f'{china[0]:,}', xy=(2013, china[0]), xytext=(2013, china[0] - 5000),
                fontsize=8, color='#c0392b', ha='center')
    ax.annotate(f'{us[0]:,}', xy=(2013, us[0]), xytext=(2013, us[0] + 3000),
                fontsize=8, color='#2166ac', ha='center')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:,.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=7.5)
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

    # Annotate parity
    ax.annotate('Parity reached', xy=(5, 15008), xytext=(4.2, 16000),
                fontsize=8, color='#555555',
                arrowprops=dict(arrowstyle='->', color='#999999', lw=0.8))

    # Value labels on bars
    for bar, val in zip(bars_cn, china):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{val:,}', ha='center', va='bottom', fontsize=7.5, color='#c0392b', fontweight='bold')
    for bar, val in zip(bars_us, us):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{val:,}', ha='center', va='bottom', fontsize=7.5, color='#2166ac', fontweight='bold')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years])
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=7.5)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_llm_china_us.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 8 saved")


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
    print("\n✅ All 8 charts generated successfully.")
