import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
        LDAP_SERVER=os.environ.get('FLASK_LDAP_SERVER'),
        LDAP_ROOT_DN=os.environ.get('FLASK_LDAP_ROOT_DN')

    )

    from . import db
    db.init_app(app)

    from . import survey
    app.register_blueprint(survey.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app