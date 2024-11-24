from database import db

# 存储
def log_message_to_db(sender, recipient, message):
    try:
        with db.cursor() as cursor:
            cursor.execute("select id from users where username = %s", (sender,))
            sender_result = cursor.fetchone()
            if sender_result is None:
                print(f"Sender {sender} does not exist in the database.")
                return
            sender_id = sender_result[0]

            cursor.execute("select id from users where username = %s", (recipient,))
            recipient_result = cursor.fetchone()
            if recipient_result is None:
                print(f"Recipient {recipient} does not exist in the database.")
                return
            recipient_id = recipient_result[0]
            sql = "insert into messages (sender_id, recipient_id, message) values (%s, %s, %s)"
            cursor.execute(sql, (sender_id, recipient_id, message))
            db.commit()
    except Exception as e:
        print(f"Error logging message to DB: {e}")

# 获取记录
def get_chat_history(sender, recipient):
    try:
        with db.cursor() as cursor:
            cursor.execute("select id from users where username = %s", (sender,))
            sender_id = cursor.fetchone()[0]
            cursor.execute("select id from users where username = %s", (recipient,))
            recipient_id = cursor.fetchone()[0]

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
            cursor.execute("SELECT * FROM users WHERE id = %s", (userid,))
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1]}  # Adjust fields as per your DB schema
            else:
                return None
    except Exception as e:
        print(f"Error retrieving user by ID: {e}")
        return None