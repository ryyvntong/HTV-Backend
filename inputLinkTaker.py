import flask
from youtube_transcript_api import YouTubeTranscriptApi
import os
from flask import request, jsonify, send_from_directory,abort
import numpy as np
from fpdf import FPDF

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/file')
def note():
    return send_from_directory(directory="/", filename='tuto2.pdf')



@app.route('/submit')
def query():
    outputTimes = []
    link = request.args.get("link")
    searchTerm = request.args.get("search")
    link = link.split("v=")[1]
    captions = YouTubeTranscriptApi.get_transcript(link)
    for i in captions:
        if searchTerm in i["text"]:
            outputTimes.append(i['start'])

    f=open("Captions.text", "w")
    f.write(str(captions))
    f.close()
    return jsonify(outputTimes)



if __name__=="main":
    app.run()
