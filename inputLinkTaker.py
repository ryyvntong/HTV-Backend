import flask
from youtube_transcript_api import YouTubeTranscriptApi
import os
from flask import request, jsonify, send_from_directory
import numpy as np
from fpdf import FPDF

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


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
    return jsonify((outputTimes))

@app.route("/pdf")
def note():
    f = open("Captions.text", "r")
    line1 = f.read()
    data = line1.splitlines()
    data = [i for i in data if len(i) > 0]
    data = np.array(data)
    data = np.delete(data, np.arange(0, data.size, 3))
    data = data.tolist()
    f.close()

    infile = open("Captions.text", "r")
    content = infile.readlines()
    infile.close()

    lst = []
    content = content[0].split(",")
    for entry in content:
        if 'text' in entry:
            strip = entry.strip()
            lst.append(strip)

    lst2 = []
    for entry in lst:
        strip = entry.strip("{'text': ")
        lst2.append(strip)

    lst3 = []
    for entry in lst2:
        strip = entry.strip("[{'text': '[Music]")
        lst3.append(strip)

    lst4 = []
    for entry in lst3:
        strip = entry.strip("Appla")
        lst4.append(strip)

    class PDF(FPDF):
        def header(self):
            # Arial bold 15
            self.set_font('Arial', 'B', 15)
            # Move to the right
            self.cell(80)
            # Title
            self.cell(30, 10, 'Note it', 1, 0, 'C')
            # Line break
            self.ln(20)
       # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    # Instantiation of inherited class
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for j in range(len(lst4)):
        pdf.cell(0, 10, lst4[j], 0, 1)
        pdf.output('tuto2.pdf', 'F')

    return send_from_directory(directory="/", filename='tuto2.pdf')


if __name__=="main":
    app.run()
