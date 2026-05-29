from config import app, db
from models import User, Note


with app.app_context():
    print("Clearing old data...")

    Note.query.delete()
    User.query.delete()

    print("Creating users...")

    user_1 = User(username="demo_user")
    user_1.password = "password123"

    user_2 = User(username="second_user")
    user_2.password = "password123"

    db.session.add_all([user_1, user_2])
    db.session.commit()

    print("Creating notes...")

    notes = [
        Note(
            title="First Demo Note",
            content="This is a note that belongs to demo_user.",
            user_id=user_1.id,
        ),
        Note(
            title="Project Ideas",
            content="Build a secure notes API with session auth.",
            user_id=user_1.id,
        ),
        Note(
            title="Second User Note",
            content="This note belongs to second_user and should stay private.",
            user_id=user_2.id,
        ),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("Seed complete!")