from flask import Flask
from TrackerPack.app import DBManager, TrackerCore
app = Flask(__name__)
db = DBManager.DBManager()
core = TrackerCore.TrackerCore(db)
from TrackerPack.app.routes import *