import sqlite3
import uuid, os


class DBManager:

    def __init__(self):
        db_file = os.path.join('Files', 'Kurrent.db')
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = 'CREATE TABLE BlockTable(FileHash VARCHAR(64), BlockNum Integer, PRIMARY KEY(FileHash, BlockNum))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

        try:
            sql = 'CREATE TABLE FileTable(FileHash VARCHAR(64), FileSize Integer, LastIndex Integer, FIlePath VARCHAR(' \
                  '200), PRIMARY KEY(FileHash)) '
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        self.conn.commit()

    def put_file_info(self, file_hash, file_size, last_index, file_path):
        try:
            sql = "insert into FileTable(FileHash, FileSize, LastIndex, FilePath) values (?, ?, ?, ?)"
            self.cursor.execute(sql, (file_hash, file_size, int(last_index), file_path))
            self.conn.commit()
        except Exception as e:
            print(e)

    def put_block_info(self, file_hash, block_num):
        try:
            sql = "insert into BlockTable(FileHash, BlockNum) values (?, ?)"
            self.cursor.execute(sql, (file_hash, block_num))
            self.conn.commit()
        except Exception as e:
            print(e)

    def put_total_blocks(self, total_blocks):
        try:
            sql = "insert into BlockTable(FileHash, BlockNum) values (?, ?)"
            self.cursor.executemany(sql, total_blocks)  # , None ))
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_file_data(self, file_hash):
        try:
            sql = "select FilePath, LastIndex from FileTable where FileHash=?"
            self.cursor.execute(sql, (file_hash, ))
            rows = self.cursor.fetchone()
            return rows[0], rows[1]
        except Exception as e:
            print(e)

    def get_blocks(self, file_hash):
        try:
            sql = "select BlockNum from BlockTable where FileHash=? order by BlockNum asc"
            self.cursor.execute(sql, (file_hash, ))#, None ))
            rows = self.cursor.fetchall()
            block_list = []
            for i in range(rows.__len__()):
                block_list.append(rows[i][0])
            return block_list
        except Exception as e:
            print(e)