# Glue Data Catalog

Database: `ecommerce_lakehouse`

## Tables Overview

| Table Name        | Location (S3 Path)                                      | Format   | Partition Key | Description                          |
|-------------------|----------------------------------------------------------|----------|---------------|--------------------------------------|
| raw_orders        | s3://karina-ecommerce-lakehouse/ecommerce/raw/orders/    | CSV      | None          | Raw input data (before cleaning)     |
| curated_orders    | s3://karina-ecommerce-lakehouse/ecommerce/curated/orders/| Parquet  | order_date    | Cleaned & enriched orders            |
| quarantine_orders | s3://karina-ecommerce-lakehouse/ecommerce/quarantine/orders/ | Parquet | order_date    | Rejected records with reason         |

## Table Details

### 1. raw_orders
- Location: `s3://karina-ecommerce-lakehouse/ecommerce/raw/orders/`
- Format: CSV
- Schema:

```json
[
  {"Name": "order_id", "Type": "string", "Comment": "Unique order identifier"},
  {"Name": "customer_id", "Type": "string", "Comment": "Customer identifier"},
  {"Name": "product_id", "Type": "string", "Comment": "Product identifier"},
  {"Name": "quantity", "Type": "int", "Comment": "Number of items ordered"},
  {"Name": "price", "Type": "double", "Comment": "Unit price"},
  {"Name": "status", "Type": "string", "Comment": "Order status (raw)"},
  {"Name": "order_timestamp", "Type": "timestamp", "Comment": "Order placement timestamp"}
]
```

### 2. curated_orders
- Location: `s3://karina-ecommerce-lakehouse/ecommerce/curated/orders/`
- Format: CSV
- Partition key: order_date (date)
- Schema:
```json
[
  {"Name": "order_id", "Type": "string", "Comment": "Unique order identifier"},
  {"Name": "customer_id", "Type": "string", "Comment": "Customer identifier"},
  {"Name": "product_id", "Type": "string", "Comment": "Product identifier"},
  {"Name": "quantity", "Type": "int", "Comment": "Number of items ordered"},
  {"Name": "price", "Type": "double", "Comment": "Unit price"},
  {"Name": "status", "Type": "string", "Comment": "Normalized status"},
  {"Name": "order_timestamp", "Type": "timestamp", "Comment": "Order placement timestamp"},
  {"Name": "order_date", "Type": "date", "Comment": "Date extracted from timestamp (partition key)"},
  {"Name": "hour_of_day", "Type": "int", "Comment": "Hour of the day (0-23)"},
  {"Name": "total_amount", "Type": "double", "Comment": "quantity * price"}
]
```

### 2. quarantine_orders
- Location: `s3://karina-ecommerce-lakehouse/ecommerce/quarantine/orders/`
- Format: CSV
- Partition key: order_date (date)
- Schema:
```json
[
  {"Name": "order_id", "Type": "string", "Comment": "Unique order identifier"},
  {"Name": "customer_id", "Type": "string", "Comment": "Customer identifier"},
  {"Name": "product_id", "Type": "string", "Comment": "Product identifier"},
  {"Name": "quantity", "Type": "int", "Comment": "Number of items ordered"},
  {"Name": "price", "Type": "double", "Comment": "Unit price"},
  {"Name": "status", "Type": "string", "Comment": "Normalized status"},
  {"Name": "order_timestamp", "Type": "timestamp", "Comment": "Order placement timestamp"},
  {"Name": "rejection_reason", "Type": "string", "Comment": "Reason for rejection"}
]
```

## Screenshots

1. **List of tables in ecommerce_lakehouse**
<img width="1429" height="421" alt="image" src="https://github.com/user-attachments/assets/d5d34103-e4cb-4824-83d8-ed9e29b9d3b5" />

2. **raw_orders schema and location**
<img width="922" height="570" alt="image" src="https://github.com/user-attachments/assets/497fc4fd-9416-436e-9cb3-654b189c25d8" />

3. **curated_orders schema + partition key**
<img width="1215" height="635" alt="image" src="https://github.com/user-attachments/assets/15b17258-ee61-438f-a399-96e65b76eeac" />

4. **quarantine_orders schema**
<img width="1210" height="650" alt="image" src="https://github.com/user-attachments/assets/b67e7c51-3fa0-435b-9a3d-63466e6b0160" />
