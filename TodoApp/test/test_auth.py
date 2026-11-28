from datetime import timedelta

from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt


app.dependency_overrides[get_db] = override_get_db()

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('gfgfffyfy', 'testpassword', db)
    assert non_existent_user is False


    wrong_password_user = authenticate_user(test_user.username, 'jhgjh', db)
    assert wrong_password_user is False

def test_create_access_token():
    username = 'sristy'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(minutes=10)

    token = create_access_token(username, user_id, role, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub': 'sristy', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm= ALGORITHM)

    user = await get_current_user(token = token)
    assert user == {'username': 'sristy', 'id': 1, 'role': 'admin'}
