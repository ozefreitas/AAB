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
                no, custo = d
                print (v, " -> ", no, "with a cost of:", custo)


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
        if d not in self.graph[o]:  # se o vertice o ainda nao tiver o vertice destino d associado
            self.graph[o].append((d,c))  # adiciona-se a lista o tuplo com esse vertice d e o custo associado de o para d

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
                res.append(key)  # então o nó de origem que é a key em cada ciclo será um predecessor
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

    ## BFS and DFS searches    

    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem[0] != v: 
                    res.append(elem[0])
                if elem[0] not in res and elem[0] not in l and elem[0] != node:
                    l.append(elem[0])
        return res


    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem[0] != v: 
                    res.append(elem[0])
                s = 0
                if elem[0] not in res and elem[0] not in l:
                    l.insert(s, elem[0])
                    s += 1
            return res


    def distance(self, s, d): 
        ''' entre s e d, retornar a distancia com menor peso, ou seja, a distancia para a qual a soma
        dos custos é a mais baixa '''
        if s == d:
            return 0
        l = [(s,0)]  # lista de tuplos, que guarda um nó e o custo
        visited = [s]  # lista que guarda os nós que já foram visitados
        while len(l) > 0:  # o ciclo irá parar assim que l não volte a ser preenchida e passar a ter uma len de 0
            node, score = l.pop(0)  # node passa a ser o primeiro elemento do tuplo guardado em l, e dist o segundo, ao mesmo tempo que esse tuplo é apagado e l fica vazia
            for elem in self.graph[node]:  # vai a lista que contém os tuplos de dois elementos com (no destino, custo)
                if elem[0] == d:  # se o elemento a que chegou for o parameterizado 
                    return score + elem[1]  # então damos return ao score 
                elif elem[0] not in visited:  # caso nao se encontre o nó
                    l.append((elem[0], score + elem[1]))  # voltamos a adicionar a l (que estava vazia) esse mesmo elemento, assim como o custo acumulado em cada momento
                    visited.append(elem[0])  # adiciona-se a viseted esse nó
        return None  


    def shortest_path(self, s, d):  # igual à distance, mas retorna os nos por onde passa
        ''' entre s e d, retornar o caminho com menor peso, ou seja, o caminho para o qual a soma
        dos custos é a mais baixa '''
        if s == d:  # se forem dados dois vetices iguais, o custo será 0
            return [s,d,0]
        l = [(s,[],0)]  # tuplo de 3 elementos (nó de partida s, lista de vertices até chegar ao vertive d, e custo acumulado 0 por default)
        visited = [s]  # lista que vai guardar se um vertice ja foi visitado
        while len(l) > 0:  # o ciclo irá parar assim que l não for preenchida e passar a ter uma len de 0
            node, preds, score = l.pop(0)  # cada elemento do tuplo vai ser atribuido a uma variável ao mesmo tempoq que l fica vazia
            bestscore = 100000000000  # um valor muito alto para que o primeiro score a ser analisado seja sempre mais baixo
            for elem in self.graph[node]:  # ciclo para correr todos os tuplos que a lista tinha
                if elem[0] == d:  # se o primeiro elemento desse tuplo, que é o nó destino, for igual ao d especificado, encontramos o vertice
                    return preds+[node, elem[0]], score + elem[1]  # e da-se return ao caminho que está gravado e o respetivo score acumulado
                if elem[1] < bestscore:  # sempre que o score for mais baixo que o anterior
                    bestscore = elem[1]  # atualiza-se o melhor score 
                    newnode = elem[0]  # e o nó destino que tem esse custo no seu ramo
            if newnode not in visited:  # se esse no não for igual e se ainda nao tiver sido visitdado
                l.append((newnode, preds + [node], score + bestscore))  # dá-se append na lista l desse no, do caminho até ao momento, e do score ate ao momento
                visited.append(newnode)  # adiciona-se esse no a lista dos nos visitados
        return None


    def shortest_path_alt(self, s, d):  # igual à distance, mas retorna os nos por onde passa
        ''' entre s e d, retornar o caminho com menor peso, ou seja, o caminho para o qual a soma
        dos custos é a mais baixa '''
        if s == d:  # se forem dados dois vetices iguais, o custo será 0
            return [s,d,0]
        l = [(s,[],0)]  # tuplo de 3 elementos (nó de partida s, lista de vertices até chegar ao vertive d, e custo acumulado 0 por default)
        visited = [s]  # lista que vai guardar se um vertice ja foi visitado
        while len(l) > 0:  # o ciclo irá parar assim que l não for preenchida e passar a ter uma len de 0
            node, preds, score = l.pop(0)  # cada elemento do tuplo vai ser atribuido a uma variável ao mesmo tempoq que l fica vazia
            bestscore = 100000000000  # um valor muito alto para que o primeiro score a ser analisado seja sempre mais baixo
            for elem in self.graph[node]:  # ciclo para correr todos os tuplos que a lista tinha
                dest, cost = elem
                if dest == d:  # se o primeiro elemento desse tuplo, que é o nó destino, for igual ao d especificado, encontramos o vertice
                    return preds+[node, dest], score + cost  # e da-se return ao caminho que está gravado e o respetivo score acumulado
                if cost < bestscore:  # sempre que o score for mais baixo que o anterior
                    bestscore = cost  # atualiza-se o melhor score 
                    newnode = dest  # e o nó destino que tem esse custo no seu ramo
            if newnode not in visited:  # se esse no não for igual e se ainda nao tiver sido visitdado
                l.append((newnode, preds + [node], score + bestscore))  # dá-se append na lista l desse no, do caminho até ao momento, e do score ate ao momento
                visited.append(newnode)  # adiciona-se esse no a lista dos nos visitados
        return None


    def reachable_with_dist(self, s):
        res = []
        l = [(s, 0)]
        while len(l) > 0:
            node, score = l.pop(0)
            if node != s: 
                res.append((node, score))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l, elem[0]) and not is_in_tuple_list(res, elem[0]): 
                    l.append((elem[0], score + elem[1]))
        return res
    
    ## cycles

    def node_has_cycle (self, v):  # verifica se um no esta contido dentro de um ciclo, ou seja, se volta a ocorrer 
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem[0] == v:  # se o vertice fornecido voltar a ser verificado com o correr do grafo, então quer dizer que há um ciclo
                    return True
                elif elem[0] not in visited:  # se este no ainda nao tiver sido visitado 
                    l.append(elem[0])  # adiciona-se a l esse nó
                    visited.append(elem[0])  # e adiciona-se a lista de vertices visitados 
        return res


    def has_cycle(self):  # verifica se o grafo é ciclico ou aciclico
        res = False
        for v in self.graph.keys():  # para todos os nós do grafo
            if self.node_has_cycle(v):  # corre a função, que retorna um binário, se for True, verifica-se e passa a condição
                return True  # retornando True para o facto de que o grafo é ciclico
        return res


def is_in_tuple_list (tl, val):  # verifica se um valor está contido num tuplo
    res = False
    for (x,_) in tl:  # para os valores que estao no tuplo
        if val == x:  # se o valor for igual ao primeiro elemento desse tuplo
            return True  # entao verifica-se
    return res

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


def test4():
    gr = MyGraphHeavy( {1:[(2,12)], 2:[(3,12)], 3:[(2,4),(4,15)], 4:[(2,9)]} )
    
    gr.print_graph()

    print (gr.distance(1,4))
    #print (gr.distance(4,3))

    #print (gr.shortest_path(1,2))
    #print (gr.shortest_path(1,4))
    #print (gr.shortest_path(4,3))
    print (gr.shortest_path(1,4))
    #print (gr.reachable_with_dist(1))
    #print (gr.reachable_with_dist(3))


def test5():
    gr = MyGraphHeavy( {1:[(2,12)], 2:[(3,12)], 3:[(2,4),(4,15)], 4:[(2,9)]} )
    print (gr.node_has_cycle(2))
    print (gr.node_has_cycle(1))
    print (gr.has_cycle())


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
