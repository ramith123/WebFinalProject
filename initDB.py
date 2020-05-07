from app import app
from model import db
import deezerAndYoutubeThings as dez

# db.init_app(app)
db.create_all(app=app)

# temp test
# import deezerThings
# from model import User, Playlist


li = dez.getSongsList("let it go")
for song in li:
    print(song["youtubeUrl"])

# song = deezerThings.getSongModel(li[0])
# print(song)
# # user = User(username="hi", password="hi")
# # playlist = Playlist(name="playlist1", userid="1")
# user = User.query.filter_by(id="1").first()
# playlist = Playlist.query.filter_by(id="3").first()

# playlist.songs.append(song)
# print(user.playlists)

# db.session.add(playlist)
# db.session.commit()
