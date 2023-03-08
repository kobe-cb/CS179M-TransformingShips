from tkinter import *
from tkinter import messagebox


class balanceUI:
    def __init__(self):
        self.base = Tk()
        self.base.title("TransformingShips")
        self.base.geometry("640x300")

        # Create a frame to hold the buttons and container list
        self.base_menu = Frame(self.base)
        self.base_menu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create the "Comment" button
        comment_button = Button(self.base_menu, text="Comment", width=8, height=1, command=self.run)
        comment_button.grid(row=1, column=0, sticky="nw")

        # Title the Element
        title_label = Label(self.base_menu, text="Balance", font=("Comic Sans", 16))
        title_label.grid(row=0, column=3, padx=25, sticky="nsew")

        # Create the "Run" button
        run_button = Button(self.base_menu, text="Balance", width=10, height=5, command=self.run)
        run_button.grid(row=2, column=2, pady=20, sticky="sew")

        # Create the "Main Menu" button
        main_menu_button = Button(self.base_menu, text="Main Menu", width=10, height=2, command=self.run)
        main_menu_button.grid(row=3, column=1, pady=50, sticky="sew")

        self.base.mainloop()

    def run(self):
        # Print "Running" in the console
        print("Running")


balanceUI()
