from marshmallow import Schema, fields


class MessageSchema(Schema):
    sender = fields.Str()
    date = fields.Str()
    text = fields.Str()


class ChatSchema(Schema):
    participants = fields.List(fields.Str())
    messages = fields.Nested(MessageSchema, many=True)


class UserMessageStatSchema(Schema):
    username = fields.Str()
    message_count = fields.Int()
    message_percent = fields.Float()
    word_count = fields.Int()
    word_percent = fields.Float()
    avg_words_per_message = fields.Float()


class ChatMessageStatSchema(Schema):
    total_messages_count = fields.Int()
    total_words_count = fields.Int()
    user_stats = fields.Nested(UserMessageStatSchema, many=True)


class ScoreSchema(Schema):
    label = fields.Str()
    value = fields.Float()


class MessagesPerDayStatSchema(Schema):
    date_sent = fields.Date()
    scores = fields.Nested(ScoreSchema, many=True)


class StatsWrapperSchema(Schema):
    legend = fields.List(fields.Str())
    stats = fields.Nested(MessagesPerDayStatSchema, many=True)
