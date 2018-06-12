
from flask import render_template, jsonify, request #, send_file, abort, Markup, jsonify
from TrackerPack.app import app, db
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
    data = {'ip': '1', 'port': '5000', 'file_hash': 'aaa'}
    return jsonify(data)


@app.route('/download_request', methods=['POST'])
def add_peer():
    ip = request.values.get('ip')
    port = request.values.get('port')
    hash = request.values.get('hash')

    uid = db.get_user_hash(ip, port)
    db.insert_leecher(uid, hash)
    leecher_list = db.get_leecher_list(hash)
    for leecher in leecher_list:
        print(leecher)
    leecher = leecher_list[0]
    block_num_list = db.get_block_num_list(hash, leecher)
    for block in block_num_list:
        print(block)
    block = block_num_list[0]
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