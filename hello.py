from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("hello_spark")\
        .getOrCreate()

    print("Hello spark world, welcome adsoft ... ")

    spark.stop()