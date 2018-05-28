from flask import Flask
from app import DBManager
app = Flask(__name__)
db = DBManager.DBManager()

from app.routes import *