import os, hashlib
from PeerPack import KurrentParser

class PeerCore:
    def __init__(self, c2t):
        self.KUrrentLIST = []
        self.c2t = c2t
        self.parser = KurrentParser.Parser()

    def getHash(self, dir, fNames):
        sha = hashlib.sha256()

        for fName in fNames:
            try:
                file = open(dir + fName, "rb")
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
        f = open(fName, "w", encoding='utf-8')
        tll = trackerList.splitlines()
        tracker_list = []
        flist = self.getFileListRecur(sharingDir + os.path.sep, "")
        sha = self.getHash(sharingDir, flist)
        f.write(sha.hexdigest() + "\n")

        for i in tll:
            if len(i.strip()) > 0:
                tracker_list.append(i.strip())

        f.write("trackers : " + str(len(tracker_list)) + "\n")

        for i in tracker_list:
            f.write(i.strip() + "\n")

        f.write("files : " + str(len(flist)) + "\n")
        for i in flist:
            f.write(i + "\n")
            f.write(str(os.path.getsize(sharingDir + i)) + "\n")

        f.close()
        return tracker_list

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

    def add_download_list(self, tracker_text, kurrent_file):
        file_hash = self.parser.get_file_hash(kurrent_file)
        tracker_list = self.parser.parse_tracker_text(tracker_text)
        for tracker in tracker_list:
            self.c2t.add_request(tracker, file_hash)

    def add_seeder(self, tracker_list, kurrent_file):
        file_hash = self.parser.get_file_hash(kurrent_file)
        for tracker in tracker_list:
            self.c2t.add_seeder_request(tracker, file_hash)