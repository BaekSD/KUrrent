from PeerPack import PeerGUI
from PeerPack import PeerCore as Core
from PeerPack import DBManager, FileManager
from PeerPack.Connection import Receiver, PeerSocket
from PyQt5.QtWidgets import *
import sys

ip = '127.0.0.1'
port = 7777

db = DBManager.DBManager()
fm = FileManager.FileManager()
server = Receiver.ServerThread(ip, port)
core = Core.PeerCore(server)
app = QApplication(sys.argv)
gui = PeerGUI.PeerGUI(core)
#sock = PeerSocket.PeerSocket(ip=ip, port=port, core=core)