"""
This module reads a CSV file using SparkSession.
"""

from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("CSV Reader").getOrCreate()

# Path to the CSV file
CSV_FILE_PATH = r'C:\Users\ahafsi\timsoftScrapper\ticket_data\2023-12-04_01-26-08'

# Read the CSV file
data = spark.read.csv(CSV_FILE_PATH, header=True, inferSchema=True)

# Display the data
data.show()
