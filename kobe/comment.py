import tkinter as tk

# https://www.w3schools.com/python/python_file_write.asp


class CommentWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Comment Window")

        # Create text box and label
        self.comment_label = tk.Label(
            self.window, text="Write your comment below:")
        self.comment_label.pack()
        self.comment_textbox = tk.Text(self.window, height=10, width=50)
        self.comment_textbox.pack()

        # Create save button
        self.save_button = tk.Button(
            self.window, text="Save Comment", command=self.save_comment)
        self.save_button.pack()

        # Initialize comment variable
        self.comment = ""

        self.window.mainloop()

    def save_comment(self):
        self.comment = self.comment_textbox.get("1.0", "end-1c")
        print("Comment saved:", self.comment)


# Create an instance of the CommentWindow class
comment_window = CommentWindow()
