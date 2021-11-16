from fastapi import FastAPI
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)
# api랑 database 묶기

@app.get("/")
async def create_database():
    return {"Database": "Created"}
# 묶인거 확인

# Dependency
def get_db():
    try:
        db = SessionaLocal()
        yield db
    finally:
        db.close()


@app.get("/trials/{trial_id}", response_model=schemas.Trial)
async def read_trial(trial_id: UUID, db: Session = Depends(get_db)):
    db_trial = crud.get_trial(db, trial_id=trial_id)
    if db_trial is None:
        raise HTTPException(status_code=404, detail="Trial_Not_Found")
    return db_trial


@app.get("/list", response_model=List[schemas.Item])
async def read_list_of_trial(offset: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    trials = crud.get_trial(db, offset=offset, limit=limit)
    return trials