# -*- coding: utf-8 -*-

from MyGraphComp import MyGraph

class MetabolicNetwork (MyGraph):  # tudo o que definimos no mygraph ficam disponiveis
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
        MyGraph.__init__(self, {})  # inicializa a classe MyGraph
        self.net_type = network_type  # de que tipo é a rede metabolica 
        self.node_types = {}  # dicionário que vai dizer de que tipo é cada nó
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []  # cria uma key para dizer quais os nós serão de metabolitos
            self.node_types["reaction"] = []  # igual mas para nós de reações 
        self.split_rev =  split_rev  # diz se queremos que as reações reversiveis sejam consideradas como duas reações distintas
    
    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v)  # função da classe MyGraph
        self.node_types[nodetype].append(v)  # adiciona o numero do nó ao à lista correspondente ao tipo do nó
    
    def get_nodes_type(self, node_type): 
        if node_type in self.node_types:
            return self.node_types[node_type]  # retorna os nós que são do tipo parametrizado
        else: 
            return None
    
    def load_from_file(self, filename):
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")  # sempre que abrimos o ficheiro, fazemos logo o grafico metabolit-reaction
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: 
                raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: 
                raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction":   # se o que quero criar for metabolite reaction, vai ficar guardado no self.graph o que fico em gmr
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr)
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr)
        else: self.graph = {}
        
        
    def convert_metabolite_net(self, gmr):  # fazer o grafo só de metabolitos
        for m in gmr.node_types["metabolite"]:  # para cada metabolito que aparece
            self.add_vertex(m)  # adicona o nó 
            s = gmr.get_successors(m)  # retorna os sucessores de cada r
            for suc in s:
                s1 = gmr.get_successors(suc)  # retorna os sucessores dos sucessores de r
                for suc2 in s1:
                    if m != suc2:  # se nos sucessores dos sucessores de r estiver alguma reação diferente de r, então quer dizer que
                        # podemos chegar a essa reação partindo de r, e por isso: 
                        self.add_edge(m,suc2)

        
    def convert_reaction_graph(self, gmr):  # fazer o grafo so de reações
        for r in gmr.node_types["reaction"]:  # para cada reação
            self.add_vertex(r)  # adicona o nó 
            s = gmr.get_successors(r)  # retorna os sucessores de cada r
            for suc in s:
                s1 = gmr.get_successors(suc)  # os sucessores dos sucessores de r
                for suc2 in s1:
                    if r != suc2:  # se nos sucessores dos sucessores de r estiver alguma reação diferente de r, então quer dizer que
                        # podemos chegar a essa reação partindo de r, e por isso: 
                        self.add_edge(r,suc2)  # no grado das reações podemos criar uma ligação entre r e essa reação


def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1","reaction")
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1")
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") )
    print("Metabolites: ", m.get_nodes_type("metabolite") )

        
def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/example-net.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/example-net.txt")
    rrsn.print_graph()
    print()

  
def test3():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/ecoli.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    print (mrn.mean_degree("out"))
    d = mrn.prob_degree("out")
    for x in sorted(d.keys()):
        print (x, "\t", d[x])
    print(mrn.mean_distances())
    print(mrn.all_clustering_coefs())
    print(mrn.mean_clustering_perdegree())

   #print("metabolite-metabolite network:")
   #mmn = MetabolicNetwork("metabolite-metabolite")
   #mmn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/ecoli.txt")
   #mmn.print_graph()
   #print()
   #print (mmn.mean_degree("out"))
    #d = mmn.prob_degree("out")
    #for x in sorted(d.keys()):
    #    print (x, "\t", d[x])

   #print("reaction-reaction network:")
   #rrn = MetabolicNetwork("reaction-reaction")
   #rrn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/ecoli.txt")
   #rrn.print_graph()
   #print()
   #
   #print("metabolite-reaction network (splitting reversible):")
   #mrsn = MetabolicNetwork("metabolite-reaction", True)
   #mrsn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/ecoli.txt")
   #mrsn.print_graph()
   #print()
   #
   #print("reaction-reaction network (splitting reversible):")
   #rrsn = MetabolicNetwork("reaction-reaction", True)
   #rrsn.load_from_file("C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/ecoli.txt")
   #rrsn.print_graph()
   #print()

#test1()
#print()
#test2()
test3()