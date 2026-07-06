from tests.config_test import client

# test user registration
def test_register_user():
    response = client.post("/auth/register", json={
        "name": "user1",
        "email": "user1@abc.com",
        "password": "user1"
    })
    
    assert response.status_code == 201
    assert response.json()["email"] == 'user1@abc.com'