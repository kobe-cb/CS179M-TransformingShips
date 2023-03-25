from helpers.imports import *
import helpers.custom_global as custom_global

from windows.comment import CommentWindow
from windows.prerun import PreRunWindow


class UnloadLoadWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

#        self.unloadload_root_window = tk.Frame(self)
#        self.unloadload_root_window.pack(side="top", fill="both", expand=True)

        self.containers = []
        self.container_weight_entry = None
        self.container_name_entry = None
        self.add_container_frame = None

        self.base_menu = tk.Frame(self)
        self.base_menu.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # create label for "Currently Working:"
        self.currWorker_label = tk.Label(
            self.base_menu, text="Currently Working:")
        self.currWorker_label.pack(side="top", anchor="nw")

        self.ship_label = tk.Label(
            self.base_menu, text="Ship: ")
        self.ship_label.pack(side="top", anchor="ne")

        # create sign out button
        self.button_sign_out = tk.Button(
            self.base_menu, text="Sign out", command=self.sign_out, relief="solid", borderwidth=1)
        self.button_sign_out.pack(side="top", anchor="e", padx=(0, 100))

        # create two frames
        self.frame_left = tk.Frame(self.base_menu, width=400)
        self.frame_right = tk.Frame(self.base_menu, width=800)
        self.frame_left.pack(side="left", fill="y", padx=10, pady=10)
        self.frame_right.pack(side="right", fill="both",
                              expand=True, padx=0, pady=10)  # Updated pack method

        # add label to the top of the left frame
        self.label_left = tk.Label(
            self.frame_left, text="Actions Queued", height=2)
        self.label_left.pack()

        # create a Listbox in the left frame
        self.action_queue = tk.Listbox(
            self.frame_left, width=50, background='light gray', relief="groove", borderwidth=1)
        self.action_queue.pack(expand=True, fill="both")

        # create a frame for the "Load/Unload" text and comments button
        self.top_frame = tk.Frame(self.frame_right)
        self.top_frame.pack(side="top", fill="x")

        # add label and button to the top frame
        self.label_right = tk.Label(
            self.top_frame, text="Load/Unload", font=("Arial", 32))
        self.label_right.pack(side="left")

        self.toggle_var = tk.BooleanVar()
        self.toggle_var.set(False)
        self.toggle_button = tk.Checkbutton(
            self.top_frame, text="Toggle Labels", variable=self.toggle_var)
        self.toggle_button.pack()

        self.comment_button = tk.Button(
            self.top_frame, text="Comments", command=self.add_comment, relief="solid", borderwidth=1)
        self.comment_button.pack(side="right", padx=(0, 100))

        # create a frame for the grid
        self.grid_frame = tk.Frame(self.frame_right)
        self.grid_frame.pack(side="top", expand=True,
                             fill="both", pady=(40, 0), padx=(20, 0))

        self.label_names = [
            ['UNUSED' for column in range(12)] for row in range(18)]

        self.grid_maker()

        self.button1 = tk.Button(
            self.frame_right, text="Add Container", width=15, height=10, command=self.show_add_container_frame, relief="solid", borderwidth=1)
        self.button1.pack(side="left", padx=10, pady=(30, 0))

        self.button2 = tk.Button(
            self.frame_right, text="Run", width=15, height=10, command=self.run, relief="solid", borderwidth=1)
        self.button2.pack(side="right", padx=10, pady=(30, 0))

    def label_click(self, event):
        row = int(event.widget.grid_info()['row'])
        column = int(event.widget.grid_info()['column'])
        name = event.widget["text"]

        column += 1  # zero index column
        row = 8 - row  # re-reverse row and add 1 to account for zero index

        # print("Name:", self.label_names[column-1][row-1])
        # print(column-1, row-1)

        print(
            f"Label clicked at row {row} and column {column} and name is {name}")
        # Check if the label has already been clicked once
        if self.toggle_var.get():
            event.widget.fullname = event.widget.cget("text")
            messagebox.showinfo("Label Info", event.widget.fullname)
        else:
            if event.widget["text"] != 'UNUSED' and event.widget["text"] != 'NAN':
                # Change the background color of the label
                current_color = event.widget.cget("bg")
                if current_color == "red":
                    event.widget.config(bg=self.grid_frame.cget("bg"))
                    if [column, row] in custom_global.grid_colors:
                        custom_global.grid_colors.remove([column, row])
                    for i in reversed(self.containers):
                        if i[1] == name:
                            self.containers.remove(i)
                            break
                    self.update_action_queue()
                else:
                    event.widget.config(bg="red")
                    custom_global.grid_colors.append([column, row])
                    self.containers.append(('UNLOAD', name))
                    self.update_action_queue()
                    self.last_del_index = len(self.containers) - 1

       # print("=============YOOOO============")
       # print(custom_global.manifest_contents)

    def grid_maker(self, event=None):
        # Read the file and map the coordinates to the grid
        file_name = "../" + custom_global.ship_label
        try:
            with open(file_name, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    coords = [0, 0]
                    coords[0] = parts[0].strip("[")
                    coords[1] = parts[1].strip("]")
                    name = parts[3].strip()
                    # print("Name:" + name)
                    # print(coords[0])
                    # print(coords[1])
                    # Adjust for zero-indexing
                    column = int(coords[1])
                    row = int(coords[0])
                    zero_column, zero_row = column - 1, row - 1
                    # print("COORDS:", name, zero_column,
                    #      zero_row, "|", coords[0], coords[1])
                    # print("ADDING", zero_column, zero_row)
                    self.label_names[zero_column][zero_row] = name
                    # make sure row index is not negative
                    zero_row = max(zero_row, 0)
                    zero_row = 8 - zero_row - 1  # reverse the row index
                    # print("row:", name, row)
                    """
                    label = tk.Label(window, text=name)
                    label.grid(row=row, column=column)
                    """
                    self.label = tk.Label(self.grid_frame, text=name, width=7, height=3,
                                          borderwidth=1, relief="solid")
                    self.label.grid(row=zero_row, column=zero_column)
                    # label.clicked = False
                    self.label.bind("<Button-1>", self.label_click)
                    if [column, row] in custom_global.grid_colors:
                        self.label.configure(bg="red")
        except:
            print("== ERR-UI: Couldn't Load Grid for Unload/Load")

    def add_comment(self):
        custom_global.comment_prev_window = UnloadLoadWindow
        self.controller.show_frame(CommentWindow)

    def show_add_container_frame(self):
        # Hide the main frame
        self.base_menu.grid_forget()

        # Create a new frame for adding a container
        self.add_container_frame = tk.Frame(self.master)
        self.add_container_frame.grid(
            row=0, column=0, padx=10, pady=30, sticky="nsew")

        # Create labels and entry fields for the container name and weight
        container_name = tk.Label(self.add_container_frame,
                                  text="Container Name:")
        container_name.grid(row=0, column=0, padx=10,
                            pady=10, sticky="w")
        self.container_name_entry = tk.Entry(
            self.add_container_frame, background='light gray', relief="groove", borderwidth=1)
        self.container_name_entry.grid(
            row=0, column=1, padx=10, pady=10, sticky="e")
        container_weight = tk.Label(
            self.add_container_frame, text="Container Weight (in kgs):")
        container_weight.grid(row=1, column=0,
                              padx=10, pady=10, sticky="w")
        self.container_weight_entry = tk.Entry(
            self.add_container_frame, background='light gray', relief="groove", borderwidth=1)
        self.container_weight_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="e")

        # Create a "Submit" button to add the container to the list
        place_button = tk.Button(self.add_container_frame,
                                 text="Place", command=self.submit_container, relief="solid", borderwidth=1, width=30)
        place_button.grid(row=2, column=1, padx=10,
                          pady=10, sticky="e")

        # Create a "Back" button to go back to the main frame
        back_button = tk.Button(self.add_container_frame,
                                text="Back", command=self.show_base_menu, relief="solid", borderwidth=1, width=30)
        back_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.add_container_frame.update_idletasks()

    def show_base_menu(self):
        # Destroy the add container frame
        self.add_container_frame.destroy()

        # Show the main frame
        self.base_menu.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # https://stackoverflow.com/questions/51956545/python3-tkinter-entry-cannot-select-text-field-until-i-click-outside-app-windo
        self.base_menu.update_idletasks()

    def submit_container(self):
        # Get the container name and weight from the entry fields
        container_name = self.container_name_entry.get()
        container_weight = self.container_weight_entry.get()

        # Check if container name is empty
        if not container_name:
            messagebox.showerror(
                "Error", "Container name cannot be empty")
            return

        # Check if container weight is a number
        try:
            weight = int(container_weight)
        except ValueError:
            messagebox.showerror(
                "Error", "Container weight must be a number")
            return

        # Check if container weight is less than or equal to 99999
        if weight > 99999:
            messagebox.showerror(
                "Error", "Container weight cannot be higher than 99999 kgs")
            return

        # Add the container to the list
        self.containers.append(('LOAD', container_name, container_weight))
        custom_global.container_weight.append(
            [container_name, container_weight])
        print(self.containers)

        # Update the container list in the UI
        self.update_action_queue()
        messagebox.showinfo(
            "Success", f"Container {container_name} successfully added")

    def update_action_queue(self):
        # Clear the container list in the UI
        self.action_queue.delete(0, 'end')
        # Add the containers to the list in the UI
        for i, container in enumerate(self.containers):
            if container[0] == 'LOAD':
                self.action_queue.insert(
                    i, f"{i + 1}. LOAD: {container [1]} ({container[2]} kg)")
            elif container[0] == 'UNLOAD':
                self.action_queue.insert(
                    i, f"{i + 1}. UNLOAD: {container [1]}")
        self.update_idletasks()

    def run(self):
        # Print "Running" in the console
        # print("Running")
        # print("Array:")
        # print(self.containers)
        custom_global.list_of_actions = self.containers
        # print(custom_global.grid_colors)
        if (len(custom_global.list_of_actions) > 0):
            self.controller.show_frame(PreRunWindow)
        else:
            self.non_loaded()

    def unload_clear(self):
        # self.action_queue.delete(0, 'end')
        self.containers.clear()
        custom_global.list_of_actions.clear()
        self.update_action_queue()
        custom_global.grid_colors.clear()
        # self.action_queue.update()

    def sign_out(self):
        print("Signing Out")
        from windows.login import LoginWindow
        self.controller.show_frame(LoginWindow)
        response = requests.get('http://worldtimeapi.org/api/ip')
        current_time = datetime.fromisoformat(
            response.json()['datetime'])
        log_name = "logfile" + str(current_time.year) + ".txt"
        log_file = os.path.join(
            os.environ['USERPROFILE'], 'AppData', 'Local', "TransformingShipsContent", log_name)
        with open(log_file, "a+") as log:
            response = requests.get('http://worldtimeapi.org/api/ip')
            current_time = datetime.fromisoformat(
                response.json()['datetime'])
            timestamp = current_time.strftime('%B %dth %Y: %H:%M ')
            comment = custom_global.curr_employee + " signs out"
            log.write(f'{timestamp} {comment}\n')

    def non_loaded(self):
        messagebox.showerror(
            "Error", "No Actions so far, will not continue")
