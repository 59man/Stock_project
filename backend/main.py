from fastapi import FastAPI
from database import Base, engine
from routers.assets_router import router as assets_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio API",
    version="1.0.0",
)

# Register routers
app.include_router(assets_router)


# Root endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "Portfolio API running"}
