import sys, os
sys.path.append(os.path.dirname(os.getcwd()))

from pyspark.sql import SparkSession
from config.config import RAW_PREFIX, BRONZE_PREFIX, RAW_FILES
from config.codes import d_minus_data,reading_data,Generate_Batch_ID,partition_by_date,FinalLoad

TABLE_NAME = "facilities"
column_name = "facility_id"

raw_path= d_minus_data(RAW_PREFIX,TABLE_NAME)
print(raw_path)
df= reading_data(spark,raw_path,column_name)

df.show(10)

# aasd = Generate_Batch_ID()
# df_final = aasd.col_create(df)
# # df_final.show(10)

# df_final = partition_by_date(df_final)
# # df_final.show(10)

# print(BRONZE_PREFIX)
# # Usage
# TAD = FinalLoad()
# TAD.loading_final_bronze_order(df_final,BRONZE_PREFIX,TABLE_NAME)

