import tkinter as tk
from tkinter import ttk
from machine_widget import MachineWidget


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Machine Manager")
        self.geometry("400x300")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.machine_widget = MachineWidget(self)
        self.notebook.add(self.machine_widget, text="Machines")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
