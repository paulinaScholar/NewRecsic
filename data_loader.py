import os
import pandas as pd
import boto3

print("DEBUG: SPACES_KEY=", os.getenv("SPACES_KEY"))
print("DEBUG: SPACES_BUCKET=", os.getenv("SPACES_BUCKET"))
print("DEBUG: SPACES_FILE=", os.getenv("SPACES_FILE"))

_cached_df = None

def load_dataset():
    global _cached_df
    if _cached_df is not None:
        return _cached_df

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

    # ---- Download CSV (streaming) ----
    obj = client.get_object(Bucket=SPACES_BUCKET, Key=SPACES_FILE)
    stream = obj["Body"]

    # ---- Read CSV ----
    df = pd.read_csv(stream, engine="pyarrow")

    # ---- Cache ----
    _cached_df = df
    return df
