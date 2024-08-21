import services, schemas, logging
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

logger = logging.getLogger(__name__)
webhook_blueprint = Blueprint("webhook", __name__)
questionnaire_blueprint = Blueprint("questionnaire", __name__)


@webhook_blueprint.route("/start_questionnaire", methods=["GET"])
def start_questionnaire():
    phone_number = request.args.get("phone_number")
    if phone_number:
        services.start_questionnaire(phone_number)
        return jsonify({"status": "Questionnaire started"}), 200
    else:
        return jsonify({"error": "Phone number is required"}), 400


# Iterate over the received messages and call handle_questionnaire for each message.
@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if entrys := data.get("entry"):
        entry = entrys[0]

        for change in entry.get("changes", []):
            value = change["value"]

            for event in value.get("statuses", []):
                try:
                    status_schema = schemas.StatusEventSchema()
                    validated_status = status_schema.load(event)
                    logger.info(validated_status)
                except ValidationError as err:
                    logger.warning(f"Validation error in status event: {err.messages}")

            for message in value.get("messages", []):
                try:
                    message_schema = schemas.MessageSchema()
                    text = (
                        message.get("text", {}).get("body")
                        or message.get("button", {}).get("payload")
                        or message.get("interactive", {})
                        .get("button_reply")
                        .get("title")
                    )
                    validated_message = message_schema.load(
                        {"from": message["from"], "text": text}
                    )
                    services.handle_questionnaire(
                        validated_message["phone_number"], validated_message["text"]
                    )
                except ValidationError as err:
                    logger.warning(f"Validation error in message: {err.messages}")

    return "EVENT_RECEIVED", 200


@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_verify():
    verified, challenge = services.isVerify()
    if verified:
        return challenge, 200
    else:
        return "Forbidden", 403
