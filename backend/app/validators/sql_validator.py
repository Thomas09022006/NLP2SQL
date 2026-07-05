import re
from typing import Tuple

def validate_sql_query(sql: str) -> Tuple[bool, str]:
    """
    Validates that a generated SQL query is a safe, read-only SELECT statement.
    Returns (is_valid, error_message).
    """
    # Remove leading/trailing spaces and convert to uppercase for check
    clean_sql = sql.strip().replace("\n", " ").replace("\r", " ")
    
    # Check for multiple statements (separated by semicolon)
    statements = [s for s in clean_sql.split(";") if s.strip()]
    if len(statements) > 1:
        return False, "Execution of multiple SQL statements is forbidden."
        
    # Standardize spaces for keyword check
    sql_upper = " ".join(clean_sql.upper().split())
    
    # 1. MUST start with SELECT or WITH (for CTEs)
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Only SELECT or WITH statements are allowed for execution."
        
    # 2. Forbidden destructive commands/keywords
    forbidden_patterns = [
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b",
        r"\bCREATE\b",
        r"\bREPLACE\b",
        r"\bRENAME\b",
        r"\bEXEC\b",
        r"\bEXECUTE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bLOAD\b",
        r"\bINTO\b\s+\bOUTFILE\b",
        r"\bINTO\b\s+\bDUMPFILE\b",
    ]
    
    for pattern in forbidden_patterns:
        if re.search(pattern, sql_upper):
            return False, f"Dangerous SQL operation detected: Matches forbidden keyword pattern '{pattern}'"
            
    return True, ""
