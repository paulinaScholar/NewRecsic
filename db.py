import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load enviroment vars
load_dotenv()

# Read vars
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Path to CA certificate
CA_CERT_PATH = os.path.join(os.getcwd(), "ca-certificate.crt")

db_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode=require&sslrootcert={CA_CERT_PATH}"
)

engine = create_engine(db_url)