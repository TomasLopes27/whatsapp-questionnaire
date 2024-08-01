import services
from flask import Blueprint, request, jsonify

webhook_blueprint = Blueprint("webhook", __name__)


    


@webhook_blueprint.route("/start_questionnaire", methods=["GET"])
def start_questionnaire():
    phone_number = request.args.get('phone_number')
    if phone_number:
        services.start_questionnaire(phone_number)
        return jsonify({"status": "Questionnaire started"}), 200
    else:
        return jsonify({"error": "Phone number is required"}), 400

# Iterate over the received messages and call handle_questionnaire for each message.
@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and 'entry' in data:
        for entry in data['entry']:
            if 'changes' in entry:
                for change in entry['changes']:
                    if 'value' in change and 'messages' in change['value']:
                        for message in change['value']['messages']:
                            services.handle_questionnaire(message)

    return "EVENT_RECEIVED", 200

@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return services.verify()
