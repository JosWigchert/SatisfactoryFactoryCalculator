# gui/gui_manager.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
from db.models import Item, Machine, Recipe
from gui.gui_data_manager import DataManager
from logic.production_logic import ProductionLogic
import tkinter.simpledialog as simpledialog
from db.db_manager import DBManager
from tkinter import PhotoImage


class GUIManager:
    def __init__(self, root):
        self.root = root
        self.db_manager = DBManager()
        self.data_manager = DataManager(self.db_manager)
        self.production_logic = ProductionLogic(self.db_manager)

        self.setup_gui()

    def setup_gui(self):
        self.root.title("Factory Designer")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.machine_tab = ttk.Frame(self.notebook)
        self.item_tab = ttk.Frame(self.notebook)
        self.recipe_tab = ttk.Frame(self.notebook)
        self.generate_tree_tab = ttk.Frame(self.notebook)

        # Set up each tab, order specifies the order of the tabs
        self.setup_generate_tree_tab(self.generate_tree_tab)
        self.setup_machine_tab(self.machine_tab)
        self.setup_item_tab(self.item_tab)
        self.setup_recipe_tab(self.recipe_tab)

        # Bind tab selection events
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def setup_machine_tab(self, frame: tk.Widget):
        self.notebook.add(frame, text="Machines")

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        tk.Label(frame, text="Machine Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        self.machine_name_entry = tk.Entry(frame)
        self.machine_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.add_machine_button = tk.Button(
            frame,
            text="Add Machine",
            command=self.add_machine,
            # command=self.data_manager.add_machine,
        )
        self.add_machine_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        # self.machine_listbox = tk.Listbox(frame)
        # self.machine_listbox.grid(
        #     row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        # )

        # Canvas and Frame to hold the machine list with buttons
        self.canvas = tk.Canvas(frame)
        self.canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.machine_list_frame = tk.Frame(self.canvas)
        self.machine_list_frame.grid(sticky="nsew")

        self.canvas.create_window((0, 0), window=self.machine_list_frame, anchor="nw")

        self.machine_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Adding a scrollbar
        self.scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=2, sticky="ns")

        self.machines = []

        # Load icons (you would typically use actual image files)
        self.update_icon = PhotoImage(
            width=16, height=16
        )  # Placeholder for an actual icon
        self.delete_icon = PhotoImage(
            width=16, height=16
        )  # Placeholder for an actual icon
        self.apply_icon = PhotoImage(
            width=16, height=16
        )  # Placeholder for an actual icon
        self.cancel_icon = PhotoImage(
            width=16, height=16
        )  # Placeholder for an actual icon
        self.menu_icon = PhotoImage(
            width=16, height=16
        )  # Placeholder for an actual icon

    def add_machine(self):
        machine_name = self.machine_name_entry.get().strip()
        if machine_name:
            self.machines.append(machine_name)
            self.update_machine_list()

    def update_machine_list(self):
        for widget in self.machine_list_frame.winfo_children():
            widget.destroy()

        for i, machine in enumerate(self.machines):
            frame = tk.Frame(self.machine_list_frame)
            frame.grid(row=i, column=0, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)

            # Create a menu button with a triple-dot icon
            menu_button = tk.Menubutton(frame, image=self.menu_icon, relief="flat")
            menu = tk.Menu(menu_button, tearoff=0)
            menu.add_command(label="Update", command=lambda i=i: self.edit_machine(i))
            menu.add_command(label="Delete", command=lambda i=i: self.delete_machine(i))
            menu_button["menu"] = menu
            menu_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

            label = tk.Label(frame, text=machine)
            label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Attach the label widget to the frame for later access
            frame.label_widget = label

    def edit_machine(self, index):
        frame = self.machine_list_frame.winfo_children()[index]

        # Hide the label and replace it with an entry widget
        frame.label_widget.grid_forget()
        entry = tk.Entry(frame)
        entry.insert(0, self.machines[index])
        entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Hide the menu button and add Apply/Cancel buttons
        frame.winfo_children()[1].grid_forget()  # Hide menu button

        apply_button = tk.Button(
            frame, image=self.apply_icon, command=lambda: self.apply_edit(index, entry)
        )
        apply_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        cancel_button = tk.Button(
            frame, image=self.cancel_icon, command=lambda: self.cancel_edit(index)
        )
        cancel_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        frame.apply_button = apply_button
        frame.cancel_button = cancel_button

    def apply_edit(self, index, entry):
        new_name = entry.get().strip()
        if new_name:
            self.machines[index] = new_name
        self.update_machine_list()

    def cancel_edit(self, index):
        self.update_machine_list()

    def delete_machine(self, index):
        del self.machines[index]
        self.update_machine_list()

    def setup_item_tab(self, frame: tk.Widget):
        self.notebook.add(frame, text="Items")

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

        tk.Label(frame, text="Item Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.item_name_entry = tk.Entry(frame)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.add_item_button = tk.Button(
            frame,
            text="Add Item",
            # command=self.add_item,
        )
        self.add_item_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.item_listbox = tk.Listbox(frame)
        self.item_listbox.grid(
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

    def setup_recipe_tab(self, frame: tk.Widget):
        self.notebook.add(frame, text="Recipes")

        tk.Label(self.recipe_tab, text="Recipe for Item:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.recipe_item_combobox = ttk.Combobox(self.recipe_tab)
        self.recipe_item_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.recipe_tab, text="Machine:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.recipe_machine_combobox = ttk.Combobox(self.recipe_tab)
        self.recipe_machine_combobox.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

        tk.Label(self.recipe_tab, text="Output Amount:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )
        self.output_amount_entry = tk.Entry(self.recipe_tab)
        self.output_amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        tk.Label(self.recipe_tab, text="Inputs:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        self.input_frame = tk.Frame(self.recipe_tab)
        self.input_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.input_items: List[Tuple[Item, int]] = []
        self.add_input_button = tk.Button(
            self.recipe_tab,
            text="Add Input",
            # command=self.data_manager.add_input_item,
        )
        self.add_input_button.grid(row=4, column=1, pady=10, sticky="e")

        self.add_recipe_button = tk.Button(
            self.recipe_tab,
            text="Add Recipe",
            # command=self.data_manager.add_recipe,
        )
        self.add_recipe_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Make sure input frame expands with the window
        self.recipe_tab.grid_rowconfigure(3, weight=1)
        self.recipe_tab.grid_columnconfigure(1, weight=1)

    def setup_generate_tree_tab(self, frame: tk.Widget):
        self.notebook.add(frame, text="Generate Production Tree")

        tk.Label(self.generate_tree_tab, text="Target Item:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.target_item_combobox = ttk.Combobox(self.generate_tree_tab)
        self.target_item_combobox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.generate_tree_tab, text="Amount:").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.amount_entry = tk.Entry(self.generate_tree_tab)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.generate_tree_button = tk.Button(
            self.generate_tree_tab,
            text="Generate Tree",
            # command=self.generate_production_tree,
        )
        self.generate_tree_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.generate_tree_tab)
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.generate_tree_tab.grid_rowconfigure(3, weight=1)
        self.generate_tree_tab.grid_columnconfigure(0, weight=1)

    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab is self.notebook.index(self.machine_tab):
            self.get_machine_tab_data()
        elif selected_tab is self.notebook.index(self.item_tab):
            self.get_item_tab_data()
        elif selected_tab is self.notebook.index(self.recipe_tab):
            self.get_recipe_tab_data()
        elif selected_tab is self.notebook.index(self.generate_tree_tab):
            self.get_generate_tree_tab_data()

    def get_machine_tab_data(self):
        self.machine_listbox.delete(0, tk.END)
        for machine in self.db_manager.get_machines():
            self.machine_listbox.insert(tk.END, machine.name)

    def get_item_tab_data(self):
        self.item_listbox.delete(0, tk.END)
        for item in self.db_manager.get_items():
            self.item_listbox.insert(tk.END, item.name)

    def get_recipe_tab_data(self):
        self.recipe_item_combobox["values"] = [
            item.name for item in self.db_manager.get_items()
        ]
        self.recipe_machine_combobox["values"] = [
            item.name for item in self.db_manager.get_machines()
        ]

    def get_generate_tree_tab_data(self):
        self.target_item_combobox["values"] = [
            item.name for item in self.db_manager.get_items()
        ]

    def refresh_input_items(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        for i, (item, qty) in enumerate(self.input_items):
            tk.Label(self.input_frame, text=item.name).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )
            quantity_entry = tk.Entry(
                self.input_frame, textvariable=tk.StringVar(value=qty)
            )
            quantity_entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

            def remove_callback(i=i):
                self.input_items.pop(i)
                self.refresh_input_items()

            tk.Button(self.input_frame, text="Remove", command=remove_callback).grid(
                row=i, column=2, padx=5, pady=5
            )
        # Make sure the input frame expands with the window
        self.input_frame.grid_rowconfigure(len(self.input_items), weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

    def clear_recipe_form(self):
        self.recipe_item_combobox.set("")
        self.recipe_machine_combobox.set("")
        self.input_items = []
        self.refresh_input_items()

    def generate_production_tree(self):
        target_item_name = self.target_item_combobox.get()
        try:
            amount = int(self.amount_entry.get())
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount")
            return

        production_tree = self.production_logic.calculate_production(
            target_item_name, amount
        )
        self.display_production_tree(production_tree)

    def display_production_tree(self, production_tree):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self._insert_tree("", production_tree)

    def _insert_tree(self, parent, tree_data):
        for item_name, details in tree_data.items():
            item_node = self.tree.insert(
                parent, "end", text=f"{item_name} ({details['amount']})"
            )
            for input_name, input_details in details["inputs"].items():
                self._insert_tree(item_node, {input_name: input_details})
