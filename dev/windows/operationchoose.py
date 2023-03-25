from helpers.imports import *
import helpers.custom_global as custom_global

from windows.unloadload import UnloadLoadWindow
from windows.balance import BalanceWindow
from windows.comment import CommentWindow


class OperationChooseWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create the frame
        self.operation_frame = tk.Frame(self)
        self.operation_frame.grid(row=0, column=0, sticky='nsew')

        # Create the label
        self.currWorker_label = tk.Label(
            self.operation_frame, text="Currently Working:")
        self.currWorker_label.grid(
            row=0, column=0, padx=20, pady=20, sticky="W")

        # Create the label
        self.button_sign_out = tk.Button(
            self.operation_frame, text="Sign out", command=self.sign_out, relief="solid", borderwidth=1)
        self.button_sign_out.grid(
            row=0, column=1, padx=20, pady=20, sticky="W")

        # create some widgets inside operationchoose frame
        self.label = tk.Label(
            self.operation_frame, text="Choose an operation:", font=("Arial", 14))
        self.label.grid(row=1, column=0, padx=20, pady=20)

        self.button1 = tk.Button(self.operation_frame, text='Unload/Load',
                                 width=30, height=10, command=self.unload_load, relief="solid", borderwidth=1)
        self.button1.grid(row=2, column=0, padx=50, pady=50)

        self.button2 = tk.Button(self.operation_frame, text='Balance',
                                 width=30, height=10, command=self.balance, relief="solid", borderwidth=1)
        self.button2.grid(row=2, column=1, padx=50, pady=50)

        self.comment_button = tk.Button(
            self.operation_frame, text='Comment', command=self.comment, relief="solid", borderwidth=1)
        self.comment_button.grid(row=0, column=1, padx=20, pady=20, sticky="E")

    def unload_load(self):
        self.controller.show_frame(UnloadLoadWindow)
        custom_global.curr_operation = UnloadLoadWindow
        custom_global.str_operation = "unload_load"

    def balance(self):
        self.controller.show_frame(BalanceWindow)
        custom_global.curr_operation = BalanceWindow
        custom_global.str_operation = "balance"

    def comment(self):
        # prev_frame still operationchoose
        custom_global.comment_prev_window = OperationChooseWindow
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
