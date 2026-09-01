def d_minus_data(RAW_PREFIX,TABLE_NAME):
    from datetime import datetime, timedelta
    # Get yesterday's date
    now = datetime.now() - timedelta(days=0) 
    # yr, mon, dt = now.year, now.month, now.day
    year = now.year
    month = now.month
    day = now.day
    raw_path = f"s3://{RAW_PREFIX}/{TABLE_NAME}/year={year}/month={month}/day={day}/"
    return raw_path



    # Read data from S3 path
from pyspark.sql.functions import when, col ,lit
### Read CSV
def reading_data(spark,raw_path,column_name):
    # Read CSV from S3
    df = (
        spark.read.csv(raw_path,header = True , inferSchema= True)  
    )
    df = df.withColumn(
            "_is_quarantined",
            when(
                col(column_name).isNull(),
                True
            ).otherwise(False)
        )
    df = df.select("*","_metadata.file_name","_metadata.file_size")
    # Add ingestion timestamp
    return df


from datetime import datetime 
class Generate_Batch_ID: 
    def batch_ids(self):
        self.batch_id = "BATCH_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.batch_id
        # Add metadata columns
        # self.batch_id = batch_id
    def col_create(self,df):
        # Ensure batch_id exists
        if not hasattr(self, "batch_id"):
            self.batch_ids()
        df_final = (df
            .withColumn("batch_id", lit(self.batch_id))
            .withColumn("ingestion_time", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            )
        return df_final
from pyspark.sql.functions import year, month, dayofmonth

def partition_by_date(df_final):
    # Add year, month, and day columns derived from load_ts
    df_final = df_final.withColumn("year", year("load_ts")) \
                   .withColumn("month", month("load_ts")) \
                   .withColumn("day", dayofmonth("load_ts"))
    return df_final


    ##### Save data
## bronze write to s3
from pyspark.sql.utils import AnalysisException
import traceback

class FinalLoad:
    def loading_final_bronze_order(self, df_final,bronze_path,TABLE_NAME):
        try:
            # Attempt to write DataFrame to csv
            df_final.write.format("csv") \
                .option("header", "true")\
                .mode("overwrite") \
                .partitionBy("year","month","day") \
                .save(f"{bronze_path}/{TABLE_NAME}")
             # .option("overwriteSchema", "true") \
            print("✅ Data successfully written to bronze layer.")
        
        except AnalysisException as ae:
            print("AnalysisException occurred while writing data:")
            print(ae)
        
        except Exception as e:
            print("Unexpected error occurred while writing data:")
            print(str(e))
            traceback.print_exc()   # optional: prints full stack trace for debugging




