import sqlite3
import logging
from datetime import datetime, timedelta
from sqlite3 import Error

from queries import CREATE_TABLE_LOGIN, INSERT_CREDS_LOGIN, SELECT_CREDS_LOGIN, SELECT_ALL_FOOD_ENTRIES_BY_USER

from queries import CREATE_TABLE_SIGNUP, INSERT_SIGNUP, SELECT_ALL_SIGNUP, SELECT_FULLNAME_SIGNUP

from queries import CREATE_TABLE_INFO_TAKER, INSERT_INFO_TAKER, SELECT_ALL_INFO

from queries import CREATE_TABLE_CALORIE_TAKER, INSERT_CALORIE_TAKER, SELECT_NET_CALORIE

from queries import CREATE_TABLE_FOOD, INSERT_FOOD_ENTRY, SELECT_ALL_FOOD_ENTRIES, \
    UPDATE_FOOD_ENTRY, DELETE_FOOD_ENTRY

from queries import CREATE_TABLE_ALL_CALORIE, INSERT_ALL_CALORIE, SELECT_ALL_CALORIE

from models import FoodModel


class LogInCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_log(self):
        try:
            self.cur.execute(CREATE_TABLE_LOGIN)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_creds_log(self, username, password):
        try:
            self.cur.execute(INSERT_CREDS_LOGIN, (username, password))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_creds_log(self, username, password):
        try:
            self.cur.execute(SELECT_CREDS_LOGIN, (username, password))
            user = self.cur.fetchone()
            return user if user else None
        except sqlite3.Error as e:
            logging.error(e)
            return None


class SignupCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_sign(self):
        try:
            self.cur.execute(CREATE_TABLE_SIGNUP)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_creds_sign(self, username, full_name, email, password, confirm_password):
        try:
            self.cur.execute(INSERT_SIGNUP, (username, full_name, email, password, confirm_password))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_all_creds_sign(self):
        try:
            self.cur.execute(SELECT_ALL_SIGNUP)
            users = self.cur.fetchall()
            return users if users else None
        except sqlite3.Error as e:
            logging.error(e)
            return None

    def select_full_name_sign(self, username: str):
        try:
            self.cur.execute(SELECT_FULLNAME_SIGNUP, (username,))
            full_name = self.cur.fetchone()
            return full_name[0] if full_name else None
        except sqlite3.Error as e:
            logging.error(e)
            return None
        # username taker for info taker page ito.


class InfoTakerCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_info(self):
        try:
            self.cur.execute(CREATE_TABLE_INFO_TAKER)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_creds_info(self, user_id, age, gender, height, weight, fitness_objective, activity_level, desired_weight,
                          months_to_achieve_goal):
        try:
            self.cur.execute(INSERT_INFO_TAKER,
                             (user_id, age, gender, height, weight, fitness_objective, activity_level, desired_weight,
                              months_to_achieve_goal))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_creds_info(self):
        try:
            self.cur.execute(SELECT_ALL_INFO)
            user = self.cur.fetchall()
            return user if user else None
        except sqlite3.Error as e:
            logging.error(e)
            return None


class NetCalorieCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_info(self):
        try:
            self.cur.execute(CREATE_TABLE_CALORIE_TAKER)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_calorie_taker(self, user_id, net_calorie):
        try:
            self.cur.execute(INSERT_CALORIE_TAKER, (user_id, net_calorie))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_net_calorie(self, user_id):
        try:
            self.cur.execute(SELECT_NET_CALORIE, (user_id,))
            net_calorie = self.cur.fetchone()
            return net_calorie if net_calorie else None
        except sqlite3.Error as e:
            logging.error(e)
            return None


class TotalCalorieCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_all_calorie(self):
        try:
            self.cur.execute(CREATE_TABLE_ALL_CALORIE)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(e)
            return False

    def insert_all_calorie(self, user_id, all_calorie):
        try:
            self.cur.execute(INSERT_ALL_CALORIE, (user_id, all_calorie))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(e)
            return False

    def select_all_calorie(self, user_id):
        try:
            self.cur.execute(SELECT_ALL_CALORIE, (user_id,))
            all_calorie = self.cur.fetchall()
            return all_calorie if all_calorie else None
        except sqlite3.Error as e:
            logging.error(e)
            return None

    def get_total_calories_last_24_hours(self, user_id):
        try:
            now = datetime.now()
            last_24_hours = now - timedelta(days=1)
            self.cur.execute(
                "SELECT SUM(calories) FROM food_tbl WHERE user_id = ? AND created_at BETWEEN ? AND ?",
                (user_id, last_24_hours, now)
            )
            total_calories = self.cur.fetchone()[0]
            return total_calories if total_calories else 0
        except sqlite3.Error as e:
            logging.error(e)
            return None

    def record_daily_calories(self):
        try:
            self.cur.execute("SELECT DISTINCT user_id FROM food_tbl")
            user_ids = self.cur.fetchall()
            for user_id_tuple in user_ids:
                user_id = user_id_tuple[0]
                total_calories = self.get_total_calories_last_24_hours(user_id)
                if total_calories:
                    self.insert_all_calorie(user_id, total_calories)
            return True
        except sqlite3.Error as e:
            logging.error(e)
            return False


class FoodCredentials:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db')
        self.cur = self.conn.cursor()

    def create_table_food(self):
        try:
            self.cur.execute(CREATE_TABLE_FOOD)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_food(self, food_name, food_quantity, meal_category, calories, created_at, updated_at, user_id):
        try:
            self.cur.execute(INSERT_FOOD_ENTRY,
                             (food_name, food_quantity, meal_category, calories, created_at, updated_at, user_id))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_food(self):
        try:
            rows: list[FoodModel] = self.cur.execute(SELECT_ALL_FOOD_ENTRIES).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def update_food_by_id(self, food_id, food_name, food_quantity, meal_category, calories):
        try:
            self.cur.execute(UPDATE_FOOD_ENTRY, (food_name, food_quantity, meal_category, calories, food_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(e)
            return False

    def remove_food_by_id(self, food_id):
        try:
            self.cur.execute(DELETE_FOOD_ENTRY, (food_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(e)
            return False

    def __del__(self):
        if self.conn is not None:
            self.conn.close()


def add_user_id_column():
    conn = sqlite3.connect('fitness.db')
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE food_tbl ADD COLUMN user_id INTEGER")
        conn.commit()
        print("Column added successfully")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()


fc = FoodCredentials()
