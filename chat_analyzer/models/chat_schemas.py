from marshmallow import Schema, fields


class MessageSchema(Schema):
    sender = fields.Str()
    date = fields.Str()
    text = fields.Str()


class ChatSchema(Schema):
    participants = fields.List(fields.Str())
    messages = fields.Nested(MessageSchema, many=True)
