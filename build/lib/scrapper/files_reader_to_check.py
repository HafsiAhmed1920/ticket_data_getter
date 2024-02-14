from pyspark.sql import SparkSession
from firebase_admin import storage
import tempfile
from firebase_config.fireConf import initialise_firebase
import os
from Common.reader.reader import reader_bytes, text_to_df


def reader(folder: str):
    data = reader_bytes(folder)
    df, temp = text_to_df(data)
    return df

    def reader(folder: str):
        # Get the list of subfolders inside the main folder
        subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

        # Initialize a SparkSession
        spark = SparkSession.builder.getOrCreate()

        # Create a list to store the final DataFrame
        dfs = []

        for subfolder in subfolders:
            # Read all CSV files inside the subfolder
            files = [f.path for f in os.scandir(subfolder) if f.is_file() and f.name.endswith('.csv')]
            for file in files:
                df = spark.read.csv(file, header=True, inferSchema=True)
                dfs.append(df)

        # Concatenate all DataFrames into a single DataFrame
        final_df = dfs[0].unionAll(dfs[1:]) if len(dfs) > 1 else dfs[0]

        return final_df


initialise_firebase()

# Read from the "ticket_data" folder
folder_path = "ticket_data"
df = reader(folder_path)

# Show the DataFrame
df.show()




