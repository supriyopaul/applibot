import uuid
import pytest
import requests

BASE_URL = "http://localhost:9000"  # Adjust if your server runs on a different address

@pytest.fixture(scope="session")
def test_user():
    """
    Generates a unique test user for this test session.
    """
    # Generate a unique email to avoid collisions on repeated runs
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123"
    return {"email": email, "password": password}

def test_signup(test_user):
    """
    Tests the signup endpoint.
    If the user already exists, the endpoint returns a 400 with "Email already registered".
    """
    url = f"{BASE_URL}/signup"
    response = requests.post(url, json=test_user)
    # Accept either a successful signup (200) or a 400 indicating duplicate registration
    if response.status_code == 400:
        assert "Email already registered" in response.text
    else:
        assert response.status_code == 200, f"Signup failed: {response.text}"
        json_data = response.json()
        assert json_data["email"] == test_user["email"]

def test_login(test_user):
    """
    Tests the login endpoint and stores the access token in the test_user dict.
    """
    url = f"{BASE_URL}/token"
    # The login endpoint expects form data with keys 'username' and 'password'
    data = {"username": test_user["email"], "password": test_user["password"]}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    json_data = response.json()
    assert "access_token" in json_data
    # Save the token for subsequent tests
    test_user["token"] = json_data["access_token"]

def test_update_openai_key(test_user):
    """
    Tests the endpoint to update the user's OpenAI API key.
    If the token is not available (login did not occur), the test is skipped.
    """
    if "token" not in test_user:
        pytest.skip("User not logged in; skipping OpenAI key update test.")
    # Use a trailing slash to ensure route matching
    url = f"{BASE_URL}/update_openai_key/"
    new_key = "sk-test-openai-key-123456"
    headers = {"token": test_user["token"]}
    data = {"new_openai_key": new_key}
    response = requests.post(url, data=data, headers=headers)
    assert response.status_code == 200, f"Failed to update OpenAI key: {response.text}"
    json_data = response.json()
    assert json_data.get("message") == "OpenAI API key updated successfully"

if __name__ == "__main__":
    pytest.main(["-v"])
