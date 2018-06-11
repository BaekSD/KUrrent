import os
import hashlib

class PeerCore():
    def __init__(self):
        self.KUrrentLIST = []

    def getHash(self, fName):
        sha = hashlib.sha256()
        try:
            file = open(fName, "rb")
        except IOError:
            pass
        while True:
            buf = file.read(8196)
            if not buf:
                break
            sha.update(buf)
        file.close()
        return sha

    def make_torrent(self, fName, sharingDir, trackerList):
        f = open(fName, "w")
        tll = trackerList.splitlines()

        tracker = []
        for i in tll:
            if len(i.strip()) > 0:
                tracker.append(i.strip())

        f.write("trackers : " + str(len(tracker)) + "\n")
        for i in tracker:
            f.write(i.strip() + "\n")

        flist = self.getFileListRecur(sharingDir + os.path.sep, "")

        f.write("files : " + str(len(flist)) + "\n")
        for i in flist:
            sha = self.getHash(sharingDir + i)
            f.write(i + "\n")
            f.write(str(os.path.getsize(sharingDir + i)) + "\n")
            f.write(sha.hexdigest() + "\n")

        f.close()

        self.add_torrent(fName, sharingDir, trackerList, new_add=False)

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

    def add_torrent(self, fName, sharingDir, trackerList, new_add = True):

        if new_add: # completely new adding
            pass
        else:       # add after make torrent
            pass

        pass