from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func, case, select, text, and_, or_, cast, Date, literal_column
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import is_not

from models import Roll
from schemas import RollCreate

def create_roll(db: Session, roll: RollCreate):
    db_roll = Roll(length=roll.length, weight=roll.weight)
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll

def delete_roll(db: Session, roll_id: int):
    roll = db.query(Roll).filter(Roll.id == roll_id).first()
    if roll:
        if not roll.removed_at:
            roll.removed_at = datetime.utcnow()
            print(f"Дата удаления: {roll.removed_at}")
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Roll is already removed from the stock")
    return roll


def get_rolls(
        db: Session,
        id_min: Optional[int],
        id_max: Optional[int],
        weight_min: Optional[float],
        weight_max: Optional[float],
        length_min: Optional[float],
        length_max: Optional[float],
        added_after: Optional[datetime],
        added_before: Optional[datetime],
        removed_after: Optional[datetime],
        removed_before: Optional[datetime],
):
    query = db.query(Roll)

    # Фильтрация по ID
    if id_min is not None:
        query = query.filter(Roll.id >= id_min)
    if id_max is not None:
        query = query.filter(Roll.id <= id_max)

    # Фильтрация по весу
    if weight_min is not None:
        query = query.filter(Roll.weight >= weight_min)
    if weight_max is not None:
        query = query.filter(Roll.weight <= weight_max)

    # Фильтрация по длине
    if length_min is not None:
        query = query.filter(Roll.length >= length_min)
    if length_max is not None:
        query = query.filter(Roll.length <= length_max)

    # Фильтрация по дате добавления
    if added_after is not None:
        query = query.filter(Roll.added_at >= added_after)
    if added_before is not None:
        query = query.filter(Roll.added_at <= added_before)

    # Фильтрация по дате удаления
    if removed_after is not None:
        query = query.filter(Roll.removed_at >= removed_after)
    if removed_before is not None:
        query = query.filter(Roll.removed_at <= removed_before)

    return query.all()


def get_rolls_statistics(db: Session, start_date: datetime, end_date: datetime):
    stats = db.query(
        func.count(Roll.id).label("added_count"),
        func.count(case((Roll.removed_at.between(start_date, end_date), Roll.id))).label("removed_count"),
        func.avg(Roll.length).label("avg_length"),
        func.avg(Roll.weight).label("avg_weight"),
        func.max(Roll.length).label("max_length"),
        func.min(Roll.length).label("min_length"),
        func.max(Roll.weight).label("max_weight"),
        func.min(Roll.weight).label("min_weight"),
        func.sum(Roll.weight).label("total_weight"),
    ).filter(Roll.added_at.between(start_date, end_date)).first()
    time = db.query(
        func.max(Roll.removed_at - Roll.added_at).label("max_storage_duration"),
        func.min(Roll.removed_at - Roll.added_at).label("min_storage_duration"),
    ).filter(Roll.added_at.between(start_date, end_date), Roll.removed_at.isnot(None)).first()


    # date_series = db.query(
    #     func.generate_series(start_date, end_date, literal_column("'1 day'::interval")).label("day")
    # ).subquery()
    #
    # subquery = (
    #     db.query(
    #         date_series.c.day,
    #         func.count(Roll.id).label("roll_count")
    #     )
    #     .join(Roll, and_(
    #         cast(Roll.added_at, Date) <= date_series.c.day,
    #         or_(Roll.removed_at == None, cast(Roll.removed_at, Date) >= date_series.c.day)
    #     ), isouter=True)
    #     .group_by(date_series.c.day)
    #     .subquery()
    # )
    #
    # min_max_query = (
    #     db.query(subquery.c.day, subquery.c.roll_count)
    #     .filter(
    #         or_(
    #             subquery.c.roll_count == db.query(func.min(subquery.c.roll_count)).scalar_subquery(),
    #             subquery.c.roll_count == db.query(func.max(subquery.c.roll_count)).scalar_subquery()
    #         )
    #     )
    #     .all()
    # )
    # for day, roll_count in min_max_query:
    #     print(f"Day: {day}, Roll Count: {roll_count}")

    max_storage_duration = None
    min_storage_duration = None
    if stats and time.max_storage_duration:
        max_duration = time.max_storage_duration
        min_duration = time.min_storage_duration

        # Форматирование продолжительности в дни, часы и минуты
        max_days = max_duration.days
        max_hours, remainder = divmod(max_duration.seconds, 3600)
        max_minutes, _ = divmod(remainder, 60)
        max_storage_duration = f"{max_days}d {max_hours}h {max_minutes}m"

        min_days = min_duration.days
        min_hours, remainder = divmod(min_duration.seconds, 3600)
        min_minutes, _ = divmod(remainder, 60)
        min_storage_duration = f"{min_days}d {min_hours}h {min_minutes}m"

    return {
        "added_count": stats.added_count,
        "removed_count": stats.removed_count,
        "avg_length": stats.avg_length,
        "avg_weight": stats.avg_weight,
        "max_length": stats.max_length,
        "min_length": stats.min_length,
        "max_weight": stats.max_weight,
        "min_weight": stats.min_weight,
        "total_weight": stats.total_weight,
        "max_storage_duration": max_storage_duration if max_storage_duration else None,
        "min_storage_duration": min_storage_duration if min_storage_duration else None,
        # "min_rolls_day": min_max_query
        # "min_rolls_day": min_rolls_day[0] if min_rolls_day else None,
        # "max_rolls_day": max_rolls_day[0] if max_rolls_day else None,
        # "min_weight_day": min_weight_day[0] if min_weight_day else None,
        # "max_weight_day": max_weight_day[0] if max_weight_day else None,
    }