CREATE EXTERNAL SCHEMA ecommerce_lakehouse
FROM DATA CATALOG
DATABASE 'ecommerce_lakehouse'
IAM_ROLE 'arn:aws:iam::<account-id>:role/RedshiftSpectrumRole-karina'
CREATE EXTERNAL DATABASE IF NOT EXISTS;