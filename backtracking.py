from Edge import Edge
import random
from graphviz import Graph
import graphviz as gv

filename = "wiener_araya.txt"
graph = list()
edges = list() 
colors = list()

def read_input():
    data = open(filename, "r")
    vs = list() # lista grana sa ponavljanjem
    for line in data:
        edge, v1, v2 = line.split(",") # grana i dva cvora na krajevima
        v1 = int(v1)
        v2 = int(v2)
        graph.append([edge, v1, v2])
        vs.append(v1)
        vs.append(v2)
    chromatic_index = 0
    # nalazenje stepena grafa(chromatic_index):
    #print(vs)
    for i in range(len(vs)):
        counter = 1
        for j in range(i+1, len(vs)):
            if vs[i] == vs[j]:
                counter += 1
        if chromatic_index < counter:
            chromatic_index = counter
    #print(chromatic_index)
    
    return graph, chromatic_index

def add_adjacent_edges():
	for edge in edges:
		for edge2 in edges:
			if (edge2.name != edge.name) and (edge2.v1 == edge.v1 or edge2.v2 == edge.v2 or edge2.v2 == edge.v1 or edge2.v1 == edge.v2):
				edge.add_adjacent(edge2) #ubacujemo u listu susednih grana
                

def try_to_color(color_to_set, edge_to_color): #pokusavamo da obojimo granu datom bojom

	for adjacent_edge in edge_to_color.adjacent_edges:
		if adjacent_edge.color == color_to_set:
			return False
	edge_to_color.set_color(color_to_set)
	return True


def backtracking(edge, color, optimal):

	if edge.color is not None: 
		return

	colored = try_to_color(color, edge)

	if colored == False:
		not_colored = True
		return
	else:
		not_colored = False
		#print(edge)
		#print(edge.color)

	for k in edge.adjacent_edges:
		for c in colors:
			backtracking(k,c,optimal)
		#optimal = True
		
	optimal = True

graph, chromatic_index = read_input()

for i in range(1, chromatic_index + 1):
    colors.append(i)

for item in graph:
	edges.append(Edge(item[0],item[1],item[2])) #Lista grana (klasa)

add_adjacent_edges()


optimal = False
not_colored = False

for edge in edges:
	for color in colors:
		backtracking(edge, color, optimal)
		if optimal == True:
			break
	#optimal = True
	if not_colored == True:
		optimal = False




for edge in edges:
	print(edge.name, edge.color)

#######################crtanje

g = Graph('G', filename='solution.gv')#, engine='sfdp')
##
colors1 = ['blue','green','red', 'yellow', 'pink']

for edge in edges:
    i = edge.color
    g.edge(str(edge.v1), str(edge.v2), color = colors1[i - 1])
    
    

print(g.source)

g.view()
