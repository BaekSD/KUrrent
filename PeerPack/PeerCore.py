import os, hashlib, sys
from PeerPack import KurrentParser

class PeerCore:
    def __init__(self, server):
        self.KUrrentLIST = {}
        self.server = server
        self.parser = KurrentParser.Parser()
        self.server.start()

    def closeEvent(self):
        print('close')
        # save status

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

    '''
    def piece_exist(self, hash, file_name, piece_num):
        if hash not in self.KUrrentLIST.keys():
            return False
        if file_name not in self.KUrrentLIST[hash]['files'].keys():
            return False
        if piece_num >= len(self.KUrrentLIST[hash]['files'][file_name]['hash_table']):
            return False
        return self.KUrrentLIST[hash]['files'][file_name]['hash_table'][piece_num]

    def get_piece(self, hash, file_name, piece_num):
        if hash not in self.KUrrentLIST.keys():
            return False
        if file_name not in self.KUrrentLIST[hash]['files'].keys():
            return False
        if piece_num >= len(self.KUrrentLIST[hash]['files'][file_name]['hash_table']):
            return False
        if self.KUrrentLIST[hash]['files'][file_name]['hash_table'][piece_num]:
            # find, read and return the piece
            if self.KUrrentLIST[hash]['status'] == 'complete':
                # complete file so just read, get and return the piece
                f = open(self.KUrrentLIST[hash]['dir']+'/'+file_name, 'rb')
                f.read(piece_num*1024)
                ret = f.read(1024)
                f.close()
                return ret
            else:
                # downloading status. so just read the temperature file 'file_name-piece_num' and return that
                full_file_name = self.KUrrentLIST[hash]['dir'] + '/' + file_name + "-" + str(piece_num)
                f = open(full_file_name, 'rb')
                ret = f.read()
                f.close()
                return ret
        else:
            return False
    '''

    def get_todolist(self):
        return []

    def make_torrent(self, file_name, sharing_file, tracker_text):
        f = open(file_name, "w", encoding='utf-8')
        tll = tracker_text.splitlines()
        tracker_list = []
        size = os.path.getsize(sharing_file)
        sha = self.getHash(sharing_file)
        f.write(sha.hexdigest() + "\n")

        self.KUrrentLIST[sha] = {
                                    'status': 'complete',
                                    'dir': os.path.abspath(sharing_file),
                                    'size': size,
                                    'hash_table': []
                                 }

        for i in range(int((size+8191)/8192)):
            self.KUrrentLIST[sha]['hash_table'].append(True)

        for i in tll:
            if len(i.strip()) > 0:
                tracker_list.append(i.strip())

        f.write("trackers : " + str(len(tracker_list)) + "\n")

        for i in tracker_list:
            f.write(i.strip() + "\n")

        f.write(os.path.basename(sharing_file)+'\n')
        f.write(str(size))
        f.close()

        print(self.KUrrentLIST[sha])

        f = open(file_name, 'rt')
        #self.add_seeder(tracker_list, f)
        f.close()
        # We have to do here => put client to dht and put data to database


    def get_file_list_recur(self, abs_path, file):
        if os.path.isfile(abs_path+file):
            if os.path.basename(abs_path+file).startswith("."):
                return None
            return file
        elif os.path.isdir(abs_path+file):
            child = os.listdir(abs_path+file)
            ret = []
            for i in child:
                f = self.get_file_list_recur(abs_path, file + os.path.sep + i)
                if f is None:
                    continue
                if type(f) is str:
                    ret.append(f)
                elif type(f) is list:
                    for j in f:
                        ret.append(j)
            return ret

    def add_torrent(self, file_name, saving_dir, tracker_text):
        kurrent_file = open(file_name, 'rt', encoding='utf-8')
        file_hash = self.parser.get_file_hash(kurrent_file)
        tracker_list = self.parser.parse_tracker_text(tracker_text)
        size = self.parser.get_size(kurrent_file)

        self.KUrrentLIST[file_hash] = {
                                        'status': 'downloading',
                                        'dir': saving_dir,
                                        'size': size,
                                        'hash_table': []
                                        }

        for i in range(int((size+8191)/8192)):
            self.KUrrentLIST[file_hash]['hash_table'].append(False)

        '''

        for i in file_list.keys():
            #self.KUrrentLIST[file_hash]['files'][i] = {}
            self.KUrrentLIST[file_hash]['files'][i]['hash_table'] = []
            self.KUrrentLIST[file_hash]['files'][i]['size'] = int(file_list[i])
            for j in range(int((int(file_list[i])+1023)/1024)):
                self.KUrrentLIST[file_hash]['files'][i]['hash_table'].append(False)
        '''

        # We have to do here => Request to DHT and DHT Should insert this peer into hash table and saving_dir should be added real file name
        # File Manager should write file with real file name and size
        from PeerPack import db, fm
        db.put_file_info(file_hash, size, (size/8192) + 1, saving_dir)
        fm.write_new_file(saving_dir, size)


    def get_torrent_table(self):
        torrent_table = []

        for i in self.KUrrentLIST.keys():
            t = [i,
                 self.KUrrentLIST[i]['dir'],
                 self.KUrrentLIST[i]['status'],
                 self.get_seeder_num(i)]
            torrent_table.append(t)

        return torrent_table
