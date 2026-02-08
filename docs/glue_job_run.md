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



