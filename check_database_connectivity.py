import os
import sys
from sqlalchemy import create_engine, text

def check_connection():
    print("=" * 60)
    print("MySQL & Database Connectivity Diagnostics")
    print("=" * 60)

    # 1. Load configuration from settings/environment
    # Add project root to sys.path to resolve backend imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
        from backend.app.config.config import settings
        db_url = settings.database_url
    except Exception as e:
        print(f"[ERROR] Could not import settings: {e}")
        # Try reading .env file manually as fallback
        db_url = "mysql+pymysql://root@127.0.0.1/ipl_ai"
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("DATABASE_URL="):
                        db_url = line.split("=", 1)[1].strip()
                        break
    
    print(f"Target Database URL: {db_url.split('@')[-1] if '@' in db_url else db_url}")

    # 2. Check base connection to MySQL server (without database)
    # Parse connection string to get server URL
    if "@" in db_url:
        server_part = db_url.split("@")[1]
        db_name = server_part.split("/")[-1]
        server_url = db_url.replace(f"/{db_name}", "")
    else:
        db_name = "ipl_ai"
        server_url = "mysql+pymysql://root@127.0.0.1"

    print("\n1. Connecting to MySQL server...")
    try:
        temp_engine = create_engine(server_url, connect_args={"connect_timeout": 5})
        with temp_engine.connect() as conn:
            # Execute simple select to verify server status
            res = conn.execute(text("SELECT VERSION()")).fetchone()
            print(f"[SUCCESS] Connected to MySQL Server successfully!")
            print(f"          Server Version: {res[0]}")
    except Exception as e:
        print(f"[FAILURE] Could not connect to MySQL server. Please make sure MySQL is running.")
        print(f"          Error Details: {e}")
        return False

    # 3. Check if database exists
    print(f"\n2. Verifying database '{db_name}' exists...")
    try:
        with temp_engine.connect() as conn:
            databases = conn.execute(text("SHOW DATABASES")).fetchall()
            database_list = [db[0] for db in databases]
            if db_name in database_list:
                print(f"[SUCCESS] Database '{db_name}' exists.")
            else:
                print(f"[WARNING] Database '{db_name}' does not exist yet.")
                print(f"          To create it and import data, run: python backend/import_data.py")
                return False
    except Exception as e:
        print(f"[ERROR] Could not query databases list: {e}")
        return False

    # 4. Connect to target database and check tables
    print(f"\n3. Checking tables and row counts in '{db_name}'...")
    try:
        engine = create_engine(db_url)
        required_tables = ["ball_by_ball", "ipl_match", "player_info", "teams"]
        
        with engine.connect() as conn:
            tables = conn.execute(text("SHOW TABLES")).fetchall()
            existing_tables = [t[0] for t in tables]
            print(f"Existing tables in database: {existing_tables}")
            
            all_tables_exist = True
            for tbl in required_tables:
                if tbl in existing_tables:
                    # Count rows
                    cnt_res = conn.execute(text(f"SELECT COUNT(*) FROM {tbl}")).fetchone()
                    row_count = cnt_res[0]
                    print(f"  - Table '{tbl}': [FOUND] with {row_count} rows.")
                    if row_count == 0:
                        print(f"    [WARNING] Table '{tbl}' is empty. You need to run the ingestion script.")
                else:
                    print(f"  - Table '{tbl}': [MISSING]")
                    all_tables_exist = False
            
            if not all_tables_exist:
                print(f"\n[WARNING] Some tables are missing. Run: python backend/import_data.py")
                return False
                
    except Exception as e:
        print(f"[FAILURE] Failed to connect or query target database: {e}")
        return False

    # 5. Run test query
    print("\n4. Running sample SQL query execution test...")
    try:
        with engine.connect() as conn:
            # Let's run a test query on teams table
            q = text("SELECT team_name, team_name_short FROM teams LIMIT 3")
            results = conn.execute(q).fetchall()
            print("[SUCCESS] Test query executed successfully. Sample data:")
            for row in results:
                print(f"  - {row[0]} ({row[1]})")
    except Exception as e:
        print(f"[FAILURE] Test query execution failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Diagnostics summary: Database setup is fully working!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    check_connection()
