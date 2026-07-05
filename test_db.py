import os
import sys
from sqlalchemy import create_engine, text, inspect

def run_diagnostics():
    print("=" * 60)
    print("CricSQL Database & Tables Diagnostics")
    print("=" * 60)

    # Add project root to sys path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Load config
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
        from backend.app.config.config import settings
        db_url = settings.database_url
    except Exception as e:
        print(f"[ERROR] Could not load settings: {e}")
        db_url = os.getenv("DATABASE_URL", "mysql+pymysql://root@127.0.0.1/ipl_ai")
        
    print(f"Target Database URL: {db_url.split('@')[-1] if '@' in db_url else db_url}")

    # 2. Connect to MySQL server
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            res = conn.execute(text("SELECT VERSION()")).fetchone()
            print(f"[SUCCESS] Connected to MySQL Database. Server Version: {res[0]}")
    except Exception as e:
        print(f"[FAILURE] Could not connect to the MySQL database.")
        print(f"          Error Details: {e}")
        print("\nPossible solutions:")
        print("1. Make sure your MySQL Server is running locally.")
        print("2. Check if the username/password in your '.env' file is correct.")
        return

    # 3. Check for tables
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        print(f"\nExisting tables: {existing_tables}")
        
        required_app_tables = ["users", "query_history", "saved_queries"]
        required_data_tables = ["ball_by_ball", "ipl_match", "player_info", "teams"]
        
        # Check data tables
        missing_data = [t for t in required_data_tables if t not in existing_tables]
        if missing_data:
            print(f"\n[WARNING] Missing IPL data tables: {missing_data}")
            print("          Please run: python backend/import_data.py to ingest datasets.")
        else:
            print("[SUCCESS] All IPL data tables found.")
            
        # Check app tables
        missing_app = [t for t in required_app_tables if t not in existing_tables]
        if missing_app:
            print(f"\n[WARNING] Missing application/auth tables: {missing_app}")
            print("          Attempting to create them now...")
            try:
                from backend.app.db.database import Base
                # Import models to ensure they are registered with Base.metadata
                import backend.app.models.models
                Base.metadata.create_all(bind=engine)
                print("[SUCCESS] Application/auth tables created successfully!")
            except Exception as create_err:
                print(f"[FAILURE] Could not create application tables: {create_err}")
        else:
            print("[SUCCESS] All application/auth tables found ('users' is active).")

        # 4. Check user count
        if "users" in inspector.get_table_names():
            with engine.connect() as conn:
                user_count = conn.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0]
                print(f"\nRegistered users in database: {user_count}")
                if user_count > 0:
                    print("Sample registered usernames:")
                    users = conn.execute(text("SELECT username, email FROM users LIMIT 5")).fetchall()
                    for u in users:
                        print(f"  - Username: '{u[0]}', Email: '{u[1]}'")
                else:
                    print("Database 'users' table is currently empty.")

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during diagnostics: {e}")

if __name__ == "__main__":
    run_diagnostics()
