import boto3
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
from tabulate import tabulate

load_dotenv()

BUCKET = os.getenv('BUCKET')
AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
REPORT_DATE = datetime.now().strftime('%Y-%m-%d')  # today's date for report name
REPORT_KEY = f"ecommerce/reports/daily_report_{REPORT_DATE}.md"
boto3.setup_default_session(profile_name=os.getenv('AWS_PROFILE', 'karina-hw'))

# For demo purposes we take data from the same day but one month ago
# In production this should be yesterday: datetime.now() - timedelta(days=1)
report_data_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

REDSHIFT_CONN = psycopg2.connect(
    host=os.getenv('REDSHIFT_HOST'),
    port=os.getenv('REDSHIFT_PORT'),
    database=os.getenv('REDSHIFT_DB'),
    user=os.getenv('REDSHIFT_USER'),
    password=os.getenv('REDSHIFT_PASSWORD'),
    sslmode='require'
)

bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)

s3 = boto3.client('s3', region_name=AWS_REGION)

def run_query(sql):
    """Execute SQL query and return columns + rows"""
    cur = REDSHIFT_CONN.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    return columns, rows

# 1. Fetch KPI for the selected date (same day, one month ago)
kpi_sql = f"""
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
WHERE order_date = '{report_data_date}'
"""

top10_sql = f"""
SELECT 
    product_id,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
WHERE order_date = '{report_data_date}'
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10
"""

quarantine_sql = f"""
SELECT 
    rejection_reason,
    COUNT(*) AS count
FROM ecommerce_lakehouse.quarantine_orders
WHERE DATE(order_timestamp) = '{report_data_date}'
GROUP BY rejection_reason
ORDER BY count DESC
"""

# Execute queries
kpi_cols, kpi_data = run_query(kpi_sql)
top10_cols, top10_data = run_query(top10_sql)
quar_cols, quar_data = run_query(quarantine_sql)

# 2. Format data as markdown tables
kpi_table = tabulate(kpi_data, kpi_cols, tablefmt="pipe") if kpi_data else "No data for this date"
top10_table = tabulate(top10_data, top10_cols, tablefmt="pipe") if top10_data else "No data"
quar_table = tabulate(quar_data, quar_cols, tablefmt="pipe") if quar_data else "No data"

# 3. Build the prompt
prompt = f"""
You are a senior business analyst for an e-commerce platform.

Generate a concise daily Markdown business + data quality report.

Note: This report uses data from {report_data_date} (same day of month, but one month ago).
In production, the report should always use yesterday's data.

Use ONLY the following aggregated data (do not invent numbers):

**KPI Summary ({report_data_date}):**
{kpi_table}

**Top 10 Products by Revenue ({report_data_date}):**
{top10_table}

**Data Quality - Quarantine Breakdown ({report_data_date}):**
{quar_table}

Report MUST contain:
- KPI summary section (total orders, total revenue)
- Top 10 products table (use Markdown table)
- Data quality summary (quarantine reasons and counts)
- 2-3 short insights (1-2 sentences each, explain trends using ONLY provided numbers)
- Next actions checklist (3-5 items with - [ ] checkboxes, tied to anomalies like low revenue, high rejects, top product concentration)

Keep tone professional, concise and actionable.
Output ONLY the Markdown report, no extra text.
Max output: 1000 tokens.
"""

# 4. Call Bedrock (Claude 3 Sonnet)
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": prompt}]
})

response = bedrock.invoke_model(
    modelId=model_id,
    contentType="application/json",
    accept="application/json",
    body=body
)

response_body = json.loads(response['body'].read())
report_content = response_body['content'][0]['text']

# 5. Save report to S3
s3.put_object(
    Bucket=BUCKET,
    Key=REPORT_KEY,
    Body=report_content.encode('utf-8'),
    ContentType='text/markdown'
)

print(f"Report generated and saved to: s3://{BUCKET}/{REPORT_KEY}")
print("\nReport preview (first 500 chars):\n")
print(report_content[:500] + "..." if len(report_content) > 500 else report_content)