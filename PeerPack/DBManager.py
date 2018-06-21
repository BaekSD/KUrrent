import sqlite3
import uuid, os


class DBManager:

    def __init__(self):
        db_file = os.path.join('Files', 'Kurrent.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = 'CREATE TABLE HashBlock(FileHash VARCHAR(64), BlockNum Integer, PRIMARY KEY(FileHash, BlockNum))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        self.conn.commit()

    def put_block_info(self, file_hash, block_num):
        try:
            sql = "insert into HashBlock(FileHash, BlockNum) values (?, ?)"
            self.cursor.execute(sql, (file_hash, block_num))
            self.conn.commit()
        except Exception as e:
            print(e)

    def get_blocks(self, file_hash):
        try:
            sql = "select BlockNum from HashBlock where FileHash=?"
            self.cursor.execute(sql, file_hash)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(e)
