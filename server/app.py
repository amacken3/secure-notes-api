from flask import request, session
from config import app, db
from models import User, Note
from schemas import user_schema, note_schema, notes_schema


@app.route("/")
def index():
    return {"message": "Secure Notes API"}, 200

def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return User.query.get(user_id)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not username or not password or not password_confirmation:
        return {"errors": ["Username, password, and password confirmation are required"]}, 400
    
    if password != password_confirmation:
        return {"errors": ["Password confirmation does not match password"]}, 400
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"errors": ["Username already exists"]}, 400
    
    new_user = User(username=username)
    new_user.password = password

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return user_schema.dump(new_user), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"errors": ["Username and password are required"]}, 400
    
    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session["user_id"] = user.id
        return user_schema.dump(user), 200

    return {"errors": ["Invalid username or password"]}, 401

@app.route("/check_session")
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return {"errors": ["Unauthorized"]}, 401

    user = User.query.get(user_id)

    if not user:
        session.pop("user_id", None)
        return {"errors": ["Unauthorized"]}, 401

    return user_schema.dump(user), 200

@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return {}, 204

@app.route("/notes", methods=["GET"])
def get_notes():
    current_user = get_current_user()

    if not current_user:
        return {"errors": ["Unauthorized"]}, 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Note.query.filter_by(user_id=current_user.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "notes": notes_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }, 200

@app.route("/notes", methods=["POST"])
def create_note():
    current_user = get_current_user()

    if not current_user:
        return {"errors": ["Unauthorized"]}, 401

    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return {"errors": ["Title and content are required"]}, 400

    note = Note(
        title=title,
        content=content,
        user_id=current_user.id
    )

    db.session.add(note)
    db.session.commit()

    return note_schema.dump(note), 201

@app.route("/notes/<int:id>", methods=["PATCH"])
def update_note(id):
    current_user = get_current_user()

    if not current_user:
        return {"errors": ["Unauthorized"]}, 401

    note = Note.query.filter_by(id=id, user_id=current_user.id).first()

    if not note:
        return {"errors": ["Note not found"]}, 404

    data = request.get_json() or {}

    if "title" in data:
        note.title = data["title"]

    if "content" in data:
        note.content = data["content"]

    db.session.commit()

    return note_schema.dump(note), 200

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    current_user = get_current_user()

    if not current_user:
        return {"errors": ["Unauthorized"]}, 401

    note = Note.query.filter_by(id=id, user_id=current_user.id).first()

    if not note:
        return {"errors": ["Note not found"]}, 404

    db.session.delete(note)
    db.session.commit()

    return {}, 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)