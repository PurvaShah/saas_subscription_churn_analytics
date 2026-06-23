import pandas as pd

df = pd.read_csv("output/user_plg_summary.csv")

# Identify feature columns (feature_1 ... feature_40)
feature_cols = [col for col in df.columns if col.startswith("feature_")]

results = []

for feature in feature_cols:
    # Users who used the feature
    used = df[df[feature] == 1]
    not_used = df[df[feature] == 0]

    # Conversion rates
    conv_used = used["upgraded"].mean()
    conv_not_used = not_used["upgraded"].mean()

    # Avoid division by zero
    lift = conv_used / conv_not_used if conv_not_used > 0 else None

    # Usage rate
    usage_rate = used.shape[0] / df.shape[0]

    results.append({
        "feature": feature,
        "usage_rate": usage_rate,
        "conversion_used": conv_used,
        "conversion_not_used": conv_not_used,
        "lift": lift
    })

results_df = pd.DataFrame(results)

# Sort by lift descending
results_df = results_df.sort_values(by="lift", ascending=False)

# Save results
results_df.to_csv("output/feature_conversion_analysis.csv", index=False)

print("Analysis complete! Check output/feature_conversion_analysis.csv")