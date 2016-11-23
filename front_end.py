"""
Functionality that is currently working:

Press the circle button once: click anywhere to create a node there.
Press the circle button before clicking anywhere else: turn off node creation.

Press the line button: click one node and then another node and will create a line between the two nodes.
Press the line button before clicking the second node (or the first node): turn off line creation. 
"""
from tkinter import *
from smart_backend import *
#import tkMessageBox

#global graph_height
#global visual_graph_height
global definition_list
global def_list_string
global graph
graph = None

definition_list = Definition_List()

class FrontEndNode(Node):

    def __init__(self, x, y, i):
        self.i = i
        self.x = x
        self.y = y
        self.connection_list = []
        self.text_id = ""

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_i(self):
        return self.i

    def set_text_id(self, text_id):
        self.text_id = text_id

    def get_text_id(self):
        return self.text_id

    def get_connections(self):
        return self.connection_list

    def append_connections(self, line):
        self.connection_list.append(line)
        

def is_in_node(x, y, cir_x, cir_y):
    if x > cir_x - 50:
        if cir_x + 50 > x:
            if y > cir_y - 50:
                if cir_y + 50 > y:
                    return True

    return False

def switch_on_make_circle():
    global make_circle_switch
    
    if make_circle_switch == 1:
        make_circle_switch = 0
    else:
        make_circle_switch = 1

def switch_on_make_line():
    global make_line_switch

    if make_line_switch == 0:
        make_line_switch = 1
    else:
        make_line_switch = 0

def switch_on_del():
    global del_switch

    if del_switch == 0:
        del_switch = 1
    else:
        del_switch = 0

def display_text():

    if graph == None:
        graph = Graph(fnode)
    else:
        graph.add_node(fnode)
    
    main_window.delete(text_entry_id)
    main_window.delete(text_button_id)
    text_id = main_window.create_text(event_x, event_y, text=E1.get(), width=95)
    fnode.set_text_id(text_id)
    fnode.set_text(E1.get())
    definition_list.parse_node(fnode)
    
def make_circle(event):
    global make_circle_switch
    global make_line_switch
    global line_pos
    global del_switch
    global E1
    global event_x
    global event_y
    global text_entry_id
    global text_button_id
    global fnode
    global def_list_string
    
    if make_circle_switch == 1: 
        arc = main_window.create_rectangle(event.x - 50, event.y - 50, event.x + 50, event.y + 50, outline="#ABA7A7", width=5, fill="#FFFFFF")
        fnode = FrontEndNode(event.x, event.y, arc)

        E1 = Entry(main_window, bd=5)
        text_entry_id = main_window.create_window(event.x, event.y, window=E1)

        event_x = event.x
        event_y = event.y

        text_button = Button(main_window, text="Create", command=display_text)
        text_button_id = main_window.create_window(event.x, event.y+50, window=text_button)
    
        circ_list.append(fnode)
        make_circle_switch = 0

    elif del_switch == 1:
        for i in range(len(circ_list)):
            if is_in_node(event.x, event.y, circ_list[i].get_x(), circ_list[i].get_y()):
                for line in circ_list[i].get_connections():
                    main_window.delete(line)
                main_window.delete(circ_list[i].get_i())
                main_window.delete(circ_list[i].get_text_id())
                circ_list.pop(i)
                del_switch = 0
                break

    elif make_line_switch != 0:
        for cir in circ_list:
            if is_in_node(event.x, event.y, cir.get_x(), cir.get_y()):
                line_pos.append(cir)
                make_line_switch = make_line_switch + 1
                break

        if make_line_switch == 3:
            if  will_create_cycle():
                tkMessageBox.showinfo("Error", "This line will create a cycle!")
                make_line_switch = 0
                line_pos = []
            else:
                line = main_window.create_line(line_pos[0].get_x(), line_pos[0].get_y(), line_pos[1].get_x(), line_pos[1].get_y(), width=7)
                line_pos[0].append_connections(line)
                line_pos[1].append_connections(line)
                main_window.tag_raise(line_pos[0].get_i())
                main_window.tag_raise(line_pos[0].get_text_id())
                main_window.tag_raise(line_pos[1].get_i())
                main_window.tag_raise(line_pos[1].get_text_id())
                graph.connect_to(line_pos[0], line_pos[1])
                make_line_switch = 0
                line_pos = []

    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(1060, 60, anchor=NW, text=definition_list.string(), font=("Times", 14), width=220)

def will_create_cycle():
    return False

def send_text_to_list():
    global def_list_string

    new_def = Definition(Eterm.get(), Edef.get())
    Eterm.get()
    Edef.get()
    definition_list.add_term(new_def)
    def_list_string = main_window.create_text(1060, 60, anchor=NW, text=definition_list.string(), font=("Times", 14), width=220)
    
if __name__ == "__main__":

    global Eterm
    global Edef
    
    #Initialize Window
    top = Tk()
    top.wm_title("SmartNotes")
    main_window = Canvas(top, bg="#FFFFFF", height=700, width=1300)

    #Global Variables
    circ_list = []
    make_circle_switch = 0
    make_line_switch = 0
    del_switch = 0
    line_pos = []

    #Initalize Button Images
    line_photo = PhotoImage(file="arrow.png")
    plus_photo = PhotoImage(file="plus.png")
    minus_photo = PhotoImage(file="minus.png")
    circle_photo = PhotoImage(file="circle.png")
    cross_photo = PhotoImage(file="cross.png")

    #Create Node Button
    node_button = Button(main_window, command=switch_on_make_circle)
    node_button.place(x=0, y=0)
    node_button.config(image=circle_photo, width="75", height="75")

    #Create Line Button
    line_button = Button(main_window, command=switch_on_make_line)
    line_button.place(x=100, y=0)
    line_button.config(image=line_photo, width="75", height="75")

    #Create Display Layer Button
    plus_button = Button(main_window)
    plus_button.place(x=200, y=0)
    plus_button.config(image=plus_photo, width="75", height="75")

    #Create Hide Layer Button
    minus_button = Button(main_window)
    minus_button.place(x=300,y=0)
    minus_button.config(image=minus_photo, width="75", height="75")

    #Create Delete Button
    cross_button = Button(main_window, command=switch_on_del)
    cross_button.place(x=400, y=0)
    cross_button.config(image=cross_photo, width="75", height="75")

    #Create Definition List
    deflist = [1050, 15, 1285, 685]
    main_window.create_rectangle(deflist[0], deflist[1], deflist[2], deflist[3], outline="#ABA7A7", width=5, fill="#FFFFFF")
    main_window.create_text((deflist[2] + deflist[0]) / 2, 40, text="Definition List", font=("Times", 24))

    main_window.create_text((deflist[2] + deflist[0]) / 2, 560, text="Term", font=("Times", 16))
    Eterm = Entry(main_window, bd=2)
    term_entry_id = main_window.create_window((deflist[2] + deflist[0]) / 2, 580, window=Eterm)

    main_window.create_text((deflist[2] + deflist[0]) / 2, 600, text="Enter Definition", font=("Times", 16))
    Edef = Entry(main_window, bd=2)
    definition_entry_id = main_window.create_window((deflist[2] + deflist[0]) / 2, 620, window=Edef)
    
    term_create_button = Button(main_window, text="Submit", command=send_text_to_list)
    text_button_id = main_window.create_window((deflist[2] + deflist[0]) / 2, 660, window=term_create_button)
    
    #Run Program
    main_window.bind("<Button-1>", make_circle)
    main_window.pack()
    top.mainloop()
