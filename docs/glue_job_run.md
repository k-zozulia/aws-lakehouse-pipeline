# Glue ETL Job Run Documentation

## Job Overview
- **Job name**: orders-raw-to-curated
- **IAM Role**: GlueServiceRole-karina
- **Resources**: G.1X worker type, 10 workers
- **Runs executed**: 3 (1 test + 1 final)
- **Last run status**: SUCCEEDED
- **Dedup key**: `order_id`

## Execution Results (from final run)

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
- Retention policy: Set to **7 days** (to minimize storage costs)
- Logs contain: input/curated/quarantine counts, rejection reasons grouping, start/end timestamps

## Screenshots (add to docs/images/ or root images/)

1. Job configuration (resources, IAM role, script location)  
   ![Job configuration](images/glue-job-config.png)

2. Successful job run details (status SUCCEEDED)  
   ![Job run success](images/glue-run-success.png)

3. CloudWatch logs snippet (with all required counts, reasons, timestamps)  
   ![CloudWatch logs](images/glue-cloudwatch-logs.png)

4. Log retention policy set to 7 days  
   ![Log retention](images/glue-log-retention.png)

5. S3 curated folder with partitions (order_date=...)  
   ![S3 curated partitions](images/s3-curated-partitions.png)

6. S3 quarantine folder with files  
   ![S3 quarantine](images/s3-quarantine.png)

