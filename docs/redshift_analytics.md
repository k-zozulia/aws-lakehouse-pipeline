# Redshift Analytics

## Approach
- Redshift Spectrum – external tables over S3 + Glue Catalog
- No data loading into Redshift
- External schema: `ecommerce_lakehouse`
- Queries run directly on curated Parquet files in S3

## DDL – External Schema Creation
File: `sql/redshift_ddl.sql`

```sql
-- redshift_ddl.sql
CREATE EXTERNAL SCHEMA ecommerce_external
FROM DATA CATALOG
DATABASE 'ecommerce_lakehouse'
IAM_ROLE 'arn:aws:iam::<your-account-id>:role/GlueServiceRole-karina-homework'
CREATE EXTERNAL DATABASE IF NOT EXISTS;
```

---

## Analytics Queries
File: `sql/redshift_ddl.sql`

### 1. Daily revenue




### 2. Revenue per product




### 3. Top 10 products by revenue



### 4. Revenue by hour of day



### 5. Orders and revenue by status




### 6. Top 5 customers by total revenue



### 7. Average order value (AOV) per day




### 8. Orders and revenue by day of week

