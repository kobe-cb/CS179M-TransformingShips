from helpers.imports import *
import helpers.custom_global as custom_global

from windows.manifest import ManifestWindow


class LoginWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # controller is the SUPERROOT that allows transitions to hide and show other classes (UI)
        # assign it to self to use it later
        self.controller = controller

        self.login_root_window = tk.Frame(self)
        self.login_root_window.pack(side="top", fill="both", expand=True)

        self.login_root_window.grid_rowconfigure(0, weight=1)
        self.login_root_window.grid_columnconfigure(0, weight=1)

        self.username_label = tk.Label(
            self.login_root_window, text="Username:")
        self.username_label.pack()
        self.username_label.place(relx=0.36, rely=0.4, anchor='center')

        self.username_entry = tk.Entry(
            self.login_root_window, width=30, background='light gray', relief="groove", borderwidth=1)
        self.username_entry.pack()
        self.username_entry.place(relx=0.54, rely=0.4, anchor='center')
        # provides enter key functionality
        self.username_entry.bind('<Return>', self.update_employee)

        self.currWorker_label = tk.Label(
            self.login_root_window, text="Currently Working:")
        self.currWorker_label.pack()
        self.currWorker_label.place(x=0)

        # provides sign in button functinonality
        self.sign_in_button = tk.Button(
            self.login_root_window, text="Sign In", height=2, width=20, command=self.update_employee, relief="solid", borderwidth=1)
        self.sign_in_button.pack()
        self.sign_in_button.place(relx=0.5, rely=0.47, anchor='center')

    # https://stackoverflow.com/questions/21943718/how-to-bind-the-enter-key-to-a-button-in-tkinter
    # enter key functionality requires event, but we set to none to resolve button passing no arguments
    def update_employee(self, event=None):
        # https://stackoverflow.com/questions/74412503/cannot-access-local-variable-a-where-it-is-not-associated-with-a-value-but
        # tldr, declare global variable outside, then define it here as global to let the function know we're referencing global, not local scope
        employee_name = self.username_entry.get()
        if not employee_name:
            print("No Name Entered")
            print("(Global) Name:", custom_global.curr_employee)
        else:
            self.currWorker_label.config(
                text="Currently Working: " + employee_name)
            print("== UI: Name set to:", employee_name, "==")
            custom_global.curr_employee = employee_name
            if (custom_global.mid_operation):
                from windows.steps import StepsWindow
                self.controller.show_frame(StepsWindow)
            else:
                self.controller.show_frame(ManifestWindow)
            custom_global.comment_prev_window = ManifestWindow
            self.username_entry.delete(0, tk.END)

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
                comment = custom_global.curr_employee + " signs in"
                log.write(f'{timestamp} {comment}\n')
