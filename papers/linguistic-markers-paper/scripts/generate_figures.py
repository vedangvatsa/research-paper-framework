#!/usr/bin/env python3
"""Generate all publication-quality figures for the linguistic markers paper."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

# Setup
PROJECT_DIR = '/Users/vedang/ZCodeProject/research-paper-framework/papers/linguistic-markers-paper'
FEATURES_CSV = os.path.join(PROJECT_DIR, 'data/features/corpus_features.csv')
FIG_DIR = os.path.join(PROJECT_DIR, 'results/figures')
os.makedirs(FIG_DIR, exist_ok=True)

# Load data
df = pd.read_csv(FEATURES_CSV)
human = df[df['label'] == 0]
ai = df[df['label'] == 1]
print(f"Loaded {len(df)} rows ({len(human)} human, {len(ai)} AI)")

# ═══════════════════════════════════════════════════════════════
# Palette and style
# ═══════════════════════════════════════════════════════════════
HUMAN_COLOR = '#2563EB'  # blue-600
AI_COLOR = '#F97316'     # orange-500
HUMAN_LIGHT = '#93C5FD'  # blue-300
AI_LIGHT = '#FDBA74'     # orange-300
BG_COLOR = '#FFFFFF'
GRID_COLOR = '#E5E7EB'

sns.set_theme(
    style='whitegrid',
    rc={
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': '#FFFFFF',
        'axes.grid': True,
        'grid.color': GRID_COLOR,
        'grid.linewidth': 0.5,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
        'axes.spines.top': False,
        'axes.spines.right': False,
    }
)

FEATURE_LABELS = {
    'sent_len_cv': 'Sentence Length\nVariation (CV)',
    'self_mention_density': 'Self-Mention\nDensity',
    'mean_sent_len': 'Mean Sentence\nLength',
    'lexical_diversity_mtld': 'Lexical Diversity\n(MTLD)',
    'connector_density': 'Connector\nDensity',
    'booster_density': 'Booster\nDensity',
    'hedge_density': 'Hedge\nDensity',
    'first_word_connector_ratio': 'Sentence-Opener\nConnector Ratio',
}

FEATURE_XLABELS = {
    'sent_len_cv': 'CV Score (0 = uniform, 1 = high variation)',
    'self_mention_density': 'First-person pronouns per 1,000 words',
    'mean_sent_len': 'Words per sentence',
    'lexical_diversity_mtld': 'MTLD Score (higher = more diverse vocabulary)',
    'connector_density': 'Transition words per 1,000 words',
    'booster_density': 'Booster words per 1,000 words',
    'hedge_density': 'Hedge words per 1,000 words',
    'first_word_connector_ratio': 'Ratio of sentences starting with a transition (0 to 1)',
}

# ═══════════════════════════════════════════════════════════════
# FIGURE 1: Ridgeline density plots for all 8 features
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 1: Ridgeline density plots...")

from scipy.stats import gaussian_kde

features_order = [
    'lexical_diversity_mtld', 'sent_len_cv', 'self_mention_density',
    'first_word_connector_ratio', 'connector_density', 'hedge_density',
    'mean_sent_len', 'booster_density'
]

fig, axes = plt.subplots(8, 1, figsize=(10, 14), sharex=False)
fig.subplots_adjust(hspace=0.45)

for idx, feat in enumerate(features_order):
    ax = axes[idx]
    
    human_vals = human[feat].dropna().values
    ai_vals = ai[feat].dropna().values
    
    x_min = min(human_vals.min(), ai_vals.min())
    x_max = np.percentile(human_vals, 99.5) if np.percentile(human_vals, 99.5) > np.percentile(ai_vals, 99.5) else np.percentile(ai_vals, 99.5)
    x_min = max(x_min, np.percentile(human_vals, 0.5))
    
    x_grid = np.linspace(x_min, x_max, 300)
    
    for vals, color, label in [(human_vals, HUMAN_COLOR, 'Human'), (ai_vals, AI_COLOR, 'AI')]:
        try:
            kde = gaussian_kde(vals, bw_method=0.3)
            density = kde(x_grid)
            density = density / density.max()
            ax.fill_between(x_grid, density, alpha=0.3, color=color, linewidth=0)
            ax.plot(x_grid, density, color=color, linewidth=1.5, label=label)
        except Exception:
            pass
    
    ax.set_yticks([])
    ax.set_ylabel(FEATURE_LABELS[feat].replace('\n', ' '), fontsize=9, fontweight='bold',
                  rotation=0, ha='right', va='center', labelpad=10)
    ax.set_xlim(x_min, x_max)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', labelsize=8)
    ax.set_xlabel(FEATURE_XLABELS[feat], fontsize=8)
    
    if idx == 0:
        ax.legend(fontsize=9, loc='upper right', framealpha=0.7)

fig.suptitle('Distribution of Linguistic Features: Human vs. AI Abstracts',
             fontsize=13, fontweight='bold', y=0.98)
plt.savefig(os.path.join(FIG_DIR, 'fig1_distributions.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig1_distributions.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 2: Cohen's d effect size bar chart (horizontal)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 2: Effect size chart...")

stats = pd.read_csv(os.path.join(PROJECT_DIR, 'results/tables/statistical_comparisons.csv'))
stats["Cohen's d"] = stats["Cohen's d"].astype(float)
stats['abs_d'] = stats["Cohen's d"].abs()
stats = stats.sort_values('abs_d', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))

colors = [AI_COLOR if d > 0 else HUMAN_COLOR for d in stats["Cohen's d"]]
bars = ax.barh(
    range(len(stats)),
    stats["Cohen's d"],
    color=colors,
    edgecolor='white',
    linewidth=0.8,
    height=0.6,
    alpha=0.85
)

# Labels
feature_names = [FEATURE_LABELS.get(f, f).replace('\n', ' ') for f in stats['Feature']]
ax.set_yticks(range(len(stats)))
ax.set_yticklabels(feature_names, fontsize=10)
ax.set_xlabel('How different AI and Human distributions are\n(negative = higher in human text, positive = higher in AI text)', fontsize=10, fontweight='bold')
ax.axvline(x=0, color='#374151', linewidth=1.2, linestyle='-')

# Threshold lines with plain labels
for thresh, label_text in [(-0.8, 'Large'), (0.8, 'Large'), (-0.5, 'Medium'), (0.5, 'Medium')]:
    ax.axvline(x=thresh, color='#9CA3AF', linewidth=0.7, linestyle='--', alpha=0.6)
ax.text(0.52, len(stats) - 0.3, 'medium\ndifference', fontsize=7, color='#9CA3AF', va='top')
ax.text(0.82, len(stats) - 0.3, 'large\ndifference', fontsize=7, color='#9CA3AF', va='top')

# Annotations on bars
for i, (d_val, bar) in enumerate(zip(stats["Cohen's d"], bars)):
    x_pos = d_val + (0.03 if d_val >= 0 else -0.03)
    ha = 'left' if d_val >= 0 else 'right'
    ax.text(x_pos, i, f'{d_val:.2f}', va='center', ha=ha, fontsize=9, fontweight='bold', color='#374151')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=AI_COLOR, alpha=0.85, label='Higher in AI text'),
    Patch(facecolor=HUMAN_COLOR, alpha=0.85, label='Higher in Human text'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, frameon=True, framealpha=0.9)

ax.set_title('How Differently Each Feature Behaves in Human vs. AI Text',
             fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig2_effect_sizes.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig2_effect_sizes.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 3: Feature importance (clean ranked bars)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 3: Feature importance chart...")

imp = pd.read_csv(os.path.join(PROJECT_DIR, 'results/tables/feature_importances.csv'))
imp = imp.sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))

n = len(imp)
pct_vals = imp['Importance'].values * 100

# Two-tone: top 2 features primary color, rest secondary
bar_colors = [HUMAN_COLOR if i >= n - 2 else '#93C5FD' for i in range(n)]

bars = ax.barh(
    range(n),
    pct_vals,
    color=bar_colors,
    edgecolor='white',
    linewidth=1.0,
    height=0.6
)

feature_names = [FEATURE_LABELS.get(f, f).replace('\n', ' ') for f in imp['Feature']]
ax.set_yticks(range(n))
ax.set_yticklabels(feature_names, fontsize=12)
ax.set_xlabel('Share of the model\'s detection decisions (%)', fontsize=12, fontweight='bold')
ax.set_xlim(0, max(pct_vals) * 1.35)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax.tick_params(axis='x', labelsize=11)

# Percentage labels just outside the right end of each bar
for i, val in enumerate(pct_vals):
    ax.text(val + 0.4, i, f'{val:.1f}%', va='center', ha='left',
            fontsize=11, fontweight='bold', color='#1E3A5F')

ax.set_title(
    'Which writing features does the AI detector rely on most?\n'
    'Top two signals (dark blue): vocabulary variety and sentence length rhythm',
    fontsize=13, fontweight='bold', pad=12
)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig3_feature_importance.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig3_feature_importance.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 4: Accuracy Scorecard (replaces ROC curve)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 4: Accuracy scorecard...")

features_to_test = [c for c in df.columns if c not in ['label', 'word_count', 'sentence_count']]
X = df[features_to_test]
y = df['label']

# Run 5-fold CV to get real metric values
from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.metrics import make_scorer, f1_score, precision_score, recall_score, roc_auc_score
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf_cv = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
cv_results = cross_validate(clf_cv, X, y, cv=skf, scoring={
    'accuracy': 'accuracy',
    'precision': make_scorer(precision_score),
    'recall': make_scorer(recall_score),
    'f1': make_scorer(f1_score),
})
auc_scores = cross_val_score(clf_cv, X, y, cv=skf, scoring='roc_auc')
cv_results['test_auc'] = auc_scores

metrics = [
    {
        'value': f"{cv_results['test_accuracy'].mean()*100:.1f}%",
        'label': 'Overall Accuracy',
        'desc': 'of all 200,000 abstracts\ncorrectly classified',
        'color': HUMAN_COLOR,
    },
    {
        'value': f"{cv_results['test_precision'].mean()*100:.1f}%",
        'label': 'Precision',
        'desc': 'of texts flagged as AI\nwere actually AI',
        'color': HUMAN_COLOR,
    },
    {
        'value': f"{cv_results['test_recall'].mean()*100:.1f}%",
        'label': 'Recall',
        'desc': 'of all AI texts in the\ndataset were caught',
        'color': AI_COLOR,
    },
    {
        'value': f"{cv_results['test_f1'].mean()*100:.1f}%",
        'label': 'Balanced Score',
        'desc': 'combined precision\nand recall score',
        'color': AI_COLOR,
    },
    {
        'value': f"{cv_results['test_auc'].mean():.3f}",
        'label': 'Ranking Score (AUC-ROC)',
        'desc': 'out of 1.000 — how well the model\nranks AI above human (1.0 = perfect)',
        'color': '#6366F1',
    },
]

fig, axes = plt.subplots(1, 5, figsize=(13, 4.5))
fig.patch.set_facecolor(BG_COLOR)

for ax_i, (ax_card, m) in enumerate(zip(axes, metrics)):
    ax_card.set_facecolor('white')
    ax_card.set_xlim(0, 1)
    ax_card.set_ylim(0, 1)
    ax_card.axis('off')

    # Colored top bar
    ax_card.add_patch(plt.Rectangle((0, 0.82), 1, 0.18, color=m['color'], transform=ax_card.transAxes, clip_on=False))

    # Big metric value
    ax_card.text(0.5, 0.58, m['value'],
                 ha='center', va='center', fontsize=28, fontweight='bold',
                 color=m['color'], transform=ax_card.transAxes)

    # Label
    ax_card.text(0.5, 0.34, m['label'],
                 ha='center', va='center', fontsize=11, fontweight='bold',
                 color='#1F2937', transform=ax_card.transAxes)

    # Description
    ax_card.text(0.5, 0.12, m['desc'],
                 ha='center', va='center', fontsize=8.5, color='#6B7280',
                 transform=ax_card.transAxes, linespacing=1.5)

    # Border
    for spine in ['top', 'bottom', 'left', 'right']:
        ax_card.spines[spine].set_visible(True)
        ax_card.spines[spine].set_color('#E5E7EB')
        ax_card.spines[spine].set_linewidth(1.2)

fig.suptitle(
    'How well does the detector perform?  (5-fold cross-validation on 200,000 abstracts)',
    fontsize=13, fontweight='bold', y=1.04
)

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig(os.path.join(FIG_DIR, 'fig4_roc_curve.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig4_roc_curve.png saved (scorecard)")


# ═══════════════════════════════════════════════════════════════
# FIGURE 5: Confusion Matrix
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 5: Confusion matrix...")

# Train on full data with single split for visualization
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
clf_full = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf_full.fit(X_train, y_train)
y_pred = clf_full.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(7, 6.5))
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_aspect('equal')
ax.axis('off')

cell_colors = [
    [HUMAN_COLOR, '#DBEAFE'],
    ['#DBEAFE', AI_COLOR],
]
cell_sublabels = [
    ['Correctly identified\nas Human', 'Human text\nwrongly flagged as AI\n(False Positive)'],
    ['AI text\nmissed by detector\n(False Negative)', 'Correctly identified\nas AI'],
]

total = cm.sum()
for i in range(2):
    for j in range(2):
        x, y_pos = j, 1 - i
        rect = plt.Rectangle((x, y_pos), 1, 1, facecolor=cell_colors[i][j], edgecolor='white', linewidth=3)
        ax.add_patch(rect)
        count = cm[i, j]
        pct = count / total * 100
        text_color = 'white' if cell_colors[i][j] in [HUMAN_COLOR, AI_COLOR] else '#374151'
        ax.text(x + 0.5, y_pos + 0.62, f'{count:,}',
                ha='center', va='center', fontsize=22, fontweight='bold', color=text_color)
        ax.text(x + 0.5, y_pos + 0.42, f'({pct:.1f}% of total)',
                ha='center', va='center', fontsize=9, color=text_color, alpha=0.85)
        ax.text(x + 0.5, y_pos + 0.20, cell_sublabels[i][j],
                ha='center', va='center', fontsize=8, color=text_color,
                alpha=0.8, style='italic', linespacing=1.4)

ax.text(0.5, 2.04, 'Predicted: Human', ha='center', va='bottom', fontsize=12, fontweight='bold', color='#374151')
ax.text(1.5, 2.04, 'Predicted: AI',    ha='center', va='bottom', fontsize=12, fontweight='bold', color='#374151')
ax.text(-0.12, 1.5, 'Actually\nHuman', ha='right', va='center', fontsize=12, fontweight='bold', color='#374151', linespacing=1.4)
ax.text(-0.12, 0.5, 'Actually\nAI',    ha='right', va='center', fontsize=12, fontweight='bold', color='#374151', linespacing=1.4)

ax.text(1.0, -0.08, 'What the model predicted →', ha='center', va='top', fontsize=10, color='#6B7280', style='italic')
ax.text(-0.28, 1.0, '← What the\ntext actually is', ha='center', va='center', fontsize=10, color='#6B7280', style='italic',
        rotation=90, linespacing=1.4)

ax.set_title('Classification Results: 80/20 Hold-Out Split (40,000 abstracts)',
             fontsize=12, fontweight='bold', pad=14)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig5_confusion_matrix.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig5_confusion_matrix.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 6: Correlation heatmap of features
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 6: Feature correlation heatmap...")

corr_features = features_to_test
corr_labels = [FEATURE_LABELS.get(f, f).replace('\n', ' ') for f in corr_features]
corr_matrix = df[corr_features].corr()

fig, ax = plt.subplots(figsize=(9, 7.5))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='RdBu_r',
    center=0,
    vmin=-1, vmax=1,
    square=True,
    linewidths=0.5,
    linecolor='white',
    xticklabels=corr_labels,
    yticklabels=corr_labels,
    annot_kws={'fontsize': 9},
    ax=ax,
    cbar_kws={'shrink': 0.8, 'label': 'Correlation Score  (−1 = opposite, 0 = unrelated, +1 = identical)'}
)

ax.set_title('How Related Are the Eight Features to Each Other?\n(values near 0 = independent, values near ±1 = overlapping)', fontsize=12, fontweight='bold', pad=12)
ax.tick_params(axis='both', labelsize=9)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig6_correlation_heatmap.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig6_correlation_heatmap.png saved")


print("\nAll 6 figures generated successfully!")
