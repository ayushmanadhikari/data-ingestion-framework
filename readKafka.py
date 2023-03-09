import os
from pyspark.sql.functions import from_json
from pyspark import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro, to_avro
from pyspark.sql.avro import SchemaBuilder


CONS_KAFKA_SERVER = "localhost:29092, localhost:29093"
CONS_KAFKA_TOPIC = "dbserver1.source_db.demo"


spark = SparkSession.builder.appName("mysql-cdc-kafka").getOrCreate()

spark.sparkContext.setLogLevel("WARN")
#os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 pyspark-shell"
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,za.co.absa:abris_2.12:5.0.0 --repositories https://packages.confluent.io/maven/ pyspark-shell'


readingStreamDF = spark.readStream.format("kafka").option("kafka.bootstrap.servers", CONS_KAFKA_SERVER).\
    option("subscribe", CONS_KAFKA_TOPIC).option("startingOffsets", "earliest").load().\
    select(from_avro("value"))

readingStreamDF.writeStream.format("console").outputMode("append").start().awaitTermination()














