from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, SessionLocal, engine, get_db
from app import schemas, models
from app.config import settings

# Use the same database for testing
TEST_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Override the dependency to use the test database
app.dependency_overrides[get_db] = lambda: SessionLocal()

# Create tables in the test database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_get_all_events():
    # Assuming you have a fixture or mechanism to create test events
    # Adjust the assertions based on your specific data
    test_events = [
        {"title": "Test Event 1", "time": "2023-01-01T12:00:00", "location": "Test Location 1", "description": "Test Description 1"},
        {"title": "Test Event 2", "time": "2023-01-02T14:00:00", "location": "Test Location 2", "description": "Test Description 2"},
    ]

    # Create test events in the test database
    with SessionLocal() as db:
        for event_data in test_events:
            db_event = models.Event(**event_data)
            db.add(db_event)
        db.commit()

    # Get all events using the test client
    with client as c:
        res = c.get("/events/")
        print(res)
        def validate(event):
            return schemas.Event(**event)

        events_map = map(validate, res.json())
        events_list = list(events_map)

        assert len(events_list) == len(test_events)+2
        assert res.status_code == 200


def test_create_event():
    event_data = {"title": "Test Event", "time": "2023-01-01T12:00:00", "location": "Test Location", "description": "Test Description"}

    with client as c:
        response = c.post("/events/", json=event_data)
        
        assert response.status_code == 201
        assert "id" in response.json()
        assert response.json()["title"] == "Test Event"

        # Return the created event's id for subsequent tests
        return response.json()["id"]

def test_get_event(created_event_id):
    with client as c:
        response = c.get(f"/events/{created_event_id}")

        assert response.status_code == 200
        assert response.json()["id"] == created_event_id
        assert response.json()["title"] == "Test Event"
        
def test_update_event(created_event_id):
    updated_data = {"title": "Updated Event", "location": "Updated Location", "description": "Updated Description"}

    with client as c:
        response = c.put(f"/events/{created_event_id}", json=updated_data)

        assert response.status_code == 200
        assert response.json()["id"] == created_event_id
        assert response.json()["title"] == "Updated Event"
        assert response.json()["location"] == "Updated Location"

def test_delete_event(created_event_id):
    with client as c:
        response = c.delete(f"/events/{created_event_id}")

        assert response.status_code == 204

        # Verify that the event has been deleted by trying to get it again
        response_get_after_delete = c.get(f"/events/{created_event_id}")
        assert response_get_after_delete.status_code == 404