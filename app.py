from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask import Flask, request, render_template, redirect, flash, url_for
import os
import requests
from isodate import parse_duration

# from sqlalchemy.exc import IntegrityError
# from datetime import timedelta

from model import db, User
from forms import Register, Login

# import json


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


""" Begin boilerplate code """


def create_app():
    app = Flask(__name__, static_url_path="")
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgres://hxzhttja:6A7fF17bjLUaeditu817xyU7x0AOzZTh@drona.db.elephantsql.com:5432/hxzhttja"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SECRET_KEY"] = "c3a93f55-2015-4042-9ef7-77de85976f78"
    login_manager.init_app(app)

    app.config["YOUTUBE_API_KEY"] = "AIzaSyC0VqCv-KW7cRsmYBUUHHqTJeRBTVnP-h0"

    # =======
    # """ Begin boilerplate code """

    # persistenceUrl = "postgres://hxzhttja:6A7fF17bjLUaeditu817xyU7x0AOzZTh@drona.db.elephantsql.com:5432/hxzhttja"
    # def create_app():
    #     app = Flask(__name__, static_url_path="")
    #     app.config["SQLALCHEMY_DATABASE_URI"] = persistenceUrl
    #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    #     # app.config['SECRET_KEY'] = "c3a93f55-2015-4042-9ef7-77de85976f78"
    #     # app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7)
    # >>>>>>> Ramith-working
    db.init_app(app)
    return app


app = create_app()

app.app_context().push()


@app.route("/")
def hello():
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    videos = []

    playlist_params = {
            "key": app.config["YOUTUBE_API_KEY"],
            "playlistId" : "PL4fGSI1pDJn69On1f-8NAvX_CYlx7QyZc", #Top 100 Music Videos United States(Playlist) on YouTube Music Global Charts channel",
            "part": "snippet,contentDetails",
            "maxResults": 6,
        }

    r = requests.get(playlist_url, params=playlist_params)
    results = r.json()["items"]
    video_ids = []
    for result in results:
        video_ids.append(result["contentDetails"]["videoId"])
    
    video_params = {
            "key": app.config["YOUTUBE_API_KEY"],
            "id": ",".join(video_ids),
            "part": "snippet,contentDetails",
            # "nextPageToken": result['nextPageToken'], #Do something
            # "prevPageToken": result['prevPageToken'], #Do something
            "maxResults": 6,
        }

    r = requests.get(video_url, params=video_params)
    
    results = r.json()["items"]

    for result in results:
        video_data = {
            "id": result["id"],
            "url": f"https://www.youtube.com/watch?v={ result['id'] }",
            "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
            "duration": int(
                parse_duration(result["contentDetails"]["duration"]).total_seconds() #not used currently 
                // 60
            ),
            "title": result["snippet"]["title"],
        }
        videos.append(video_data)
    return render_template("home.html", videos=videos)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        data = request.form
        x = User.query.filter_by(username=data["username"]).count()
        if x > 0:
            flash("That username is already taken, please choose another")
            return render_template("register.html", form=form)
        else:
            newuser = User(username=data["username"])
            newuser.set_password(data["password"])
            db.session.add(newuser)
            db.session.commit()
            flash("Account Created!")
            print("User added")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("loginTest"))
    form = Login()
    if form.validate_on_submit():
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            flash("Logged in successfully.")
            login_user(user)
            return redirect(url_for("loginTest"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.")
    # return redirect(url_for("hello"))
    return render_template("logout.html")


@app.route("/loginTest", methods=["GET"])
@login_required
def loginTest():
    return render_template("testlogin.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    videos = []

    #Search Requests from user        
    if request.method == "POST":
        search_params = {
            "key": app.config["YOUTUBE_API_KEY"],
            "q": request.form.get("query"),
            "part": "snippet",
            "maxResults": 8,
            "type": "video",
        }
        r = requests.get(search_url, params=search_params)
        results = r.json()["items"]

        video_ids = []
        for result in results:
            video_ids.append(result["id"]["videoId"])

        video_params = {
            "key": app.config["YOUTUBE_API_KEY"],
            "id": ",".join(video_ids),
            "part": "snippet,contentDetails",
            "maxResults": 8,
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()["items"]

        for result in results:
            video_data = {
                "id": result["id"],
                "url": f"https://www.youtube.com/watch?v={ result['id'] }",
                "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                "duration": int(
                    parse_duration(result["contentDetails"]["duration"]).total_seconds()
                    // 60
                ),
                "title": result["snippet"]["title"],
            }
            videos.append(video_data)

        

    return render_template("search.html", videos=videos)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  # Remember to remove Debug
# =======
# if __name__ == "__main__":
#     # Bind to PORT if defined, otherwise default to 5000.
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
# >>>>>>> Ramith-working
