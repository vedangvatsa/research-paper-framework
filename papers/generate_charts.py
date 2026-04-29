import matplotlib.pyplot as plt
import numpy as np

# 1. Market Projections Chart
labels = ['McKinsey (B2C)', 'Bain (Total)', 'Morgan Stanley']
highs = [1000, 500, 385]
lows = [0, 300, 190] # 0 just means point estimate of 1T for McKinsey up to

x = np.arange(len(labels))
width = 0.5

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(x, highs, width, label='High Estimate', color='#214a79')
ax.bar(x, lows, width, label='Low Estimate', color='#a3c1e0')

ax.set_ylabel('USD Billions')
ax.set_title('Figure 1: U.S. Agentic Commerce Market Size by 2030')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.tight_layout()
plt.savefig('market_projections.png', dpi=300)
plt.close()

# 2. Consumer Trust Chart
labels = ['Q4 2025', 'Q1 2026']
comfortable = [70, 45]
uncomfortable = [30, 55]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(6, 4))
rects1 = ax.bar(x - width/2, comfortable, width, label='Comfortable', color='#4caf50')
rects2 = ax.bar(x + width/2, uncomfortable, width, label='Not Comfortable', color='#f44336')

ax.set_ylabel('Percentage of Consumers (%)')
ax.set_title('Figure 2: Consumer Comfort with Autonomous Purchases')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig('consumer_trust.png', dpi=300)
plt.close()

# 3. Selection Bias Chart
labels = ['Overall Pick', 'Complete Metadata', '4.5+ Stars', 'Sponsored Label', 'Missing Attributes']
values = [35, 25, 20, -15, -30]
colors = ['#4caf50' if v > 0 else '#f44336' for v in values]

y_pos = np.arange(len(labels))

fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(y_pos, values, color=colors)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Change in Selection Probability (%)')
ax.set_title('Figure 3: AI Agent Selection Bias (ACES Research)')

plt.tight_layout()
plt.savefig('selection_bias.png', dpi=300)
plt.close()
