"""
Functionality that is currently working:

Press the circle button once: click anywhere to create a node there.
Press the circle button before clicking anywhere else: turn off node creation.

Press the line button: click one node and then another node and will create a line between the two nodes.
Press the line button before clicking the second node (or the first node): turn off line creation. 
"""
import string
from tkinter import *
from smart_backend import *
#from checker import check_cycle

global graph_height
global visual_graph_height
global definition_list
global def_list_string
global graph
global circ_list
global selected_node
graph = None
visual_graph_height = None

global plus_minus_list
plus_minus_list = []

definition_list = Definition_List()

class FrontEndNode(Node):
    
    def __init__(self, x, y, i):
        Node.__init__(self)
        self.i = i
        self.x = x
        self.y = y
        self.connection_list = []
        self.text_id = ""
        self.connect_id = []
        self.comments = dict()

    def get_x(self):
        return self.x
    
    def set_x(self, x):
        self.x = x
    
    def get_y(self):
        return self.y
    
    def set_y(self, y):
        self.y = y

    def get_i(self):
        return self.i

    def set_text_id(self, text_id):
        self.text_id = text_id

    def get_text_id(self):
        return self.text_id
    
    def get_connect_id(self):
        return self.connect_id

    def append_connect_id(self, ID):
        self.connect_id.append(ID)

    def get_connections(self):
        return self.connection_list

    def append_connections(self, line):
        self.connection_list.append(line)
    
    def append_connect_id(self, ID):
        self.connect_id.append(ID)   
        
    def bind_comment(self, node, comment):
        self.comments[node] = comment
        
    def get_comments(self):
        return self.comments

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
        make_line_switch = 0
        del_switch = 0

"""turn on make line button"""
def switch_on_make_line():
    global make_line_switch
    #make_line_switch = 1
    if make_line_switch == 0:
        make_line_switch = 1
        make_circle_switch = 0
        del_switch = 0
    else:
        make_line_switch = 1
        del_switch = 0
        
        
"""turn on delete node button"""
def switch_on_del():
    global del_switch

    if del_switch == 0:
        del_switch = 1
        make_circle_switch = 0
        make_line_switch = 0
    else:
        del_switch = 1

"""create node and display text of node"""
def display_text():
    global graph
    global def_list_string
    
    default_text = ''
    if graph == None:
        graph = Graph(fnode)
    else:
        graph.add_node(fnode)
    
    main_window.delete(text_entry_id)
    main_window.delete(text_button_id)
    text_id = main_window.create_text(event_x, event_y+10, text=E1.get(1.0, END)+default_text, width=95, tags="node")
    fnode.set_text_id(text_id)
    fnode.set_text(E1.get(1.0, END))
    definition_list.parse_node(fnode)
    

    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(960, 60, anchor=NW, text=definition_list.string(), font=("Times", 12), width=320)
    
def delete_connections(node):
    con_text = node.get_connect_id()
    for a in range(len(node.get_connections())):
        main_window.delete(node.get_connections()[a])
        if(len(con_text)>a):
            main_window.delete(con_text[a][0])
            main_window.delete(con_text[a][1])

def draw_connection(node1, node2):
    line = main_window.create_line(node1.get_x(), node1.get_y(), node2.get_x(), node2.get_y(), width=7, tags="line", fill='blue')
    node1.append_connections(line)
    node2.append_connections(line)    
    main_window.tag_raise(node1.get_i())
    main_window.tag_raise(node1.get_text_id())
    main_window.tag_raise(node2.get_i())
    main_window.tag_raise(node2.get_text_id())    

def redraw_connections(node):
    delete_connections(node)
    print(node.comments)
    for a in graph.graph:
        if a!=node and node in a.get_con():
            #redrawline with comments
            draw_connection(a, node)
            new_coors = (abs(int(a.get_x()+node.get_x())/2), abs(int(a.get_y()+node.get_y())/2))
            conn_id = main_window.create_text(new_coors, text = a.get_comments()[node])
            comment_rect_id = main_window.create_rectangle(main_window.bbox(conn_id), fill="#FFFFFF")
            main_window.tag_raise(conn_id)
            node.append_connect_id((conn_id, comment_rect_id))
            a.append_connect_id((conn_id, comment_rect_id))            

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
    global graph_height
    global comment_entry_id
    global comment_button_id
    global comment_entry    
    global second_line_pos
    
    #Create Circle
    if make_circle_switch == 1: 
        make_line_switch = 0
        del_switch = 0
        arc = main_window.create_rectangle(event.x - 50, event.y - 50, event.x + 50, event.y + 50, outline="#ABA7A7", width=5, fill="#FFFFFF", tags="node")
        
        
        fnode = FrontEndNode(event.x, event.y, arc)

        E1 = Text(main_window,height=5, width=10)
        text_entry_id = main_window.create_window(event.x, event.y, window=E1)

        event_x = event.x
        event_y = event.y

        text_button = Button(main_window, text="Create", command=display_text)
        text_button_id = main_window.create_window(event.x, event.y+50, window=text_button)
    
        circ_list.append(fnode)
        #print(circ_list)
        make_circle_switch = 0

    #Delete Circle
    elif del_switch == 1:
        make_line_switch = 0
        for i in range(len(circ_list)):
            if is_in_node(event.x, event.y, circ_list[i].get_x(), circ_list[i].get_y()):
                delete_connections(circ_list[i])
                main_window.delete(circ_list[i].get_i())
                main_window.delete(circ_list[i].get_text_id())
                graph.delete(circ_list[i])
                circ_list.pop(i)
                del_switch = 0
                break
        

    #Choosing Nodes to Connect
    elif make_line_switch != 0:
        del_switch = 0
        for cir in circ_list:
            if is_in_node(event.x, event.y, cir.get_x(), cir.get_y()):
                line_pos.append(cir)
                make_line_switch = make_line_switch + 1
                break

        #Both Nodes have been chosen
        if make_line_switch == 3:
            graph.connect_to(line_pos[0], line_pos[1])
            draw_connection(line_pos[0], line_pos[1])

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
        if make_line_switch > 3:
            make_line_switch = 1
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

    #-----
    second_line_pos[0].add_con(second_line_pos[1])
    second_line_pos[0].bind_comment(second_line_pos[1], comment_entry.get())
    second_line_pos[1].add_con(second_line_pos[0])
    second_line_pos[1].bind_comment(second_line_pos[0], comment_entry.get())
    #----
    
    conn_id = main_window.create_text(new_coors,text=comment_entry.get())

    comment_rect_id = main_window.create_rectangle(main_window.bbox(conn_id), fill="#FFFFFF")
    main_window.tag_raise(conn_id)

    second_line_pos[0].append_connect_id((conn_id, comment_rect_id))
    second_line_pos[1].append_connect_id((conn_id, comment_rect_id))

    second_line_pos = []
    
    
"""Check if this connection is valid in the graph"""
def will_create_cycle():
    global line_pos
    global graph

    return not check_cycle(graph, line_pos[1])

def del_text_from_list():
    global def_list_string
    definition_list.remove_term(Eterm.get())
    Eterm.get()
    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(960, 60, anchor=NW, text=definition_list.string(), font=("Times", 12), width=320)    
"""Update and present the definition list"""

def send_text_to_list():
    global def_list_string

    new_def = Definition(Eterm.get(), Edef.get())
    Eterm.delete(0, END)
    Edef.delete(0, END)
    Eterm.get()
    Edef.get()
    definition_list.add_term(new_def)
    if(graph != None):
        definition_list.update_ref(graph.graph)
    main_window.delete(def_list_string)
    def_list_string = main_window.create_text(960, 60, anchor=NW, text=definition_list.string(), font=("Times", 12), width=320)
    
def find_selected_node(event, circ_list):
    for cir in circ_list:
                if is_in_node(event.x, event.y, cir.get_x(), cir.get_y()):
                    return cir
    
def OnTokenButtonPress(event):
    '''Being drag of an object'''
    overlaplist = main_window.find_overlapping(event.x-25, event.y-25, event.x+25, event.y+25)
    overlaptaglist = []
    for element in overlaplist:
        overlaptaglist.insert(0,main_window.gettags(element)[0])
    # record the item and its location
    if(overlaptaglist.count("node")>=2):
        main_window.drag_data["items"] = main_window.find_overlapping(event.x-25, event.y-25, event.x+25, event.y+25)
    main_window.drag_data["x"] = event.x
    main_window.drag_data["y"] = event.y
    selected_node = find_selected_node(event, circ_list)
    

def OnTokenButtonRelease(event):
    '''End drag of an object'''
    # reset the drag information
    main_window.drag_data["items"] = None
    main_window.drag_data["x"] = 0
    main_window.drag_data["y"] = 0

def OnTokenMotion(event):
    
    selected_node = find_selected_node(event, circ_list) 
    '''Handle dragging of an object'''
    # compute how much this object has moved
    if(selected_node!=None):
        delta_x = event.x - main_window.drag_data["x"]
        delta_y = event.y - main_window.drag_data["y"]
        # move the object the appropriate amount
        if(main_window.drag_data["items"]!=None):
            tags = []
            for item in main_window.drag_data['items']:
                if(len(main_window.gettags(item))>0):
                    tags.insert(0, main_window.gettags(item)[0])
            if tags.count("node")==2:
                for item in main_window.drag_data['items']:
                    if len(main_window.gettags(item))!=0:
                        if main_window.gettags(item)[0] == 'node':
                            main_window.move(item, delta_x, delta_y)
                            # record the new position
                            main_window.drag_data["x"] = event.x
                            main_window.drag_data["y"] = event.y
        
        
                selected_node.set_x(selected_node.get_x()+delta_x)
                selected_node.set_y(selected_node.get_y()+delta_y)
                redraw_connections(selected_node)

if __name__ == "__main__":

    global Eterm
    global Edef
    global circ_list
    global main_window
    #Initialize Window
    top = Tk()
    
    top.wm_title("SmartNotes")
    main_window = Canvas(top, bg="#FFFFFF", height=7000, width=1300)
    main_window.pack()
    def_list_string = main_window.create_text(500, 60, anchor=NW, text=definition_list.string(), font=("Times", 12), width=220)
    main_window.drag_data = {"x": 0, "y": 0, "items": None}
    #Global Variables
    circ_list = []
    make_circle_switch = 0
    make_line_switch = 0
    del_switch = 0
    line_pos = []
    selected_node = None
    
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
    deflist = [950, 15, 1285, 685]
    main_window.create_rectangle(deflist[0], deflist[1], deflist[2], deflist[3], outline="#ABA7A7", width=5, fill="#FFFFFF")
    main_window.create_text((deflist[2] + deflist[0]) / 2, 40, text="Definition List", font=("Times", 24))

    main_window.create_text((deflist[2] + deflist[0]) / 2, 560, text="Term", font=("Times", 12))
    Eterm = Entry(main_window, bd=2)
    term_entry_id = main_window.create_window((deflist[2] + deflist[0]) / 2, 580, window=Eterm)

    main_window.create_text((deflist[2] + deflist[0]) / 2, 600, text="Enter Definition", font=("Times", 12))
    Edef = Entry(main_window, bd=2)
    definition_entry_id = main_window.create_window((deflist[2] + deflist[0]) / 2, 620, window=Edef)
    
    term_create_button = Button(main_window, text="Submit", command=send_text_to_list)
    text_button_id = main_window.create_window(deflist[0]+135, 660, window=term_create_button)
    
    term_delete_button = Button(main_window, text="Delete", command=del_text_from_list)
    text_del_button_id = main_window.create_window(deflist[0]+200, 660, window=term_delete_button)    
    
    #Run Program
    main_window.bind("<Button-1>", make_circle)
    main_window.tag_bind("node", "<ButtonPress-1>", OnTokenButtonPress)
    main_window.tag_bind("node", "<ButtonRelease-1>", OnTokenButtonRelease)
    main_window.tag_bind("node", "<B1-Motion>", OnTokenMotion)     
    main_window.pack()
    top.mainloop()
