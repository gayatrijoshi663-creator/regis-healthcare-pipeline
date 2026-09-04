from config.config import BRONZE_PREFIX , SILVER_PREFIX
from pyspark.sql.functions import*
from config.codes import d_minus_data ,reading_bronze
table_name = "admissions" 
raw_path = d_minus_data(BRONZE_PREFIX,table_name)
print(raw_path)
df=reading_bronze(spark,raw_path)
df.show(10)

