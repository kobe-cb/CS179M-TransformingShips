import tkinter as tk

"""
https://www.w3schools.com/python/python_file_write.asp
# First, open the file in "append" mode, which allows you to write to the end of the file
with open("filename.txt", "a") as file:
    # Replace "filename.txt" with the name of the file you want to append to

    # Then, prompt the user to enter the string they want to append
    string_to_append = input("Enter the string you want to append: ")

    # Write the string to the end of the file
    file.write(string_to_append)

# Finally, close the file
file.close()
"""


# Create a function to handle the "Save Comment" button click
def save_comment(comment_textbox):
    comment = comment_textbox.get("1.0", "end-1c")
    print("Comment saved:", comment)
    with open("log.txt", "a") as file:
        # TODO idk how we want the newline spacing to go here
        comment += "\n"
        file.write(comment)
    file.close()
    # You can do whatever you want with the comment variable here


# Create the main Tkinter window
window = tk.Tk()
window.title("Comment Window")

# Create the "Write your comment below" label
comment_label = tk.Label(window, text="Write your comment below:")
comment_label.pack()

# Create the comment text box
comment_textbox = tk.Text(window, height=10, width=50)
comment_textbox.pack()

# Create the "Save Comment" button
save_button = tk.Button(window, text="Save Comment",
                        command=lambda: save_comment(comment_textbox))
save_button.pack()

# Start the main loop
window.mainloop()
