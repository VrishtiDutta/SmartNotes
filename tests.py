import smart_backend

test = smart_backend
graph = test.Graph(test.Node())
root = graph.root
root.set_text("root")
node1 = test.Node()
node1.set_text("node1")
graph.connect_to(root, node1)
print("root")
print(root.get_con())
print("node1")
print(node1.get_con())
node2= test.Node()
node2.set_text("node2")
graph.connect_to(node1, node2)
print(root.get_height())