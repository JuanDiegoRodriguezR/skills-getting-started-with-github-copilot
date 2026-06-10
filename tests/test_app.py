from urllib.parse import quote

from src.app import activities


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_activity(client):
    activity_name = quote("Chess Club")
    email = "test@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    activity_name = quote("Chess Club")
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant(client):
    activity_name = quote("Chess Club")
    email = "daniel@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email)}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    activity_name = quote("Chess Club")
    email = "ghost@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_missing_activity_returns_404(client):
    activity_name = quote("Nonexistent Club")
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={quote(email)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
