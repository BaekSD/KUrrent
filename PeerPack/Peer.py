from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os
import hashlib

class Peer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kurrentLIST = []
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

        self.categorycb.addItems(["All", "Complete", "Downloading", "Stopped"])

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
        self.addDialog = QDialog(self)
        self.addDialog.setFixedSize(350, 370)
        self.addDialog.setModal(True)

        self.addDialog.setLayout(QHBoxLayout())

        fileNameLabel = QLabel("File Name : ")
        fileNameLabel.setFont(QFont("Arial", 13, QFont.Bold))
        fileNameLabel.setFixedSize(85, 30)
        fileNameLabel.move(15, 10)
        fileNameLabel.setAlignment(Qt.AlignCenter | Qt.AlignLeft)

        self.addFileNameText = QLineEdit("")
        self.addFileNameText.setFont(QFont("Arial", 13, QFont.Bold))
        self.addFileNameText.setFixedSize(200, 30)
        self.addFileNameText.move(105, 10)

        toolBtn = QToolButton()
        toolBtn.setFixedSize(30, 30)
        toolBtn.move(305, 10)
        toolBtn.setText("...")

        sharingDirLabel = QLabel("Sharing Dir : ")
        sharingDirLabel.setFont(QFont("Arial", 13, QFont.Bold))
        sharingDirLabel.setFixedSize(85, 30)
        sharingDirLabel.move(15, 50)
        sharingDirLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.savingDirText = QLineEdit("")
        self.savingDirText.setFont(QFont("Arial", 13, QFont.Bold))
        self.savingDirText.setFixedSize(200, 30)
        self.savingDirText.move(105, 50)

        toolBtn2 = QToolButton()
        toolBtn2.setFixedSize(30, 30)
        toolBtn2.move(305, 50)
        toolBtn2.setText("...")

        trackerListLabel = QLabel("Tracker List")
        trackerListLabel.setFont(QFont("Arial", 13, QFont.Bold))
        trackerListLabel.setFixedSize(85, 30)
        trackerListLabel.move(15, 90)
        trackerListLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.addTrackerListText = QTextEdit()
        self.addTrackerListText.setFont(QFont("Arial", 13, QFont.Bold))
        self.addTrackerListText.setFixedSize(320, 200)
        self.addTrackerListText.move(15, 120)

        okBtn = QPushButton("Make")
        okBtn.setFont(QFont("Arial", 12, QFont.Bold))
        okBtn.setFixedSize(70, 35)
        okBtn.move(180, 330)

        cancelBtn = QPushButton("Cancel")
        cancelBtn.setFont(QFont("Arial", 12, QFont.Bold))
        cancelBtn.setFixedSize(70, 35)
        cancelBtn.move(265, 330)

        toolBtn.clicked.connect(self.setAddFileName)
        toolBtn2.clicked.connect(self.setSavingDir)
        okBtn.clicked.connect(self.add_torrent_ok)
        cancelBtn.clicked.connect(self.add_torrent_cancel)

        self.addDialog.layout().addChildWidget(fileNameLabel)
        self.addDialog.layout().addChildWidget(self.addFileNameText)
        self.addDialog.layout().addChildWidget(toolBtn)

        self.addDialog.layout().addChildWidget(sharingDirLabel)
        self.addDialog.layout().addChildWidget(self.savingDirText)
        self.addDialog.layout().addChildWidget(toolBtn2)

        self.addDialog.layout().addChildWidget(trackerListLabel)
        self.addDialog.layout().addChildWidget(self.addTrackerListText)

        self.addDialog.layout().addChildWidget(okBtn)
        self.addDialog.layout().addChildWidget(cancelBtn)

        self.addDialog.show()

    def add_torrent_job(self, torrentFile, saveDir, trackerList):
        self.kurrentLIST.append([torrentFile, saveDir, trackerList])
        # update list
        model = QStandardItemModel(len(self.kurrentLIST), 5, self)

        model.setHorizontalHeaderItem(0, QStandardItem("Name"))
        model.setHorizontalHeaderItem(1, QStandardItem("Location"))
        model.setHorizontalHeaderItem(2, QStandardItem("Status"))
        model.setHorizontalHeaderItem(3, QStandardItem("Speed"))
        model.setHorizontalHeaderItem(4, QStandardItem("Seeder"))

        for i in range(len(self.kurrentLIST)):
            model.setItem(i, 0, QStandardItem(os.path.basename(self.kurrentLIST[i][0])))
            model.setItem(i, 1, QStandardItem(self.kurrentLIST[i][1]))

        self.torrentlist.setModel(model)

    def setAddFileName(self):
        torrentFiles = QFileDialog.getOpenFileName(self, "", "", "KUrrent Files (*.kurrent)")
        if torrentFiles is not None and torrentFiles[0] is not None and torrentFiles[0] is not "":
            self.addFileNameText.setText(torrentFiles[0])

        self.addTrackerListText.setText("")

        f = open(torrentFiles[0], 'r')

        content = f.read().splitlines()

        trackernum = -1
        filenum = -1

        for i in content:
            if i.startswith("trackers : "):
                trackernum = int(i[10:])
                filenum = -1
            elif i.startswith("files : "):
                filenum = int(i[8:])
                trackernum = -1
            elif filenum == -1 and trackernum != -1:
                self.addTrackerListText.append(i)
            else:
                pass

        f.close()


    def setSavingDir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.exec_()
        dir = dialog.selectedFiles()
        if dir is not None and dir[0] is not None and dir[0] is not "":
            self.savingDirText.setText(dir[0])

    def add_torrent_ok(self):
        self.addDialog.destroy()

    def add_torrent_cancel(self):
        self.addDialog.destroy()

    def delete_torrent(self):
        # selected torrents deletion
        print("deleteeeeeee")

    def make_torrent(self):
        self.makeDialog = QDialog(self)
        self.makeDialog.setFixedSize(350,370)
        self.makeDialog.setModal(True)

        self.makeDialog.setLayout(QHBoxLayout())

        fileNameLabel = QLabel("File Name : ")
        fileNameLabel.setFont(QFont("Arial", 13, QFont.Bold))
        fileNameLabel.setFixedSize(85, 30)
        fileNameLabel.move(15, 10)
        fileNameLabel.setAlignment(Qt.AlignCenter | Qt.AlignLeft)

        self.fileNameText = QLineEdit("")
        self.fileNameText.setFont(QFont("Arial", 13, QFont.Bold))
        self.fileNameText.setFixedSize(200, 30)
        self.fileNameText.move(105, 10)

        toolBtn = QToolButton()
        toolBtn.setFixedSize(30,30)
        toolBtn.move(305, 10)
        toolBtn.setText("...")

        sharingDirLabel = QLabel("Sharing Dir : ")
        sharingDirLabel.setFont(QFont("Arial", 13, QFont.Bold))
        sharingDirLabel.setFixedSize(85, 30)
        sharingDirLabel.move(15, 50)
        sharingDirLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.sharingDirText = QLineEdit("")
        self.sharingDirText.setFont(QFont("Arial", 13, QFont.Bold))
        self.sharingDirText.setFixedSize(200, 30)
        self.sharingDirText.move(105, 50)

        toolBtn2 = QToolButton()
        toolBtn2.setFixedSize(30,30)
        toolBtn2.move(305, 50)
        toolBtn2.setText("...")

        trackerListLabel = QLabel("Tracker List")
        trackerListLabel.setFont(QFont("Arial", 13, QFont.Bold))
        trackerListLabel.setFixedSize(85,30)
        trackerListLabel.move(15, 90)
        trackerListLabel.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.trackerListText = QTextEdit()
        self.trackerListText.setFont(QFont("Arial", 13, QFont.Bold))
        self.trackerListText.setFixedSize(320, 200)
        self.trackerListText.move(15, 120)

        okBtn = QPushButton("Make")
        okBtn.setFont(QFont("Arial", 12, QFont.Bold))
        okBtn.setFixedSize(70, 35)
        okBtn.move(180, 330)

        cancelBtn = QPushButton("Cancel")
        cancelBtn.setFont(QFont("Arial", 12, QFont.Bold))
        cancelBtn.setFixedSize(70, 35)
        cancelBtn.move(265, 330)

        toolBtn.clicked.connect(self.setSaveFileName)
        toolBtn2.clicked.connect(self.setSharingDir)
        okBtn.clicked.connect(self.make_torrent_job)
        cancelBtn.clicked.connect(self.make_torrent_cancel)

        self.makeDialog.layout().addChildWidget(fileNameLabel)
        self.makeDialog.layout().addChildWidget(self.fileNameText)
        self.makeDialog.layout().addChildWidget(toolBtn)

        self.makeDialog.layout().addChildWidget(sharingDirLabel)
        self.makeDialog.layout().addChildWidget(self.sharingDirText)
        self.makeDialog.layout().addChildWidget(toolBtn2)

        self.makeDialog.layout().addChildWidget(trackerListLabel)
        self.makeDialog.layout().addChildWidget(self.trackerListText)

        self.makeDialog.layout().addChildWidget(okBtn)
        self.makeDialog.layout().addChildWidget(cancelBtn)

        self.makeDialog.show()

    def setSaveFileName(self):
        file = QFileDialog.getSaveFileName(self.makeDialog, "", "", "KUrrent Files (*.kurrent)")
        if file is not None and file[0] is not None and file[0] is not "":
            self.fileNameText.setText(file[0])

    def setSharingDir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.exec_()
        dir = dialog.selectedFiles()
        if dir is not None and dir[0] is not None and dir[0] is not "":
            self.sharingDirText.setText(dir[0])

    def make_torrent_job(self):
        # make torrent file
        fn = self.fileNameText.text()
        sd = self.sharingDirText.text()
        tl = self.trackerListText.toPlainText()
        f = open(fn, "w")
        tll = tl.splitlines()

        tracker = []
        for i in tll:
            if len(i.strip()) > 0:
                tracker.append(i.strip())

        f.write("trackers : " + str(len(tracker)) + "\n")
        for i in tracker:
            f.write(i.strip() + "\n")

        flist = self.getFileListRecur(sd + os.path.sep, "")

        f.write("files : " + str(len(flist)) + "\n")
        for i in flist:
            sha = hashlib.sha256()
            try:
                file = open(sd+i,"rb")
            except IOError:
                pass
            while True:
                buf = file.read(8192)
                if not buf:
                    break
                sha.update(buf)
            file.close()
            f.write(i + "\n")
            f.write(str(os.path.getsize(sd+i)) + "\n")
            f.write(sha.hexdigest() + "\n")

        f.close()
        # add to torrent list
        self.add_torrent_job(fn, sd, tracker)

        # destroy
        self.makeDialog.destroy()

    def getFileListRecur(self, abs_path, file):
        if os.path.isfile(abs_path+file):
            if os.path.basename(abs_path+file).startswith("."):
                return None
            return file
        elif os.path.isdir(abs_path+file):
            child = os.listdir(abs_path+file)
            ret = []
            for i in child:
                f = self.getFileListRecur(abs_path, file+os.path.sep+i)
                if f is None:
                    continue
                if type(f) is str:
                    ret.append(f)
                elif type(f) is list:
                    for j in f:
                        ret.append(j)
            return ret


    def make_torrent_cancel(self):
        self.makeDialog.destroy()

