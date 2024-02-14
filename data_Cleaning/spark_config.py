from pyspark.sql import SparkSession


class SparkConfig:
    def __init__(self):
        self.spark = self.create_spark_session()

    def create_spark_session(self):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                spark = SparkSession.builder \
                    .appName("SparkApplication") \
                    .config("spark.driver.memory", "4g") \
                    .config("spark.executor.memory", "8g") \
                    .getOrCreate()
                return spark
            except Exception as e:
                print(f"Error creating Spark session: {e}")
                retry_count += 1
        raise Exception("Failed to create Spark session after multiple retries")
