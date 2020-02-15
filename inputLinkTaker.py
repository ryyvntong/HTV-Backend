import flask
import pytube
import os
from moviepy.editor import *
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/submit')
def query():
    link = request.args.get("link")
    youtubeVid = pytube.YouTube(link)
    title=youtubeVid.title
    video = youtubeVid.streams.filter(only_audio=True).all()
    video[0].download()
    return '''<h1>The language value is: {}</h1>'''.format(title)


app.run()