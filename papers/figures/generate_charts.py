import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Global style ──────────────────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

SAVE_DIR = "/Users/vedang/.gemini/antigravity/scratch/research-paper-framework/papers/figures"

def cleanup_axes(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ══════════════════════════════════════════════════════════════════════════
# Chart 1: Publication Volume
# ══════════════════════════════════════════════════════════════════════════
def chart1():
    years = list(range(2013, 2027))
    counts = [73894, 80456, 94127, 119483, 171025, 259975, 350756, 430576,
              500389, 532506, 619297, 704048, 803988, 455728]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    colors = ['#2166ac'] * 13 + ['#92c5de']
    bars = ax.bar(years, counts, color=colors, edgecolor='white', width=0.75)
    
    ax.annotate('(Jan–Jun)', xy=(2026, 455728), xytext=(2026, 455728 + 30000),
                ha='center', fontsize=9, fontstyle='italic', color='#555555')
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Total AI Research Publications by Year (2013–2026)', fontsize=14, fontweight='bold')
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
    years_full = list(range(2013, 2027))
    neural = [23395, 24339, 25612, 31000, 42023, 61555, 83428, 102938,
              124016, 134741, 154256, 175688, 207140, 332481]
    deep =   [4120, 4967, 6836, 9737, 16844, 29328, 46622, 65944,
              86254, 102536, 128200, 157947, 216713, 104022]
    rl =     [1784, 1963, 1970, 2366, 3552, 5740, 8916, 12179,
              15363, 17604, 22553, 28688, 47498, 30922]
    
    years_trans = list(range(2017, 2027))
    transformer = [7201, 7914, 9239, 11497, 16450, 23726, 36452, 49951, 78135, 48158]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years_full, neural, marker='o', markersize=5, linewidth=2, label='Neural Network', color='#2166ac')
    ax.plot(years_full, deep,   marker='s', markersize=5, linewidth=2, label='Deep Learning',  color='#d6604d')
    ax.plot(years_full, rl,     marker='^', markersize=5, linewidth=2, label='Reinforcement Learning', color='#4daf4a')
    ax.plot(years_trans, transformer, marker='D', markersize=5, linewidth=2, label='Transformer', color='#ff7f00', linestyle='--')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Established AI Method Trajectories (2013–2026)', fontsize=14, fontweight='bold')
    ax.set_xticks(years_full)
    ax.set_xticklabels([str(y) for y in years_full], rotation=45)
    fig.text(0.5, 0.93, 'Note: 2026 reflects Jan–Jun only (partial year)', ha='center', fontsize=9, fontstyle='italic', color='#666666')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=10)
    cleanup_axes(ax)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(f'{SAVE_DIR}/fig_established_methods.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 2 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 3: LLM Explosion
# ══════════════════════════════════════════════════════════════════════════
def chart3():
    years = list(range(2018, 2027))
    counts = [3248, 4131, 5243, 6583, 7931, 21612, 49970, 96984, 84957]

    fig, ax = plt.subplots(figsize=(10, 6))

    # gradient-like fill: stack several alpha layers
    ax.plot(years, counts, marker='o', markersize=6, linewidth=2.5, color='#1a5276', zorder=5)
    ax.fill_between(years, counts, alpha=0.15, color='#2980b9')
    ax.fill_between(years, [c * 0.7 for c in counts], alpha=0.10, color='#2980b9')
    ax.fill_between(years, [c * 0.4 for c in counts], alpha=0.08, color='#2980b9')

    ax.axvline(x=2022.5, color='#c0392b', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.annotate('ChatGPT\nrelease', xy=(2022.5, max(counts) * 0.85),
                xytext=(2021, max(counts) * 0.92),
                fontsize=10, color='#c0392b', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.5))

    # 2026 partial annotation
    ax.annotate('2026\n(Jan–Jun)', xy=(2026, 84957), xytext=(2025.2, 92000),
                fontsize=9, fontstyle='italic', color='#555555',
                arrowprops=dict(arrowstyle='->', color='#999999', lw=1))

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Large Language Model Papers by Year (2018–2026)', fontsize=14, fontweight='bold')
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
    years_diff = list(range(2019, 2027))
    diffusion = [18640, 20028, 20657, 20762, 27128, 35208, 49862, 34797]

    years_fed = list(range(2017, 2027))
    federated = [46, 127, 442, 1628, 3427, 5245, 8174, 11319, 18519, 10205]

    years_gnn = list(range(2017, 2027))
    gnn = [966, 1561, 2826, 4808, 7224, 9264, 12286, 15505, 21873, 12813]

    years_kg = list(range(2013, 2027))
    knowledge = [1700, 1973, 2118, 2229, 2660, 3253, 4207, 5798,
                 7315, 8272, 10579, 11907, 16519, 11704]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years_diff, diffusion, marker='o', markersize=5, linewidth=2, label='Diffusion Model', color='#e41a1c')
    ax.plot(years_fed, federated,  marker='s', markersize=5, linewidth=2, label='Federated Learning', color='#377eb8')
    ax.plot(years_gnn, gnn,        marker='^', markersize=5, linewidth=2, label='Graph Neural Network', color='#4daf4a')
    ax.plot(years_kg, knowledge,   marker='D', markersize=5, linewidth=2, label='Knowledge Graph', color='#984ea3')

    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Publications')
    ax.set_title('Rising AI Methods (2013–2026)', fontsize=14, fontweight='bold')
    all_years = sorted(set(years_diff + years_fed + years_gnn + years_kg))
    ax.set_xticks(all_years)
    ax.set_xticklabels([str(y) for y in all_years], rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    ax.legend(frameon=True, fancybox=True, shadow=False, fontsize=10)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_rising_methods.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 4 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 5: Top 15 Countries
# ══════════════════════════════════════════════════════════════════════════
def chart5():
    countries = ['China', 'United States', 'India', 'United Kingdom', 'Germany',
                 'Japan', 'South Korea', 'Canada', 'France', 'Italy',
                 'Australia', 'Spain', 'Brazil', 'Indonesia', 'Iran']
    counts = [964825, 834541, 443780, 227403, 171048,
              163449, 119459, 116937, 114024, 100764,
              92614, 80694, 71720, 65993, 60690]

    # Reverse for horizontal bar (top at top)
    countries = countries[::-1]
    counts = counts[::-1]

    # Sequential blue palette
    cmap = plt.cm.Blues
    norm_vals = np.linspace(0.3, 0.9, len(countries))
    colors = [cmap(v) for v in norm_vals]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(countries, counts, color=colors, edgecolor='white', height=0.7)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 8000, bar.get_y() + bar.get_height() / 2,
                f'{count:,}', va='center', fontsize=9)

    ax.set_xlabel('Number of Publications')
    ax.set_title('Top 15 Countries by AI Research Output (2013–2026)', fontsize=14, fontweight='bold')
    ax.set_xlim(0, max(counts) * 1.15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e3:.0f}K'))
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_countries.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 5 saved")


# ══════════════════════════════════════════════════════════════════════════
# Chart 6: Citation Distribution
# ══════════════════════════════════════════════════════════════════════════
def chart6():
    categories = ['0', '1–10', '11–50', '51–100', '101–500', '501–1000', '1000+']
    counts = [2445876, 1700854, 648139, 122722, 78688, 5029, 2475]

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.bar(categories, counts, color='#2166ac', edgecolor='white', width=0.65)

    ax.set_yscale('log')
    ax.set_xlabel('Citation Count')
    ax.set_ylabel('Number of Papers (log scale)')
    ax.set_title('Citation Distribution of AI Papers (2013–2026)', fontsize=14, fontweight='bold')

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.15,
                f'{count:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylim(1e3, 1e7)
    cleanup_axes(ax)
    plt.tight_layout()
    fig.savefig(f'{SAVE_DIR}/fig_citation_dist.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("✓ Chart 6 saved")


# ── Run all ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    chart1()
    chart2()
    chart3()
    chart4()
    chart5()
    chart6()
    print("\n✅ All 6 charts generated successfully.")
