import datetime
import os

from .db import db
from .app import app


class Artwork(db.Model):
    '''
    A SQLAlchemy model corresponding to a single artwork.
    '''
    __tablename__ = "artworks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text())

    price_cents = db.Column(db.Integer())
    sold = db.Column(db.Boolean(), nullable=False, default=False)

    width = db.Column(db.Float())
    length = db.Column(db.Float())
    depth = db.Column(db.Float())

    added = db.Column(db.TIMESTAMP, default=datetime.datetime.now())

    # the use_alter is important, because these rows mutually
    # reference each other.

    primary_image_id = db.Column(db.Integer(),
                                 db.ForeignKey('artwork_images.id',
                                               use_alter=True,
                                               name='fk_primary_image'))

    primary_image = db.relationship('ArtworkImage',
                                    uselist=False,
                                    primaryjoin="Artwork.primary_image_id == ArtworkImage.id")

    images = db.relationship('ArtworkImage',
                             primaryjoin="Artwork.id == ArtworkImage.artwork_id")


class ArtworkImage(db.Model):
    '''
    A SQLAlchemy model corresponding to an image of an artwork.
    '''
    __tablename__ = "artwork_images"

    IMAGE_FORMAT = 'png'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))

    caption = db.Column(db.Text())

    artwork_id = db.Column(db.Integer,
                           db.ForeignKey('artworks.id'),
                           nullable=False)

    def filepath(self):
        return os.path.join(app.config['UPLOAD_FOLDER'],
                            "{}.{}".format(self.id, ArtworkImage.IMAGE_FORMAT))
