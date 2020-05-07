import requests

# from termcolor import colored
from model import Song

trackUrl = "https://api.deezer.com/track/"
serachUrl = "https://api.deezer.com/search?q="
youtubeApiKey = "AIzaSyC0VqCv-KW7cRsmYBUUHHqTJeRBTVnP-h0"
search_url = "https://www.googleapis.com/youtube/v3/search"
youtubeVideoLink = "https://www.youtube.com/watch?v="


def getJsonForSearch(query):  # get json data for a search query
    url = serachUrl + query
    reply = requests.get(url)
    return reply.json()["data"]


def getSongsList(query):  # get SongList with required information
    data = getJsonForSearch(query)
    songList = []
    for i, song in enumerate(data):
        track = {
            "id": song["id"],
            "title": song["title"],
            "artist": song["artist"]["name"],
            "album": song["album"]["title"],
            "albumImgUrl": song["album"]["cover_big"],
            "url": song["link"],
            # maybe add youtube link here. Cerate a separate function that will get artist and song name
        }
        if i < 3:
            track["youtubeUrl"] = getYoutubeLink(song["title"], song["artist"]["name"])
        else:
            track["youtubeUrl"] = getYoutubeLink(
                song["title"], song["artist"]["name"], True
            )
        songList.append(track)
    return songList


def getSongModel(song):  # returns sqlalchemy Song model for a song

    ele = Song(
        id=song["id"],
        title=song["title"],
        artist=song["artist"],
        album=song["album"],
        albumImgUrl=song["albumImgUrl"],
        url=song["url"],
        # youtubeUrl=getYoutubeLink(song["title"], song["artist"])
        youtubeUrl=song["youtubeUrl"],
    )
    return ele


def getYoutubeLink(song, artist, quota=False):
    query = song + " by " + artist
    search_params = {
        "key": youtubeApiKey,
        "q": query,
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
    }
    defaultLink = "https://www.youtube.com/results?search_query=" + query.replace(
        " ", "+"
    )
    if quota:
        return defaultLink
    r = requests.get(search_url, params=search_params)
    try:
        videoId = r.json()["items"][0]["id"]["videoId"]
        return youtubeVideoLink + videoId
    except KeyError:
        return defaultLink


# pip install termcolor before executing this file
# if __name__ == "__main__":

# print(getYoutubeLink("hello", "Adele"))
