
from flask import render_template, jsonify, request #, send_file, abort, Markup, jsonify
from TrackerPack.app import app, db, core
import os

PROFILE_FOLDER = os.path.join('static', 'Image')
app.config['UPLOAD_FOLDER'] = PROFILE_FOLDER

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/download_request', methods=['POST'])
def add_peer():
    ip = request.values.get('ip')
    port = request.values.get('port')
    hash = request.values.get('hash')

    uid = db.get_user_hash(ip, port)
    db.insert_leecher(uid, hash)

    leecher, block = core.match_peer(hash)


    peer_dict = {
        'ip': leecher.get('ip'),
        'port': leecher.get('port'),
        'block_num': block
    }

    return peer_dict


@app.route('/add_seeder_request', methods=['POST'])
def add_seeder():
    ip = request.values.get('ip')
    port = request.values.get('port')
    hash = request.values.get('hash')

    uid = db.get_user_hash(ip, port)
    db.insert_seeder(uid, hash)
    #db.insert_leecher(uid, hash)

    return 'true'