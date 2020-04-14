from Edge import Edge
import random

filename = "franklin.txt"
graph = list()
edges = list() 
colors = [1,2,3]

def read_input(): #ucitavamo podatke
	data = open(filename, "r")
	for line in data:
		edge, v1, v2 = line.split(",")
		v1 = int(v1)
		v2 = int(v2)
		graph.append([edge,v1,v2])

	return graph

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

"""
Bool optimal = True
Bool not_colored

for each grana in lista_grana
	for each boja in lista_boja #imacemo ih onoliko koliki je stepen grafa
		BnB(grana, boja, optimal)
			if optimal == True:
				break
	if not_colored == True: #Znaci nismo granu uspeli da
		optimal = False		obojimo ni jednom bojom iz liste boja i
							 trebala bi nam nova pa to nije optimalno



def BnB(grana,boja,optimal):

	if grana obojena: #vec je obojena pa izlazimo iz rekurzije
		return

	colored = try_to_color(grana,boja)

	if colored == False: #Ako ne mozemo da je obojimo datom bojom "boja"
		not_colored = True # Nije jos uvek obojena, probacemo sledecom bojom
	  	return

	else: not_colored = False 

	for each k in lista_susednih_grana_trenutne_grane:
		for each b in lista_boja:
			BnB(k,b,optimal) #Nastavljamo rekurziju na ostale grane
"""
def BnB(edge, color, optimal):

	if edge.color is not None: 
		return

	colored = try_to_color(color, edge)

	if colored == False:
		not_colored = True
		return
	else:
		not_colored = False

	for k in edge.adjacent_edges:
		for c in colors:
			BnB(k,c,optimal)

graph = read_input()  

for item in graph:
	edges.append(Edge(item[0],item[1],item[2])) #Lista grana (klasa)

add_adjacent_edges()


optimal = True
not_colored = False

for edge in edges:
	for color in colors:
		BnB(edge, color, optimal)
		if optimal == True:
			break
	if not_colored == True:
		optimal = False



for edge in edges:
	print(edge.name, edge.color)

