from werkzeug.security import generate_password_hash, check_password_hash
from database import db


# 注册
def register_user(username, password):
    try:
        hashed_password = generate_password_hash(password)
        with db.cursor() as cursor:
            sql = "insert into users (username, password) values (%s, %s)"
            cursor.execute(sql, (username, hashed_password))
            db.commit()
        return {"status": "success", "message": f"User {username} registered successfully."}
    except Exception as e:
        return {"status": "failure", "message": str(e)}

def authenticate_user(username, password):
    try:
        with db.cursor() as cursor:
            sql = "select password from users where username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result and check_password_hash(result[0], password):
                return True
        return False
    except Exception as e:
        return False