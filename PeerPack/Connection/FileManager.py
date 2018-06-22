import os


class FileManager:

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
