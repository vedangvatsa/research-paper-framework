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
from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay

# Setup
PROJECT_DIR = '/Users/vedang/.gemini/antigravity/scratch/linguistic-markers-paper'
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
BG_COLOR = '#FAFAFA'
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

# ═══════════════════════════════════════════════════════════════
# FIGURE 1: Violin + Box plots for all 8 features (2x4 grid)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 1: Distribution violin plots...")

features_order = [
    'sent_len_cv', 'self_mention_density', 'mean_sent_len',
    'lexical_diversity_mtld', 'booster_density', 'hedge_density',
    'connector_density', 'first_word_connector_ratio'
]
fig, axes = plt.subplots(2, 4, figsize=(20, 9))
axes = axes.flatten()

for idx, feat in enumerate(features_order):
    ax = axes[idx]
    
    parts = ax.violinplot(
        [human[feat].dropna().values, ai[feat].dropna().values],
        positions=[0, 1],
        showmeans=False,
        showmedians=False,
        showextrema=False,
        widths=0.7
    )
    
    for i, body in enumerate(parts['bodies']):
        body.set_facecolor(HUMAN_COLOR if i == 0 else AI_COLOR)
        body.set_alpha(0.35)
        body.set_edgecolor(HUMAN_COLOR if i == 0 else AI_COLOR)
        body.set_linewidth(1.2)
    
    # Box plots on top
    bp = ax.boxplot(
        [human[feat].dropna().values, ai[feat].dropna().values],
        positions=[0, 1],
        widths=0.15,
        patch_artist=True,
        showfliers=False,
        medianprops=dict(color='white', linewidth=2),
        whiskerprops=dict(color='#6B7280', linewidth=1),
        capprops=dict(color='#6B7280', linewidth=1),
    )
    for i, patch in enumerate(bp['boxes']):
        patch.set_facecolor(HUMAN_COLOR if i == 0 else AI_COLOR)
        patch.set_alpha(0.85)
        patch.set_edgecolor('white')
        patch.set_linewidth(1)
    
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Human', 'AI'], fontsize=10)
    ax.set_title(FEATURE_LABELS[feat], fontsize=11, fontweight='bold', pad=8)
    ax.tick_params(axis='y', labelsize=9)

fig.suptitle('Distribution of Linguistic Features: Human vs. AI Abstracts',
             fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
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
ax.set_xlabel("Cohen's d (Effect Size)", fontsize=11, fontweight='bold')
ax.axvline(x=0, color='#374151', linewidth=1.2, linestyle='-')

# Threshold lines
for thresh, label_text in [(-0.8, 'Large'), (0.8, 'Large'), (-0.5, 'Medium'), (0.5, 'Medium')]:
    ax.axvline(x=thresh, color='#9CA3AF', linewidth=0.7, linestyle='--', alpha=0.6)

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

ax.set_title("Effect Sizes (Cohen's d) of Linguistic Feature Differences",
             fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig2_effect_sizes.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig2_effect_sizes.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 3: Feature importance (horizontal bar)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 3: Feature importance chart...")

imp = pd.read_csv(os.path.join(PROJECT_DIR, 'results/tables/feature_importances.csv'))
imp = imp.sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))

# Gradient-like colors from light to dark
n = len(imp)
cmap = plt.cm.Blues
norm_vals = np.linspace(0.3, 0.9, n)
bar_colors = [cmap(v) for v in norm_vals]

bars = ax.barh(
    range(n),
    imp['Importance'],
    color=bar_colors,
    edgecolor='white',
    linewidth=0.8,
    height=0.6
)

feature_names = [FEATURE_LABELS.get(f, f).replace('\n', ' ') for f in imp['Feature']]
ax.set_yticks(range(n))
ax.set_yticklabels(feature_names, fontsize=10)
ax.set_xlabel('Gini Importance', fontsize=11, fontweight='bold')

# Annotations
for i, (val, bar) in enumerate(zip(imp['Importance'], bars)):
    ax.text(val + 0.003, i, f'{val:.1%}', va='center', fontsize=9, fontweight='bold', color='#374151')

ax.set_title('Random Forest Feature Importance for Human vs. AI Classification',
             fontsize=13, fontweight='bold', pad=12)
ax.set_xlim(0, max(imp['Importance']) * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig3_feature_importance.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig3_feature_importance.png saved")


# ═══════════════════════════════════════════════════════════════
# FIGURE 4: ROC Curve (5-fold)
# ═══════════════════════════════════════════════════════════════
print("Generating Figure 4: ROC curve...")

features_to_test = [c for c in df.columns if c not in ['label', 'word_count', 'sentence_count']]
X = df[features_to_test]
y = df['label']

fig, ax = plt.subplots(figsize=(7, 7))

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
tprs = []
aucs_list = []
mean_fpr = np.linspace(0, 1, 100)

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X.iloc[train_idx], y.iloc[train_idx])
    probs = clf.predict_proba(X.iloc[val_idx])[:, 1]
    
    fpr, tpr, _ = roc_curve(y.iloc[val_idx], probs)
    roc_auc = auc(fpr, tpr)
    aucs_list.append(roc_auc)
    
    interp_tpr = np.interp(mean_fpr, fpr, tpr)
    interp_tpr[0] = 0.0
    tprs.append(interp_tpr)
    
    ax.plot(fpr, tpr, color=HUMAN_LIGHT, alpha=0.3, linewidth=1)

mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = np.mean(aucs_list)
std_auc = np.std(aucs_list)

ax.plot(mean_fpr, mean_tpr, color=HUMAN_COLOR, linewidth=2.5,
        label=f'Mean ROC (AUC = {mean_auc:.3f} ± {std_auc:.3f})')

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color=HUMAN_COLOR, alpha=0.15,
                label='± 1 std. dev.')

ax.plot([0, 1], [0, 1], linestyle='--', color='#9CA3AF', linewidth=1, label='Random Chance')
ax.set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
ax.set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
ax.set_title('ROC Curve (5-Fold Cross-Validation)', fontsize=14, fontweight='bold', pad=12)
ax.legend(loc='lower right', fontsize=10, frameon=True, framealpha=0.9)
ax.set_xlim([-0.01, 1.01])
ax.set_ylim([-0.01, 1.01])
ax.set_aspect('equal')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig4_roc_curve.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig4_roc_curve.png saved")


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

fig, ax = plt.subplots(figsize=(6, 5.5))
im = ax.imshow(cm, interpolation='nearest', cmap='Blues')

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Human', 'AI'], fontsize=12)
ax.set_yticklabels(['Human', 'AI'], fontsize=12)
ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
ax.set_ylabel('True Label', fontsize=12, fontweight='bold')

# Text annotations
thresh = cm.max() / 2.
for i in range(2):
    for j in range(2):
        ax.text(j, i, format(cm[i, j], 'd'),
                ha='center', va='center',
                fontsize=20, fontweight='bold',
                color='white' if cm[i, j] > thresh else '#374151')

ax.set_title('Confusion Matrix (80/20 Hold-Out Split)', fontsize=13, fontweight='bold', pad=12)
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
    cbar_kws={'shrink': 0.8, 'label': "Pearson's r"}
)

ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold', pad=12)
ax.tick_params(axis='both', labelsize=9)
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig6_correlation_heatmap.png'), dpi=300,
            bbox_inches='tight', facecolor=BG_COLOR)
plt.close()
print("  -> fig6_correlation_heatmap.png saved")


print("\nAll 6 figures generated successfully!")
