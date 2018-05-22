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
        self.btnEventInit()
        self.infoTabW.setCurrentIndex(0)


    def retranslateUi(self):
        self.setWindowTitle("KUrrent")
        self.addbtn.setText("ADD")
        self.delbtn.setText("DELETE")
        self.mkbtn.setText("MAKE")
        self.infoTabW.setTabText(self.infoTabW.indexOf(self.tab), "tab1")
        self.infoTabW.setTabText(self.infoTabW.indexOf(self.tab2), "tab2")

    def btnEventInit(self):
        self.addbtn.clicked.connect(self.add_torrent)
        self.delbtn.clicked.connect(self.delete_torrent)
        self.mkbtn.clicked.connect(self.make_torrent)

    def add_torrent(self):
        self.torrentFiles = QFileDialog.getOpenFileNames()

    def delete_torrent(self):
        # selected torrents deletion
        print("deleteeeeeee")

    def make_torrent(self):
        dialog = QDialog(self)
        dialog.setFixedSize(350,500)
        dialog.setModal(True)

        dialog.setLayout(QHBoxLayout())

        fileNameLabel = QLabel("File Name : ")
        fileNameLabel.setFont(QFont("Arial", 13, QFont.Bold))
        fileNameLabel.setFixedSize(75, 30)
        fileNameLabel.move(15, 10)
        fileNameLabel.setAlignment(Qt.AlignCenter)

        self.fileNameText = QLineEdit("")
        self.fileNameText.setFont(QFont("Arial", 13, QFont.Bold))
        self.fileNameText.setFixedSize(210, 30)
        self.fileNameText.move(95, 10)

        toolBtn = QToolButton()
        toolBtn.setFixedSize(30,30)
        toolBtn.move(305, 10)
        toolBtn.setText("...")

        sharingFilesLabel = QLabel("Files")
        sharingFilesLabel.setFont(QFont("Arial", 13, QFont.Bold))
        sharingFilesLabel.setFixedSize(75,30)
        sharingFilesLabel.move(15, 50)
        sharingFilesLabel.setAlignment(Qt.AlignVCenter)

        addBtn = QToolButton()
        addBtn.setFixedSize(30,30)
        addBtn.move(275, 50)
        addBtn.setText("+")

        rmBtn = QToolButton()
        rmBtn.setFixedSize(30,30)
        rmBtn.move(305, 50)
        rmBtn.setText("-")

        toolBtn.clicked.connect(self.setSaveFileName)
        addBtn.clicked.connect(self.addSharingFiles)

        dialog.layout().addChildWidget(fileNameLabel)
        dialog.layout().addChildWidget(self.fileNameText)
        dialog.layout().addChildWidget(toolBtn)

        dialog.layout().addChildWidget(sharingFilesLabel)
        dialog.layout().addChildWidget(addBtn)
        dialog.layout().addChildWidget(rmBtn)

        dialog.show()
        #self.files = QFileDialog.getOpenFileNames()

    def setSaveFileName(self):
        file = QFileDialog.getSaveFileName()
        if file is not None and file[0] is not None and file[0] is not "":
            self.fileNameText.setText(file[0])

    def addSharingFiles(self):
        dir = QFileDialog.getExistingDirectory()