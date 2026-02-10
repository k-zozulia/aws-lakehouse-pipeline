# Glue ETL Job Run Documentation

## Job Overview
- **Job name**: orders-raw-to-curated
- **IAM Role**: GlueServiceRole-karina
- **Resources**: G.1X worker type, 2 workers
- **Runs executed**: 3 (1 test + 1 final)
- **Last run status**: SUCCEEDED
- **Dedup key**: `order_id`

## Execution Results (from final run)
<img width="942" height="341" alt="image" src="https://github.com/user-attachments/assets/db039d97-cd4f-4267-914a-9495fd21cb8c" />

## How to Run the Job
1. Go to AWS Glue Console → ETL jobs
2. Select job `orders-raw-to-curated`
3. Click **Run job**
4. Use minimum resources (G.1X, 2 workers)
5. Monitor run in **Runs** tab
6. After completion: check CloudWatch logs and S3 paths:
   - Curated: `s3://karina-ecommerce-lakehouse/ecommerce/curated/orders/`
   - Quarantine: `s3://karina-ecommerce-lakehouse/ecommerce/quarantine/orders/`

## Mandatory CloudWatch Steps
- Log groups: `/aws-glue/jobs/output` and `/aws-glue/jobs/error`
- Retention policy: Set to **5 days**
- Logs contain: input/curated/quarantine counts, rejection reasons grouping, start/end timestamps

## Screenshots

1. Successful job run details
   <img width="1079" height="258" alt="image" src="https://github.com/user-attachments/assets/0a9a5322-5975-450c-94d3-ef1cd607986c" />

2. Log retention policy set to 5 days  
   <img width="1163" height="425" alt="image" src="https://github.com/user-attachments/assets/9347dd46-4846-45e2-b805-4c7def0ecefc" />

3. S3 curated folder with partitions
   <img width="1427" height="667" alt="image" src="https://github.com/user-attachments/assets/53ed18d9-355a-4c55-88b5-9b327e8a6820" />

4. S3 quarantine folder with files  
   <img width="1424" height="643" alt="image" src="https://github.com/user-attachments/assets/b6e18a4a-2e91-4959-be06-80237b655fac" />

5. CloudWatch Alarm for job failure
   <img width="1192" height="308" alt="image" src="https://github.com/user-attachments/assets/092fdbe0-87ff-4763-af90-38edc6182ca8" />

---

# Glue Studio Visual ETL (Optional - Recommended)

Created visual job: visual-orders-raw-to-curated

## Visual Pipeline Overview
- Source: Glue Catalog table raw_orders
- Filters: missing order_id, invalid quantity/price
- Transformations: normalize status, derive order_date/hour_of_day/total_amount
- Branching: valid → curated, invalid → quarantine with rejection_reason
- Targets: Parquet to curated/orders/ (partition by order_date), quarantine/orders/

## Generated PySpark Code
```bash
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1770649962801 = glueContext.create_dynamic_frame.from_catalog(database="ecommerce_lakehouse", table_name="raw_orders", transformation_ctx="AWSGlueDataCatalog_node1770649962801")

# Script generated for node Filter invalid rows
Filterinvalidrows_node1770651678637 = Filter.apply(frame=AWSGlueDataCatalog_node1770649962801, f=lambda row: (bool(re.match("^$", row["order_id"])) or row["quantity"] <= 0 or row["price"] < 0), transformation_ctx="Filterinvalidrows_node1770651678637")

# Script generated for node Filter valid order_id
Filtervalidorder_id_node1770650066791 = Filter.apply(frame=AWSGlueDataCatalog_node1770649962801, f=lambda row: (bool(re.match(".+", row["order_id"]))), transformation_ctx="Filtervalidorder_id_node1770650066791")

# Script generated for node Add rejection_reason
Addrejection_reason_node1770651864057 = Filterinvalidrows_node1770651678637.gs_derived(colName="rejection_reason", expr="CASE    WHEN order_id IS NULL THEN 'missing_order_id'   WHEN quantity <= 0 OR price < 0 THEN 'invalid_quantity_or_price'   ELSE 'other_invalid' END")

# Script generated for node Filter valid quantity/price
Filtervalidquantityprice_node1770650177176 = Filter.apply(frame=Filtervalidorder_id_node1770650066791, f=lambda row: (row["quantity"] > 0 and row["price"] > 0), transformation_ctx="Filtervalidquantityprice_node1770650177176")

# Script generated for node Normalize status
Normalizestatus_node1770650705719 = Filtervalidquantityprice_node1770650177176.gs_derived(colName="status", expr="CASE    WHEN lower(trim(status)) IN ('complete', 'done') THEN 'completed'   WHEN lower(trim(status)) = 'canceled' THEN 'cancelled'   ELSE lower(trim(status)) END")

# Script generated for node Add order_date
Addorder_date_node1770650980802 = Normalizestatus_node1770650705719.gs_derived(colName="order_date", expr="to_date(order_timestamp)")

# Script generated for node Add hour_of_day
Addhour_of_day_node1770651063199 = Addorder_date_node1770650980802.gs_derived(colName="hour_of_day", expr="hour(order_timestamp)")

# Script generated for node Add total_amount
Addtotal_amount_node1770651117503 = Addhour_of_day_node1770651063199.gs_derived(colName="total_amount", expr="quantity * price")

# Script generated for node Write quarantine
Writequarantine_node1770653399413 = glueContext.write_dynamic_frame.from_catalog(frame=Addrejection_reason_node1770651864057, database="ecommerce_lakehouse", table_name="quarantine_orders", transformation_ctx="Writequarantine_node1770653399413")

# Script generated for node Write curated
Writecurated_node1770653489738 = glueContext.write_dynamic_frame.from_catalog(frame=Addtotal_amount_node1770651117503, database="ecommerce_lakehouse", table_name="curated_orders", transformation_ctx="Writecurated_node1770653489738")

job.commit()
```

## Comparison with Manual PySpark Code
- Visual: simpler for basic filters/derive, auto-partitioning, less custom logic
- Manual: more flexible (custom functions, detailed logging, unionByName handling)
- Visual code is more declarative, uses DynamicFrame API


## Visual canvas graph
<img width="1260" height="278" alt="image" src="https://github.com/user-attachments/assets/3948e276-8c1e-4ff2-818b-da2550b50299" />


