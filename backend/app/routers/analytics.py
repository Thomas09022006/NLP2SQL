from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import time

from backend.app.db.database import get_db
from backend.app.models.models import User, QueryHistory, SavedQuery
from backend.app.schemas.schemas import QueryRequest, QueryResponse, SavedQueryCreate, SavedQueryOut
from backend.app.auth.auth_handler import get_current_user
from backend.app.validators.sql_validator import validate_sql_query
from backend.app.services.sql_executor import SqlExecutor
from backend.app.services.gemini_service import GeminiService

router = APIRouter(
    prefix="/api/analytics",
    tags=["IPL Analytics Engine"]
)

@router.post("/query", response_model=QueryResponse)
def ask_analytics_question(
    payload: QueryRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Executes a natural language query against the IPL database.
    Converts question to SQL -> Validates safety -> Executes -> Summarizes & Recommends Charts.
    Includes a self-repair feedback loop for SQL generation errors.
    """
    user_query = payload.query
    
    # 1. Translate question to SQL and get recommendation
    gemini_resp = GeminiService.generate_sql(user_query)
    raw_sql = gemini_resp.get("sql")
    generated_sql = raw_sql.strip() if isinstance(raw_sql, str) else ""
    chart_recommendation = gemini_resp.get("recommended_chart")

    if not generated_sql:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate SQL query from the prompt."
        )

    # 2. Safety Validation
    is_valid, validation_err = validate_sql_query(generated_sql)
    if not is_valid:
        # Log failed attempt
        history = QueryHistory(
            user_id=current_user.id,
            natural_language_query=user_query,
            generated_sql=generated_sql,
            is_success=False,
            error_message=f"Validation Rejected: {validation_err}"
        )
        db.add(history)
        db.commit()
        
        return QueryResponse(
            query=user_query,
            sql=generated_sql,
            success=False,
            error=f"SQL Sandbox rejection: {validation_err}"
        )

    # 3. Execute SQL Query
    success, columns, rows, exec_time, exec_err = SqlExecutor.execute_query(generated_sql)
    
    # 4. Self-Repair Loop (Attempt once if MySQL execution failed)
    if not success and exec_err:
        print(f"Execution failed. Attempting self-repair on error: {exec_err}")
        repaired_gemini_resp = GeminiService.repair_sql(generated_sql, exec_err, user_query)
        raw_repaired_sql = repaired_gemini_resp.get("sql")
        repaired_sql = raw_repaired_sql.strip() if isinstance(raw_repaired_sql, str) else ""
        
        if repaired_sql and repaired_sql != generated_sql:
            # Re-validate repaired SQL
            is_repaired_valid, validation_err = validate_sql_query(repaired_sql)
            if is_repaired_valid:
                # Re-execute repaired SQL
                success, columns, rows, exec_time, exec_err = SqlExecutor.execute_query(repaired_sql)
                if success:
                    generated_sql = repaired_sql
                    if repaired_gemini_resp.get("recommended_chart"):
                        chart_recommendation = repaired_gemini_resp.get("recommended_chart")

    # 5. Log Query to History
    history = QueryHistory(
        user_id=current_user.id,
        natural_language_query=user_query,
        generated_sql=generated_sql,
        execution_time_ms=exec_time,
        is_success=success,
        error_message=exec_err if not success else None
    )
    db.add(history)
    db.commit()

    if not success:
        return QueryResponse(
            query=user_query,
            sql=generated_sql,
            success=False,
            error=f"Database execution error: {exec_err}"
        )

    # 6. Generate Commentary/Explanation
    explanation = GeminiService.generate_explanation(user_query, generated_sql, rows)

    return QueryResponse(
        query=user_query,
        sql=generated_sql,
        success=True,
        execution_time_ms=exec_time,
        columns=columns,
        rows=rows,
        explanation=explanation,
        chart_recommendation=chart_recommendation
    )


@router.get("/history", response_model=List[Any])
def get_user_query_history(
    limit: int = 20, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the execution history of the logged-in user.
    """
    history = db.query(QueryHistory).filter(
        QueryHistory.user_id == current_user.id
    ).order_by(QueryHistory.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "query": h.natural_language_query,
            "sql": h.generated_sql,
            "execution_time_ms": h.execution_time_ms,
            "is_success": h.is_success,
            "error_message": h.error_message,
            "created_at": h.created_at
        } for h in history
    ]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
def clear_user_query_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Deletes all query history records for the logged-in user.
    """
    db.query(QueryHistory).filter(QueryHistory.user_id == current_user.id).delete()
    db.commit()
    return


@router.delete("/history/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_query_history_item(
    history_id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Deletes a specific query history record for the logged-in user.
    """
    history_item = db.query(QueryHistory).filter(
        QueryHistory.id == history_id,
        QueryHistory.user_id == current_user.id
    ).first()
    
    if not history_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found."
        )
        
    db.delete(history_item)
    db.commit()
    return


@router.post("/saved", response_model=SavedQueryOut)
def save_query(
    payload: SavedQueryCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Saves a specific generated query to the user's dashboard library.
    """
    saved = SavedQuery(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
        natural_language_query=payload.natural_language_query,
        generated_sql=payload.generated_sql
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


@router.get("/saved", response_model=List[SavedQueryOut])
def get_saved_queries(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all saved queries for the logged-in user.
    """
    return db.query(SavedQuery).filter(SavedQuery.user_id == current_user.id).order_by(SavedQuery.created_at.desc()).all()


@router.delete("/saved/{query_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_query(
    query_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Deletes a saved query from the user's library.
    """
    query = db.query(SavedQuery).filter(
        SavedQuery.id == query_id, 
        SavedQuery.user_id == current_user.id
    ).first()
    
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved query not found."
        )
        
    db.delete(query)
    db.commit()
    return
