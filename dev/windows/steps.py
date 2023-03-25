from helpers.imports import *
import helpers.custom_global as custom_global

from PIL import Image, ImageTk

from windows.comment import CommentWindow


class StepsWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.curr_index = -1
        # self.old_labels = []

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
        self.button_sign_out.pack(side="top", anchor="e")

        # create two frames
        # self.frame_left = tk.Frame(self.base_menu, width=400)
        # self.frame_right = tk.Frame(self.base_menu, width=800)
        self.frame_all = tk.Frame(self.base_menu, width=1200)
        # self.frame_left.pack(side="left", fill="y", padx=10, pady=(100, 100))
        # self.frame_right.pack(side="right", fill="both",
        #                      expand=True, padx=0, pady=10)  # Updated pack method
        self.frame_all.pack(fill="both",
                            expand=True, padx=0, pady=10)

        # self.image_file = Image.open(
        #    "/Users/saunturs/KBProjects/testGUIPython/FINAL/windows/truck.png")
        # self.max_image_width = 200
        # self.max_image_height = 200
        # self.image_file.thumbnail(
        #    (self.max_image_width, self.max_image_height))
        # self.image_use = ImageTk.PhotoImage(self.image_file)

        # add label to the top of the left frame
        # self.truck_image = tk.Label(
        #    self.frame_left, image=self.image_use)
        # self.truck_image.pack()

        # self.step_label = tk.Label(
        #    self.frame_left, text="null", font=("Arial", 15), wraplength=200
        # )
        # self.step_label.pack(expand=True, fill="both")

        # create a frame for the "Load/Unload" text and comments button
        self.top_frame = tk.Frame(self.frame_all)
        self.top_frame.pack(side="top", fill="x")

        self.comment_button = tk.Button(
            self.top_frame, text="Comments", command=self.add_comment, relief="solid", borderwidth=1)
        self.comment_button.pack(side="right", padx=(100, 0))

        # add label and button to the top frame
        self.label_right = tk.Label(
            self.top_frame, text="Move 1 of 3", font=("Arial", 48))
        self.label_right.pack(padx=(10, 0))

        # self.toggle_var = tk.BooleanVar()
        # self.toggle_var.set(False)
        # self.toggle_button = tk.Checkbutton(
        #    self.top_frame, text="Toggle Labels", variable=self.toggle_var)
        # self.toggle_button.pack()

        # create a frame for the grid
        # self.grid_frame = tk.Frame(self.frame_all)
        # self.grid_frame.pack(side="top", expand=True,
        #                     fill="both", pady=(40, 0), padx=(20, 0))
        self.step_label = tk.Label(
            self.frame_all, text="null", font=("Arial", 24), wraplength=400
        )
        self.step_label.pack(side="top", expand=True,
                             fill="both", pady=(50, 100), padx=(20, 0))

        # self.label_names = [
        #    ['UNUSED' for column in range(12)] for row in range(12)]

        # self.grid_maker()

        self.button1 = tk.Button(
            self.frame_all, text="Back", width=25, height=10, command=self.back_window, relief="solid", borderwidth=1)
        self.button1.pack(side="left", padx=10, pady=(30, 0))

        self.button2 = tk.Button(
            self.frame_all, text="Next", width=25, height=10, command=self.next_window, relief="solid", borderwidth=1)
        self.button2.pack(side="right", padx=10, pady=(30, 0))
    """
    def grid_maker(self, event=None):
        # Read the file and map the coordinates to the grid
        file_name = "../data/" + custom_global.ship_label
        with open(file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                coords = [0, 0]
                coords[0] = parts[0].strip("[")
                coords[1] = parts[1].strip("]")
                name = parts[3].strip()

                column = int(coords[1])
                row = int(coords[0])
                zero_column, zero_row = column - 1, row - 1

                self.label_names[zero_column][zero_row] = name
                # make sure row index is not negative
                zero_row = max(zero_row, 0)
                zero_row = 8 - zero_row - 1  # reverse the row index
                # print("row:", name, row)
                self.label = tk.Label(self.grid_frame, text=name, width=7, height=3,
                                      borderwidth=1, relief="solid")
                self.label.grid(row=zero_row, column=zero_column)
                # print(custom_global.paths_list)

    def label_click(self, event):
        # row = int(event.widget.grid_info()['row'])
        # column = int(event.widget.grid_info()['column'])
        # name = event.widget["text"]
        # print(
        # f"Label clicked at row {row} and column {column} and name is {name}")
        # Check if the label has already been clicked once
        if self.toggle_var.get():
            event.widget.fullname = event.widget.cget("text")
            messagebox.showinfo("Label Info", event.widget.fullname)

    def clear_grid(self):
        for i in range(8):
            for j in range(12):
                label_widget = self.grid_frame.grid_slaves(row=i, column=j)[
                    0]
                label_widget.configure(bg="green")
    """

    def next_window(self):
        if self.curr_index == len(custom_global.steps_list) - 2:
            self.button2.configure(text="Finish")
            # self.button1.pack_forget()
        else:
            self.button2.configure(text="Next")

        if self.curr_index < len(custom_global.steps_list) - 1:
            # self.old_labels.append(self.label_names)
            self.curr_index += 1
            self.step_label.configure(
                text=custom_global.steps_list[self.curr_index])
            self.label_right.configure(
                text="Move " + str(self.curr_index + 1) + " out of " + str(len(custom_global.steps_list)))
            """
            self.clear_grid()
            curr_path = custom_global.paths_list[self.curr_index]
            print("Executing:", curr_path)
            for i in curr_path:
                row = 8 - i[0]
                row = max(row, 0)
                col = i[1] - 1
                label_widget = self.grid_frame.grid_slaves(
                    row=row, column=col)[0]
                # print(row, col)
                label_widget.configure(bg="red")

            if (custom_global.op_list[self.curr_index][0] == 0):
                # moving out so remove the text
                label_widget.configure(text="UNUSED")
                # print(self.label_names[col][7-row], row, col)
                self.label_names[col][7-row] = 'UNUSED'
            else:
                # loading in
                temp_name = custom_global.op_list[self.curr_index][1]
                label_widget.configure(text=temp_name)
                self.label_names[col][7-row] = temp_name
        """
        else:
            self.manifest_generate()
            custom_global.mid_operation = False
            custom_global.initial_steps = True
            custom_global.grid_colors.clear()
            messagebox.showinfo(
                "REMINDER", "REMINDER: Please email the new generated manifest file that is on the desktop.")
            from windows.manifest import ManifestWindow
            self.controller.show_frame(ManifestWindow)
            self.curr_index = -1
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
                comment = f'Finished a Cycle. Manifest {custom_global.ship_label.replace(".txt", "")}OUTBOUND.txt was written to desktop, and a reminder pop-up to operator to send file was displayed.'
                log.write(f'{timestamp} {comment}\n')
                # self.grid_maker()

    # save all work to the final manifest
    def manifest_generate(self):
        file_path = custom_global.ship_label.replace(
            ".txt", "") + "OUTBOUND.txt"
        file_name = os.path.join(
            os.environ['USERPROFILE'], 'Desktop', file_path)

        with open(file_name, "w") as file:
            for index in custom_global.manifest_contents:
                print("WRITING: ", index)
                # Convert the index to a string and add a newline character
                # line = ",".join([str(item) for item in index]) + "\n"
                line = '[{},{}], {{{}}}, {}'.format(
                    *index[0], index[1], index[2])
                line += "\n"
                file.write(line)  # Write the line to the file

        # except:
        #    print("no maminfest create")

    def back_window(self):
        self.button2.configure(text="Next")
        if self.curr_index > 0:
            self.curr_index -= 1
            # print(self.curr_index)
            self.step_label.configure(
                text=custom_global.steps_list[self.curr_index])
            self.label_right.configure(
                text="Move " + str(self.curr_index + 1) + " out of " + str(len(custom_global.steps_list)))
            """
            self.clear_grid()
            print(self.label_names)
            self.label_names = self.old_labels.pop()
            print("------")
            # print(self.label_names)
            for i in range(0, 11, 1):
                for j in range(7, 0, -1):
                    label_widget = self.grid_frame.grid_slaves(
                        row=j, column=i)[0]
                    # label_widget.configure(bg="yellow")
                    label_widget.configure(text=self.label_names[i][7-j])
                    # print(self.label_names[1][0])
                    # cat is at 7, 0
                    # cat is at 1, 0

            curr_path = custom_global.paths_list[self.curr_index]
            for i in curr_path:
                row = 8 - i[0]
                row = max(row, 0)
                col = i[1] - 1
                label_widget = self.grid_frame.grid_slaves(
                    row=row, column=col)[0]
                print(row, col)
                label_widget.configure(bg="red")
        
            if (custom_global.op_list[self.curr_index][0] == 0):
                # moving out so remove the text
                label_widget = self.grid_frame.grid_slaves(
                    row=8-curr_path[0][0], column=curr_path[0][1]-1)
                label_widget.configure(text="UNUSED")
            else:
                # loading in
                label_widget = self.grid_frame.grid_slaves(
                    row=8-curr_path[-1][0], column=curr_path[-1][1]-1)
                temp_name = custom_global.op_list[self.curr_index][1]
                label_widget.configure(text=temp_name)
            """

    def add_comment(self):
        custom_global.comment_prev_window = StepsWindow
        self.controller.show_frame(CommentWindow)

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
