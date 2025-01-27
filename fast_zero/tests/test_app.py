from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_read_root_should_return_ok_and_hello_world():
    client = TestClient(app)  # arrange
    response = client.get("/")  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {"message": "Hello, World!"}  # assert


def test_create_user():
    client = TestClient(app)

    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "email": "testemail@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
