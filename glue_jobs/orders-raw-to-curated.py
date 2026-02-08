import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, lower, trim, to_date, hour, when, lit
from pyspark.sql import functions as F
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType, DateType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

BUCKET = "karina-ecommerce-lakehouse"
RAW_PATH = f"s3://{BUCKET}/ecommerce/raw/orders/"
CURATED_PATH = f"s3://{BUCKET}/ecommerce/curated/orders/"
QUARANTINE_PATH = f"s3://{BUCKET}/ecommerce/quarantine/orders/"

raw_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("order_timestamp", TimestampType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True),
    StructField("status", StringType(), True),
])

raw_df = spark.read.schema(raw_schema).csv(RAW_PATH, header=True, inferSchema=False)

def filter_missing_order_id(df):
    valid = df.filter(col("order_id").isNotNull())
    invalid = df.filter(col("order_id").isNull())
    return valid, invalid

def filter_invalid_values(df):
    valid = df.filter((col("quantity") > 0) & (col("price") >= 0))
    invalid = df.filter((col("quantity") <= 0) | (col("price") < 0))
    return valid, invalid

def normalize_status(df):
    df = df.withColumn("status", lower(trim(col("status"))))
    df = df.withColumn(
        "status",
        when(col("status").isin(["complete", "done"]), "completed")
        .when(col("status") == "canceled", "cancelled")
        .otherwise(col("status")),
    )
    return df
    
def remove_duplicates(df):
    return df.dropDuplicates(["order_id"])

def derive_columns(df):
    df = (
        df.withColumn("order_date", to_date(col("order_timestamp")))
        .withColumn("hour_of_day", hour(col("order_timestamp")))
        .withColumn("total_amount", col("quantity") * col("price"))
    )
    return df

start_time = datetime.now()
print(f"Job started at: {start_time.isoformat()}")

input_count = raw_df.count()
print(f"Input row count: {input_count}")

valid_df, missing_id_df = filter_missing_order_id(raw_df)
print(f"After order_id filter - valid: {valid_df.count()}, missing: {missing_id_df.count()}")

valid_df, invalid_values_df = filter_invalid_values(valid_df)
print(f"After values filter - valid: {valid_df.count()}, invalid: {invalid_values_df.count()}")

valid_df = normalize_status(valid_df)
valid_df = remove_duplicates(valid_df)
print(f"After dedup: {valid_df.count()}")

valid_df = derive_columns(valid_df)
print(f"After derive: {valid_df.count()}")

quarantine_parts = []
if missing_id_df.count() > 0:
    missing_id_df = missing_id_df.withColumn("rejection_reason", lit("missing_order_id"))
    if "order_date" not in missing_id_df.columns:
        missing_id_df = missing_id_df.withColumn(
            "order_date", 
            when(col("order_timestamp").isNotNull(), to_date(col("order_timestamp")))
            .otherwise(lit(None).cast(DateType()))
        )
    quarantine_parts.append(missing_id_df)

if invalid_values_df.count() > 0:
    invalid_values_df = invalid_values_df.withColumn("rejection_reason", lit("invalid_quantity_or_price"))
    if "order_date" not in invalid_values_df.columns:
        invalid_values_df = invalid_values_df.withColumn(
            "order_date", 
            when(col("order_timestamp").isNotNull(), to_date(col("order_timestamp")))
            .otherwise(lit(None).cast(DateType()))
        )
    quarantine_parts.append(invalid_values_df)

if quarantine_parts:
    quarantine_df = quarantine_parts[0]
    for df in quarantine_parts[1:]:
        quarantine_df = quarantine_df.unionByName(df, allowMissingColumns=True)
    
    quarantine_count = quarantine_df.count()
    print(f"Quarantine row count: {quarantine_count}")
    
    quarantine_stats = quarantine_df.groupBy("rejection_reason").count().collect()
    print("Quarantine counts by reason:")
    for row in quarantine_stats:
        print(f"{row['rejection_reason']}: {row['count']}")
    
    quarantine_df.write.mode("append").parquet(QUARANTINE_PATH)
else:
    print("Quarantine row count: 0")

curated_count = valid_df.count()
print(f"Curated row count: {curated_count}")
valid_df.write.mode("append").partitionBy("order_date").parquet(CURATED_PATH)

end_time = datetime.now()
print(f"Job ended at: {end_time.isoformat()}")

job.commit()
