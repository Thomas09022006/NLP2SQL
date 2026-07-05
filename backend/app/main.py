import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config.config import settings
from backend.app.db.database import engine, Base
from backend.app.routers.auth import router as auth_router
from backend.app.routers.analytics import router as analytics_router

# Initialize database metadata tables on startup
try:
    Base.metadata.create_all(bind=engine)
    print("Database metadata tables verified/created.")
except Exception as e:
    print(f"Warning: Could not create metadata tables on start (db might not be ready yet): {e}")

app = FastAPI(
    title="CricSQL API",
    description="AI-Powered Natural Language to SQL IPL Analytics Platform Backend",
    version="1.0.0"
)

# CORS configuration to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://nlp2sql.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Measure request process time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include Router endpoints
app.include_router(auth_router)
app.include_router(analytics_router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "CricSQL API Server",
        "engine": "Gemini 2.5 Flash",
        "docs_url": "/docs"
    }

# Health Check Route
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
