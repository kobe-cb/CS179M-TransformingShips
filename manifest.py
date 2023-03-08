from tkinter import filedialog
from tkinter import *

root = Tk()
root.title("Read File")
root.geometry("1000x600")
root.resizable(False,False)

my_text = Text(root, width=80, height=18, font =("Comic Sans", 16))
my_text.pack(pady=20)

filename_entry = Entry(root)
filename_entry.pack()
filename_entry.place(x=440,y=490)

instruction_label = Label(root, text="Enter the Manifest name:")
instruction_label.pack()
instruction_label.place(x=435,y=470)

name = ""
text=".txt"

def open_txt(name):
    text_file = open(name, 'r')
    contents = text_file.read()

    my_text.insert(END, contents)
    text_file.close()

def update_name(event):
    name = filename_entry.get()
    name += text
    open_txt(name)


#open_button = Button(root, text = "Open Manifest file", command=open_txt)

#open_button.pack(pady=30)

filename_entry.bind('<Return>', update_name)


# Start the Tkinter event loop
root.mainloop()
