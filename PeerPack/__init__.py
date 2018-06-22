from PeerPack import PeerGUI
from PeerPack import PeerCore as Core
from PeerPack import DBManager
from PeerPack.Connection import ServerThread, PeerSocket
from PyQt5.QtWidgets import *
import sys

ip = '127.0.0.1'
port = 7777

db = DBManager.DBManager()
server = ServerThread.ServerThread(ip, port)
core = Core.PeerCore(server)
app = QApplication(sys.argv)
gui = PeerGUI.PeerGUI(core)
#sock = PeerSocket.PeerSocket(ip=ip, port=port, core=core)