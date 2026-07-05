import pandas as pd
import os

try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "datasets", "PLAYER_INFO.csv")
    
    encodings = ["utf-8", "latin1", "cp1252"]
    df = None
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"Read successful with {encoding}")
            break
        except Exception:
            continue
            
    if df is not None:
        info_str = f"Columns: {df.columns.tolist()}\n\nFirst 5 rows:\n{df.head(5).to_string()}"
        output_path = os.path.join(base_dir, "player_info_summary.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(info_str)
        print("Successfully wrote summary to player_info_summary.txt")
    else:
        print("Failed to read CSV")
except Exception as e:
    print(f"Error: {e}")
