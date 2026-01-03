# Secure Notes API – FastAPI

A backend REST API built with FastAPI that allows users to securely
create and manage personal notes.

## Features
- User Signup & Login
- Password hashing using bcrypt
- JWT-based authentication
- Protected routes
- User-specific Notes (CRUD)
- Notes are accessible only by their owner

## Tech Stack
- FastAPI
- SQLModel
- SQLite
- JWT Authentication

## Project Structure
- main.py – application entry point
- routers/ – API route definitions
- models.py – database models
- schemas.py – request/response validation
- database.py – database configuration

## How to Run
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Start the server:
   uvicorn main:app --reload
5. Open API docs:
   http://127.0.0.1:8000/docs

## Authentication

This API uses JWT (JSON Web Token)–based authentication.

After successful login, the server returns a JWT token.  
This token must be provided to access protected routes.

### How Authorization Works
- Login endpoint returns a JWT token
- Protected routes require this token
- Authentication is handled using `HTTPBearer`

### How to Use the Token in Swagger UI
1. Login using the `/login` endpoint
2. Copy the JWT token from the response
3. Click the **Authorize** button in Swagger UI
4. Paste the token **without adding `Bearer` manually**
5. Click **Authorize**
6. Access protected routes like notes CRUD endpoints


## Learning Outcome
This project helped me understand how real backend systems handle
authentication, authorization, and user-specific data access.

## Future Improvements
- Role-based access control
- Token refresh & logout
- PostgreSQL integration