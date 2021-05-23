import os
import subprocess
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Flask, Request, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
 
UPLOAD_FOLDER =""
# file input type extensions
ALLOWED_EXTENSIONS = {'avi', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
    	
        # check if the post request has the file part
        if 'audio' not in request.files:
            flash('No file part')
            return redirect(request.url)
        audio = request.files['audio']
        if 'pic' not in request.files:
            flash('No file part')
            return redirect(request.url)
        pic = request.files['pic']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if audio.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if pic.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if (audio and allowed_file(audio.filename)) or (pic and allowed_file(pic.filename)):
            filename = secure_filename(audio.filename)
            audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = secure_filename(pic.filename)
            p = "vc.png"
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.rename(pic.filename,p)
            q = "va.mp3"
            os.rename(audio.filename,q)
            cmd = 'ffmpeg -loop 1 -r 1 -i vc.png -i va.mp3 -c:a copy -shortest -c:v libx264 video.avi'
            subprocess.call(cmd, shell=True)
            file = "%s.avi" % "video"
            return redirect(url_for('views.download_file', name='video.avi'))
    return render_template("home.html", user=current_user)


@views.route('/<name>')
def download_file(name):
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1 align=center>File Uploaded</h1>
    <body style="background-color:powderblue;"><br><br><br><br><br><br><br><br><br>
    <center>File has been Uploaded in the folder where main.py is located<strong></center></body>
    '''
    
app.add_url_rule(
    "/<name>", endpoint="download_file", build_only=True
)
