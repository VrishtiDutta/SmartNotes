# Function for checking if first node in graph forms a cycle with the second node
def check_cycle(graph, node): 
	if node.parent == None:
		return True
	else:
		return False
	# current = node1.parent
	# while current != None:
	# 	print(current.string())
	# 	if node2.parent is current:
	# 		return False
	# 	current = current.parent
	# return True
