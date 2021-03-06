"""
Functionality that is currently working:

Press the circle button once: click anywhere to create a node there.
Press the circle button before clicking anywhere else: turn off node creation.

Press the line button: click one node and then another node and will create a line between the two nodes.
Press the line button before clicking the second node (or the first node): turn off line creation. 
"""

from tkinter import *
from smart_backend import *


global definition_list
global def_list_string
global graph
graph = None

definition_list = Definition_List()

class FrontEndNode(Node):

    def __init__(self, x, y, i):
        Node.__init__(self)
        self.i = i
        self.x = x
        self.y = y
        self.connection_list = []
        self.text_id = ""
        self.pmlist = []
        self.connect_id = []

    def get_connect_id(self):
        return self.connect_id

    def append_connect_id(self, ID):
        self.connect_id.append(ID)

    def get_pmlist(self):
        return self.pmlist

    def append_pmlist(self, node):
        self.pmlist.append(node)

    def pop_pmlist(self, i):
        self.pmlist.pop(i)

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

"""Check if click is in node"""
def is_in_node(x, y, cir_x, cir_y):
    if x > cir_x - 50:
        if cir_x + 50 > x:
            if y > cir_y - 50:
                if cir_y + 50 > y:
                    return True

    return False

"""turn on the make node button"""
def switch_on_make_circle():
    global make_circle_switch
    
    if make_circle_switch == 1:
        make_circle_switch = 0
    else:
        make_circle_switch = 1

"""turn on make line button"""
def switch_on_make_line():
    global make_line_switch

    if make_line_switch == 0:
        make_line_switch = 1
    else:
        make_line_switch = 0
        
"""turn on delete node button"""
def switch_on_del():
    global del_switch

    if del_switch == 0:
        del_switch = 1
    else:
        del_switch = 0

"""create node and display text of node"""
def display_text():
    global graph
    global def_list_string
    
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

    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(1060, 60, anchor=NW, text=definition_list.string(), font=("Times", 14), width=220)
    
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
    global graph
    global comment_entry_id
    global comment_button_id
    global comment_entry
    global second_line_pos


    #Create Circle
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

    #Delete Circle
    elif del_switch == 1:
        for i in range(len(circ_list)):
            if is_in_node(event.x, event.y, circ_list[i].get_x(), circ_list[i].get_y()):
                con_text = circ_list[i].get_connect_id()
                for a in range(len(circ_list[i].get_connections())):
                    main_window.delete(circ_list[i].get_connections()[a])
                    main_window.delete(con_text[a][0])
                    main_window.delete(con_text[a][1])
                main_window.delete(circ_list[i].get_i())
                main_window.delete(circ_list[i].get_text_id())
                graph.delete(circ_list[i])

                for item in circ_list:
                    ind_list = []
                    for j in range(len(item.get_pmlist())):
                        if item.get_pmlist()[j].get_i() == circ_list[i].get_i():
                            ind_list.append(j)

                    for ind in ind_list:
                        item.pop_pmlist(ind)
    
                circ_list.pop(i)
                del_switch = 0
                break

    #Choosing Nodes to Connect
    elif make_line_switch != 0:
        for cir in circ_list:
            if is_in_node(event.x, event.y, cir.get_x(), cir.get_y()):
                line_pos.append(cir)
                make_line_switch = make_line_switch + 1
                break

        #Both Nodes have been chosen
        if make_line_switch == 3:
            graph.connect_to(line_pos[0], line_pos[1])
            line = main_window.create_line(line_pos[0].get_x(), line_pos[0].get_y(), line_pos[1].get_x(), line_pos[1].get_y(), width=7)
            line_pos[0].append_connections(line)
            line_pos[1].append_connections(line)
            main_window.tag_raise(line_pos[0].get_i())
            main_window.tag_raise(line_pos[0].get_text_id())
            main_window.tag_raise(line_pos[1].get_i())
            main_window.tag_raise(line_pos[1].get_text_id())
            line_pos[0].append_pmlist(line_pos[1])
            line_pos[1].append_pmlist(line_pos[0])

            line_comment_x = (line_pos[0].get_x() + line_pos[1].get_x()) / 2
            line_comment_y = (line_pos[0].get_y() + line_pos[1].get_y()) / 2

            comment_entry = Entry(main_window, bd=5)
            comment_entry_id = main_window.create_window(line_comment_x, line_comment_y, window=comment_entry)
            comment_entry_bottom = main_window.bbox(comment_entry_id)[3]

            second_line_pos = [line_pos[0], line_pos[1]]

            comment_button = Button(main_window, text="Create", command=lambda: createConnection(line_pos))
            comment_button_id = main_window.create_window(line_comment_x, comment_entry_bottom + 5, window=comment_button, anchor=N)
            
            make_line_switch = 0
            line_pos = []

def createConnection(line_pos):
    global comment_entry_id
    global comment_button_id
    global comment_entry
    global second_line_pos

    ebbox = main_window.bbox(comment_entry_id)
    tbbox = main_window.bbox(comment_button_id)
    
    main_window.delete(comment_entry_id)
    main_window.delete(comment_button_id)

    new_coors = (ebbox[0] + ebbox[2]) / 2, (ebbox[1] + ebbox[3]) / 2

    conn_id = main_window.create_text(new_coors,text=comment_entry.get())

    comment_rect_id = main_window.create_rectangle(main_window.bbox(conn_id), fill="#FFFFFF")
    main_window.tag_raise(conn_id)

    second_line_pos[0].append_connect_id((conn_id, comment_rect_id))
    second_line_pos[1].append_connect_id((conn_id, comment_rect_id))

    second_line_pos = []
    
"""Check if this connection is valid in the graph"""
#def will_create_cycle():
    #global line_pos
    #global graph

    ##return not check_cycle(graph, line_pos[1])
    #return False

"""Update and present the definition list"""
def send_text_to_list():
    global def_list_string

    new_def = Definition(Eterm.get(), Edef.get())
    Eterm.get()
    Edef.get()
    definition_list.add_term(new_def)
    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(1060, 60, anchor=NW, text=definition_list.string(), font=("Times", 14), width=220)
    
if __name__ == "__main__":

    global Eterm
    global Edef
    global circ_list
    
    #Initialize Window
    top = Tk()
    
    top.wm_title("SmartNotes")
    main_window = Canvas(top, bg="#FFFFFF", height=7000, width=1300)
    main_window.pack()

    def_list_string = main_window.create_text(1060, 60, anchor=NW, text=definition_list.string(), font=("Times", 14), width=220)

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

    #Create Delete Button
    cross_button = Button(main_window, command=switch_on_del)
    cross_button.place(x=200, y=0)
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
