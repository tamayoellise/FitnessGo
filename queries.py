CREATE_TABLE_FOOD = """
CREATE TABLE IF NOT EXISTS food_tbl (
    food_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    food_name TEXT NOT NULL,
    food_quantity REAL NOT NULL,
    meal_category TEXT NOT NULL,
    calories REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

INSERT_FOOD_ENTRY = """
INSERT INTO food_tbl (food_name, food_quantity, meal_category, calories,created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?)
"""

SELECT_ALL_FOOD_ENTRIES = """
SELECT * FROM food_tbl
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