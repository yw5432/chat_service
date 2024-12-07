from database import db_user_credential,db_user_chat

# 存储
def log_message_to_db(sender_id: int, recipient_id: int, message: str):
    try:
        with db_user_chat.cursor() as cursor:
            sql = "insert into messages (sender_id, recipient_id, message) values (%s, %s, %s)"
            cursor.execute(sql, (sender_id, recipient_id, message))
            db_user_chat.commit()
    except Exception as e:
        print(f"Error logging message to DB: {e}")

# 获取记录
def get_chat_history(sender_id: int, recipient_id: int):
    try:
        with db_user_chat.cursor() as cursor:
            sql = (
                "select sender_id, recipient_id, message, timestamp "
                "from messages "
                "where (sender_id = %s and recipient_id = %s) "
                "or (sender_id = %s and recipient_id = %s) "
                "order by timestamp asc"
            )
            cursor.execute(sql, (sender_id, recipient_id, recipient_id, sender_id))
            messages = cursor.fetchall()
            return messages
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return []

def get_user_by_id(userid):
    try:
        with db_user_credential.cursor() as cursor:
            cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (userid,))
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            else:
                return None
    except Exception as e:
        print(f"Error retrieving user by ID: {e}")
        return None

def get_user_by_email(email: str):
    try:
        with db_user_credential.cursor() as cursor:
            cursor.execute("SELECT id, username, email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            else:
                return None
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None

