# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node, se for -1 representa um nó, caso contrário é uma folha
        self.num = 0
        self.sequence = ""


    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:  # vai buscar o tuplo que esta como value da key k, e dentro desse tulo, vai buscar o primeiro valor
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])


    def add_node(self, origin, symbol, leafnum = -1): # mesmo efeito que na trie
        self.num += 1
        self.nodes[origin][1][symbol] = self.num  # seleciona-se a posição 2 do tuplo para adicionar no segundo dicionário com o simbolo
        self.nodes[self.num] = (leafnum,{})


    def add_suffix(self, p, sufnum):  # mesmo efeito que add_pattern em trie
        no = 0
        for s in range(len(p)):
            if p[s] not in self.nodes[no][1].keys():  # vai buscar a chave com o valor de s, 
            # dentro desse value (que é um tuplo de um inteiro e um dicionário) 
            # vai buscar a segunda posição e vai dividir por keys (que são simbolos do alfabeto da sequencia)
                if s == len(p)-1: #se a posição em que nos encontramos é a final do sufixo
                    self.add_node(no, p[s], sufnum)  #adiciona o ultimo nó, ou seja a folha
                else:
                    self.add_node(no, p[s]) # caso contrario adiona outro nó
            no = self.nodes[no][1][p[s]]  # passa para o proximo nó e continua o ciclo
   

    def suffix_tree_from_seq(self, text):
        self.sequence = text
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)  # adiciona no final da sequencia um "$", e a partir dessa faz a arvore de sufixos com a função add_suffix


    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]  # o value do dicionario "interno" diz para qual no se deve ir a seguir para continuarmos a ver o sufixo
            else:
                return None
        return self.get_leafes_below(node)  # se encontrar um match, corre a funçar a baixo para ver qual a posição inicial do padrao na sequencia, que é dada pelas folhas
        

    def get_leafes_below(self, node):
        res = [] #posicoes onde ocorre o padrao
        if self.nodes[node][0] >=0:  # se esse no, no primeiro elemento do tuplo nao tiver um valor positivo ou zero, quer dizer que é uma folha, e que encontramos o padrao
            res.append(self.nodes[node][0]) # por isso podemos adicionar o valor desse tuplo, que corresponde ao indice de onde começa o sufixo na sequencia
        else:
            for k in self.nodes[node][1].keys():  # para os restantes nós
                newnode = self.nodes[node][1][k]  # vai percorrer os values de k dentro das keys node
                leafes = self.get_leafes_below(newnode)  # e vai correr novamente esta função para esse value, até encontrar um valor negativo, que representa o $
                res.extend(leafes)
        return res


#    def nodes_below(self, node):
#        # enquanto nao encontrar um dicionário "interno" com apenas um elemento e esse elemento seja $; quando encontrar, para
#        res = []
#        t = 0
#        if self.nodes[node][0] < 0:
#            while t < len(self.nodes):  # dar uma folga
#                for k in self.nodes[node+t][1].keys():
#                    res.append(k)
#                    if k == "$" and len(self.nodes[node+t][1]) == 1:  # se essa key for igual a $ e estiver sozinha nesse dicionario do no a analisar, quer dizer que chegamos à folha
#                        return res  # e pode-se dar return à lista 
#                t += 1  
#            return res 
#        else:
#            return "That's a leaf!"
#

    def nodes_below_2(self, node):
        res = []  # lista de simbolos que aparecem depois do nó especificado
        t = 0
        if self.nodes[node][0] < 0:  # tem que ser um nó, ou seja o primeiro elemento do tuplo tem que ser -1
            for sym, no in self.nodes[node][1].items():  # sym vai tomar os simbolos que estao nesse nó, e no vai tomar os nos que estao a seguir do no que se quer 
                res.append(symb)  # adiciona imediatamente o primero simbolo que vê
                no = node  # o proximo no a ser visto será o que esta logo a seguir (que é o que esta associado ao simbolo)
                if self.nodes[no][0] >= 0:  # quando chegar a folha
                    continue
                else:
                    for symb in self.nodes[no][1].keys():  # este nó agora é analisado, sendo que symb toma o simbolo que está nesse nó
                        res.append(symb)  # adicona-se o simbolo
                        no = self.nodes[no][1][symb]  # passa-se para o proximo nó
                        if self.nodes[no][0] >= 0:  # quando chegar a folha
                            break  # quebra este ciclo e passa ao ciclo exterior
            return res  # retorna a lista de simbolos
        else:
            return "That's a leaf!"


    def matches_prefix(self, prefix):
        res = [] # primeiro elemento será sempre o próprio prefixo
        st = ""  # string para, de cada vez que se avança o nó e se ve qual o elemento seguinte, concatena-se esse elemento para, em cada adição, adicinar à lista
        # pos = self.find_pattern(prefix)  # pos será uma lista com os indices onde o padrão se inicia na sequencia usada para construir a arvore
        node = 0
        for s in range(len(prefix)):
            if prefix[s] in self.nodes[node][1].keys():
                st += prefix[s]
                node = self.nodes[node][1][prefix[s]]
                if len(st) == len(prefix):
                    res.append(st)
        for x in range(len(prefix), len(self.sequence)):
            if self.sequence[x] in self.nodes[node][1].keys():
                st += self.sequence[x]
                node = self.nodes[node][1][self.sequence[x]]
                res.append(st)
        return res


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    # print(st.repeats(2,2))

test()
print()
#test2()

#0 -> {'T': 1, 'A': 7, 'C': 12, '$': 18}
#1 -> {'A': 2}
#2 -> {'C': 3, '$': 16}
#3 -> {'T': 4}
#4 -> {'A': 5}
#5 -> {'$': 6}
#6 : 0
#7 -> {'C': 8, '$': 17}
#8 -> {'T': 9}
#9 -> {'A': 10}
#10 -> {'$': 11}
#11 : 1
#12 -> {'T': 13}
#13 -> {'A': 14}
#14 -> {'$': 15}
#15 : 2
#16 : 3
#17 : 4
#18 : 5
#[0, 3]
#None