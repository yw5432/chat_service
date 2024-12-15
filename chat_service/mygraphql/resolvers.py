from message import get_user_by_email, get_user_by_id, get_chat_history, fetch_friend_list
from mygraphql.type import Message, User, Friend


def resolve_get_user_by_email(email: str)-> User:
    user = get_user_by_email(email)
    if user:
        return User(id=user["id"], email=user["email"], username=user["username"])
    return None

def resolve_get_chat_history(sender_id: int, recipient_id: int) -> list[Message]:
    raw_messages = get_chat_history(sender_id, recipient_id)

    return [
        Message(
            sender_id=row[0],
            recipient_id=row[1],
            message=row[2],
            timestamp=row[3].isoformat()
        )
        for row in raw_messages
    ]


def resolve_get_user_by_id(user_id: int)-> User:
    user = get_user_by_id(user_id)
    if user:
        return User(id=user["id"], email=user["email"], username=user["username"])
    return None

def resolve_fetch_friend_list(user_id: int) -> list[Friend]:
    raw_friends = fetch_friend_list(user_id)
    return [
        Friend(
            friend_id=friend["friend_id"],
            username=friend["username"],
            email=friend["email"]
        )
        for friend in raw_friends
    ]
