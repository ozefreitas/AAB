class MyGraphHeavy:

    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g


    def print_graph(self):
        ''' Prints the content of the graph as ADJACENCY LIST '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])


    def print_graph_w_costs(self):
        ''' Prints the conten of the draph in a more frendly way '''
        for v in self.graph.keys():
            for d in self.graph[v]:
                print (v, " -> ", d[0], "with a cost of:", d[1])


    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())


    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d[0]))
        return edges


    def get_weights(self):
        ''' Returns a list of the costs in the graph '''
        costs = []
        for v in self.graph.values():
            costs.append(v[1])
        return costs

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())


    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []


    def add_edge_w_cost(self, o, d, c):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph 
        receives the vertex of origen and destiny, aswell as the corresponding cost ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append((d,c))

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        lst = []
        for no in self.graph[v]:   # para cada elemento (que é um tuplo de dois) da lista que corresponde ao value do nó fornecido
            lst.append(no[0])  # vai dar append ao primeiro elemento desse tuplo que é o nó de destino e que será um sucessor
        return lst


    def get_predecessors(self, v):
        res = []
        for key in self.graph.keys():  # corre todas as keys do grafo
            dest = []  # lista que vai ser inicilizada em cada ciclo
            for no in self.graph[key]:  # para cada elemento (que é um tuplo de dois) da lista que corresponde ao value da key em causa no ciclo
                dest.append(no[0])  # vai adicionar a lista des o primeiro elemento de cada um desses tuplos (que corresponde ao vertice de destino)
            if v in dest:  # se v estiver presente nessa lista
                res.append(key)  # então será um predecessor
        return res


    def get_adjacents(self, v):  
        s = self.get_successors(v)  # pega na lista resultante dos sucessores e atribui a s
        p = self.get_predecessors(v)  # pega na lista resultante dos predecessors e atribui a p
        res = []
        res.extend(p)  # adiciona logo os elementos da lista dos predecessors a res
        for n in s:  # para cada no em s (lista de sucessores)
            if n not in res:  # se esse no ainda nao estiver em res
                res.append(n)  # vai adicioná-lo
        return res

    ## degrees (igual ao grafo normal, uma vez que cada tuplo é considerado na mesma como um unico elemento)

    def out_degree(self, v):
        return len(self.graph[v])


    def in_degree(self, v):
        return len(self.get_predecessors(v))


    def degree(self, v):
        return len(self.get_adjacents(v)) 


    def distance(self, s, d): 
        ''' entre s e d, retornar a distancia com menor peso, ou seja, a distancia para a qual a soma
        dos custos é a mais baixa '''
        if s == d: 
            return 0
        l = [(s,0)]  # lista de tuplos, que guarda um nó e o custo
        visited = [s]  # lista que guarda os nós que já foram visitados
        score = 0
        while len(l) > 0:  # o ciclo irá parar assim que l não for preenchida e passar a ter uma len de 0
            node, score = l.pop(0)  # node passa a ser o primeiro elemento do tuplo guardado em l, e dist o segundo, ao mesmo tempo que esse tuplo é apagado e l fica vazia
            for elem in self.graph[node]:  # vai a lista que contém os tuplos de dois elementos com (no destino, custo)
                for node, sc in elem:
                    if node == d:  # se o elemento a que chegou for o parameterizado 
                        return score + sc  # então damos return ao score 
                    elif node not in visited:  # caso nao se encontre o nó
                        l.append((node, score + sc))  # voltamos a adicionar a l (que estava vazia) esse mesmo elemento, assim como o custo acumulado em cada momento
                        visited.append(node)  # adiciona-se a viseted esse nó
        return None  


    def shortest_path(self, s, d):  # igual à distance, mas retorna os nos por onde passa
        ''' entre s e d, retornar o caminho com menor peso, ou seja, o caminho para o qual a soma
        dos custos é a mais baixa '''
        if s == d: 
            return [s,d]
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: 
                    return preds+[node,elem]
                elif elem not in visited:
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None


def test1():
    gr = MyGraphHeavy ( {1:[(2,12)], 2:[(3,12)], 3:[(2,4),(4,15)], 4:[(2,9)]} )

    gr.print_graph()
    print()
    gr.print_graph_w_costs()
    print (gr.get_nodes())
    print (gr.get_edges())

def test2():
    gr2 = MyGraphHeavy()

    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge_w_cost(1,2,12)
    gr2.add_edge_w_cost(2,3,12)
    gr2.add_edge_w_cost(3,2,4)
    gr2.add_edge_w_cost(3,4,15)
    gr2.add_edge_w_cost(4,2,9)
    
    gr2.print_graph()

    gr2.print_graph_w_costs()

def test3():
    gr = MyGraphHeavy( {1:[(2,12)], 2:[(3,12)], 3:[(2,4),(4,15)], 4:[(2,9)]} )

    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

if __name__ == "__main__":
    #test1()
    #test2()
    test3()
