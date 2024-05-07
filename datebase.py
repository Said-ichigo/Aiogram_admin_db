import sqlite3
from datetime import datetime

class DataBase:
    def __init__(self, name: str = "DateBase.db"):
        self.name = name
        self.connector = sqlite3.connect(self.name)
        self.cursor = self.connector.cursor()
        q1 = """CREATE TABLE IF NOT EXISTS "admins" ("telegramid" INTEGER unique)"""
        q2 = """CREATE TABLE IF NOT EXISTS "channels" ("link" TEXT unique)"""
        q3 = """CREATE TABLE IF NOT EXISTS "messages" ("messageid"	INTEGER)"""
        q4 = """CREATE TABLE IF NOT EXISTS "users" ("telegramid" INTEGER unique, "is_active" INTEGER, "joined_date" TEXT)"""
        self.cursor.execute(q1)
        self.connector.commit()
        self.cursor.execute(q2)
        self.connector.commit()
        self.cursor.execute(q3)
        self.connector.commit()
        self.cursor.execute(q4)
        self.connector.commit()

    def add_user(self, telegramid, is_active, joined_date):
        try:
            query = f"""INSERT INTO users VALUES ('{telegramid}', '{is_active}', '{joined_date}')"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_user(self, telegramid):
        try:
            query = f"""SELECT * FROM users WHERE telegramid={telegramid}"""
            return list(self.cursor.execute(query))
        except Exception as e:
            print(e)
            return []
        
    def get_users(self):
        try:
            query = f"""SELECT * FROM users WHERE is_active=1"""
            return list(self.cursor.execute(query))
        except Exception as e:
            return []
        
    def get_now_users(self):
        try:
            now = datetime.now().strftime("%d/%m/%Y")
            query = f"""SELECT FROM users WHERE joined_date="{now}" """
            return list(self.cursor.execute(query))
        except:
            return []

    def get_all_users(self):
        try:
            query = f"""SELECT * FROM users"""
            return list(self.cursor.execute(query))
        except Exception as e:
            return []

    def update_user(self, telegramid):
        try:
            query = f"""UPDATE users SET is_active=1 WHERE telegramid='{telegramid}'"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_channel(self, link):
        try:
            query = f"""INSERT INTO channels VALUES ('{link}')"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_channels(self):
        query = f"""SELECT link FROM channels;"""
        channels = self.cursor.execute(query)
        return channels

    def delete_channel(self, link):
        try:
            query = f"""DELETE FROM channels WHERE link='{link}'"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def add_admin(self, telegramid):
        try:
            query = f"""INSERT INTO admins VALUES ('{telegramid}')"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_admin(self, telegramid):
        try:
            query = f"""SELECT * FROM admins WHERE telegramid={telegramid}"""
            return list(self.cursor.execute(query))
        except Exception as e:
            print(e)
            return False
        
    def get_admins(self):
        query = f"""SELECT * FROM admins"""
        return self.cursor.execute(query)

    def delete_admin(self, telegramid):
        try:
            query = f"""DELETE FROM admins WHERE telegramid='{telegramid}'"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    def add_message(self, messageid):
        try:
            query = f"""INSERT INTO messages VALUES ({messageid})"""
            self.cursor.execute(query)
            self.connector.commit()
            return True
        except Exception as e:
            print(e)
            return False
