import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), '.env'))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(PROJECT_DIR, "data", "franchisedna.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_DIR = os.path.join(PROJECT_DIR, 'data')
    RAW_DATASET_PATH = os.environ.get('RAW_DATASET_PATH', '')
    CLEANED_CSV_PATH = os.path.join(PROJECT_DIR, 'data', 'cleaned_population.csv')
    GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')
