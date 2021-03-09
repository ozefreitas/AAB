# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node, se for -1 representa um nó, caso contrário é uma folha
        self.num = 0


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
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)  # adiciona no final da sequencia um "$", e a partir dessa faz a arvore de sufixos com a função add_suffix


    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)  # sse encontrar um match, corre a funçar a baixo para ver qual a posição inicial do padrao na sequencia, que é dada pelas folhas
        

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