from helpers.imports import *
import helpers.custom_global as custom_global


class CommentWindow(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.comment_label = tk.Label(self, text="Write your comment below:")
        self.comment_label.pack()
        self.comment_textbox = tk.Text(
            self, height=10, width=50, background='light gray', relief="groove", borderwidth=1)
        self.comment_textbox.pack()

        self.currWorker_label = tk.Label(
            self, text="Currently Working:")
        self.currWorker_label.pack()
        self.currWorker_label.place(x=0)

        self.save_button = tk.Button(
            self, text="Save Comment", command=self.save_comment, relief="solid", borderwidth=1)
        self.save_button.pack(pady=(10, 10))

        self.done_button = tk.Button(
            self, text="Done", command=self.back_window, relief="solid", borderwidth=1
        )
        self.done_button.pack()

        self.comment = ""

        # TODO no point in enter  button since it newlines
        # or are we doing the multiple lines per log entry

    def back_window(self):
        self.comment_textbox.delete('1.0', tk.END)
        self.controller.show_frame(custom_global.comment_prev_window)

    def save_comment(self, event=None):
        self.comment = self.comment_textbox.get("1.0", "end-1c")
        print("Comment saved:", self.comment)
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
            comment = "; ".join(self.comment.strip().split("\n")).strip()
            log.write(f'{timestamp} {comment}\n')
