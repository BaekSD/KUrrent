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
            sql = 'CREATE TABLE User(UID VARCHAR(36) PRIMARY KEY,IP VARCHAR(15),Port INTEGER)'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        try:
            sql = 'CREATE TABLE Seeder(UserIdx VARCHAR(36), FileHash VARCHAR(64), FOREIGN KEY (UserIdx) REFERENCES User (UID), PRIMARY KEY(UserIdx, FileHash) )'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        try:
            sql = 'CREATE TABLE Leecher(UserIdx VARCHAR(36),FileHash VARCHAR(64), FOREIGN KEY (UserIdx) REFERENCES User (UID), PRIMARY KEY(UserIdx, FileHash))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        try:
            sql = 'CREATE TABLE HashTable(FileHash VARCHAR(64), UserIdx VARCHAR(36), BlockNum INTEGER, FOREIGN KEY (UserIdx) REFERENCES User (UID))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        try:
            '''
            self.insert_leecher('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
            self.insert_leecher('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
            self.insert_seeder('cccccccc-cccc-cccc-cccc-cccccccccccc', 'zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz')
            self.insert_seeder('dddddddd-dddd-dddd-dddd-dddddddddddd', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
            self.insert_user('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '127.0.0.1', 8090)
            self.insert_file_hash('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz', '1')
            self.insert_file_hash('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', '3')
            self.insert_file_hash('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz', '2')
            self.insert_file_hash('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', '4')
            '''
        except Exception as e:
            print(e)

        self.conn.commit()

    def get_user_hash(self, ip, port):
        try:
            sql = "select UID from User where IP=? and Port=?"
            uid = self.cursor.execute(sql, (ip, port)).fetchone()
            if not uid:
                uid = uuid.uuid4()
                self.insert_user(str(uid), ip, port)
            return str(uid)
        except Exception as e:
            print(e)


    def get_seeder_list(self, file_hash):
        try:
            sql = "select * from Seeder where FileHash=?"
            self.cursor.execute(sql, file_hash)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
        finally:
            pass

    def get_leecher_list(self, file_hash):
        try:
            sql = "select UserIdx from Leecher where FileHash=?"
            self.cursor.execute(sql, (file_hash,))
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
            return rows
        except Exception as e:
            print(e)
    def get_block_num_list(self, user_idx, file_hash):
        try:
            sql = "select BlockNum from HashTable where UserIdx=? and FileHash=? "
            self.cursor.execute(sql, (user_idx, file_hash))
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
            return rows
        except Exception as e:
            print(e)


    def insert_user(self, uid, ip, port):
        try:
            sql = "insert into User(UID, IP, Port) values(?, ?, ?)"
            self.cursor.execute(sql, (uid, ip, port))
            self.conn.commit()
        finally:
            pass

    def insert_seeder(self, user_idx, file_idx):
        try:
            sql = "insert into Seeder(UserIdx, FileHash) values(?, ?)"
            self.cursor.execute(sql, (user_idx, file_idx))
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            pass

    def insert_leecher(self, user_idx, file_idx):
        try:
            sql = "insert into Leecher(UserIdx, FileHash) values (?, ?)"
            self.cursor.execute(sql, (user_idx, file_idx))
            self.conn.commit()
        finally:
            pass

    def insert_file_hash(self, user_idx, file_idx, block_num):
        try:
            sql = "insert into HashTable(UserIdx, FileHash, BlockNum) values(?, ?, ?)"
            self.cursor.execute(sql, (user_idx, file_idx, block_num))
            self.conn.commit()
        finally:
            pass

    def delete_leecher_user(self, user_idx):
        try:
            sql = "delete from Leecher where UserIdx=?"
            self.cursor.execute(sql, user_idx)
            self.conn.commit()
        finally:
            pass

    def delete_seeder_user(self, user_idx):
        try:
            sql = "delete from Seeder where UserIdx=?"
            self.cursor.execute(sql, user_idx)
            self.conn.commit()
        finally:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()