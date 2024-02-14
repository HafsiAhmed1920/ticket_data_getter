import firebase_admin
from firebase_admin import credentials


def initialise_firebase():
    cred = credentials.Certificate(r'C:\Users\ahafsi\timsoftScrapper\firebase_config\timesoft-fad2f-firebase-adminsdk-a4620-fc09ed2754.json')
    firebase_admin.initialize_app(cred, {'storageBucket': 'timesoft-fad2f.appspot.com'})
