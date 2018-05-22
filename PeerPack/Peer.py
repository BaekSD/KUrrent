from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Peer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    def closeEvent(self, event):
        self.deleteLater()

    def initGUI(self):
        self.setMinimumSize(720, 450)
        self.resize(720,450)
        self.cw = QWidget(self)
        self.cw.setObjectName("cw")
        self.cw.setEnabled(True)
        self.gridLayout = QGridLayout(self.cw)
        self.gridLayout.setObjectName("gridLayout")
        self.vl = QVBoxLayout()
        self.vl.setObjectName("vl")
        self.btnl = QHBoxLayout()
        self.btnl.setObjectName("btnl")
        self.addbtn = QPushButton(self.cw)
        self.addbtn.setObjectName("addbtn")
        self.btnl.addWidget(self.addbtn)

        self.delbtn = QPushButton(self.cw)
        self.delbtn.setObjectName("delbtn")
        self.btnl.addWidget(self.delbtn)

        self.mkbtn = QPushButton(self.cw)
        self.mkbtn.setObjectName("mkbtn")
        self.btnl.addWidget(self.mkbtn)

        #self.btnspacer = QSpacerItem(40,20, QSizePolicy("Expanding"), QSizePolicy("Minimum"))
        self.btnspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btnl.addItem(self.btnspacer)

        self.categorycb = QComboBox(self.cw)
        self.categorycb.setObjectName("categorycb")
        self.btnl.addWidget(self.categorycb)
        self.vl.addLayout(self.btnl)

        self.mainl = QHBoxLayout()
        self.mainl.setObjectName("mainl")
        self.mainl2 = QVBoxLayout()
        self.mainl2.setObjectName("mainl2")
        self.torrentlist = QTableView()
        self.torrentlist.setObjectName("torrentlist")
        self.mainl2.addWidget(self.torrentlist)

        self.infoTabW = QTabWidget(self.cw)
        self.infoTabW.setObjectName("infoTab")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tab.setEnabled(True)
        self.gridLayout2 = QGridLayout(self.tab)
        self.gridLayout2.setObjectName("gridLayout2")
        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 642, 166))
        self.gridLayout3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout3.setObjectName("gridLayout3")
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout3.addWidget(self.textBrowser,0,0,1,1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout2.addWidget(self.scrollArea,0,0,1,1)

        self.infoTabW.addTab(self.tab, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout4 = QGridLayout(self.tab2)
        self.gridLayout4.setObjectName("gridLayout4")
        self.scrollArea2 = QScrollArea(self.tab2)
        self.scrollArea2.setObjectName("scrollArea2")
        self.scrollArea2.setWidgetResizable(True)
        self.scrollAreaWidgetContents2 = QWidget()
        self.scrollAreaWidgetContents2.setObjectName("scrollAreaWidgetContents2")
        self.scrollAreaWidgetContents2.setGeometry(QRect(0,0,642,166))
        self.scrollArea2.setWidget(self.scrollAreaWidgetContents2)

        self.gridLayout4.addWidget(self.scrollArea2,0,0,1,1)
        self.infoTabW.addTab(self.tab2, "")
        self.mainl2.addWidget(self.infoTabW)
        self.mainl.addLayout(self.mainl2)
        self.vl.addLayout(self.mainl)
        self.gridLayout.addLayout(self.vl,0,0,1,1)
        self.setCentralWidget(self.cw)

        self.retranslateUi()
        self.infoTabW.setCurrentIndex(0)


    def retranslateUi(self):
        self.setWindowTitle("KUrrent")
        self.addbtn.setText("ADD")
        self.delbtn.setText("DELETE")
        self.mkbtn.setText("MAKE")
        self.infoTabW.setTabText(self.infoTabW.indexOf(self.tab), "tab1")
        self.infoTabW.setTabText(self.infoTabW.indexOf(self.tab2), "tab2")
        pass


    def add_torrent(self):
        pass

    def delete_torrent(self):
        pass

    def view_torrent(self):
        pass

    def make_torrent(self):
        '''
        app = QApplication(sys.argv)
        q = QWidget()
        fname = QFileDialog.getOpenFileNames(q)
        print(fname)
        app.exec_()
        '''
        pass