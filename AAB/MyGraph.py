# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())

    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())

    ## add nodes and edges    

    def add_vertex(self, v):
        """ Add a vertex to the graph; tests if vertex exists not adding if it does """
        if v not in self.graph.keys():
            self.graph[v] = []

    def add_edge(self, o, d):
        """ Add edge to the graph; if vertices do not exist, they are added to the graph
        receives the vertex of origen an destiny """
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        res = []
        for key in self.graph.keys():
            if v in self.graph[key]:
                res.append(key)
        return res

    def get_adjacents(self, v):
        s = self.get_successors(v)
        p = self.get_predecessors(v)
        res = []
        res.extend(p)
        for n in s:
            if n not in res:
                res.append(n)
        return res

    ## degrees    

    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return len(self.get_adjacents(v)) 

    ## BFS and DFS searches    

    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: 
                res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: 
                res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def distance(self, s, d):
        if s == d: 
            return 0
        l = [(s, 0)]  # lista de tuplos, que guarda um n?? e dist??ncia percorrida (em numero de n??s) num determinado momento
        visited = [s]  # lista que guarda os n??s que j?? foram visitados
        while len(l) > 0:  # o ciclo ir?? parar assim que l n??o for preenchida e passar a ter uma len de 0
            node, dist = l.pop(0)  # node passa a ser o primeiro elemento do tuplo guardado em l, e dist o segundo, ao mesmo tempo que esse tuplo ?? apagado e l fica vazia
            # print (node, dist)
            for elem in self.graph[node]:  # vai buscar os n??s que est??o na lista do value correspondente ao node que est?? guardado
                if elem == d:  # se o elemento a que chegou for o parameterizado 
                    return dist + 1  # ent??o damos return ?? distancia que est?? guardada + 1
                elif elem not in visited:  # caso nao se encontre o n??
                    l.append((elem, dist + 1))  # voltamos a adicionar a l (que estava vazia) esse mesmo elemento, assim como a dist??ncia que foi percorrida, que ser?? sempre itera????es de +1 com cada itera????o do ciclo
                    visited.append(elem)  # adiciona-se a viseted esse n??
        return None  

    def shortest_path(self, s, d):  # igual ?? distance, mas retorna os nos por onde passa
        if s == d: 
            return [s,d]
        l = [(s, [])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: 
                    return preds+[node, elem]
                elif elem not in visited:
                    l.append((elem, preds+[node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s):
        res = []
        l = [(s, 0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: 
                res.append((node, dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem): 
                    l.append((elem, dist+1))
        return res

## cycles

    def node_has_cycle (self, v):  # verifica se um no esta contido dentro de um ciclo, ou seja, se volta a ocorrer 
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:  # se o vertice fornecido voltar a ser verificado com o correr do grafo, ent??o quer dizer que h?? um ciclo
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):  # verifica se o grafo ?? ciclico ou aciclico
        res = False
        for v in self.graph.keys():  # para todos os n??s do grafo
            if self.node_has_cycle(v):  # corre a fun????o 
                return True
        return res


def is_in_tuple_list (tl, val):  # verifica se um valor est?? dentro da lista de tuplos
    res = False
    for (x,_) in tl:
        if val == x: 
            return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())


def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()


def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))


def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    gr.print_graph()

    #print (gr.distance(1,4))
    #print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    #print (gr.reachable_with_dist(1))
    #print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )

    gr2.print_graph()
    
    # print (gr2.distance(2,1))
    # print (gr2.distance(1,5))
    
    # print (gr2.shortest_path(1,5))
    # print (gr2.shortest_path(2,1))

    # print (gr2.reachable_with_dist(1))
    # print (gr2.reachable_with_dist(5))


def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print(gr.node_has_cycle(2))
    print(gr. node_has_cycle(1))
    print(gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print(gr2. node_has_cycle(1))
    print(gr2.has_cycle())


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    test4()
    # test5()
