import logging
import sqlite3
from sqlite3 import Error

DB_NAME = "data_info.db"


class Db:
    __conn = None
    __cur = None

    def __init__(self):
        self.set_connection(DB_NAME)
        self.set_cursor()

    def set_connection(self, db):
        self.__conn = sqlite3.connect(db)

    def set_cursor(self):
        self.__cur = self.__conn.cursor()

    def get_connection(self):
        return self.__conn

    def get_cursor(self):
        return self.__cur

    def __del__(self):
        if self.__conn:
            self.__conn.close()


class AuthTbl(Db):
    def __init__(self):
        super().__init__()
        self.conn = self.get_connection()
        self.cur = self.get_cursor()
        self.create_table()

    def create_table(self):
        try:
            sql = """CREATE TABLE IF NOT EXISTS auth_tbl(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT NOT NULL,
                        age REAL NOT NULL,
                        gender TEXT NOT NULL, 
                        height REAL NOT NULL,
                        weight REAL NOT NULL,
                        fitness_objective TEXT NOT NULL,
                        activity_level TEXT NOT NULL,
                        fitness_goal TEXT NOT NULL,
                        how_many_months_process REAL NOT NULL,
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL
                  )"""
            self.cur.execute(sql)
            self.conn.commit()
        except Error as e:
            logging.error(e)

    def insert_info(self, username, email, password, name, age, gender, height, weight, fitness_objective,
                    activity_level, fitness_goal, how_many_months_process, created_at, updated_at):
        try:
            sql = """INSERT INTO auth_tbl(
                            username,
                            email,
                            password,
                            name,
                            age,
                            gender,
                            height,
                            weight,
                            fitness_objective,
                            activity_level,
                            fitness_goal,
                            how_many_months_process,
                            created_at,
                            updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            result = self.cur.execute(sql, (
                username,
                email,
                password,
                name,
                age,
                gender,
                height,
                weight,
                fitness_objective,
                activity_level,
                fitness_goal,
                how_many_months_process,
                created_at,
                updated_at))
            self.conn.commit()
            return result.lastrowid or None
        except Error as e:
            logging.error(e)
            return None

    def login(self, username, password):
        try:
            sql = """SELECT * FROM auth_tbl WHERE username = ? AND password = ?"""
            result = self.cur.execute(sql, (username, password)).fetchone()
            return result or None
        except Error as e:
            logging.error(e)
            return None

    def select_by_id(self, user_id):
        try:
            sql = """SELECT * FROM auth_tbl WHERE id = ?"""
            result = self.cur.execute(sql, (user_id,)).fetchone()
            return result or None
        except Error as e:
            logging.error(e)
            return None

    def delete_data_by_id(self, user_id):
        try:
            sql = """DELETE FROM auth_tbl WHERE id = ?"""
            self.cur.execute(sql, (user_id,))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False


auth_tbl = AuthTbl()
