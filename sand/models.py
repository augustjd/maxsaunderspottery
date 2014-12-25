import datetime
import os
import shutil

from sqlalchemy import event
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
                             primaryjoin="Artwork.id == ArtworkImage.artwork_id",
                             backref='artwork')


def artwork_image_filepath(artwork_id, artwork_image_id=None, is_primary=True):
    if is_primary:
        return os.path.join(app.config['UPLOAD_FOLDER'],
                            "{}.{}".format(artwork_id,
                                           ArtworkImage.IMAGE_FORMAT))
    else:
        return os.path.join(app.config['UPLOAD_FOLDER'],
                            "{}-{}.{}".format(artwork_id, artwork_image_id,
                                              ArtworkImage.IMAGE_FORMAT))


@event.listens_for(Artwork.primary_image_id, 'set', retval=True)
def copy_image_to_primary_image_slot(target, value, oldvalue, initiator):
    artwork_id = target.id

    current_path = artwork_image_filepath(artwork_id, value, is_primary=False)
    artwork_image_path = artwork_image_filepath(artwork_id)
    try:
        print("Since {} is now primary, copying {} to {}".format(
            value, current_path, artwork_image_path))

        shutil.copyfile(current_path, artwork_image_path)

        return value
    except IOError:
        print("Failed to copy {} to {}. Rolling back primary id to {}".format(
            current_path, artwork_image_path, oldvalue))

        return oldvalue


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

    def url(self):
        return os.path.relpath(self.filepath())

    def is_primary(self):
        return self.artwork.primary_image_id == self.id

    def filepath(self):
        return artwork_image_filepath(self.artwork_id,
                                      self.id, self.is_primary)
