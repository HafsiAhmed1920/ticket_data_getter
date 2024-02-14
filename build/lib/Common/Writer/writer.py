from firebase_admin import storage


def upload_to_firebase(fileName: str):
   
    # Get a reference to the storage bucket
    bucket = storage.bucket()

    # Upload the file
    blob = bucket.blob('softdata/' + fileName)
    blob.upload_from_filename(fileName)

    # Optional: Delete the local CSV file after upload
    # os.remove(fileName)
    print("File saved")

    # Print the public URL of the uploaded file
    print("Your file URL:", blob.public_url)
    print("Your file URL:", blob.public_url)

    # Print the public URL of the uploaded file
    print("Your file URL:", blob.public_url)
