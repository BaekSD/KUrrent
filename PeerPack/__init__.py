from PeerPack import PeerGUI
from PeerPack import PeerCore as Core
from PeerPack.Connection import Connect2Tracker
from PyQt5.QtWidgets import *
import sys

c2t = Connect2Tracker.Connect2Tracker()
app = QApplication(sys.argv)
core = Core.PeerCore(c2t)
gui = PeerGUI.PeerGUI(core)