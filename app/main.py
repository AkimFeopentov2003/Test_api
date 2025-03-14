from fastapi import FastAPI, Depends, HTTPException, Query
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.schemas import RollCreate, RollResponse
from app.crud import create_roll, delete_roll, get_rolls, get_rolls_statistics
from typing import List, Optional

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/rolls/", response_model=RollResponse)
def add_roll(roll: RollCreate, db: Session = Depends(get_db)):
    return create_roll(db, roll)

@app.put("/rolls/{roll_id}", response_model=RollResponse)
def remove_roll(roll_id: int, db: Session = Depends(get_db)):
    roll = delete_roll(db, roll_id)
    if not roll:
        raise HTTPException(status_code=404, detail="Roll not found")
    return roll

@app.get("/rolls/", response_model=List[RollResponse])
def list_rolls(
        db: Session = Depends(get_db),
        id_min: Optional[int] = Query(None),
        id_max: Optional[int] = Query(None),
        weight_min: Optional[float] = Query(None),
        weight_max: Optional[float] = Query(None),
        length_min: Optional[float] = Query(None),
        length_max: Optional[float] = Query(None),
        added_after: Optional[datetime] = Query(None),
        added_before: Optional[datetime] = Query(None),
        removed_after: Optional[datetime] = Query(None),
        removed_before: Optional[datetime] = Query(None),
    ):
    return get_rolls(db, id_min, id_max, weight_min, weight_max,
        length_min, length_max, added_after, added_before,
        removed_after, removed_before
    )

@app.get("/rolls/statistics/")
def rolls_statistics(
    start_date: datetime = Query(..., description="Начальная дата периода"),
    end_date: datetime = Query(..., description="Конечная дата периода"),
    db: Session = Depends(get_db)
):
    if start_date > end_date:
        return {"error": "Начальная дата не может быть больше конечной даты"}
    return get_rolls_statistics(db, start_date, end_date)
