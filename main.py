from Edge import Edge
import random
import os
from graphviz import Graph


filename = "franklin.txt"
graph = list() #lista ciji je element grana i njena dva cvora
edges = list() #lista grana
sorted_edges = list() #lista sortiranih grana prema broju suseda
solution = list() #resenje
colors = list() #koriscene boje
colors.append(1) #Na pocetku imamo barem jednu boju


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

def color(): #algoritam za bojenje 
	#sortiramo grane prema stepenu (broju suseda) 
	sorted_edges = edges
	sorted_edges.sort(key=lambda edge: edge.degree, reverse=True)
	not_colored = [x for x in sorted_edges if x.color is None]
	#random.shuffle(colors) #mesamo boje zbog redosleda uzimanja
	#random.shuffle(not_colored) #mesamo neobojene zbog redosleda bojenja
	
	for nc_edge in not_colored:
		
		colored = False

		for color in colors:
			if try_to_color(color, nc_edge) == True:
				colored = True
				break
			
		if colored == False:
			colors.append(max(colors) + 1) #dodajemo novu boju u listu boja
			nc_edge.set_color(max(colors)) 
			colored = True


		#for edge in sorted_edges: #bojimo istom bojom sve neobojene nesusedne grane 
		#	if edge not in nc_edge.adjacent_edges and edge.color is None:
		#		try_to_color(nc_edge.color,edge)

		#not_colored = [x for x in sorted_edges if x.color is None] #azuriramo listu neobojenih (ako smo obojili nesusedne one vise ne treba da budu u listi neobojenih)

def Solution():

	solution.clear() #Brisemo sadrzaj prethodnog resenja

	color(); #Bojimo neobojene grane

	colors.clear()

	for edge in edges: #Cuvamo resenje u listi solution
		solution.append([edge.name,edge.color])
		if edge.color not in colors: #Azuriramo listu boja (ako smo uspeli da obojimo sa manje boja nego prethodni put) 
			colors.append(edge.color)

	num_colors = len(colors);
	return solution, num_colors

def invert(k): #invertujemo grane tako sto im oduzimamo boju
	
	indexs = list()
	old_colors = list()

	for i in range(k):
		rand_index = random.randrange(len(edges)) #slucajno biramo granu za invertovanje
		indexs.append(rand_index) #ubacujemo u listu indeksa
		old_color = edges[rand_index].color #pamtimo staru boju grane
		old_colors.append(old_color) #ubacujemo u listu starih boja
		edges[rand_index].set_color(None) #obrisali boju grane rand_index

	return indexs,old_colors #vracamo indekse i stare boje invertovanih grana

def restore(k,indexs,old_colors,old_colors_num,old_solution):

	for i in range(k):
		edges[indexs[i]].set_color(old_colors[i]) #vracamo stare boje 
	 
	
	colors_num = old_colors_num #Vracamo na stari broj boja (ovo je nepotrebno?)
	solution = old_solution #Vracamo se na staro resenje (jer je bolje) (ovo je nepotrebno?)


def simulatedAnnealing(maxIters):

    #currValue = (FirstSolution,numF_colors) #za najgore resenje
    currValue = FirstSolution  

    bestValue = currValue
    i = 1
    k = 1
    while i < maxIters:
        indexs, old_colors = invert(k)
       	newValue = Solution()
        #print(currValue[0],currValue[1]) #ispis trenutnog resenja
        if newValue[1] < currValue[1]: #ako smo uspeli sa manje boja
            currValue = newValue
        else:
            p = 1.0 / i ** 0.5
            q = random.uniform(0, 1)
            if p > q:
                currValue = newValue
            else:
                restore(k,indexs,old_colors,currValue[1],currValue[0]) #Nije bolje pa vracamo kako je bilo obojeno
        if newValue[1] < bestValue[1]:
            bestValue = newValue
        i += 1
        k += 1
        if k == 4:
        	k = 1 
        
    for edge in edges: #listu grana postavljamo na najbolje resenje (zbog crteza) ps nisam sigurna da li je ovo potrebno, ali ne steti
        for item in bestValue[0]:
            if(edge.name == item[0]):
                edge.set_color(item[1])
                
        
    return bestValue



graph = read_input()  
#print("Graf [grana,v1,v2] gde grana spaja cvorove v1 i v2:")   
#print(graph)

for item in graph:
	edges.append(Edge(item[0],item[1],item[2])) #Lista grana (klasa)

add_adjacent_edges() #Za svaku granu punimo listu suseda


#------------------------------------------------------------------------------------------------
#Pocetno resenje (NAJGORE RESENJE)
"""
FirstSolution = list()
i=1
for edge in edges:
	FirstSolution.append([edge.name,i])
	colors.append(i)
	i+=1
numF_colors = i-1

print("●▬▬▬▬ Pocetno resenje: ▬▬▬▬●")
print(FirstSolution,numF_colors)
print()
"""
#-------------------------------------------------------------------------------------------------
#RESENJE GENERISANO ALGORITMOM ZA BOJENJE

print("●▬▬▬▬ Pocetno resenje: ▬▬▬▬●")
FirstSolution = Solution()
print(FirstSolution[0],FirstSolution[1])
print()

#-------------------------------------------------------------------------------------------------
maxIters = 100000
BestValue = simulatedAnnealing(maxIters)
print("●▬▬▬▬ Resenje simuliranim kaljenjem ▬▬▬▬●")
print(BestValue[0], BestValue[1])

#print()

#koriscene boje
#colors.sort()
#print(colors)


#ISCRTAVANJE RESENJA


g = Graph('G', filename='solution.gv')#, engine='sfdp')

for edge in edges:
	g.edge(str(edge.v1), str(edge.v2),label = str(edge.color))
	
#print(g.source)
#g.view() #Ovo meni nesto ne radi, ali upisuje u fajl sta treba..
