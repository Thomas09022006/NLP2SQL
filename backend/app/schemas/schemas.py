from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ==========================
# Authentication Schemas
# ==========================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# ==========================
# Natural Language to SQL
# ==========================

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, description="The natural language question to ask about IPL data.")


class QueryResponse(BaseModel):
    query: str
    sql: str
    success: bool
    execution_time_ms: Optional[int] = None
    columns: Optional[List[str]] = None
    rows: Optional[List[Dict[str, Any]]] = None
    explanation: Optional[str] = None
    chart_recommendation: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ==========================
# Saved Queries
# ==========================

class SavedQueryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    natural_language_query: str
    generated_sql: str


class SavedQueryOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    natural_language_query: str
    generated_sql: str
    created_at: datetime

    class Config:
        from_attributes = True
