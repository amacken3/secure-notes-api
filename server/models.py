from config import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    notes = db.relationship("Note", back_populates="user", cascade="all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("Password cannot be read.")
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def authenticate(self, plain_text_password):
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)
    
    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    user = db.relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"