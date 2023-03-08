from tkinter import *
from tkinter import messagebox


class UnloadLoadUI:
    def __init__(self):
        self.base = Tk()
        self.base.title("TransformingShips")
        self.base.geometry("640x300")
        self.container_weight_entry = None
        self.container_name_entry = None
        self.add_container_frame = None

        # Create an array to hold the containers
        self.containers = []

        self.base.rowconfigure(0, weight=1)
        self.base.columnconfigure(0, weight=1)

        # Create a frame to hold the buttons and container list
        self.base_menu = Frame(self.base)
        self.base_menu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.base_menu.rowconfigure(2, weight=1)
        self.base_menu.columnconfigure(0, weight=1)
        self.base_menu.columnconfigure(5, weight=1)

        # Create the "Run" button
        run_button = Button(self.base_menu, text="Run", width=5, height=5, command=self.run)
        run_button.grid(row=2, column=5, pady=30, sticky="sew")

        # Create the "Add Container" button
        load_new_button = Button(self.base_menu, text="Add Container", width=5, height=5, command=self.show_add_container_frame)
        load_new_button.grid(row=2, column=5, pady=30, sticky='new')

        # Title the Element
        title_label = Label(self.base_menu, text="Load/Unload", font=("Comic Sans", 16))
        title_label.grid(row=0, column=1, sticky="nsew")

        # Create a label for the container list
        action_title = Label(self.base_menu, text="Actions Queued")
        action_title.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Create a Listbox widget to hold the container list
        self.action_queue = Listbox(self.base_menu)
        self.action_queue.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.base_menu.rowconfigure(2, weight=1)
        self.base_menu.columnconfigure(0, weight=1)

        self.base.mainloop()

    def show_add_container_frame(self):
        # Hide the main frame
        self.base_menu.grid_forget()

        # Create a new frame for adding a container
        self.add_container_frame = Frame(self.base)
        self.add_container_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create labels and entry fields for the container name and weight
        container_name = Label(self.add_container_frame, text="Container Name:")
        container_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.container_name_entry = Entry(self.add_container_frame)
        self.container_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        container_weight = Label(self.add_container_frame, text="Container Weight (in kgs):")
        container_weight.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.container_weight_entry = Entry(self.add_container_frame)
        self.container_weight_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Create a "Submit" button to add the container to the list
        place_button = Button(self.add_container_frame, text="Place", command=self.submit_container)
        place_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Create a "Back" button to go back to the main frame
        back_button = Button(self.add_container_frame, text="Back", command=self.show_base_menu)
        back_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def show_base_menu(self):
        # Destroy the add container frame
        self.add_container_frame.destroy()

        # Show the main frame
        self.base_menu.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def submit_container(self):
        # Get the container name and weight from the entry fields
        container_name = self.container_name_entry.get()
        container_weight = self.container_weight_entry.get()

        # Check if container name is empty
        if not container_name:
            messagebox.showerror("Error", "Container name cannot be empty")
            return

        # Check if container weight is a number
        try:
            weight = int(container_weight)
        except ValueError:
            messagebox.showerror("Error", "Container weight must be a number")
            return

        # Check if container weight is less than or equal to 99999
        if weight > 99999:
            messagebox.showerror("Error", "Container weight cannot be higher than 99999 kgs")
            return

        # Add the container to the list
        self.containers.append((container_name, container_weight))

        # Update the container list in the UI
        self.update_action_queue()
        messagebox.showinfo("Success", f"Container {container_name} successfully added")

    def update_action_queue(self):
        # Clear the container list in the UI
        self.action_queue.delete(0, END)

        # Add the containers to the list in the UI
        for i, container in enumerate(self.containers):
            self.action_queue.insert(i, f"{i + 1}. {container[0]} ({container[1]} kg)")

    def run(self):
        # Print "Running" in the console
        print("Running")


UnloadLoadUI()
