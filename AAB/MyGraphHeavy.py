class MyGraphHeavy:

    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g


    def print_graph(self):
        ''' Prints the content of the graph as ADJACENCY LIST '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])


    def print_graph_w_costs(self):
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


    def get_successors(self, v):
        return list(self.graph[v])


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


if __name__ == "__main__":
    test1()