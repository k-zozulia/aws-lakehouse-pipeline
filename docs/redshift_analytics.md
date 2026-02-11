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
<img width="641" height="555" alt="image" src="https://github.com/user-attachments/assets/1978b1ff-2d89-40ca-8b8b-983a1e7f7673" />


### 2. Revenue per product
<img width="651" height="559" alt="image" src="https://github.com/user-attachments/assets/ce65c820-5c6f-4a87-a060-2c0df767eb24" />


### 3. Top 10 products by revenue
<img width="652" height="531" alt="image" src="https://github.com/user-attachments/assets/8c48be4d-c995-49d0-af72-9747ce507520" />


### 4. Revenue by hour of day
<img width="638" height="551" alt="image" src="https://github.com/user-attachments/assets/3ad66c42-af6b-47ef-a5f0-fd903a52cb18" />


### 5. Orders and revenue by status
<img width="846" height="376" alt="image" src="https://github.com/user-attachments/assets/962992eb-6de6-485f-9ae8-8c28bedd5e23" />


### 6. Top 5 customers by total revenue
<img width="660" height="443" alt="image" src="https://github.com/user-attachments/assets/c1d81b83-484c-477b-bd6e-126cddd03233" />


### 7. Average order value (AOV) per day
<img width="853" height="561" alt="image" src="https://github.com/user-attachments/assets/96f221a2-a54f-4b8f-839e-56f305aa351b" />


### 8. Orders and revenue by day of week
<img width="652" height="540" alt="image" src="https://github.com/user-attachments/assets/fdf2ee2c-d177-410c-83e4-e3c09ff094b9" />

