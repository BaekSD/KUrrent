from flask import render_template, request, send_file, abort, Markup, jsonify
from TrackerPack import app
import os

@app.route('/')
def home():
    return "home"

@app.route('/getPeerList')
def getPeerList():
    return "getPeerList"
