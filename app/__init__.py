from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mail.init_app(app)

    from .routes import init_routes
    init_routes(app)

    return app

app = create_app()
