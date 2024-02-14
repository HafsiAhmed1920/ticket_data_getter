from pyspark.sql.functions import udf, col, length
from pyspark.sql.types import StringType
import re


def clean_text(df):
    """
    Function to perform additional text cleaning for chatbot
    """
    def text_preprocessing(text):
        # Convert to lowercase
        text = text.lower()

        # Remove special characters, numbers, and multiple spaces
        text = re.sub(r'[^a-zA-Z\s]+', ' ', text)

        # Remove specific words
        words_to_remove = [
            "bonjour", "bonsoir", "merci"
        ]
        words_to_remove_escaped = [re.escape(word) for word in words_to_remove]
        words_to_remove_pattern = r'\b(?:{})\b'.format('|'.join(words_to_remove_escaped))
        text = re.sub(words_to_remove_pattern, '', text)

        # Remove "cordialement" and everything after it
        text = re.sub(r'cordialement.*', '', text)

        return text.strip() if text else None  # return None if text is empty

    # Define the UDF for text preprocessing
    text_preprocessing_udf = udf(text_preprocessing, StringType())

    # Apply text preprocessing to each relevant column
    for column in ["description", "solution"]:
        df = df.withColumn(column, text_preprocessing_udf(col(column)))

    # Drop rows where all cleaned text columns are empty or null
    df = df.filter(
        (length("sujet_text") > 0) |
        (length("description") > 0) |
        (length("solution") > 0)
    )

    # Drop rows with null values in any of the cleaned text columns
    df = df.dropna(subset=["sujet_text", "description", "solution"])
    df = df.na.drop()

    return df

# Example usage:
# cleaned_df = clean_text(your_original_dataframe)
