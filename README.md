# Secure Notes API

## Project Description

Secure Notes API is a Flask backend application that supports session-based user authentication and protected CRUD actions for user-owned notes.

The API allows users to sign up, log in, stay authenticated through a Flask session, log out, and manage private notes. Each note belongs to a specific user, and protected routes ensure that users can only view, create, update, or delete their own notes.

This backend was built for a full-auth Flask API lab focused on authentication, authorization, password protection, database relationships, pagination, and RESTful resource routing.

## Features

* Session-based authentication
* User signup, login, check session, and logout
* Secure password hashing with Flask-Bcrypt
* User-owned notes resource
* Full CRUD actions for notes
* Pagination on the notes index route
* Route protection for authenticated users only
* Ownership protection so users cannot access or modify another user's notes
* Database migrations with Flask-Migrate
* Seed file for starter users and notes
* Backend pytest coverage for authentication and notes routes

## Tech Stack

* Python 3.9
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Bcrypt
* Marshmallow
* Pytest
* SQLite
* Pipenv

## Project Structure

```txt
secure-notes-api/
├── client-with-sessions/ # Provided React client for visual auth testing
├── server/               # Flask API backend
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── migrations/
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_notes.py
│   └── instance/
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```
This project was developed with Python 3.9.13.
## Models

### User

The `User` model handles authentication and owns notes.

Fields:

* `id`
* `username`
* `password_hash`

The app does not store plain text passwords. Passwords are passed through a write-only `password` property and hashed with Flask-Bcrypt before being saved to `password_hash`.

### Note

The `Note` model is the protected user-owned resource.

Fields:

* `id`
* `title`
* `content`
* `user_id`

Each note belongs to one user through the `user_id` foreign key.

## Relationships

```txt
User has many Notes
Note belongs to one User
```

A user can have many notes, and each note belongs to exactly one user.

## Installation

From the project root, install dependencies with Pipenv:

```bash
pipenv install
```

If needed, install the required backend packages manually:

```bash
pipenv install flask==2.2.2 flask-sqlalchemy==3.0.3 Werkzeug==2.2.2 marshmallow==3.20.1 faker==15.3.2 flask-migrate==4.0.0 flask-restful==0.3.9 importlib-metadata==6.0.0 importlib-resources==5.10.0 pytest==7.2.0 flask-bcrypt==1.0.1 SQLAlchemy==1.4.46 greenlet==2.0.2
```

## Database Setup

Move into the backend folder:

```bash
cd server
```

Set the Flask app:

```bash
export FLASK_APP=app.py
```

If setting up migrations from scratch:

```bash
pipenv run flask db init
pipenv run flask db migrate -m "Initial migration"
```

Run migrations:

```bash
pipenv run flask db upgrade head
```



## Seed the Database

From the `server/` folder, run:

```bash
pipenv run python seed.py
```

The seed file clears existing users and notes, creates starter users, hashes their passwords, and adds sample notes owned by those users.

## Run the Backend

From the `server/` folder:

```bash
pipenv run python app.py
```

The Flask API runs on:

```txt
http://127.0.0.1:5555
```

## Optional Frontend Testing

A provided session-based React client is included in:

```txt
client-with-sessions/
```

```bash
cd client-with-sessions
npm install
PORT=4000 npm start
```

The frontend is useful for visually testing signup, login, check session, and logout.

## API Endpoints

### Root

#### `GET /`

Returns a basic API status message.

Success response:

```json
{
  "message": "Secure Notes API"
}
```

---

## Auth Endpoints

### `POST /signup`

Creates a new user, hashes their password, stores the user id in the session, and returns safe user data.

Request body:

```json
{
  "username": "new_user",
  "password": "password123",
  "password_confirmation": "password123"
}
```

Success response:

```json
{
  "id": 1,
  "username": "new_user"
}
```

Possible errors:

* Missing username/password fields
* Password confirmation does not match
* Username already exists

---

### `POST /login`

Authenticates an existing user and stores their id in the session.

Request body:

```json
{
  "username": "new_user",
  "password": "password123"
}
```

Success response:

```json
{
  "id": 1,
  "username": "new_user"
}
```

Possible errors:

* Missing username/password
* Invalid username or password

---

### `GET /check_session`

Checks whether a user is currently logged in.

Success response:

```json
{
  "id": 1,
  "username": "new_user"
}
```

Error response:

```json
{
  "errors": ["Unauthorized"]
}
```

---

### `DELETE /logout`

Clears the current session.

Success response:

```txt
204 No Content
```

---

## Notes Endpoints

All notes routes require an authenticated session.

### `GET /notes?page=1&per_page=10`

Returns paginated notes owned by the logged-in user.

Success response:

```json
{
  "notes": [
    {
      "id": 1,
      "title": "Example Note",
      "content": "This is the note content.",
      "user_id": 1
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 1,
  "pages": 1
}
```

Unauthorized response:

```json
{
  "errors": ["Unauthorized"]
}
```

---

### `POST /notes`

Creates a new note for the logged-in user.

Request body:

```json
{
  "title": "Example Note",
  "content": "This is the note content."
}
```

Success response:

```json
{
  "id": 1,
  "title": "Example Note",
  "content": "This is the note content.",
  "user_id": 1
}
```

Possible errors:

* Unauthorized
* Missing title or content

---

### `PATCH /notes/<id>`

Updates a note owned by the logged-in user.

Request body:

```json
{
  "title": "Updated Note",
  "content": "Updated note content."
}
```

Success response:

```json
{
  "id": 1,
  "title": "Updated Note",
  "content": "Updated note content.",
  "user_id": 1
}
```

Possible errors:

* Unauthorized
* Note not found

The route only updates a note if the note id belongs to the current session user.

---

### `DELETE /notes/<id>`

Deletes a note owned by the logged-in user.

Success response:

```txt
204 No Content
```

Possible errors:

* Unauthorized
* Note not found

The route only deletes a note if the note id belongs to the current session user.

## Testing

Backend tests are located in:

```txt
server/tests/
```

Run the test suite from the `server/` folder:

```bash
pipenv run pytest
```

Current test coverage includes:

* Signup
* Duplicate signup rejection
* Login
* Invalid login rejection
* Check session
* Logout
* Protected notes access
* Paginated notes index
* Create note
* Update note
* Delete note
* Ownership protection for another user's notes

Latest result:

```txt
14 passed
```

## Security Notes

* Plain text passwords are never stored in the database.
* Passwords are hashed with Flask-Bcrypt.
* Serialized user responses do not expose `password_hash`.
* Notes are always queried by the current session user's id.
* Users cannot view, update, or delete notes that belong to another user.
* Unauthenticated requests to protected routes return an unauthorized error.
