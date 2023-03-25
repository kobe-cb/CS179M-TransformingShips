from helpers.imports import *


class PreRunWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.base_menu = tk.Frame(self)
        self.base_menu.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.canvas = tk.Canvas(self.base_menu, width=1200, height=1000)
        self.canvas.pack()

        self.text = self.canvas.create_text(
            600, 500, text="Calculating...", font=("Helvetica", 48), justify="center"
        )
