# Book API

A RESTful API for managing books, built with **FastAPI** and **MongoDB**. This project includes authentication, book management, and basic statistical endpoints.

## 🚀 Features

- **User Authentication**: Register and Login (JWT based).
- **Book Management**: CRUD operations for books.
- **Search & Filtering**: Search books by title/author, filter by year.
- **Statistics**: Calculate average book price by year.
- **Containerized**: Fully Dockerized with MongoDB and Mongo Express.

## 🛠️ Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/) (Optional, for easier command execution)

## ⚙️ Setup & Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd book-api
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory. You can use the example below:

    ```env
    # MongoDB Connection
    MONGODB_URL=mongodb://mongodb:27017
    DATABASE_NAME=books_db
    
    # MongoDB Container Credentials
    MONGO_DB_NAME=books_db
    MONGO_ROOT_USER=admin
    MONGO_ROOT_PASSWORD=secretpassword
    
    # Mongo Express Credentials
    ME_BASIC_USER=admin
    ME_BASIC_PASSWORD=secretpassword

    # Security
    SECRET_KEY=your_super_secret_key_change_this
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # API Configuration
    API_V1_PREFIX=/api/v1
    ```

## 🏃‍♂️ Running the Project

You can use the provided `Makefile` for simplified commands:

| Command | Description |
| :--- | :--- |
| `make build` | Build the Docker containers |
| `make up` | Start the services in detached mode |
| `make stop` | Stop the services |
| `make restart` | Restart the services |
| `make down` | Stop and remove containers/volumes |
| `make logs` | View logs for the API service |

**Manual Docker Commands:**

If you don't have `make` installed:

```bash
# Build and Start
docker compose -f docker-compose.yml up -d --build

# Stop
docker compose -f docker-compose.yml stop
```

## 📚 API Documentation

Once the project is running, you can access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🗄️ Database Management

- **Mongo Express** is available for managing the database via a GUI.
- **URL**: [http://localhost:8081](http://localhost:8081)
- **Credentials**: Use `ME_BASIC_USER` and `ME_BASIC_PASSWORD` defined in your `.env`.

## 🔑 Default Credentials

The system automatically creates a default admin user on the first run (via migration):

- **Username**: `admin`
- **Password**: `admin123`

You can use these credentials to log in and get an access token.

## 📂 Project Structure

```
book-api/
├── backend/            # FastAPI Application code
│   ├── auth/           # Authentication module (models, services, views)
│   ├── books/          # Books module (models, services, views)
│   ├── db/             # Database connection and migrations
│   ├── main.py         # Application entry point
│   └── config.py       # Configuration settings
├── docker-compose.yml  # Docker services configuration
├── Dockerfile          # API container definition
├── Makefile            # Shortcut commands
└── requirements.txt    # Python dependencies
```