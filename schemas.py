from marshmallow import Schema, fields, EXCLUDE


class MessageSchema(Schema):
    phone_number = fields.Str(required=True, data_key="from")
    text = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class StatusEventSchema(Schema):
    phone_number = fields.Str(required=True, data_key="recipient_id")
    status = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE
