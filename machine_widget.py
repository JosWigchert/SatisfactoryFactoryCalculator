import tkinter as tk
from tkinter import ttk


class MachineWidget(tk.Frame):
    def __init__(self, parent, db_manager):
        super().__init__(parent)

        self.db_manager = db_manager

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
        self.canvas.bind(
            "<Configure>",
            lambda event: self.on_resize(event),
        )

        self.machine_list_frame = tk.Frame(self.canvas)
        self.machine_list_frame.pack(fill=tk.BOTH, expand=True)
        self.machine_list_frame.grid_columnconfigure(0, weight=1)
        self.canvas.create_window(
            (1, 1),
            window=self.machine_list_frame,
            anchor="nw",
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

        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        self.machines = []

    def on_resize(self, width):
        # Update the widget width to match the canvas width
        canvas_width = self.canvas.winfo_width()
        self.canvas.create_window(
            (0, 0),
            width=canvas_width,
            window=self.machine_list_frame,
            anchor="nw",
        )

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

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
            frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0)

            # Label for machine name
            label = tk.Label(frame, text=machine)
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
        entry.insert(0, self.machines[index])
        entry.grid(row=0, column=0, padx=5, sticky="ew")

        # Hide the menu button and add Apply/Cancel buttons
        frame.winfo_children()[1].grid_forget()  # Hide menu button

        apply_button = tk.Button(
            frame,
            text="Apply",
            command=lambda: self.apply_edit(index, entry),
            background="lightgreen",
        )
        apply_button.grid(row=0, column=1, padx=5, sticky="e")

        cancel_button = tk.Button(
            frame,
            text="Cancel",
            command=lambda: self.cancel_edit(index),
            background="lightcoral",
        )
        cancel_button.grid(row=0, column=2, padx=5, sticky="e")

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
