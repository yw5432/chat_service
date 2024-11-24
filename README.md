# W4153 Chat Service

This microservice provides group chat and private messaging functionalities, utilizing WebSocket for real-time communication and MySQL for database management. The service allows user registration, login, group creation, and joining of chat groups.

## Usage

Ensure a `.env` file is present in the root directory with the necessary credentials for connecting to the database and configuration details.

### Example .env file

```plaintext
# DB credentials
DB_HOST=
DB_USER=admin
DB_PASSWORD=
DB_NAME=chat_service
```

### Setup

1. Install the dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

2. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload --port $SERVER_PORT
    ```

## OpenAPI Documentation

Visit the `/docs` endpoint in a browser to access detailed API documentation and interact with the available endpoints.

## API Endpoints

This service offers the following endpoints:

1. **`/chat-history`**  
   Retrieves the chat history between two users or within a group.

2. **WebSocket: `/ws/{username}`**  
   Establishes a WebSocket connection for real-time messaging, supporting private and group chats.

3. **`/get-user-id`**  
   Find the user based on the userid.
## WebSocket Messaging

To send messages via WebSocket, use the following message formats:

- **Private Message**:  
  `"{recipient}:{message}"`

- **Group Message**:  
  `"group:{group_name}:{message}"`

These formats allow users to send private messages to a single recipient or broadcast messages to a group they have joined.
