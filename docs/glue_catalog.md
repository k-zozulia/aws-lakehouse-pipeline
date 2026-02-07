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
  {"Name": "order_date", "Type": "date", "Comment": "Date extracted from timestamp (partition key)"},
  {"Name": "hour_of_day", "Type": "int", "Comment": "Hour of the day (0-23)"},
  {"Name": "total_amount", "Type": "double", "Comment": "quantity * price"},
  {"Name": "rejection_reason", "Type": "string", "Comment": "Reason for rejection"}
]
```

## Screenshots

1. **List of tables in ecommerce_lakehouse**

2. **raw_orders schema and location**

3. **curated_orders schema + partition key**

4. **quarantine_orders schema**
