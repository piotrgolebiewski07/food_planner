import pytest
from food_planner_app import create_app, db
from config import TestingConfig
from food_planner_app.commands.db_manage_commands import add_data

@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
        

@pytest.fixture
def user(client):
    user = {
        "username": "test",
        "password": "123456",
        "email": "test@gmail.com"
    }
    client.post("/api/v1/auth/register", json=user)
    return user


@pytest.fixture
def token(client, user):
    response = client.post('/api/v1/auth/login', json={
        'username': user['username'],
        'password': user['password']
    })
    return response.get_json()['token']


@pytest.fixture
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)

