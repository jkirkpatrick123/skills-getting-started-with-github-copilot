import urllib.parse

from src import app as app_module


def test_root_redirects_to_index(client):
    # Arrange

    # Act
    resp = client.get("/", follow_redirects=False)

    # Assert
    assert resp.status_code == 307
    assert resp.headers["location"] == "/static/index.html"


def test_get_activities_returns_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    assert resp.json() == app_module.activities


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(path, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]
    assert email in resp.json()["message"]


def test_signup_already_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(path, params={"email": existing_email})

    # Assert
    assert resp.status_code == 400
    assert existing_email in app_module.activities[activity]["participants"]


def test_signup_activity_not_found_returns_404(client):
    # Arrange
    activity = "Nonexistent"
    email = "someone@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.post(path, params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Pre-check
    assert email in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(path, params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
    assert email in resp.json()["message"]


def test_unregister_not_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Ensure not signed up
    assert email not in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(path, params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_unregister_activity_not_found_returns_404(client):
    # Arrange
    activity = "Nonexistent"
    email = "someone@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    resp = client.delete(path, params={"email": email})

    # Assert
    assert resp.status_code == 404


def test_static_index_served(client):
    # Arrange

    # Act
    resp = client.get("/static/index.html")

    # Assert
    assert resp.status_code == 200
    assert "Mergington High School" in resp.text
