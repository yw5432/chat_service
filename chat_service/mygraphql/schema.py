import strawberry
from mygraphql.resolvers import resolve_get_user_by_email, resolve_get_chat_history, resolve_fetch_friend_list, resolve_get_user_by_id
from mygraphql.type import User, Friend, Message


@strawberry.type
class Query:
    @strawberry.field
    def get_user_by_email(self, email: str) -> User:
        return resolve_get_user_by_email(email)

    @strawberry.field
    def get_user_by_id(self, user_id: int) -> User:
        return resolve_get_user_by_id(user_id)

    @strawberry.field
    def get_chat_history(self, sender_id: int, recipient_id: int) -> list[Message]:
        return resolve_get_chat_history(sender_id, recipient_id)

    @strawberry.field
    def fetch_friend_list(self, user_id: int) -> list[Friend]:
        return resolve_fetch_friend_list(user_id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def log_message(self, sender_id: int, recipient_id: int, message: str) -> str:
        return resolve_log_message(sender_id, recipient_id, message)

    @strawberry.mutation
    def google_login(self, email: str, username: str) -> str:
        return resolve_google_login(email, username)


schema = strawberry.Schema(query=Query, mutation=Mutation)
