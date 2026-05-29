from flask import request, session
from config import app, db
from models import User, Note
from schemas import user_schema


@app.route("/")
def index():
    return {"message": "Secure Notes API"}, 200

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

if __name__ == "__main__":
    app.run(port=5555, debug=True)