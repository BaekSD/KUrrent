import sqlite3
import uuid
class DBManager:

    def __init__(self):
        self.conn = sqlite3.connect("Kurrent.db")
        self.create_table()

    def create_table(self):
        try:
            with self.conn.cursor() as cursor:
                sql = 'CREATE TABLE User(UUID VARCHAR(36) PRIMARY KEY,IP VARCHAR(15),Port INTEGER)'
                cursor.execute(sql)
                sql = 'CREATE TABLE Seeder(UserIdx VARCHAR(36), FileIdx VARCHAR(36), FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
                cursor.execute(sql)
                sql = 'CREATE TABLE Leecher(UserIdx VARCHAR(36), FileIdx VARCHAR(36), FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
                cursor.execute(sql)
                sql = 'CREATE TABLE HashTable(FileHash VARCHAR(36), UserIdx VARCHAR(36), BlockNum INTEGER, FOREIGN KEY (UserIdx) REFERENCES User (UUID))'
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print(e)

    def get_user_hash(self, ip, port):
        try:
            with self.conn.cursor() as cursor:
                sql = "select UUID from User where IP=? and Port=?"
                uuid = cursor.execute(sql, (ip, port))
                if not uuid:
                    uuid = uuid.uuid4()
                    self.insert_user(uuid, ip, port)
        finally:
            pass

    def get_seeder_list(self, file_hash):
        try:
            with self.conn.cursor() as cursor:
                sql = "select * from Seeder where FileHash=?"
                cursor.execute(sql, file_hash)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        finally:
            pass

    def get_leecher_list(self, file_hash):
        try:
            with self.conn.cursor() as cursor:
                sql = "select * from Leecher where FileHash=?"
                cursor.execute(sql, file_hash)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        finally:
            pass

    def insert_user(self, uuid, ip, port):
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into User(UUID, IP, Port) values(?, ?, ?)"
                cursor.execute(sql, (uuid, ip, port))
                self.conn.execute()
        finally:
            pass

    def insert_seeder(self, user_idx, file_idx):
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into Seeder(UserIdx, FileIdx) values(?, ?)"
                cursor.execute(sql, (user_idx, file_idx))
                self.conn.commit()
        finally:
            pass

    def insert_leecher(self, user_idx, file_idx):
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into Leecher(UserIdx, FileIdx) values(?, ?)"
                cursor.execute(sql, (user_idx, file_idx))
                self.conn.commit()
        finally:
            pass

    def insert_file_hash(self, file_idx, user_idx, block_num):
        try:
            with self.conn.cursor() as cursor:
                sql = "insert into HashTable(FileHash, UserIdx, BlockNum) values(?, ?, ?)"
                cursor.execute(sql, (file_idx, user_idx, block_num))
                self.conn.commit()
        finally:
            pass

    def delete_leecher_user(self, user_idx):
        try:
            with self.conn.cursor() as cursor:
                sql = "delete from Leecher where UserIdx=?"
                cursor.execute(sql, user_idx)
                self.conn.commit()
        finally:
            pass

    def delete_seeder_user(self, user_idx):
        try:
            with self.conn.cursor() as cursor:
                sql = "delete from Seeder where UserIdx=?"
                cursor.execute(sql, user_idx)
                self.conn.commit()
        finally:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()