from flask import Flask
from TrackerPack.app import DBManager
app = Flask(__name__)
db = DBManager.DBManager()

from TrackerPack.app.routes import *