
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_login_admin():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin123*"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "ADMIN"


def test_login_user():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "usuario", "password": "Usuario123*"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "USER"


def test_admin_access():
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "Admin123*"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/admin",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_user_access():
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "usuario", "password": "Usuario123*"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/user",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_user_cannot_access_admin():
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "usuario", "password": "Usuario123*"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/admin",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

def test_user_cannot_create_candidate():
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "usuario", "password": "Usuario123*"}
    )
    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/candidatos",
        json={
            "nombre": "Candidato prueba",
            "propuesta": "Mejorar los espacios universitarios",
            "eleccion_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_user_cannot_delete_candidate():
    login = client.post(
        "/api/v1/auth/login",
        data={"username": "usuario", "password": "Usuario123*"}
    )
    token = login.json()["access_token"]

    response = client.delete(
        "/api/v1/candidatos/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    