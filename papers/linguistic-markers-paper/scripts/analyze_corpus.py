import os
import re
import numpy as np
import pandas as pd
from datasets import load_dataset
import spacy
from scipy.stats import mannwhitneyu
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from lexicalrichness import LexicalRichness

# Setup output directories
os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)
os.makedirs("data/features", exist_ok=True)

# Load spaCy
print("Loading NLP pipeline...")
nlp = spacy.load("en_core_web_sm", disable=["ner"])

# Lexical search lists (lowercased)
HEDGES = {
    "may", "might", "possibly", "suggest", "suggests", "suggested", "suggesting",
    "appear", "appears", "appeared", "appearing", "seem", "seems", "seemed", "seeming",
    "maybe", "perhaps", "probable", "probably", "likely", "unlikely", "plausible", "plausibly",
    "tentative", "tentatively", "indicate", "indicates", "indicated", "indicating"
}

BOOSTERS = {
    "clearly", "obviously", "demonstrate", "demonstrates", "demonstrated", "demonstrating",
    "prove", "proves", "proved", "proving", "establish", "establishes", "established",
    "establishing", "definitely", "show", "shows", "showed", "showing", "certainly", "certain",
    "undeniably", "undeniable", "always", "never", "evident", "evidently", "indeed"
}

SELF_MENTIONS = {"i", "we", "our", "my", "us", "me", "ours"}

CONNECTORS = {
    "however", "nevertheless", "nonetheless", "conversely", "instead", "contrastingly", # Contrastive
    "therefore", "consequently", "thus", "hence", "accordingly", "as a result", # Causal
    "furthermore", "moreover", "in addition", "additionally", "besides", "also" # Additive
}

def calculate_mtld(text):
    try:
        lr = LexicalRichness(text)
        # Handle empty/too short text
        if len(text.split()) < 10:
            return 0.0
        return lr.mtld(threshold=0.72)
    except Exception:
        return 0.0

def extract_features(text):
    doc = nlp(text)
    words = [t.text.lower() for t in doc if not t.is_punct and not t.is_space]
    word_count = len(words)
    
    if word_count == 0:
        return {
            "word_count": 0, "sentence_count": 0, "mean_sent_len": 0, "sent_len_cv": 0,
            "hedge_density": 0, "booster_density": 0, "self_mention_density": 0, "connector_density": 0,
            "lexical_diversity_mtld": 0, "first_word_connector_ratio": 0
        }
    
    # Sentence processing
    sentences = list(doc.sents)
    sent_lengths = [len([t for t in s if not t.is_punct and not t.is_space]) for s in sentences]
    sent_lengths = [l for l in sent_lengths if l > 0]
    
    mean_sent_len = np.mean(sent_lengths) if sent_lengths else 0
    sent_len_sd = np.std(sent_lengths) if sent_lengths else 0
    sent_len_cv = (sent_len_sd / mean_sent_len) if mean_sent_len > 0 else 0
    
    # Feature counts
    hedge_count = sum(1 for w in words if w in HEDGES)
    booster_count = sum(1 for w in words if w in BOOSTERS)
    self_mention_count = sum(1 for w in words if w in SELF_MENTIONS)
    connector_count = sum(1 for w in words if w in CONNECTORS)
    
    # Sentence opener check (how many sentences start with a connector)
    opener_connector_count = 0
    for s in sentences:
        first_word = next((t.text.lower() for t in s if not t.is_punct and not t.is_space), None)
        if first_word and first_word in CONNECTORS:
            opener_connector_count += 1
            
    first_word_connector_ratio = opener_connector_count / len(sentences) if sentences else 0
    
    # Lexical Diversity
    mtld = calculate_mtld(text)
    
    return {
        "word_count": word_count,
        "sentence_count": len(sentences),
        "mean_sent_len": mean_sent_len,
        "sent_len_cv": sent_len_cv,
        "hedge_density": (hedge_count / word_count) * 1000,          # count per 1,000 words
        "booster_density": (booster_count / word_count) * 1000,      # count per 1,000 words
        "self_mention_density": (self_mention_count / word_count) * 1000, # count per 1,000 words
        "connector_density": (connector_count / word_count) * 1000,  # count per 1,000 words
        "lexical_diversity_mtld": mtld,
        "first_word_connector_ratio": first_word_connector_ratio
    }

def calculate_cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.var(x, ddof=1) + (ny-1)*np.var(y, ddof=1)) / dof)

def run_analysis(sample_size=10000):
    csv_path = "data/metadata/synthetic_abstracts_multi_api.csv"
    print(f"Loading custom dataset from {csv_path}...")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist.")
        return
    df_raw = pd.read_csv(csv_path)
    
    # ── Data Cleaning ──
    print("Cleaning corpus...")
    # Drop rows with empty or too-short abstracts in either group
    df_clean = df_raw.dropna(subset=["human_abstract", "ai_abstract"])
    df_clean = df_clean[
        (df_clean["human_abstract"].str.strip().str.len() > 100) & 
        (df_clean["ai_abstract"].str.strip().str.len() > 100)
    ]
    df_clean = df_clean.drop_duplicates(subset=["human_abstract"])
    
    print(f"Cleaned paired corpus size: {df_clean.shape[0]} unique rows.")
    
    # Stratified Sampling to match user request
    half_sample = min(len(df_clean), sample_size // 2)
    df_sampled_pairs = df_clean.head(half_sample)
    
    human_records = pd.DataFrame({
        "abstract": df_sampled_pairs["human_abstract"],
        "label": 0
    })
    ai_records = pd.DataFrame({
        "abstract": df_sampled_pairs["ai_abstract"],
        "label": 1
    })
    
    df_sampled = pd.concat([human_records, ai_records], ignore_index=True)
    print(f"Sampled {df_sampled.shape[0]} documents ({half_sample} human, {half_sample} AI) for analysis.")
    
    # Feature Extraction
    print("Extracting features (this will take about 1-2 minutes for 10k texts)...")
    features_list = []
    for idx, row in df_sampled.iterrows():
        if idx % 1000 == 0 and idx > 0:
            print(f"  Processed {idx} / {sample_size}...")
        feats = extract_features(row["abstract"])
        feats["label"] = row["label"]
        features_list.append(feats)
        
    df_features = pd.DataFrame(features_list)
    df_features.to_csv("data/features/corpus_features.csv", index=False)
    print("Features extracted and saved to data/features/corpus_features.csv")
    
    # ── Statistical Analysis ──
    print("\nRunning statistical analysis...")
    human_feats = df_features[df_features["label"] == 0]
    ai_feats = df_features[df_features["label"] == 1]
    
    stats_rows = []
    features_to_test = [c for c in df_features.columns if c != "label" and c != "word_count" and c != "sentence_count"]
    
    for f in features_to_test:
        u_stat, p_val = mannwhitneyu(human_feats[f], ai_feats[f], alternative="two-sided")
        d_val = calculate_cohens_d(ai_feats[f], human_feats[f]) # AI mean - Human mean
        
        stats_rows.append({
            "Feature": f,
            "Human Mean": f"{np.mean(human_feats[f]):.4f}",
            "Human SD": f"{np.std(human_feats[f]):.4f}",
            "AI Mean": f"{np.mean(ai_feats[f]):.4f}",
            "AI SD": f"{np.std(ai_feats[f]):.4f}",
            "p-value": f"{p_val:.4g}",
            "Cohen's d": f"{d_val:.4f}"
        })
        
    df_stats = pd.DataFrame(stats_rows)
    df_stats.to_csv("results/tables/statistical_comparisons.csv", index=False)
    print("Statistical summary saved to results/tables/statistical_comparisons.csv")
    print(df_stats.to_string(index=False))
    
    # ── Visualizations ──
    print("\nGenerating visualizations...")
    sns.set_theme(style="whitegrid")
    
    # 1. Violin plots of selected features
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plot_feats = ["lexical_diversity_mtld", "sent_len_cv", "hedge_density", "connector_density"]
    plot_titles = ["Lexical Diversity (MTLD)", "Sentence Length Variation (CV)", "Hedge Density (per 1k words)", "Discourse Connector Density (per 1k words)"]
    
    for i, (feat, title) in enumerate(zip(plot_feats, plot_titles)):
        ax = axes[i // 2, i % 2]
        sns.violinplot(data=df_features, x="label", y=feat, hue="label", palette=["#1f77b4", "#ff7f0e"], legend=False, ax=ax)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Authorship (0 = Human, 1 = AI)")
        ax.set_ylabel(feat)
        
    plt.tight_layout()
    plt.savefig("results/figures/linguistic_markers_violin.png", dpi=300)
    plt.close()
    
    # ── Classification ──
    print("\nTraining classifier with 5-fold cross-validation...")
    X = df_features[features_to_test]
    y = df_features["label"]
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    accs, precs, recs, f1s, aucs = [], [], [], [], []
    
    importances = np.zeros(X.shape[1])
    
    for train_idx, val_idx in skf.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        clf.fit(X_train, y_train)
        
        preds = clf.predict(X_val)
        probs = clf.predict_proba(X_val)[:, 1]
        
        accs.append(accuracy_score(y_val, preds))
        precs.append(precision_score(y_val, preds))
        recs.append(recall_score(y_val, preds))
        f1s.append(f1_score(y_val, preds))
        aucs.append(roc_auc_score(y_val, probs))
        
        importances += clf.feature_importances_ / 5
        
    print("\nClassification Evaluation Metrics (5-Fold CV):")
    print(f"  Accuracy:  {np.mean(accs):.4f} ± {np.std(accs):.4f}")
    print(f"  Precision: {np.mean(precs):.4f} ± {np.std(precs):.4f}")
    print(f"  Recall:    {np.mean(recs):.4f} ± {np.std(recs):.4f}")
    print(f"  F1 Score:  {np.mean(f1s):.4f} ± {np.std(f1s):.4f}")
    print(f"  AUC-ROC:   {np.mean(aucs):.4f} ± {np.std(aucs):.4f}")
    
    # Save classification metrics to a file
    with open("results/tables/classification_metrics.txt", "w") as f:
        f.write("Classification Evaluation Metrics (5-Fold CV):\n")
        f.write(f"Accuracy:  {np.mean(accs):.4f} ± {np.std(accs):.4f}\n")
        f.write(f"Precision: {np.mean(precs):.4f} ± {np.std(precs):.4f}\n")
        f.write(f"Recall:    {np.mean(recs):.4f} ± {np.std(recs):.4f}\n")
        f.write(f"F1 Score:  {np.mean(f1s):.4f} ± {np.std(f1s):.4f}\n")
        f.write(f"AUC-ROC:   {np.mean(aucs):.4f} ± {np.std(aucs):.4f}\n")
        
    # Plot feature importances
    df_imp = pd.DataFrame({
        "Feature": features_to_test,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)
    
    df_imp.to_csv("results/tables/feature_importances.csv", index=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_imp, x="Importance", y="Feature", palette="viridis")
    plt.title("Feature Importance in Distinguishing Human vs. AI Academic Text", fontsize=14, fontweight="bold")
    plt.xlabel("Random Forest Gini Importance")
    plt.tight_layout()
    plt.savefig("results/figures/feature_importances.png", dpi=300)
    plt.close()
    
    print("\nAll pipeline tasks completed successfully! Results are saved in 'results/' and 'data/'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_size", type=int, default=10000, help="Total sample size (human + AI)")
    args = parser.parse_args()
    run_analysis(sample_size=args.sample_size)
