#LOG IN
CREATE_TABLE_LOGIN = """CREATE TABLE IF NOT EXISTS login_tbl (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sign_up_tbl (user_id)
)"""

INSERT_CREDS_LOGIN = """INSERT INTO login_tbl (username, password) VALUES (?, ?)"""

SELECT_CREDS_LOGIN = """SELECT * FROM login_tbl WHERE username = ? AND password = ?"""

#SIGN UP
CREATE_TABLE_SIGNUP = """CREATE TABLE IF NOT EXISTS user_signup_tbl (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    confirm_password TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES login_tbl (username)
)"""

INSERT_SIGNUP = """INSERT INTO user_signup_tbl (username, full_name, email, password, confirm_password) 
VALUES (?, ?, ?, ?, ?)"""

SELECT_ALL_SIGNUP = """SELECT username,full_name, email,password,confirm_password FROM user_signup_tbl"""

SELECT_FULLNAME_SIGNUP = """SELECT full_name FROM user_signup_tbl WHERE username = ?"""

#INFORMATION TAKER

CREATE_TABLE_INFO_TAKER = """CREATE TABLE IF NOT EXISTS info_taker_tbl (
    info_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    sign_up_username TEXT NOT NULL,
    login_username TEXT NOT NULL,
    full_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    fitness_objective TEXT,
    activity_level TEXT,
    desired_weight REAL,
    months_to_achieve_goal INTEGER,
    FOREIGN KEY (user_id) REFERENCES sign_up_tbl (user_id),
    FOREIGN KEY (full_name) REFERENCES user_signup_tbl (full_name)
)"""

INSERT_INFO_TAKER = """ INSERT INTO info_taker_tbl (age, gender, height, weight, fitness_objective, activity_level, desired_weight, months_to_achieve_goal)
VALUES (?, ?, ?, ?, ?, ?, ?)"""

SELECT_ALL_INFO = """SELECT age, gender, height, weight, fitness_objective, activity_level, desired_weight, months_to_achieve_goal FROM info_taker_tbl"""

UPDATE_INFO_TAKER = """
UPDATE info_taker
SET fitness_objective = ?, activity_level = ?
WHERE sign_up_username = ?
"""

#NET CALORIE TAKER
CREATE_TABLE_CALORIE_TAKER = """
CREATE TABLE IF NOT EXISTS net_calorie_tbl (
    user_id INTEGER NOT NULL,
    net_calorie REAL NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES info_taker_tbl (info_id)
)
"""

INSERT_CALORIE_TAKER = """
INSERT INTO net_calorie_tbl (user_id, net_calorie) VALUES (?, ?)
"""

SELECT_NET_CALORIE = """
SELECT * FROM net_calorie_tbl WHERE user_id = ?
"""

#FOOD RECORDER
CREATE_TABLE_FOOD = """
CREATE TABLE IF NOT EXISTS food_tbl (
    food_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    food_name TEXT NOT NULL,
    food_quantity REAL NOT NULL,
    meal_category TEXT NOT NULL,
    calories REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES sign_up_tbl (user_id)
)
"""

INSERT_FOOD_ENTRY = """
INSERT INTO food_tbl (food_name, food_quantity, meal_category,calories,created_at, updated_at,user_id)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""


SELECT_ALL_FOOD_ENTRIES = """
SELECT * FROM food_tbl
"""

SELECT_ALL_FOOD_ENTRIES_BY_USER = """
SELECT * FROM food_tbl
WHERE user_id = ?
"""

SELECT_FOOD_ENTRY_BY_ID = """
SELECT * FROM food_tbl
WHERE food_id = ?
"""

UPDATE_FOOD_ENTRY = """
UPDATE food_tbl
SET food_name = ?, food_quantity = ?, meal_category = ?, calories = ?, updated_at = CURRENT_TIMESTAMP
WHERE food_id = ?
"""

DELETE_FOOD_ENTRY = """
DELETE FROM food_tbl
WHERE food_id = ?
"""

#ALL CALORIE TAKER
CREATE_TABLE_ALL_CALORIE = """
CREATE TABLE IF NOT EXISTS all_calorie_tbl (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    all_calorie REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES sign_up_tbl (user_id)
) """

INSERT_ALL_CALORIE = """
INSERT INTO all_calorie_tbl (user_id, all_calorie) VALUES (?, ?)
"""

SELECT_ALL_CALORIE = """
SELECT * FROM all_calorie_tbl WHERE user_id = ?
"""
