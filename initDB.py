from app import app
from model import db

# import deezerAndYoutubeThings as dez

# db.init_app(app)
db.create_all(app=app)

# temp test
# import deezerThings
# from model import User, Playlist

# get song list for a certain query
# li = dez.getSongsList("let it go")
# for song in li:
#     print(song["youtubeUrl"])
# Get the model for a certain song from the above list
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

# if __name__ == "__main__":
#     playlists = Playlist.query.filter_by(userid="2").all()
#     print(playlists[0].songs)
