from PeerPack import PeerGUI
from PeerPack import PeerCore as Core
from PeerPack import DBManager, FileManager
from PeerPack.Connection import Receiver
from PyQt5.QtWidgets import *
import sys

ip = '192.168.43.197'
port = 7777

server = Receiver.ServerThread(ip, port)
db = DBManager.DBManager()
fm = FileManager.FileManager(server.lock)
core = Core.PeerCore(server)
app = QApplication(sys.argv)
gui = PeerGUI.PeerGUI(core)