from flask import Flask
import logging
from views import webhook_blueprint




app = Flask(__name__)

# Import and register blueprints, if any
app.register_blueprint(webhook_blueprint)


if __name__ == "__main__":
    logging.info("Flask app started")

    app.run(port=8000, debug=True)

   


