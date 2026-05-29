import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from config import db
from models import User, Note


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()

        user_1 = User(username="test_user")
        user_1.password = "password123"

        user_2 = User(username="other_user")
        user_2.password = "password123"

        db.session.add_all([user_1, user_2])
        db.session.commit()

        note_1 = Note(
            title="Test User Note",
            content="This note belongs to test_user.",
            user_id=user_1.id,
        )

        note_2 = Note(
            title="Other User Note",
            content="This note belongs to other_user.",
            user_id=user_2.id,
        )

        db.session.add_all([note_1, note_2])
        db.session.commit()

        with app.test_client() as test_client:
            yield test_client

        db.session.remove()
        db.drop_all()