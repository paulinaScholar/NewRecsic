import os
import pandas as pd
import boto3


def load_dataset():
    # ---- Load env variables ----
    SPACES_KEY = os.getenv("SPACES_KEY")
    SPACES_SECRET = os.getenv("SPACES_SECRET")
    SPACES_REGION = os.getenv("SPACES_REGION")
    SPACES_BUCKET = os.getenv("SPACES_BUCKET")
    SPACES_FILE = os.getenv("SPACES_FILE")

    # ---- Validate variables ----
    if not all([SPACES_KEY, SPACES_SECRET, SPACES_REGION, SPACES_BUCKET, SPACES_FILE]):
        raise ValueError("Missing one or more Spaces environment variables.")

    # ---- Create Spaces client ----
    session = boto3.session.Session()

    client = session.client(
        "s3",
        region_name=SPACES_REGION,
        endpoint_url=f"https://{SPACES_REGION}.digitaloceanspaces.com",
        aws_access_key_id=SPACES_KEY,
        aws_secret_access_key=SPACES_SECRET
    )

    # ---- Download CSV (streaming, no se guarda en disco) ----
    obj = client.get_object(Bucket=SPACES_BUCKET, Key=SPACES_FILE)
    stream = obj["Body"]

    # ---- Fast CSV read ----
    df = pd.read_csv(stream, engine="pyarrow")   # más rápido que el default

    return df
