import heapq

class Node: 
    '''super class for mindmap node'''
    ID = 0
    name = ''
    text = ''
    connections = dict()
    height= 1
    visibility = True
    
    def __init__(self, text): #initialized as a comment node without name
        self.ID = id
        self.text = text    
    
    def update_height(self): 
        '''find the height of tallest child and +1'''
        if (len(self.connections) == 0):
            self.height = 1
        else:
            self.height = 1 + max(self.connections.values())

    def set_text(self,text): #update text
        self.text = text

    def set_visibility(self, visible):
        self.visibility = visible

    def is_visible(self):
        return self.visibility

    def string(self): #return the entire node in string
        if(self.name == ''):
            return self.text
        return self.name+" "+self.text

    def add_con(self, node): #add a connection to another node
        self.connections[node] = node.get_height()
        self.update_height()

    def remove_con(self, node):
        del self.connections[node];
        self.update_height()

    def get_con(self): #return dictionary of all connections: nodes as keys and height as value
        return self.connections

    def set_height(self, h):    
        self.height = h

    def get_height(self):
        self.update_height() #precautious update
        return self.height

        
class Concept_Node(Node): 
    '''node specialized for storing major concepts'''
    priority = 0

    def __init__(self, name, text):
        Node.__init__(text)
        Node.name = name

    def get_name():
        Node.get_name()


class Definition():
    '''definition are implemented as priority queue elements. Number of reference is 
    value of comparison'''
    term = ''
    definition = ''
    reference = 0
    
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition
    
    def incre_ref(self, num): #increase number of references
        self.reference += num
        
    def decre_ref(self, num):
        self.reference -= num
        
    def get_ref(self):
        return self.reference
    
    def get_term(self):
        return self.term
    
    def get_def(self):
        return self.definition
    
    def string(self):
        return self.term + ": "+ self.definition
    
    def __lt__(self,other):
        return self.reference > other.reference
    def __eq__(self,other): 
        return self.reference == other.reference
    def __str__(self):
        return str(self.reference)    
    
class Definition_List:
    '''list structure that acts as self-organizing priority queue for definitions
    -Should be initialized in main program. 
    -parse_node should be evoked everytime a new node is generated'''
    dictionary = []
    def add_term(self,definition):
        self.dictionary.insert(0,definition)
        heapq.heapify(self.dictionary)
        
    def parse_node(self,node): #increment reference of definition based on number of occurrence in this node
        node_str = node.string()
        for term in self.dictionary:
            term.incre_ref(node_str.count(term.get_term()))
        heapq.heapify(self.dictionary)
    
    def print_list(self):
        for term in self.dictionary:
            print(term.string())
    
    def string(self):
        return_str = ''
        for term in self.dictionary:
            return_str += term.string()+"\n"
        return return_str

class Graph:
    '''store and maintain network of nodes
    only add_node(), connect_to, disconnect_from should be evoked, rest are helpers'''
    #update definition list whenever a new node is added
    graph = []
    root = Node("enter text") #graph must contain at least 1 node
    height = 1
    def __init__(self):
       # self.graph = list()
        self.graph.insert(0,self.root)
        
    def update_height(self):
        self.root.update_height()
    
    def get_height(self):
        self.height = self.root.get_height()
        return self.height
    
    def add_node(self, node):
        self.graph.insert(0,node)
        
    def connect_to(self, node1, node2):
        node1.add_con(node2)
        self.update_height()
    
    def disconnect_from(self, node1, node2):
        node1.remove_con(node2)
        self.update_height()
    
    def get(self):
        return self.graph
    
def test_defintion_heap():
    newnode = Node("hi")
    newdef = Definition("Asia", "An eastern continent")
    newdef2 = Definition("America", "A country on fire")
    newdef.incre_ref(4)
    newdef2.incre_ref(2)
    dictionary.add_term(newdef2)
    dictionary.add_term(newdef)
    dictionary.print_list()
    dictionary = None
    #dictionary.print_list()

def test_parse_node():
    dictionary = Definition_List()
    graph = Graph()    
    testnode = Node("China is a country in Asia Asia Asia Asia Asia Asia that has been occupied by America America America Military in the 1940s. It is also the largest country in Asia")
    newdef = Definition("Asia", "An eastern continent")
    newdef2 = Definition("America", "A country on fire")    
    dictionary.add_term(newdef)
    dictionary.add_term(newdef2)
    dictionary.parse_node(testnode)
    dictionary.print_list()
    print(dictionary.string())    

test_parse_node()
