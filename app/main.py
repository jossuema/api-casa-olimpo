from fastapi import FastAPI
from app.routers import router
from app.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown():
    SessionLocal.close_all()

@app.get("/")
async def read_root():
    return {"Hello": "World"}