from flask import Flask

app = Flask(__name__)

from TrackerPack.routes import *