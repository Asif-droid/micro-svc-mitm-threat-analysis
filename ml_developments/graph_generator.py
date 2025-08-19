import json
# import matplotlib.pyplot as plt

# # Reload the stats JSON file after reset
with open("stat.json", "r") as f:
    stats = json.load(f)

# # Dataset keys
# datasets = list(stats.keys())
# features = ["p50", "p90", "p99", "IQR", "MAD", "TailIndex", "Fano", "Population std:", "Sample std:"]

# # Collect feature values
# data = {f: [stats[d][f] for d in datasets] for f in features}

# # Plot
# num_features = len(features)
# fig, axes = plt.subplots(nrows=(num_features + 2)//3, ncols=3, figsize=(18, 12))
# axes = axes.flatten()

# for i, feature in enumerate(features[0:1]):
#     ax = axes[i]
#     ax.bar(datasets, data[feature])
#     ax.set_title(feature)
#     ax.tick_params(axis='x', rotation=45)
#     ax.grid(True, linestyle="--", alpha=0.5)

# # Hide unused subplots if any
# for j in range(i+1, len(axes)):
#     fig.delaxes(axes[j])

# plt.tight_layout()
# plt.show()


import matplotlib.pyplot as plt

# Choose one feature to visualize
feature = "Sample std:"

# Extract values
values = [stats[d][feature] for d in stats.keys()]
labels = list(stats.keys())

# Plot
plt.figure(figsize=(10, 6))
plt.bar(labels, values, color="skyblue")
plt.title(f"Comparison of {feature} across datasets")
plt.ylabel(feature)
plt.xticks(rotation=45, ha="right")
plt.grid(True, axis="y", linestyle="--", alpha=0.7)
plt.show()


