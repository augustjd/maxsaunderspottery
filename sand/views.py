import os

from .api import app, db

from flask import send_from_directory

join = os.path.join

@app.route('/')
def index():
    return send_from_directory(join(app.static_folder, 'templates/'), 'index.html')


@app.route('/admin')
def admin_index():
    return send_from_directory(join(app.static_folder, 'templates/admin'), 'index.html')
