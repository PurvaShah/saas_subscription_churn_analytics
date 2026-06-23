# Product-Led Growth (PLG) Analytics

This project analyzes user behavior, feature adoption, and upgrade patterns for a SaaS product using a Product-Led Growth (PLG) approach.  
It includes data preparation, feature engineering, and a Tableau dashboard built on top of clean user-level and feature-level datasets.

## What’s Included
- **Data Preparation (Python):**  
  Merges accounts, subscriptions, feature usage, churn events, and support tickets into a unified user-level dataset.
- **Feature Engineering:**  
  Creates binary feature usage flags, total events, upgrade labels, churn labels, and support ticket summaries.
- **Final Datasets:**  
  - `user_plg_summary.csv`  
- **Tableau Dashboard:**  
  Visualizes funnels, feature adoption, conversion drivers, and the power-user effect.

## Files & Structure
- `/data_raw` — Raw input CSVs  
- `/output` — Final cleaned datasets  
- `/src` — Python data prep script  
- `/tableau` — PLG dashboard (TWBX)  
- `/notebooks` — Kaggle notebook version  

## Key Insights
- Strong upgrade rate (~60%) from trial to paid users.  
- Feature usage strongly correlates with conversion.  
- Power users (15+ features) convert at higher rates.  
- Several low-adoption features show high conversion potential.

## Kaggle Version
A Kaggle notebook and dataset version of this project is also available.



# Source - RavenStack — Synthetic SaaS Dataset (Multi-table)

A small, fully synthetic SaaS dataset designed for learning and analytics projects. It includes account, subscription, feature-usage, support ticket, and churn tables in CSV format.

**Author:** River @ Rivalytics 

**Credit Requirement:** You may use or remix this dataset for educational or portfolio purposes, but please credit the original author.  

**Blog:** [Building a Dataset Generator App Journey](https://rivalytics.medium.com)  

**License:** MIT-like (fully synthetic, no PII)  

**Refresh Interval:** Monthly  

**Complexity:** Capstone-level (multi-table, event-driven, time-sensitive)  

**Data Format:** CSV  

**Row Volume:**

- accounts – 500

- subscriptions – 5,000

- feature_usage – 25,000

- support_tickets – 2,000


## Quick start

1. Inspect the raw data files in the `data_raw/` folder.
2. Run the preparation script (optional):

```bash
python src/prepare_plg_data.py
```

3. Run the analysis script to generate summary outputs:

```bash
python src/analyze_features.py
```

Notes:
- These scripts use standard Python data libraries (pandas, numpy). If you create a virtual environment, install required packages before running.

## Tables and relationships

- `accounts` (PK: account_id)
- `subscriptions` (FK → accounts.account_id)
- `feature_usage` (FK → subscriptions.subscription_id)
- `support_tickets` (FK → accounts.account_id)
- `churn_events` (FK → accounts.account_id)

All foreign-key links are referentially complete in the supplied data.

## Schemas (high level)

- accounts: account_id, account_name, industry, country, signup_date, referral_source, plan_tier, seats, is_trial, churn_flag
- subscriptions: subscription_id, account_id, start_date, end_date, plan_tier, seats, mrr_amount, arr_amount, is_trial, upgrade_flag, downgrade_flag, churn_flag, billing_frequency, auto_renew_flag
- feature_usage: usage_id, subscription_id, usage_date, feature_name, usage_count, usage_duration_secs, error_count, is_beta_feature
- support_tickets: ticket_id, account_id, submitted_at, closed_at, resolution_time_hours, priority, first_response_time_minutes, satisfaction_score, escalation_flag
- churn_events: churn_event_id, account_id, churn_date, reason_code, refund_amount_usd, preceding_upgrade_flag, preceding_downgrade_flag, is_reactivation, feedback_text

For full column descriptions, see the header row of each CSV in `data_raw/`.

## Suggested projects

- Predict churn using subscriptions + support data
- Analyze feature adoption during beta periods
- Forecast support workload and resolution SLAs
- Revenue cohort analysis by referral source

## License & credit

This dataset is fully synthetic and provided under a permissive, MIT-like license. You may use or remix it for learning, research, or portfolio purposes — please credit the author (River @ Rivalytics).









