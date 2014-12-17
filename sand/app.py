from flask import Flask

app = Flask(__name__, static_folder='static')

DEVELOPMENT_CONFIGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///./development.db',
    'UPLOAD_FOLDER': 'uploads/',
    'STATIC_FOLDER': 'static/'
}

app.config.update(DEVELOPMENT_CONFIGS)
