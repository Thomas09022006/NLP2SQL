import time
from typing import Dict, Any, List, Tuple
from sqlalchemy import text
from backend.app.db.database import readonly_engine

class SqlExecutor:
    @staticmethod
    def execute_query(sql_query: str) -> Tuple[bool, List[str], List[Dict[str, Any]], int, str]:
        """
        Executes a SELECT query on the read-only database.
        Returns:
            success (bool)
            columns (List[str])
            rows (List[Dict[str, Any]])
            execution_time_ms (int)
            error_message (str)
        """
        start_time = time.time()
        columns = []
        rows = []
        error_msg = ""
        success = False
        
        try:
            with readonly_engine.connect() as connection:
                result = connection.execute(text(sql_query))
                
                # Extract column names
                if result.returns_rows:
                    columns = list(result.keys())
                    # Convert query result rows to list of dictionaries
                    for row in result:
                        row_dict = {}
                        for idx, col_name in enumerate(columns):
                            val = row[idx]
                            # Handle non-serializable datatypes (like Decimals, Dates, etc.)
                            if hasattr(val, 'isoformat'):
                                val = val.isoformat()
                            elif hasattr(val, 'to_eng_string'):  # Decimal
                                val = float(val)
                            row_dict[col_name] = val
                        rows.append(row_dict)
                        
                success = True
        except Exception as e:
            error_msg = str(e)
            success = False
            
        execution_time_ms = int((time.time() - start_time) * 1000)
        return success, columns, rows, execution_time_ms, error_msg
