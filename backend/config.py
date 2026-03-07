import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'franchise-dna-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(PROJECT_DIR, "data", "franchisedna.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_DIR = os.path.join(PROJECT_DIR, 'data')
    RAW_DATASET_PATH = os.environ.get(
        'RAW_DATASET_PATH',
        '/Users/sathwik/Downloads/2011-IndiaState-0000.xlsx'
    )
    CLEANED_CSV_PATH = os.path.join(PROJECT_DIR, 'data', 'cleaned_population.csv')
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', 'AIzaSyC8gIcEPBcSfQjvjVfpJjsXFfYkvSyHSrA')
