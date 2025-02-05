from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_should_return_ok_and_hello_world(client):
    response = client.get('/')  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Hello, World!'}  # assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'testpassword',
        },
    )  # act
    assert response.status_code == HTTPStatus.CREATED  # assert
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'testemail@example.com',
    }  # assert


def test_create_user_email_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': user.email,
            'password': 'testpassword',
        },
    )  # act
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_username_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'testemail@example.com',
            'password': 'testpassword',
        },
    )  # act
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client):
    response = client.get('/users/')  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'test123',
        },
    )  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'testemail@example.com',
    }  # assert


def test_update_non_existent_user(client):
    response = client.put(
        '/users/4000',
        json={
            'username': 'testusername',
            'email': 'testemail@example.com',
            'password': 'test123',
        },
    )  # act
    assert response.status_code == HTTPStatus.NOT_FOUND  # assert
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('users/1')
    assert response.json() == {'message': 'User deleted'}


def test_delete_non_existent_user(client):
    response = client.delete('users/4000')
    assert response.status_code == HTTPStatus.NOT_FOUND  # assert
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
