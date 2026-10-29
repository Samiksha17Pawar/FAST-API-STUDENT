from fastapi.testclient import TestClient
from main import app, DATA_FILE

client = TestClient(app)


def setup_function():
    DATA_FILE.write_text("[]", encoding="utf-8")


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_add_student():
    response = client.post(
        "/students",
        json={
            "name": "Aarav",
            "roll_no": "MCA101",
            "marks": 85,
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Aarav"


def test_invalid_marks():
    response = client.post(
        "/students",
        json={
            "name": "Meera",
            "roll_no": "MCA102",
            "marks": 150,
        },
    )

    assert response.status_code == 422


def test_update_student():
    created = client.post(
        "/students",
        json={"name": "Aarav", "roll_no": "MCA101", "marks": 85},
    )
    student_id = created.json()["id"]

    response = client.put(
        f"/students/{student_id}",
        json={"name": "Aarav Updated", "roll_no": "MCA101", "marks": 90},
    )

    assert response.status_code == 200
    assert response.json()["marks"] == 90


def test_delete_student():
    created = client.post(
        "/students",
        json={"name": "Aarav", "roll_no": "MCA101", "marks": 85},
    )
    student_id = created.json()["id"]

    response = client.delete(f"/students/{student_id}")

    assert response.status_code == 204
    assert client.get(f"/students/{student_id}").status_code == 404