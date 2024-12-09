from database import db

# 存储
def log_message_to_db(sender_id: int, recipient_id: int, message: str):
    try:
        with db.cursor() as cursor:
            sql = "insert into messages (sender_id, recipient_id, message) values (%s, %s, %s)"
            cursor.execute(sql, (sender_id, recipient_id, message))
            add_friend_to_list(sender_id, recipient_id)
            db.commit()
    except Exception as e:
        print(f"Error logging message to DB: {e}")

# 获取记录
def get_chat_history(sender_id: int, recipient_id: int):
    try:
        with db.cursor() as cursor:
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
        with db.cursor() as cursor:
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
        with db.cursor() as cursor:
            cursor.execute("SELECT id, username, email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            else:
                return None
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None

def add_friend_to_list(user_id: int, friend_id: int):
    try:
        with db.cursor() as cursor:
            sql = """
                INSERT IGNORE INTO friend_list (user_id, friend_id)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (user_id, friend_id))
            cursor.execute(sql, (friend_id, user_id))
    except Exception as e:
        print(f"Error adding friend to list: {e}")

def fetch_friend_list(user_id: int):
    try:
        with db.cursor() as cursor:
            sql = """
                SELECT f.friend_id, u.username, u.email
                FROM friend_list f
                JOIN users u ON f.friend_id = u.id
                WHERE f.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            friends = cursor.fetchall()
            return [{"friend_id": friend[0], "username": friend[1], "email": friend[2]} for friend in friends]
    except Exception as e:
        print(f"Error fetching friend list: {e}")
        return []

def log_user(email: str, username: str):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                sql = "INSERT INTO users (email, username) VALUES (%s, %s)"
                cursor.execute(sql, (email, username))
                db.commit()
                print(f"New user {email} added to the database.")
            else:
                sql = "UPDATE users SET username = %s WHERE email = %s"
                cursor.execute(sql, (username, email))
                db.commit()
                print(f"User {email} updated.")
    except Exception as e:
        print(f"Error logging Google user: {e}")