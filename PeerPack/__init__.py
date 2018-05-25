from PeerPack import Peer,Connect2Tracker
from PyQt5.QtWidgets import *
import sys

c2t = Connect2Tracker.Connect2Tracker()
app = QApplication(sys.argv)
p = Peer.Peer(c2t)