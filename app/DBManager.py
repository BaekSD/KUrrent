import sqlite3

class DBManager:

    def __init__(self):
        self.conn = sqlite3.connect("Kurrent.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = 'CREATE TABLE User(UUID VARCHAR(36) PRIMARY KEY,IP VARCHAR(15),PORT INTEGER)'
            self.cur.execute(sql)
            sql = 'CREATE TABLE Seeder(UserIdx VARCHAR(36), FileIdx VARCHAR(36), FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
            self.cur.execute(sql)
            sql = 'CREATE TABLE Leecher(UserIdx VARCHAR(36), FileIdx VARCHAR(36), FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
            self.cur.execute(sql)
            sql = 'CREATE TABLE HashTable(FileHash VARCHAR(36), UserIdx VARCHAR(36), BlockNum INTEGER, FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
            self.cur.execute(sql)

            self.conn.commit()
        except :
            print('Table Already Created')


    def get_seeder_list(self, file_hash):
        sql = "select * from Seeder where FileHash=?"
        self.cur.execute(sql, file_hash)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def get_leecher_list(self, file_hash):
        sql = "select * from Leecher where FileHash=?"
        self.cur.execute(sql, file_hash)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    def insert_seeder(self, file_hash, ip, port):
        sql = "insert into seeder(FileHash, IP, Port) values(?, ?, ?)"
        self.cur.execute(sql, (file_hash, ip, port))
        self.conn.commit()

    def insert_leecher(self, file_hash, ip, port):
        sql = "insert into leecher(FileHash, IP, Port) values(?, ?, ?)"
        self.cur.execute(sql, (file_hash, ip, port))
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()