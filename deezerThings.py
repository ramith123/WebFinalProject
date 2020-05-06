import requests
from termcolor import colored
from model import Song

trackUrl = "https://api.deezer.com/track/"
serachUrl = "https://api.deezer.com/search?q="


def getJsonForSearch(query):  # get json data for a search query
    url = serachUrl + query
    reply = requests.get(url)
    return reply.json()["data"]


def getSongsList(query):  # get SongList with required information
    data = getJsonForSearch(query)
    songList = []
    for song in data:
        track = {
            "id": song["id"],
            "title": song["title"],
            "artist": song["artist"]["name"],
            "album": song["album"]["title"],
            "albumImgUrl": song["album"]["cover_big"],
            "url": song["link"],
        }
        songList.append(track)
    return songList


def getSongModel(song):

    ele = Song(
        id=song["id"],
        title=song["title"],
        artist=song["artist"],
        album=song["album"],
        albumImgUrl=song["albumImgUrl"],
        url=song["url"],
    )
    return ele


# pip install termcolor before executing this file
if __name__ == "__main__":

    l = getSongsList("James bay")
    l1 = getSongModel(l[0])
