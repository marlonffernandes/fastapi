from http import HTTPStatus

# Tests must run independently
# Testing fake database


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


def test_read_user(client):
    response = client.get('/users/')  # act
    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testusername',
                'email': 'testemail@example.com',
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('users/1')
    assert response.json() == {'message': 'User deleted'}
