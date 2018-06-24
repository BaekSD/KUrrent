import os
import queue
import asyncio
class FileManager:

    def __init__(self):
        self.total_block_list = {}
        self.block_q = queue.Queue()

    def read_block_data(self, file_dir, index):
        with open(file_dir, 'rb') as f:
            f.seek(8192*(index-1))
            block_data = f.read(8192)
            return block_data

    def write_block_data(self, file_dir, data, index):
        with open(file_dir, 'wb+') as f:
            # we have to do here
            pass

    def write_new_file(self, file_dir, file_size):
        with open(file_dir, 'wb') as f:
            f.seek(file_size-1)
            f.write(b'\0')

    '''def insert_block(self, block):
        self.block_q.put(block)
        try:
            self.total_block_list[block.file_hash].append(block)
        except Exception as e:
            block_list = [block]
            self.total_block_list[block.file_hash] = block_list
    
    def __init__(self, block_num, file_block):
        self.s = ''
        self.count = 0
        self.last = -1
        self.block_num = block_num
        self.file_block = file_block
        self.list1 = []

    def save_file(self):
        if os.path.exists("./sequence.txt"):
            fp = open('sequence.txt', 'r+t')
            self.s = fp.readline().splitlines()[0]
            self.count = int(fp.readline().splitlines()[0])
            self.last = int(fp.readline().splitlines()[0])
            fp.close()

        fp = open('sequence.txt', 'w+t')
        if self.s == '':
            fp.write(str(self.block_num))
        else:
            self.list1 = self.s.split(',')
            self.list1 = list(map(int, self.list1))
            self.s = self.s + ',' + str(self.block_num)
            fp.write(self.s)
        fp.write('\n')
        fp.write(str(self.count + 1))
        fp.write('\n')
        if len(self.file_block) > 1:
            self.last = self.block_num
            fp.write(str(self.block_num))
        else:
            fp.write('-1')

        fp.close()

        if self.count == self.last - 1:
            os.remove('./sequence.txt')
            pass

        self.check_file()

    def check_file(self):
        if self.checkRight(self.block_num):
            if self.checkLeft(self.block_num) == 1:
                with open('fileName', 'ab') as put:
                    put.write(self.file_block)
                    f = open('.' + str(self.block_num + 1), 'rb')
                    put.write(f.read())
                    f.close()
                    os.remove('./.' + str(self.block_num + 1))
            else:
                with open('.' + str(self.checkLeft(self.block_num)), 'ab') as put:
                    put.write(self.file_block)
                    f = open('.' + str(self.block_num + 1), 'rb')
                    put.write(f.read())
                    f.close()
                    os.remove('./.' + str(self.block_num + 1))
        else:
            if self.checkLeft(self.block_num) == 1:
                with open('fileName', 'ab') as put:
                    put.write(self.file_block)
            else:
                with open('.' + str(self.checkLeft(self.block_num)), 'ab') as put:
                    put.write(self.file_block)


    def checkLeft(self, block_num):
        if block_num - 1 in self.list1:
            return self.checkLeft(block_num - 1)
        else:
            return block_num


    def checkRight(self, block_num):
        if block_num + 1 in self.list1:
            return True
        else:
            return False
    '''