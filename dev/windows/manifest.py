
from helpers.imports import *
import helpers.custom_global as custom_global

from windows.comment import CommentWindow
from windows.operationchoose import OperationChooseWindow


class ManifestWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.manifest_root_window = tk.Frame(self)
        self.manifest_root_window.pack(side="top", fill="both", expand=True)

        self.currWorker_label = tk.Label(
            self.manifest_root_window, text="Currently Working:")
        self.currWorker_label.pack()
        self.currWorker_label.place(x=0)

        self.ship_label = tk.Label(
            self.manifest_root_window, text="Ship: ")
        self.ship_label.pack()
        # self.ship_label.place(x=0)

        self.comment_button = tk.Button(
            self.manifest_root_window, text="comments", height=1, width=10, command=self.add_comment, relief="solid", borderwidth=1)
        self.comment_button.pack(
            side="top", anchor="e", padx=(0, 100), pady=(0, 10))

        self.file_contents = tk.Text(
            self.manifest_root_window, width=60, height=30, font=("Comic Sans", 16), background='light gray', relief="groove", borderwidth=1)
        self.file_contents.pack()
        self.file_contents.place(relx=0.5, rely=0.55, anchor='center')

        # create sign out button
        self.button_sign_out = tk.Button(
            self.manifest_root_window, text="Sign out", command=self.sign_out, relief="solid", borderwidth=1)
        self.button_sign_out.pack(side="top", anchor="e", padx=(0, 100))

        self.filename_entry = tk.Entry(
            self, width=60, background='light gray', relief="groove", borderwidth=1)
        self.filename_entry.pack()
        self.filename_entry.place(relx=0.6, rely=0.1, anchor='center')

        self.submit_button = tk.Button(
            self.manifest_root_window, text="Submit", height=1, width=15, command=self.update_name, relief="solid", borderwidth=1)
        self.submit_button.pack()
        self.submit_button.place(relx=0.4, rely=0.14, anchor='center')

        self.next_button = tk.Button(
            self.manifest_root_window, text="Next", height=1, width=15, command=self.next_window, relief="solid", borderwidth=1)
        self.next_button.pack()
        self.next_button.place(relx=0.6, rely=0.14, anchor='center')

        self.instruction_label = tk.Label(
            self.manifest_root_window, text="Enter the Manifest name: (Capitalization Matters)\n e.g. ShipCase1.txt or Shipcase1")
        self.instruction_label.pack()
        self.instruction_label.place(relx=0.3, rely=0.1, anchor='center')

        self.name = ""

        self.filename_entry.bind('<Return>', self.update_name)

    def add_comment(self):
        # prev frame still manifest
        custom_global.comment_prev_window = ManifestWindow
        self.controller.show_frame(CommentWindow)

    def next_window(self):
        if (custom_global.manifest_load):
            # self.manifest_root_window.destroy()
            self.filename_entry.delete(0, tk.END)
            # self.file_contents.delete('1.0', tk.END)
            self.controller.show_frame(OperationChooseWindow)

            containers = 0

            for container in custom_global.manifest_contents:
                print(container)
                if container[2] not in ['UNUSED', 'NAN']:
                    containers += 1

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
                comment = f'Manifest {custom_global.ship_label } is opened, there are {containers} containers on the ship.'
                log.write(f'{timestamp} {comment}\n')
        else:
            messagebox.showinfo(
                "Error", "Cannot proceed without a manifest file.")

    def open_text(self, name):
        custom_global.manifest_load = False
        text_file = ""
        self.file_contents.delete('1.0', tk.END)

        try:
            text_file = open(name, 'r')
        except FileNotFoundError:
            print(f"== ERR-UI: File Not Found. Aborting")
        else:
            print("== UI: File Read ==")
            contents = text_file.read()
            self.file_contents.insert(tk.END, contents)
            text_file.close()

            custom_global.manifest_load = True

    def update_name(self, event=None):
        name = '../'
        name += self.filename_entry.get()
        custom_global.ship_label = self.filename_entry.get()
        if '.txt' not in name:
            name += '.txt'
            custom_global.ship_label += '.txt'
        print('== UI: FileName: ' + name + ' ==')
        try:
            # for unload, balance, runconfirmation, steps
            self.ship_label.config(
                text="Manifest: " + custom_global.ship_label)
        except:
            print("== UI: There is currently no UI element for current ship/manifest. ==")
        self.open_text(name)

    def sign_out(self):
        print("== UI: Signing Out ==")
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
