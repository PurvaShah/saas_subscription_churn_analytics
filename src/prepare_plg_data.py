import pandas as pd

# Load all CSVs
accounts = pd.read_csv("data_raw/accounts.csv")
subscriptions = pd.read_csv("data_raw/subscriptions.csv")
feature_usage = pd.read_csv("data_raw/feature_usage.csv")
churn = pd.read_csv("data_raw/churn_events.csv")
tickets = pd.read_csv("data_raw/support_tickets.csv")

# -----------------------------
# 1. Prepare feature usage flags
# -----------------------------
# Join feature_usage with subscriptions to get account_id
feature_usage_with_account = feature_usage.merge(subscriptions[["subscription_id", "account_id"]], on="subscription_id")

feature_pivot = (
    feature_usage_with_account
    .pivot_table(
        index="account_id",
        columns="feature_name",
        values="usage_count",
        aggfunc="sum"
    )
    .fillna(0)
)

# Rename columns to binary flags
feature_pivot = feature_pivot.rename(columns={
    "invite_teammate": "did_invite_teammate",
    "create_project": "did_create_project",
    "connect_integration": "did_connect_integration",
    "export_report": "did_export_report"
}, errors="ignore")  # Ignore if columns don't exist

# Convert counts → binary 0/1
for col in feature_pivot.columns:
    feature_pivot[col] = (feature_pivot[col] > 0).astype(int)

# Add total events
feature_pivot["total_events"] = feature_usage_with_account.groupby("account_id")["usage_count"].sum()

# -----------------------------
# 2. Prepare subscription labels
# -----------------------------
subscriptions["upgraded"] = subscriptions["upgrade_flag"].astype(int)

subscription_summary = subscriptions.groupby("account_id")["upgraded"].max()

# -----------------------------
# 3. Prepare churn labels
# -----------------------------
churn["churned"] = churn["churn_date"].notna().astype(int)
churn_summary = churn.groupby("account_id")["churned"].max()

# -----------------------------
# 4. Prepare support ticket summary
# -----------------------------
ticket_summary = tickets.groupby("account_id").agg(
    total_support_tickets=("ticket_id", "count"),
    avg_resolution_time=("resolution_time_hours", "mean")
)

# -----------------------------
# 5. Merge everything into one table
# -----------------------------
summary = (
    accounts.set_index("account_id")
    .join(feature_pivot, how="left")
    .join(subscription_summary, how="left")
    .join(churn_summary, how="left")
    .join(ticket_summary, how="left")
)

# Fill missing values
summary = summary.fillna({
    "did_invite_teammate": 0,
    "did_create_project": 0,
    "did_connect_integration": 0,
    "did_export_report": 0,
    "total_events": 0,
    "upgraded": 0,
    "churned": 0,
    "total_support_tickets": 0
})

# -----------------------------
# 6. Save final user-level summary
# -----------------------------
summary.to_csv("output/user_plg_summary.csv")
print("user_plg_summary.csv created!")
