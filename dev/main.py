from helpers.imports import *

# UI Components
from windows.login import LoginWindow
from windows.manifest import ManifestWindow
from windows.comment import CommentWindow
from windows.operationchoose import OperationChooseWindow
from windows.unloadload import UnloadLoadWindow
from windows.balance import BalanceWindow
from windows.runconfirmation import RunConfirmationWindow
from windows.steps import StepsWindow
from windows.prerun import PreRunWindow

# Algorithm
from algo.dylan_unloadLoadAlgo import main

# global variables
import helpers.custom_global as custom_global

# CamelCase for classes
# snake_case for everything else

# SOURCE: https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        folder_name = os.path.join(
            os.environ['USERPROFILE'], 'AppData', 'Local', "TransformingShipsContent")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        page_names = (LoginWindow,
                      ManifestWindow, OperationChooseWindow,
                      UnloadLoadWindow, BalanceWindow, PreRunWindow,
                      RunConfirmationWindow, StepsWindow,
                      CommentWindow)

        # iterating through a tuple consisting
        # of the different page layouts
        for F in page_names:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(UnloadLoadWindow)
        # self.show_frame(PreRunWindow)
        self.show_frame(LoginWindow)
        custom_global.comment_prev_window = LoginWindow

    # check global with new steps
    def manifest_compare(self):
        file_name = "../" + custom_global.ship_label
        # try:
        if os.access(file_name, os.R_OK | os.W_OK):
            print("File is available for read and write access.")
        else:
            print("File is not available for read and write access.")
        with open("./path.txt", "r") as file:
            lines = file.readlines()
        i = 0
        while i < len(lines):
            # print("before\n", custom_global.manifest_contents)
            if lines[i][0] == "M":
                # lines[i] == Move container Dog bruh bruh[1, 3] to[9, 1](off the ship)
                # A == [Move, container, dog, bruh, bruh, [1, 3]]
                A = lines[i].split()
                print(A)
                if (A[-1] == "ship)"):
                    container_name = A[2:-8]
                    container_name = "".join(container_name)
                    coords = [0, 0]
                    coords[0] = "0" + A[-8].strip("[").strip(",")
                    coords[1] = "0" + A[-7].strip("]")
                    new_coords = [0, 0]
                    new_coords[0] = "0" + A[-8].strip("[").strip(",")
                    new_coords[1] = "0" + A[-7].strip("]")
                    for j in custom_global.manifest_contents:
                        if j[0] == coords and j[2] == container_name:
                            j[1] = "00000"
                            j[2] = 'UNUSED'
                    for j in custom_global.manifest_contents:
                        if j[2] == container_name:
                            j[0] = new_coords
                else:
                    temp_weight = "00000"
                    container_name = A[2:-5]
                    container_name = "".join(container_name)
                    coords = [0, 0]
                    coords[0] = "0" + A[-5].strip("[").strip(",")
                    coords[1] = "0" + A[-4].strip("]")
                    new_coords = [0, 0]
                    new_coords[0] = "0" + A[-2].strip("[").strip(",")
                    new_coords[1] = "0" + A[-1].strip("]")
                    for j in custom_global.manifest_contents:
                        # finds the old coordinates and dissassembles
                        print("@@@@@@", j[0], coords, j[2], container_name)
                        if j[0] == coords and j[2] == container_name:
                            temp_weight = j[1]
                            j[1] = "00000"
                            j[2] = 'UNUSED'
                            del lines[i]
                            i -= 1
                        # finds new locationa nd assembles
                    for j in custom_global.manifest_contents:
                        if j[0] == new_coords:
                            j[1] = temp_weight
                            j[2] = container_name
                            break
                i += 1
            elif lines[i][0] == "L":
                B = lines[i].split()
                container_name = B[2:-3]
                container_name = "".join(container_name)
                coords = [0, 0]
                coords[0] = "0" + B[-2].strip("[").strip(",")
                coords[1] = "0" + B[-1].strip("]")
                weight = ""
                for j in custom_global.manifest_contents:
                    print(j[0], "|", coords)
                    if j[0] == coords:
                        for k in custom_global.container_weight:
                            if k[0] == container_name:
                                j[1] = str(k[1]).zfill(5)
                                weight = str(k[1]).zfill(5)
                        j[2] = "".join(container_name)
                        print('==== addded', [coords, weight, container_name])
                i += 1
            else:
                i += 1

        # except Exception as e:

        #    print("no:", str(e))

    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        # Currently Working Check
        try:
            frame.currWorker_label.config(
                text="Currently Working: " + custom_global.curr_employee)
        except:
            print("== UI: There is currently no UI element for current employee. ==")
        # Current Ship / Manifest Check
        try:
            # for unload, balance, runconfirmation, steps
            frame.ship_label.config(
                text="Manifest: " + custom_global.ship_label)
        except:
            print("== UI: There is currently no UI element for current ship/manifest. ==")

        # Checks for time update in RunConfirmation Window
        if cont is RunConfirmationWindow:
            try:
                # for runconfirmation
                frame.time_label.config(
                    text="This will take " + str(custom_global.minutes_to_complete) + " minutes to complete.")
            except:
                print(
                    "== UI: There is currently no UI element for time_to_complete (RunConfirmationWindow). ==")
            # runs the functions to generate grid again
            frame.update_action_queue()
            frame.grid_maker()

        # Re runs the grid generator when we load the unload/load window again
        elif cont is UnloadLoadWindow or cont is BalanceWindow:
            frame.grid_maker()

        elif cont is OperationChooseWindow:
            custom_global.manifest_contents.clear()
            # LOAD DEFAULT MANIFEST INTO GLOBAL
            name = '../' + custom_global.ship_label
            with open(name, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    coords = [0, 0]
                    coords[0] = parts[0].strip("[")
                    coords[1] = parts[1].strip("]")
                    parts[2] = parts[2].strip().strip("{}")
                    parts[3] = parts[3].strip()
                    custom_global.manifest_contents.append(
                        [coords, parts[2], parts[3]])
                    # print("Appended:\n", [coords, parts[2], parts[3]])
            print(custom_global.manifest_contents)

        elif cont is ManifestWindow:
            print("IM ALIVEEEEEEEEEEEE")
            cont = UnloadLoadWindow
            frame = self.frames[cont]
            frame.unload_clear()
            cont = ManifestWindow
            frame = self.frames[cont]

            file_path = os.path.join(
                os.environ['USERPROFILE'], 'Desktop', 'TransformingShips', "path.txt")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")

            file_path = os.path.join(
                os.environ['USERPROFILE'], 'Desktop', 'TransformingShips', "Instructions.txt")
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")

        # Run the algorithm when it reaches this window
        elif cont is PreRunWindow:
            new_space = -2
            self.update()
            print("== UI: Beginning to run Algorithm ==")
            temp_filename = "../" + custom_global.ship_label
            if (custom_global.str_operation == "unload_load"):
                print("== UI: Running UnloadLoad Algorithm... ==")
                main(custom_global.list_of_actions,
                     temp_filename, False)
                print("== UI: !! Finished UnloadLoad Algorithm !! ==")
                new_space = -2

                with open("./path.txt", "r") as file:
                    lines = file.readlines()
                # print("== UI: File Output: ==\n", lines)

            elif (custom_global.str_operation == "balance"):
                print("== UI: Running Balance Algorithm... ==")
                self.runBalanceCPP()
                print("== UI: !! Finished Balance Algorithm !! ==")
                print("== UI: Running Balance to Path Conversion... ==")
                main("./Instructions.txt",
                     temp_filename, True)
                print("== UI: !! Finished Balance to Path Conversion !! ==")
                new_space = -1

                with open("./path.txt", "r") as file:
                    lines = file.readlines()
                # print("== UI: File Output: ==\n", lines)

            match = re.search(r'\d+', lines[new_space])
            if match:
                number = int(match.group())
                custom_global.minutes_to_complete = number
                # print("before", lines)
                # del lines[-1]
                # print("after", lines)
                print("== UI: Mins to complete: " +
                      str(custom_global.minutes_to_complete) + "==")
            else:
                print("== ERR-UI: Couldn't parse the minutes to completion ==")
                custom_global.minutes_to_complete = -1

            i = 0
            custom_global.steps_list.clear()
            # custom_global.paths_list.clear()
            # custom_global.op_list.clear()
            while i < len(lines):
                if lines[i][0] == "M":
                    custom_global.steps_list.append(lines[i])
                    i += 1
                    # path_temp = lines[i].split(": ")[-1]
                    # custom_global.paths_list.append(eval(path_temp))
                    # i += 2
                    # custom_global.op_list.append([0, ""])
                elif lines[i][0] == "L":
                    custom_global.steps_list.append(lines[i])
                    # temp_words = lines[i].split()
                    # temp_idx = temp_words.index("container")
                    # temp_container_name = temp_words[temp_idx + 1]
                    i += 1
                    # path_temp = lines[i].split(": ")[-1]
                    # custom_global.paths_list.append(eval(path_temp))
                    # i += 2
                    # custom_global.op_list.append([1, temp_container_name])
                else:
                    i += 1
            # print(custom_global.paths_list)
            print("== UI: All steps: ==\n",  custom_global.steps_list)
            self.manifest_compare()
            self.show_frame(RunConfirmationWindow)

        elif cont is StepsWindow:
            # render the intiial step when seeing steps
            if custom_global.initial_steps:
                frame.next_window()
                custom_global.initial_steps = False
            try:
                # so we have
                # - move 1 of 3
                # - instructions
                # - when to show back button
                print("")
            except:
                print("")
        else:
            print("")

    def runBalanceCPP(self):
        subprocess.run(
            ['g++', '-std=c++20', './algo/Balancing Code.cpp', '-o', 'runC++'])
        mani_file = '../' + custom_global.ship_label
        subprocess.run(['./runC++', mani_file])


# https://stackoverflow.com/questions/41595532/tkinter-button-doesnt-accept-height-parameter
"""
It's not a bug, that's just how ttk buttons work.
If you need a highly configurable button, use a tkinter button.
ttk buttons are less configurable on purpose.
The goal of ttk widgets is to give you a set of buttons consistent with a particular theme.

"""


# Driver Code
if __name__ == "__main__":
    app = tkinterApp()
    app.title("Main Window")
    app.geometry('1200x1000')
    app.resizable(False, False)
    print("== UI: 1200x1000 Window Un-resizable Generated ==")
    app.mainloop()
