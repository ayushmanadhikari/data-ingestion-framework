from pyspark.sql import SparkSession
from pyspark import SparkContext



###CONSTANTS 
CONS_KAFKA_SERVER = "localhost:29092"
CONS_KAFKA_TOPIC = "mysql_server.source_db.demo"
CONS_SCHEMA_REGISTRY_SERVER = "http://schemaregistry0:8085"


# spark session
spark = SparkSession.builder.appName("read kafka").getOrCreate()
spark.sparkContext.setLogLevel("WARN")


#creating a reading stream to read from kafka topic and displaying it in the console
readingDf = spark.readStream.format("kafka").option("kafka.bootstrap.servers", CONS_KAFKA_SERVER).\
                option("subscribe", CONS_KAFKA_TOPIC).option("startingOffsets", "earliest").load()

readingDf.writeStream.format("console").outputMode("append").start().awaitTermination()