from flask import Flask
import logging
from views import webhook_blueprint, questionnaire_blueprint

app = Flask(__name__)

# Import and register blueprints
app.register_blueprint(webhook_blueprint)
app.register_blueprint(questionnaire_blueprint) 

# load_configurations(app) n esta a funcionar para os services

if __name__ == "__main__":
    logging.info("Flask app started")

    app.run(port=8000, debug=True)

   


