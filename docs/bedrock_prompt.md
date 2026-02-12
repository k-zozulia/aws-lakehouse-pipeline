# Bedrock Daily Report Generator

## Script location
`src/bedrock/report_generator.py`

## Key features
- Fetches aggregated data from Redshift Spectrum (KPI, top 10 products, quarantine stats)
- Uses only summarized numbers/tables — no raw data sent to Bedrock
- Single Bedrock model invocation (anthropic.claude-3-sonnet-20240229-v1:0)
- max_tokens=1000 limit
- Saves report to S3: `s3://karina-ecommerce-lakehouse/ecommerce/reports/daily_report_YYYY-MM-DD.md`

## Prompt template (main part)

```json
You are a senior business analyst...
Generate a concise daily Markdown business + data quality report.
Note: This report uses data from {report_data_date} (same day of month, but one month ago for demo purposes).
In production, the report should always use yesterday's data.
Use ONLY the following aggregated data...
KPI Summary ({report_data_date}):
{kpi_table}
Top 10 Products by Revenue ({report_data_date}):
{top10_table}
Data Quality - Quarantine Breakdown ({report_data_date}):
{quar_table}
Report MUST contain:

KPI summary section
Top 10 products table
Data quality summary
2-3 short insights
Next actions checklist (3-5 items with - [ ] checkboxes)

Output ONLY the Markdown report. Max 1000 tokens.
```


## Example generated report (2026-01-13)

## Report file in S3


## Notes
- One Bedrock call per report
- Aggregated data only → safe & cost-effective
- Date used: same day one month ago (for demo, as dataset has no recent data)
