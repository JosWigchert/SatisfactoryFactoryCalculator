# production_logic.py


class ProductionLogic:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def parse_recipe(self, recipe):
        input_items = {
            item.split(":")[0]: int(item.split(":")[1]) for item in recipe[2].split(",")
        }
        output_items = {
            item.split(":")[0]: int(item.split(":")[1]) for item in recipe[3].split(",")
        }
        return input_items, output_items

    def calculate_production(self, target_item, amount):
        recipes = self.db_manager.get_recipes()
        production_tree = {}
        self._calculate(target_item, amount, recipes, production_tree)
        return production_tree

    def _calculate(self, target_item, amount, recipes, production_tree):
        for recipe in recipes:
            name, _, input_items_str, output_items_str, machine = recipe
            input_items, output_items = self.parse_recipe(recipe)

            if target_item in output_items:
                ratio = amount / output_items[target_item]
                production_tree[target_item] = {
                    "amount": amount,
                    "machine": machine,
                    "inputs": {},
                }

                for item, qty in input_items.items():
                    required_amount = qty * ratio
                    production_tree[target_item]["inputs"][item] = {}
                    self._calculate(
                        item,
                        required_amount,
                        recipes,
                        production_tree[target_item]["inputs"],
                    )
