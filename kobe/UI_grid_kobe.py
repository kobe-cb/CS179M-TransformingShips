import tkinter as tk
from tkinter import messagebox

# Define the function to handle the label clicks


def label_click(event):
    row = int(event.widget.grid_info()['row'])
    column = int(event.widget.grid_info()['column'])
    print(f"Label clicked at row {row} and column {column}")
    # Check if the label has already been clicked once
    if toggle_var.get():
        event.widget.fullname = event.widget.cget("text")
        messagebox.showinfo("Label Info", event.widget.fullname)
    else:
        # Change the background color of the label
        current_color = event.widget.cget("bg")
        if current_color == "green":
            event.widget.config(bg="red")
        elif current_color == "red":
            event.widget.config(bg="blue")
        elif current_color == "blue":
            event.widget.config(bg=window.cget("bg"))
        else:
            event.widget.config(bg="green")


# Create the Tkinter window
window = tk.Tk()

toggle_var = tk.BooleanVar()
toggle_var.set(False)
toggle_button = tk.Checkbutton(
    window, text="Toggle Labels", variable=toggle_var)
toggle_button.grid(row=0, column=11, padx=5, pady=5, sticky="e")

label_names = [['UNUSED' for column in range(8)] for row in range(12)]
# Create the labels in a grid
for row in range(12):
    for column in range(8):
        # Create the label and add the event binding to call label_click
        label = tk.Label(window, width=5, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=row, column=column)
        label.bind("<Button-1>", label_click)

        # Define the function to handle the label hover


# Read the file and map the coordinates to the grid
with open("data/ShipCase1.txt", "r") as file:
    for line in file:
        parts = line.strip().split(",")
        coords = [0, 0]
        coords[0] = parts[0].strip("[")
        coords[1] = parts[1].strip("]")
        name = parts[3].strip()
        print("Name:" + name)
        print(coords[0])
        print(coords[1])
        label_names[row][column] = name
        # Adjust for zero-indexing
        row, column = int(coords[1])-1, int(coords[0])-1
        """
        label = tk.Label(window, text=name)
        label.grid(row=row, column=column)
        """
        label = tk.Label(window, text=name, width=10, height=2,
                         borderwidth=1, relief="solid")
        label.grid(row=row, column=column)
        # label.clicked = False
        label.bind("<Button-1>", label_click)


# Run the Tkinter event loop
window.mainloop()
