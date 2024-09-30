from database import db


# 存储
def log_message_to_db(sender, recipient, message):
    try:
        with db.cursor() as cursor:
            cursor.execute("select id from users where username = %s", (sender,))
            sender_id = cursor.fetchone()[0]
            cursor.execute("select id from users where username = %s", (recipient,))
            recipient_id = cursor.fetchone()[0]

            sql = "insert into messages (sender_id, recipient_id, message) values (%s, %s, %s)"
            cursor.execute(sql, (sender_id, recipient_id, message))
            db.commit()
    except Exception as e:
        print(f"Error logging message to DB: {e}")

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