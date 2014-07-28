from flask import render_template, Flask, request, url_for
from apps import app

from google.appengine.ext import db


class Photo(db.Model):
    photo = db.BlobProperty()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_db():
    post_data = request.files['photo']
    filestream = post_data.read()

    upload_data = Photo()
    upload_data.photo = db.Blob(filestream)
    upload_data.put()

    url = url_for("shows", key=upload_data.key())

    return render_template("index.html", url=url)


@app.route('/show/<key>', methods=['GET'])
def shows(key):
    uploaded_data = db.get(key)
    return app.response_class(uploaded_data.photo)
