import pandas as pd

# Load trait data
data = pd.read_csv("trait_results.csv")

# Define mimic trait suppression thresholds
thresholds = {
    "sf": 0,
    "sm": 0,
    "pf": 30,
    "eb": 100,
    "tt": 85,
    "mc": 90,
    "pgfi": 100
}

# Calculate match frequency
heatmap_results = {}
for trait in thresholds:
    match = data[data[trait] >= thresholds[trait]]
    heatmap_results[trait] = {
        "Match %": round((len(match) / len(data)) * 100, 2),
        "Avg Value": round(data[trait].mean(), 2),
        "Stability": "High" if len(match) / len(data) > 0.75 else "Medium"
    }

# Output result
heatmap_df = pd.DataFrame(heatmap_results).T
heatmap_df.to_csv("heatmap_output.csv")
