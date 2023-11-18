from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from fastapi import Query
from fastapi import BackgroundTasks

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[schemas.Event])
def get_events(
    db: Session = Depends(get_db),
    location: Optional[str] = Query(None, alias="loc"),
    sort_by: Optional[str] = Query("time", alias="sortBy"),):
    
    query = db.query(models.Event)

    if location:
        query = query.filter(models.Event.location == location)

    if sort_by == "time":
        query = query.order_by(models.Event.time)
    elif sort_by == "popularity":
        query = query.order_by(models.Event.guests)
    elif sort_by == "creation_time":
        query = query.order_by(models.Event.created_at)

    events = query.all()

    return events


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    
    new_event = models.Event(**event.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("/{id}", response_model=schemas.Event)
def get_event(id: int, db: Session = Depends(get_db)):
    
    event = db.query(models.Event).filter(models.Event.id == id).first()

    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event with id of {id} was not found")
    
    return event


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(id: int, db: Session = Depends(get_db)):
    
    event_query = db.query(models.Event).filter(models.Event.id == id)
    event = event_query.first()

    if event == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event with id of {id} was not found")

    event_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Event)
def update_event(id:int, updated_event: schemas.EventCreate, db: Session = Depends(get_db)):
    
    event_query = db.query(models.Event).filter(models.Event.id == id)
    event = event_query.first()

    if event == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event with id of {id} was not found")
    
    event_query.update(updated_event.model_dump() ,synchronize_session=False)
    db.commit()

    return event_query.first()


# Reminders
def send_event_reminder(event_id: int, reminder_minutes: int):
    print(f"Reminder: Event {event_id} will start in {reminder_minutes} minutes!")


@router.post("/{id}/schedule-reminder", status_code=status.HTTP_200_OK)
def schedule_event_reminder(
    id: int,
    background_tasks: BackgroundTasks,
    reminder_time: schemas.ReminderTime,
    db: Session = Depends(get_db),
):
    event = db.query(models.Event).filter(models.Event.id == id).first()

    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Event with id of {id} was not found")

    # Schedule a reminder task
    background_tasks.add_task(send_event_reminder, id, reminder_time.minutes_before)

    return {"message": f"Reminder for Event {id} scheduled successfully"}