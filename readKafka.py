import findspark
from pyspark.sql.functions import from_json

from pyspark import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
import time



spark = SparkSession.builder.appName("MYSQL-CDC-RealTime").getOrCreate()
sc = SQLContext(spark)
spark.sparkContext.setLogLevel("WARN")

schema = StructType([StructField("after", StringType())])


demoDf = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:29092").option("subscribe", "mysql_server.source_db.demo").load() 




print(demoDf)
