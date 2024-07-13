import sqlite3
import logging

from sqlite3 import Error

from queries import CREATE_TABLE_FOOD, INSERT_FOOD_ENTRY, SELECT_FOOD_ENTRY_BY_ID, UPDATE_FOOD_ENTRY, DELETE_FOOD_ENTRY


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

    def insert_food(self, food_name, food_quantity, meal_category, calories, created_at, updated_at):
        try:
            self.cur.execute(INSERT_FOOD_ENTRY, (food_name, food_quantity, meal_category, calories, created_at, updated_at))
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_food(self, food_id):
        try:
            self.cur.execute(SELECT_FOOD_ENTRY_BY_ID, (food_id,))
            user = self.cur.fetchone()
            return user if user else None
        except sqlite3.Error as e:
            logging.error(e)
            return None

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


fc = FoodCredentials()