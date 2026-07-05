import os
import json
import pandas as pd
from sqlalchemy import create_engine, text

from sqlalchemy.engine import make_url
from dotenv import load_dotenv

# Load env variables
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

# Get database URL from environment or fallback to passwordless localhost
db_url = os.getenv("DATABASE_URL", "mysql+pymysql://root@127.0.0.1/ipl_ai")
url = make_url(db_url)

username = url.username or "root"
password = url.password or ""
host = url.host or "127.0.0.1"
database = url.database or "ipl_ai"
port = url.port or 3306

# ==========================
# Create Database if not exists
# ==========================
try:
    # Connect to MySQL server without database first
    temp_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/"
    if not password:
        temp_url = f"mysql+pymysql://{username}@{host}:{port}/"
    temp_engine = create_engine(temp_url)
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))
        print(f"Database '{database}' checked/created successfully.")
except Exception as e:
    print(f"Warning/Error creating database: {e}")

# Connect to target database
engine = create_engine(db_url)

# ==========================
# Dataset Folder
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "..", "datasets")

# ==========================
# CSV Files and Table Names
# ==========================
files = {
    "BALL_BY_BALL.csv": "ball_by_ball",
    "IPL_MATCH.csv": "ipl_match",
    "PLAYER_INFO.csv": "player_info",
    "TEAMS.csv": "teams"
}

# ==========================
# Import Function
# ==========================
def read_csv_with_encoding(file_path):
    encodings = ["utf-8", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            print(f"Trying encoding: {encoding}")
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Successfully read using {encoding}\n")
            return df
        except UnicodeDecodeError:
            continue

    raise Exception(f"Could not read {file_path} with supported encodings.")

# ==========================
# Import All Files & Export Schema Summary
# ==========================
schema_summary = {}

for file_name, table_name in files.items():
    file_path = os.path.join(DATASET_DIR, file_name)

    print("=" * 60)
    print(f"Importing {file_name}")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    try:
        df = read_csv_with_encoding(file_path)

        # Ingest to SQL
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        print(f"Successfully imported into table: {table_name}")
        print(f"Rows Imported: {len(df)}")

        # Collect Schema Info
        columns_info = {}
        for col in df.columns:
            # Get data type and sample values (converted to strings to ensure JSON serializability)
            dtype = str(df[col].dtype)
            sample_vals = df[col].dropna().head(3).tolist()
            sample_vals = [str(x) for x in sample_vals]
            columns_info[col] = {
                "type": dtype,
                "samples": sample_vals
            }
        
        schema_summary[table_name] = {
            "row_count": len(df),
            "columns": columns_info
        }

    except Exception as e:
        print(f"Error importing {file_name}")
        print(e)

# Write schema summary
summary_path = os.path.join(BASE_DIR, "schema_summary.json")
try:
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(schema_summary, f, indent=4)
    print(f"\nSchema summary written to {summary_path}")
except Exception as e:
    print(f"Error writing schema summary: {e}")

print("\nAll possible datasets have been processed.")