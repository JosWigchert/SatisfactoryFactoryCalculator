from typing import List, Dict
from db.models import Item, Machine, Recipe
import sqlite3


class DBManager:
    def __init__(self, db_name="factory_designer.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            machine_id INTEGER,
            output_amount INTEGER NOT NULL,
            FOREIGN KEY(item_id) REFERENCES items(id),
            FOREIGN KEY(machine_id) REFERENCES machines(id)
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            item_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        )
        """
        )

        self.conn.commit()

    def add_item(self, item: Item) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT OR IGNORE INTO items (name) VALUES (?)
        """,
            (item.name,),
        )
        self.conn.commit()
        return cursor.lastrowid

    def add_machine(self, machine: Machine) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT OR IGNORE INTO machines (name) VALUES (?)
        """,
            (machine.name,),
        )
        self.conn.commit()
        return cursor.lastrowid

    def add_recipe(self, recipe: Recipe):
        item_id = self.add_item(recipe.item)
        machine_id = self.add_machine(recipe.machine)

        cursor = self.conn.cursor()
        cursor.execute(
            """
        INSERT INTO recipes (item_id, machine_id, output_amount) VALUES (?, ?, ?)
        """,
            (item_id, machine_id, recipe.output_amount),
        )
        recipe_id = cursor.lastrowid

        for input_item, quantity in recipe.inputs.items():
            input_item_id = self.add_item(input_item)
            cursor.execute(
                """
            INSERT INTO recipe_ingredients (recipe_id, item_id, quantity)
            VALUES (?, ?, ?)
            """,
                (recipe_id, input_item_id, quantity),
            )

        self.conn.commit()

    def update_item(self, item: Item):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        UPDATE items SET name = ? WHERE id = ?
        """,
            (item.name, item.id),
        )
        self.conn.commit()

    def update_machine(self, machine: Machine):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        UPDATE machines SET name = ? WHERE id = ?
        """,
            (machine.name, machine.id),
        )
        self.conn.commit()

    def update_recipe(self, recipe: Recipe):
        cursor = self.conn.cursor()

        # Update the recipe's main details
        cursor.execute(
            """
        UPDATE recipes SET item_id = ?, machine_id = ?, output_amount = ? WHERE id = ?
        """,
            (recipe.item.id, recipe.machine.id, recipe.output_amount, recipe.id),
        )

        # Remove existing ingredients
        cursor.execute(
            """
        DELETE FROM recipe_ingredients WHERE recipe_id = ?
        """,
            (recipe.id,),
        )

        # Insert updated ingredients
        for input_item, quantity in recipe.inputs.items():
            input_item_id = self.add_item(input_item)
            cursor.execute(
                """
            INSERT INTO recipe_ingredients (recipe_id, item_id, quantity)
            VALUES (?, ?, ?)
            """,
                (recipe.id, input_item_id, quantity),
            )

        self.conn.commit()

    def delete_item(self, item_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        DELETE FROM items WHERE id = ?
        """,
            (item_id,),
        )
        self.conn.commit()

    def delete_machine(self, machine_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            """
        DELETE FROM machines WHERE id = ?
        """,
            (machine_id,),
        )
        self.conn.commit()

    def delete_recipe(self, recipe_id: int):
        cursor = self.conn.cursor()

        # Delete ingredients associated with the recipe
        cursor.execute(
            """
        DELETE FROM recipe_ingredients WHERE recipe_id = ?
        """,
            (recipe_id,),
        )

        # Delete the recipe itself
        cursor.execute(
            """
        DELETE FROM recipes WHERE id = ?
        """,
            (recipe_id,),
        )

        self.conn.commit()

    def get_items(self) -> List[Item]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM items")
        return [Item(id=row[0], name=row[1]) for row in cursor.fetchall()]

    def get_machines(self) -> List[Machine]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM machines")
        return [Machine(id=row[0], name=row[1]) for row in cursor.fetchall()]

    def get_recipes(self) -> List[Recipe]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
        SELECT r.id, i.id, i.name, m.id, m.name, r.output_amount
        FROM recipes r
        JOIN items i ON r.item_id = i.id
        JOIN machines m ON r.machine_id = m.id
        """
        )
        recipe_rows = cursor.fetchall()

        recipes = []
        for (
            recipe_id,
            item_id,
            item_name,
            machine_id,
            machine_name,
            output_amount,
        ) in recipe_rows:
            cursor.execute(
                """
            SELECT ii.id, ii.name, ri.quantity
            FROM recipe_ingredients ri
            JOIN items ii ON ri.item_id = ii.id
            WHERE ri.recipe_id = ?
            """,
                (recipe_id,),
            )
            ingredients = cursor.fetchall()

            item = Item(id=item_id, name=item_name)
            machine = Machine(id=machine_id, name=machine_name)
            inputs = {
                Item(id=ing_id, name=ing_name): qty
                for ing_id, ing_name, qty in ingredients
            }

            recipe = Recipe(
                id=recipe_id,
                item=item,
                machine=machine,
                inputs=inputs,
                output_amount=output_amount,
            )
            recipes.append(recipe)

        return recipes

    def close(self):
        self.conn.close()
