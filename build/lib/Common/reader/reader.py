from pyspark.sql import SparkSession
from firebase_admin import storage
import tempfile
from firebase_config.fireConf import initialise_firebase


def reader_bytes(folder='facebook/',):
    bucket = storage.bucket()
    blobs = bucket.list_blobs(prefix=folder)
    data = [blob.download_as_bytes() for blob in blobs]
    return data


def text_to_df(data_list):
    # Initialize a SparkSessions
    spark = SparkSession.builder.getOrCreate()

    # Create a list to store temporary file paths
    temp_files = []

    for data in data_list:
        # Write the bytes data to a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            f.write(data)
            temp_path = f.name

        # Read the CSV file into a DataFrame
        df = spark.read.csv(temp_path, header=True, inferSchema=True)

        # Store the temporary file path
        temp_files.append(temp_path)

    return df, temp_files


"""def remove_temp(temp_files):
    
    # Delete all temporary files
    for temp_file in temp_files:
        os.remove(temp_file)
"""


def reader(folder: str):
    data = reader_bytes(folder)
    df, temp = text_to_df(data)
    return df


