# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1, -1,{}) } # {root node:(numero da sequencia 0 ou 1, se for nó será -1, {simbolo: no seguinte})}
        self.num = 0


    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][1] < 0:
                print (k, "->", self.nodes[k][2]) 
            else:
                print (k, ":", self.nodes[k][0], self.nodes[k][1])


    def add_node(self, origin, symbol, seqnum = -1, leafnum = -1):
        self.num += 1
        self.nodes[origin][2][symbol] = self.num #seleciona-se a posição 2 do tuplo para adicionar no segundo dicionário
        self.nodes[self.num] = (seqnum, leafnum,{})


    def add_suffix(self, p, seqnum, sufnum):
        no = 0
        for s in range(len(p)):
            if p[s] not in self.nodes[no][2].keys():
                if s == len(p)-1: #se a posição em que nos encontramos é a final do sufixo
                    self.add_node(no, p[s], seqnum, sufnum)  #adiciona o ultimo no, ou seja a folha
                else:
                    self.add_node(no, p[s])
            no = self.nodes[no][2][p[s]]
            

    def suffix_tree_from_seq(self, s1, s2):
        seq1 = s1 + "$"
        seq2 = s2 + "#"
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], 0, i)  # i representa a posicao incial do sufixo na sequencia, 0 representa a sequencia 1
        for j in range(len(seq2)):
            self.add_suffix(seq2[j:], 1, j)  # j representa a posicao incial do sufixo na sequencia, 1 representa a sequencia 2


    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][2].keys():
                node = self.nodes[node][2][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)


    def get_leafes_below(self, node):
        res1 = []  # posicoes onde ocorre o padrao na primeira sequencia
        res2 = []  # posicoes onde ocorre o padrao na segunda sequencia
        if self.nodes[node][1] >=0:  # se esse no, no primeiro elemento do tuplo nao tiver -1, quer dizer que é uma folha, e que encontramos o padrao
            if self.nodes[node][0] == 0:  # verifica no tuplo do dicionario nodes a qual das sequencias corresponde
                res1.append(self.nodes[node][1]) # por isso podemos adicionar o valor desse tuplo, que corresponde ao indice de onde começa o sufixo na sequencia (o valor na folha é exatamente isso)
            else:
                res2.append(self.nodes[node][1])
        else: # para o caso de o nó que veio da função find_pattern e que iniciou esta função, ainda ser um nó, 
            # e por isso tem que se continuar a percorrer a arvore, de forma a chegar a folha desse ramo e 
            # podermos saber qual o valor associado a essa folha e consequentemente o indice do sufixo 
            if self.nodes[node][0] == 0:  # para o caso de ser a sequencia 1
                for k in self.nodes[node][2].keys():
                    newnode = self.nodes[node][2][k]
                    leafes = self.get_leafes_below(newnode)  # recursividade, volta a correr esta função ate ver que o novo nó passa a ser uma folha
                    res1.extend(leafes)
            else:  # para o caso de ser a sequencia 1
                for k in self.nodes[node][2].keys():
                    newnode = self.nodes[node][2][k]
                    leafes = self.get_leafes_below(newnode)
                    res2.extend(leafes)
        return (res1, res2)


    def largestCommonSubstring(self):
        subseq = ""

        pass


def test():
    seq1 = "TACTA"
    seq2 = "TAGAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))

def test2():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    print (st.find_pattern("TA"))
    # print(st.repeats(2,2))

test()
print()
test2()
