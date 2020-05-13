from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    # email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    playlists = db.relationship("Playlist", backref="user", lazy="subquery")

    def set_password(self, password):
        self.password = generate_password_hash(password, "sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            # "email": self.email,
            "password": self.password,
        }


songs = db.Table(
    "songs",
    db.Column("playlistId", db.Integer, db.ForeignKey("playlist.id"), primary_key=True),
    db.Column("songId", db.Integer, db.ForeignKey("song.id"), primary_key=True),
)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    songs = db.relationship(
        "Song",
        secondary=songs,
        lazy="subquery",
        backref=db.backref("songPlaylists", lazy="dynamic"),
    )
    color = db.Column(db.String(256), nullable=False)

    def toDict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), nullable=False)
    album = db.Column(db.String(128), nullable=False)
    albumImgUrl = db.Column(db.String(512), nullable=False, unique=True)
    url = db.Column(db.String(512), nullable=False, unique=True)
    youtubeUrl = db.Column(db.String(512), nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "albumImgUrl": self.albumImgUrl,
            "url": self.url,
            "youtubeUrl": self.youtubeUrl,
        }
