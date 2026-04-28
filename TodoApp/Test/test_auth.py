from TodoApp.routers.auth import get_db, get_current_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from TodoApp.Test.utils import *
from fastapi import status, HTTPException
from jose import jwt
from datetime import timedelta, datetime, timezone
import pytest

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existing_user = authenticate_user("nonexistent", "testpassword", db)
    assert non_existing_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False

def test_create_access_token(test_user):
    username = 'testuser' 
    user_id = 1
    role = 'admin'
    expires_delta = timedelta(minutes=15)

    token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})

    assert decoded_token.get('sub') == username
    assert decoded_token.get('id') == user_id
    assert decoded_token.get('role') == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {"username": "testuser", "id": 1, "role": 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == 'Could not validate credentials'


