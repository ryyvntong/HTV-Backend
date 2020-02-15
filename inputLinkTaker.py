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
    en_caption = youtubeVid.captions.get_by_language_code('en')
    en_caption_convert_to_srt = (en_caption.generate_srt_captions())
    caption_file = open("Captions.text", "w")
    caption_file.write(en_caption_convert_to_srt)
    caption_file.close()
    return '''<h1>The language value is: {}</h1>'''.format(link)




app.run()