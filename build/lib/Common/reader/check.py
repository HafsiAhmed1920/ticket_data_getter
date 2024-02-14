from pyspark.sql import SparkSession

# Initialize a SparkSession
spark = SparkSession.builder.getOrCreate()

# Load your dataframe
df = spark.read.csv(r'C:\Users\ahafsi\Scrafb\scrapped_output.csv', header=True)

# Get the column
df = df.select('content')

df.show()