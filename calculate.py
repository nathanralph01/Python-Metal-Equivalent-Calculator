""""
Nathan Ralph
2020-06-08
Program for calculating weighted average, Cu equivalent, and Zn equivalent
"""
import tkinter as tk
from typing import *

root = tk.Tk()
root.minsize(700, 500)

entry_dict = {}
entry_list = []
names = ["From", "To", "Length", "Cu", "Zn", "Ag", "Au"]
display_list = []
option_list = ["Weighted", "Cu", "Zn"]
testing = []
display_bool = False
toplevel_list = []
x_cnt = 0  # Counter for navigating through entry widgets horizontally
y_cnt = 0  # Counter for navigating through entry widgets vertically


class ValueWindow:

    def __init__(self, test, current_tab):

        self.current = current_tab
        self.test = test
        self.top = tk.Toplevel()
        self.entry_dict = {}
        self.names = ["Cu/lb", "Cu/tonne", "Zn/lb", "Zn/tonne",
                      "Au/oz", "Au/g", "Ag/oz", "Ag/g"]
        self.button = tk.Button(self.top, text="Continue",
                                width=10, command=lambda: self.decide_calc())
        self.button.grid(row=4, column=4, padx=10, pady=10)
        self.return_list = []   # This is the list with calculation values
        self.display_list = []
        self.top.bind("<Down>", self.down)
        self.top.bind("<Up>", self.up)
        self.cnt = 0

    def create_labels(self) -> None:
        """Creates label widgets for headers
        """
        for i in range(len(self.names)):
            new = tk.Label(self.top, text=self.names[i])
            new.grid(row=i, column=0, pady=10)

    def create_inputs(self) -> None:
        """Creates entry box widgets for inputs"""

        for i in range(len(self.names)):
            new_entry = tk.Entry(self.top, width=10)
            new_entry.grid(row=i, column=1)
            self.entry_dict[self.names[i]] = [new_entry]

    def cu_calculation(self, value_dict) -> None:
        """ Calculates Cu equivalence
            Precondition: value_dict must be the same as the global entry_dict
        """
        global testing
        value_list = []
        new_dict = self.fix_dict(self.entry_dict)
        try:
            for i in range(len(value_dict["Cu"])):
                equiv = value_dict["Cu"][i]+(value_dict["Zn"][i]*new_dict["Zn/lb"] / new_dict["Cu/lb"])
                equiv += (value_dict["Au"][i]*new_dict["Au/g"]/new_dict["Cu/tonne"])*100
                equiv += (value_dict["Ag"][i]*new_dict["Ag/g"]/new_dict["Cu/tonne"])*100
                value_list.append(equiv)
            self.return_list = value_list
            self.display_calc()
        except ZeroDivisionError:
            pass
        self.top.destroy()

    def zn_calculation(self, value_dict) -> None:
        """Calculates Zn equivalence"""
        value_list = []
        new_dict = self.fix_dict(self.entry_dict)
        try:
            for i in range(len(value_dict["Zn"])):
                equiv = value_dict["Zn"][i]+(value_dict["Cu"][i]*new_dict["Cu/lb"]/new_dict["Zn/lb"])
                equiv += (value_dict["Au"][i]*new_dict["Au/g"]/new_dict["Zn/tonne"])*100
                equiv += (value_dict["Ag"][i]*new_dict["Ag/g"]/new_dict["Zn/tonne"])*100
                value_list.append(equiv)
            self.return_list = value_list
            self.display_calc()
        except ZeroDivisionError:
            pass
        self.top.destroy()

    def fix_dict(self, fix_dict) -> Dict[str, int]:
        """Replaces entry boxes within a dictionary with their respected value
        """

        new_dict = {"Cu/lb": 0, "Cu/tonne": 0, "Zn/lb": 0, "Zn/tonne": 0,
                    "Au/oz": 0, "Au/g": 0, "Ag/oz": 0, "Ag/g": 0}
        for key in fix_dict:
            for i in range(len(fix_dict[key])):
                temp = fix_dict[key][i].get()
                try:
                    x = float(temp)
                except ValueError:
                    x = 0
                new_dict[key] = x
        return new_dict

    def decide_calc(self) -> None:
        """ Determines whether to do a Zn or Cu calculation
        """
        if self.current == "Cu":
            self.cu_calculation(self.test)
        else:
            self.zn_calculation(self.test)

    def display_calc(self) -> None:
        """ Displays the calculation results
        """

        global display_bool

        if not display_bool:
            for i in range(len(self.return_list)):
                curr = self.return_list[i]
                label = tk.Label(root, text=str(curr))
                label.grid(row=1+i, column=10, padx=5, pady=5)
                toplevel_list.append(label)
            display_bool = True
        else:
            for i in range(len(self.return_list)):
                curr = round(self.return_list[i], 8)
                toplevel_list[i]['text'] = curr

    def down(self, *event):
        if self.cnt < len(self.entry_dict)-1:
            self.cnt += 1
            self.entry_dict[self.names[self.cnt]][0].focus()

    def up(self, *event):
        if self.cnt > 0:
            self.cnt -= 1
            self.entry_dict[self.names[self.cnt]][0].focus()


def create_labels() -> None:
    """ Creates a serues of label widgets for headers
    """

    # width = 0
    cnt = 0
    for i in range(len(names)):
        new_label = tk.Label(root, text=names[i])
        new_label.grid(row=0, column=i, padx=20)
        if i > 2:
            label2 = tk.Label(root, text=names[i] + " weighted:")
            label2.grid(row=12 + cnt, column=0, padx=5, pady=5)
            cnt += 1


def create_inputs() -> None:
    """ Creates a series of entry box widgets for inputs
    """
    for i in range(7):
        temp_list = []
        for j in range(10):
            new_entry = tk.Entry(root, width=10)
            new_entry.grid(row=j+1, column=i, padx=5, pady=10)
            temp_list.append(new_entry)

        entry_dict[names[i]] = temp_list
        entry_list.extend(temp_list)


def weighted_average() -> None:
    """ Calculates the weighted average of Cu, Zn, Ag, and Au
    """
    new_dict = fix_values(entry_dict)

    # Prints correct answer!
    total_length = cu_weighted = zn_weighted = ag_weighted = au_weighted = 0

    for i in new_dict["Length"]:
        total_length += i
        # print(i)
    # print(total_length)

    for i in range(len(new_dict["Length"])):
        curr_len = new_dict["Length"][i]
        cu_weighted += curr_len * new_dict["Cu"][i]
        zn_weighted += curr_len * new_dict["Zn"][i]
        ag_weighted += curr_len * new_dict["Ag"][i]
        au_weighted += curr_len * new_dict["Au"][i]
    if total_length != 0:
        display_values([cu_weighted/total_length, zn_weighted/total_length,
                        ag_weighted/total_length, au_weighted/total_length])


def fix_values(entry_d: dict) -> Dict[str, List[int]]:
    new_dict = {"From": [], "To": [], "Length": [], "Cu": [], "Zn": [],
                "Ag": [], "Au": []}
    for key in entry_d:
        for i in range(len(entry_d[key])):
            temp = entry_d[key][i].get()
            try:
                x = float(temp)
            except ValueError:
                x = 0
            new_dict[key].append(x)
    # print(new_dict)
    for i in range(len(new_dict["Length"])):
        if new_dict["Length"][i] == 0:
            new_dict["Length"][i] = new_dict["To"][i] - new_dict["From"][i]

    return new_dict


def display_values(value_list: List[float]) -> None:
    """ Displays the weighted averages
        Index 0 -> Cu weighted average      Index 1 -> Zn weighted average
        Index 2 -> Ag weighted average      Index 3 -> Au weighted average
    """

    clear_label(display_list)
    for i in range(len(value_list)):
        value = str(round(value_list[i], 4))
        new_label = tk.Label(root, text=value)
        display_list.append(new_label)
        new_label.grid(row=12+i, column=1, padx=5, pady=5)


def refresh_values() -> None:
    """Refresh the entry box widgets (clears the text inside them
    """
    clear_label(display_list)
    clear_label(toplevel_list)
    for i in range(len(entry_list)):
        entry_list[i].delete(0, 'end')
        entry_list[i].insert(0, '')


def clear_label(label_list: list)-> None:
    """ Clears the label text in label_list
    """
    if label_list != []:
        for i in range(len(label_list)):
            label_list[i]['text'] = ''


def callback(*args):
    # Do something for each different selection: Change tabs?
    current = variable.get()
    global testing
    if current != "Weighted":
        # Clear Labels
        new = fix_values(entry_dict)
        new_window = ValueWindow(new, current)
        new_window.create_labels()
        new_window.create_inputs()


def down(event):
    global y_cnt
    curr = root.focus_get()
    if y_cnt < len(entry_dict[names[0]])-1:
        y_cnt += 1
        entry_dict[names[x_cnt]][y_cnt].focus()


def up(event):
    global y_cnt
    curr = root.focus_get()
    if y_cnt > 0:
        y_cnt -= 1
        entry_dict[names[x_cnt]][y_cnt].focus()


def left(event):
    global x_cnt
    curr = root.focus_get()
    if x_cnt > 0:
        x_cnt -= 1
        entry_dict[names[x_cnt]][y_cnt].focus()


def right(event):
    global x_cnt
    curr = root.focus_get()
    if x_cnt < len(names) - 1:
        x_cnt += 1
        entry_dict[names[x_cnt]][y_cnt].focus()


def left_click(event):
    global x_cnt
    global y_cnt
    curr = root.focus_get()
    if type(curr) == tk.Entry:
        coord_lst = find_sub(curr)
        x_cnt = coord_lst[0]
        y_cnt = coord_lst[1]


def find_sub(curr):
    coord_list = [0,0]
    temp1 = 0
    for key in entry_dict:
        temp2 = 0
        for value in entry_dict[key]:
            if value == curr:
                coord_list = [temp1, temp2]
                break
            temp2 += 1
        temp1 += 1
    return coord_list


root.bind("<Down>", down)
root.bind("<Up>", up)
root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Button-1>", left_click)
root.bind("<Return>", down)
calculate_button = tk.Button(root, text="Calculate", width=10,
                             command=weighted_average)
calculate_button.grid(row=11, column=6, pady=20)
refresh_button = tk.Button(root, text="Refresh", width=10,
                           command=refresh_values)
refresh_button.grid(row=11, column=5, padx=5, pady=20)

variable = tk.StringVar(root)
variable.set(option_list[0])

drop_down = tk.OptionMenu(root, variable, *option_list)
drop_down.config(width=7)
drop_down.grid(row=11, column=4, padx=5, pady=0)

variable.trace("w", callback)

create_labels()
create_inputs()
root.mainloop()
