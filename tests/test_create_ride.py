from unittest.mock import ANY

from fastapi import status
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import RideModel

def test_create_ride_success(
    test_client: TestClient, 
    session: Session,
    auth_headers: dict[str, str],
 ):

    start_time = datetime(
        year=2025,
        month=11,
        day=18,
        hour=15,
        minute=30,
        tzinfo=timezone.utc,
    ).isoformat()
    payload = {
        "title": "Ride_title",
        "description": "Ride_description",
        "start_time": start_time,
    }
    response = test_client.post("/rides/", json=payload, headers=auth_headers)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert isinstance(data["id"], int)
    assert isinstance(data["code"], str) and len(data["code"]) == 6
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert datetime.fromisoformat(data["start_time"].replace("Z", "+00:00")) == datetime.fromisoformat(
        payload["start_time"].replace("Z", "+00:00")
    )
    assert isinstance(data["created_by_user_id"], int)
    assert isinstance(data["created_at"], str)
    assert data["is_active"] is True
    assert (
        session.execute(
            select(RideModel).filter(RideModel.id == data["id"])
        ).first()
        is not None
    )

def test_get_ride_by_code_success(
        test_client: TestClient,
        test_ride: RideModel,
):
    expected_response = {
        "id": ANY,
        "code": test_ride.code,
        "title": ANY,
        "description": ANY,
        "start_time": ANY,
        "created_by_user_id": ANY,
        "created_at": ANY,
        "is_active": ANY,
    }

    response = test_client.get(f"/rides/code/{test_ride.code}")

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response
    




