import tkinter as tk
from tkinter import ttk
from db.models import Machine
from db.db_manager import DBManager
from typing import List


class MachineWidget(tk.Frame):
    def __init__(self, parent, db_manager: DBManager):
        super().__init__(parent)

        self.db_manager: DBManager = db_manager

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        tk.Label(self, text="Machine Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        self.machine_name_entry = tk.Entry(self)
        self.machine_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.add_machine_button = tk.Button(
            self, text="Add Machine", command=self.add_machine
        )
        self.add_machine_button.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.machine_list_frame = tk.Frame(self.canvas)
        self.machine_list_frame.pack(fill=tk.BOTH, expand=True)
        self.machine_list_frame.grid_columnconfigure(0, weight=1)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.machine_list_frame,
            anchor="nw",
            width=self.canvas.winfo_width(),
        )

        self.machine_list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=2, sticky="ns")

        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Configure>", self.on_resize)

        self.machines: List[Machine] = []

        self.update()

    def update(self):
        self.machines = self.db_manager.get_machines()
        self.update_machine_list()

    def on_resize(self, event):
        # Update the widget width to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mouse_wheel(self, event):
        print(event)
        if event.delta:
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        else:
            # Handle case where event.delta might not be available (like in Linux)
            move = -1 if event.num == 4 else 1
            self.canvas.yview_scroll(move, "units")

    def add_machine(self):
        machine_name = self.machine_name_entry.get().strip()
        machine = Machine(name=machine_name)
        if machine_name:
            self.db_manager.add_machine(machine)
            self.update()

    def update_machine_list(self):
        for widget in self.machine_list_frame.winfo_children():
            widget.destroy()

        for i, machine in enumerate(self.machines):
            frame = tk.Frame(self.machine_list_frame)
            frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0)

            # Label for machine name
            label = tk.Label(frame, text=machine.name)
            label.grid(row=0, column=0, padx=5, sticky="w")

            # Menu button for actions
            menu_button = tk.Menubutton(frame, text="...", relief="flat")
            menu = tk.Menu(menu_button, tearoff=0)
            menu.add_command(label="Edit", command=lambda i=i: self.edit_machine(i))
            menu.add_command(label="Delete", command=lambda i=i: self.delete_machine(i))
            menu_button["menu"] = menu
            menu_button.grid(row=0, column=1, padx=5, sticky="ew")

            # Attach the label widget to the frame for later access
            frame.label_widget = label

    def edit_machine(self, index):
        frame = self.machine_list_frame.winfo_children()[index]

        # Hide the label and replace it with an entry widget
        frame.label_widget.grid_forget()
        entry = tk.Entry(frame)
        entry.insert(0, self.machines[index].name)
        entry.grid(row=0, column=0, padx=5, sticky="ew")

        # Hide the menu button and add Apply/Cancel buttons
        frame.winfo_children()[1].grid_forget()  # Hide menu button

        apply_button = tk.Button(
            frame,
            text="Save",
            command=lambda: self.apply_edit(index, entry),
        )
        apply_button.grid(row=0, column=1, padx=5, sticky="e")

        cancel_button = tk.Button(
            frame,
            text="Cancel",
            command=lambda: self.cancel_edit(index),
        )
        cancel_button.grid(row=0, column=2, padx=5, sticky="e")

        frame.apply_button = apply_button
        frame.cancel_button = cancel_button

    def apply_edit(self, index, entry):
        new_name = entry.get().strip()
        if new_name:
            self.machines[index].name = new_name
            self.db_manager.update_machine(self.machines[index])
        self.update()

    def cancel_edit(self, index):
        self.update_machine_list()

    def delete_machine(self, index):
        self.db_manager.delete_machine(self.machines[index].id)
        self.update()
