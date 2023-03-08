from tkinter import *
from tkinter import messagebox

root = Tk()

# Set the window title and size
root.title("Login Screen")
root.geometry("1000x500")


def update_employee():
    employee_name = username_entry.get()
    currWorker_label.config(text="Currently Working: " + employee_name)
    print("hello world")

username_label = Label(root, text="Username:")
username_label.pack()

username_entry = Entry(root)
username_entry.pack()
username_entry.place(relx = 0.5, rely = 0.5, anchor = 'center')

username_label.place(x=470, y=220)

currWorker_label = Label(root, text = "Currently Working: ")
currWorker_label.pack()
currWorker_label.place(x=0)

sign_in = Button(text="Sign In", height="2", width="20", command=update_employee)
#sign_in = Label(text="").pack()
sign_in.place(x=425, y=260)





root.mainloop()