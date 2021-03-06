import os

from flask import request, jsonify
import flask.ext.restless
from werkzeug import secure_filename
from wand.image import Image

from .models import app, db, Artwork, ArtworkImage


manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Artwork,
                   methods=['GET', 'POST', 'PUT', 'DELETE'])

manager.create_api(ArtworkImage,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   include_methods=['url'])

SUPPORTED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tif'])


def is_image(filename):
    extension = os.path.splitext(filename)[1][1:]
    return extension in SUPPORTED_IMAGE_EXTENSIONS


def get_full_image_path(filepath):
    return os.path.join(app.config['UPLOAD_FOLDER'], filepath)


@app.route('/api/artwork_images/<int:id>/image', methods=['POST'])
def post_image(id):
    artwork_image = ArtworkImage.query.get(id)
    if artwork_image is None:
        message = 'No ArtworkImage with id {} was found.'.format(id)
        return jsonify({'message': message}), 400

    file = request.files['file']
    if file and is_image(file.filename):
        filename = secure_filename(file.filename)

        destination_path = get_full_image_path(filename)
        file.save(destination_path)

        if process_img(artwork_image, destination_path):
            os.remove(destination_path)

            message = '{} successfully uploaded and processed into {}.'\
                      .format(file.filename, artwork_image.filepath())
            return jsonify({'message': message})
        else:
            message = '{} could not be processed.' .format(file.filename)
            return jsonify({'message': message}), 500
    else:
        message = '{} is not a valid image (supported filetypes: {})'\
                  .format(file.filename, ', '.join(SUPPORTED_IMAGE_EXTENSIONS))
        return jsonify({'message': message}), 400


def process_img(artwork_image, path):
    destination_path = artwork_image.filepath()
    with Image(filename=path) as img:
        img.save(filename=destination_path)

    return os.path.isfile(destination_path)
