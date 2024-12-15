import strawberry
@strawberry.type
class User:
    id: int
    email: str
    username: str

@strawberry.type
class Message:
    sender_id: int
    recipient_id: int
    message: str
    timestamp: str

@strawberry.type
class Friend:
    friend_id: int
    username: str
    email: str