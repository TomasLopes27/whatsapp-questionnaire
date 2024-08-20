from flask import Flask
import logging
from views import webhook_blueprint, questionnaire_blueprint

logger = logging.getLogger(__name__)

app = Flask(__name__)


app.register_blueprint(webhook_blueprint)
app.register_blueprint(questionnaire_blueprint)


if __name__ == "__main__":
    logger.info("Flask app started")

    app.run(port=8000, debug=True)
