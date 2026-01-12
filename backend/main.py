from fastapi import FastAPI
from database import Base, engine
from routers.assets_router import router as assets_router
from routers.lots_router import router as lots_router
from routers.portfolio_router import router as portfolio_router
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE
    allow_headers=["*"],         # allow all headers
)

# Register routers
app.include_router(assets_router)
app.include_router(lots_router)
app.include_router(portfolio_router)

# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "Portfolio API running"}
