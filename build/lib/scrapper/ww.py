from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# Create a SparkSession
spark = SparkSession.builder.getOrCreate()

# Define the folder path
folder_path = r'C:\Users\ahafsi\timsoftScrapper\ticket_data\2023-12-04_20-22-29'

# Read the CSV files into a DataFrame
df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(folder_path)

# Remove null values from the DataFrame
df = df.na.drop()

# Show the DataFrame
df.show()

