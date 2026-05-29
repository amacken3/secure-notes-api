from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()

class NoteSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    user_id = fields.Integer()


user_schema = UserSchema()

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)