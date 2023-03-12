from pyspark.sql import SparkSession
from pyspark import SparkContext
#from pyspark.sql.avro.functions import from_avro, to_avro
from pyspark.sql.column import Column, _to_java_column


# CONSTANTS
CONS_KAFKA_SERVER = "localhost:29092"
CONS_KAFKA_TOPIC = "mysql_server.source_db.demo"
CONS_SCHEMA_REGISTRY_SERVER = "http://schemaregistry0:8085"


spark = SparkSession.builder.appName("mysql-cdc-kafka").getOrCreate()

spark.sparkContext.setLogLevel("WARN")
#os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1 pyspark-shell"
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,za.co.absa:abris_2.12:5.0.0 --repositories https://packages.confluent.io/maven/ pyspark-shell'


readingStreamDF = spark.readStream.format("kafka").option("kafka.bootstrap.servers", CONS_KAFKA_SERVER).\
    option("subscribe", CONS_KAFKA_TOPIC).option("startingOffsets", "earliest").load()

readingStreamDF.writeStream.format("console").outputMode("append").start().awaitTermination()


### desearilizing avro messages
def from_avro(col, config):
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    abris_avro = jvm_gateway.za.co.absa.abris.avro
    return Column(abris_avro.functions.from_avro(_to_java_column(col), config))



def from_avro_abris_config(config_map, topic, is_key):
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    scala_map = jvm_gateway.PythonUtils.toScalaMap(config_map)

    return jvm_gateway.za.co.absa.abris.config\
        .AbrisConfig\
        .fromConfluentAvro()\
        .downloadReaderSchemaByLatestVersion()\
        .andTopicNameStrategy(topic, is_key)\
        .usingSchemaRegistry(scala_map)










