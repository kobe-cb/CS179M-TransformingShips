from helpers.imports import *
import helpers.custom_global as custom_global

from windows.comment import CommentWindow
from windows.prerun import PreRunWindow


class BalanceWindow(tk.Frame):
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
            self.top_frame, text="Balance", font=("Arial", 32))
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

        except Exception as e:
            print("== ERR-UI: Couldn't Load Grid for Balance", e)

    def add_comment(self):
        custom_global.comment_prev_window = BalanceWindow
        self.controller.show_frame(CommentWindow)

    def update_action_queue(self):
        # Clear the container list in the UI
        self.action_queue.delete(0, 'end')

        # Add the containers to the list in the UI
        for i, container in enumerate(self.containers):
            self.action_queue.insert(
                i, f"{i + 1}. ADD: {container[0]} ({container[1]} kg)")
        self.update_idletasks()

    def run(self):
        # Print "Running" in the console
        print("Running")
        self.containers.append(('Not Applicable'))
        custom_global.list_of_actions = self.containers
        self.containers.clear()
        self.controller.show_frame(PreRunWindow)

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
