from flask_jwt_extended import get_jwt_identity
from backend.auth.models import User
from backend.auth.queries import get_user_by_id_query


def get_logged_in_user() -> User:
    user_id = get_jwt_identity()
    user = get_user_by_id_query(user_id)
    if not user:
        raise Exception("Logged in user not found")
    return user