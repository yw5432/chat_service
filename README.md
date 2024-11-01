# W4153 Chat Service

This microservice provides group chat and private messaging functionalities, utilizing WebSocket for real-time communication and MySQL for database management. The service allows user group creation, and joining of chat groups.

## Usage

Ensure a `.env` file is present in the root directory with the necessary credentials for connecting to the database and configuration details.

### Example .env file

```plaintext
# DB credentials
DB_HOST=
DB_USER=admin
DB_PASSWORD=
DB_NAME=chat_service
DB_PORT=

# Application settings
SERVER_PORT=
JWT_SECRET=your_jwt_secret
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

1. **`/auth/signup`**  
   Allows users to create a new account.  

2. **`/auth/login`**  
   Authenticates an existing user.

3. **`/create-group`**  
   Allows an authenticated user to create a new chat group.

4. **`/join-group`**  
   Allows an authenticated user to join an existing chat group.

5. **`/chat-history`**  
   Retrieves the chat history between two users or within a group.

6. **WebSocket: `/ws/{username}`**  
   Establishes a WebSocket connection for real-time messaging, supporting private and group chats.

## WebSocket Messaging

To send messages via WebSocket, use the following message formats:

- **Private Message**:  
  `"{recipient}:{message}"`

- **Group Message**:  
  `"group:{group_name}:{message}"`

These formats allow users to send private messages to a single recipient or broadcast messages to a group they have joined.
