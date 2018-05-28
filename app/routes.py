
from flask import render_template, request, send_file, abort, Markup, jsonify
from app import app
import os

PROFILE_FOLDER = os.path.join('static', 'Image')
app.config['UPLOAD_FOLDER'] = PROFILE_FOLDER

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/peerList', methods=['GET'])
def send_peer_list():
    data = {'ip':'1', 'port':'5000', 'file_hash':'aaa'}
    return jsonify(data)
