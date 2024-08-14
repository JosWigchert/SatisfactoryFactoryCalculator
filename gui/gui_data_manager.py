from tkinter import ttk, messagebox
from db.db_manager import DBManager
from db.models import Item, Machine, Recipe


class DataManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # def add_machine(self):
    #     name = self.machine_name_entry.get()
    #     if not name:
    #         messagebox.showerror("Error", "Machine name cannot be empty")
    #         return

    #     machine = Machine(id=None, name=name)
    #     self.db_manager.add_machine(machine)
    #     self.refresh_machines()
    #     self.machine_name_entry.delete(0, tk.END)
    #     # messagebox.showinfo("Success", "Machine added successfully")

    # def add_item(self):
    #     name = self.item_name_entry.get()
    #     if not name:
    #         messagebox.showerror("Error", "Item name cannot be empty")
    #         return

    #     item = Item(id=None, name=name)
    #     self.db_manager.add_item(item)
    #     self.refresh_items()
    #     self.item_name_entry.delete(0, tk.END)
    #     # messagebox.showinfo("Success", "Item added successfully")

    # def add_recipe(self):
    #     item_name = self.recipe_item_combobox.get()
    #     machine_name = self.recipe_machine_combobox.get()
    #     try:
    #         output_amount = int(self.output_amount_entry.get())
    #         if output_amount <= 0:
    #             raise ValueError
    #     except (ValueError, TypeError):
    #         messagebox.showerror("Error", "Invalid output amount")
    #         return

    #     if not item_name or not machine_name:
    #         messagebox.showerror("Error", "Item and machine must be selected")
    #         return

    #     inputs = {}
    #     for input_item, qty in self.input_items:
    #         if qty <= 0:
    #             messagebox.showerror("Error", "Quantity must be positive")
    #             return
    #         inputs[input_item] = qty

    #     item = Item(id=None, name=item_name)
    #     machine = Machine(id=None, name=machine_name)
    #     recipe = Recipe(
    #         id=None,
    #         item=item,
    #         machine=machine,
    #         inputs=inputs,
    #         output_amount=output_amount,
    #     )
    #     self.db_manager.add_recipe(recipe)
    #     self.clear_recipe_form()
    #     self.refresh_items()

    # def add_input_item(self):
    #     item_name = tk.simpledialog.askstring("Input", "Enter item name:")
    #     if not item_name:
    #         return

    #     try:
    #         quantity = int(tk.simpledialog.askstring("Input", "Enter quantity:"))
    #         if quantity <= 0:
    #             raise ValueError
    #     except (ValueError, TypeError):
    #         messagebox.showerror("Error", "Invalid quantity")
    #         return

    #     item = Item(id=None, name=item_name)
    #     self.input_items.append((item, quantity))

    #     self.refresh_input_items()
