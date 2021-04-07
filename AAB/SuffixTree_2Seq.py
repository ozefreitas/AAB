# -*- coding: utf-8 -*-

class SuffixTree_2Seq:
    
    def __init__(self):
        self.nodes = { 0:(-1, -1,{}) } # {root node:(numero da sequencia 0 ou 1, se for nó será -1, {simbolo: nó seguinte})}
        self.num = 0
        self.seq1 = ""
        self.seq2 = ""

    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][1] < 0:
                print (k, "->", self.nodes[k][2]) 
            else:
                print (k, ": Seqnum:", self.nodes[k][0],"Sufixnum:", self.nodes[k][1])


    def add_node(self, origin, symbol, seqnum = -1, leafnum = -1):
        self.num += 1
        self.nodes[origin][2][symbol] = self.num  # seleciona-se a posição 2 do tuplo para adicionar no segundo dicionário o nó seguinte
        self.nodes[self.num] = (seqnum, leafnum,{})  # abre o proximo


    def add_suffix(self, p, seqnum, sufnum):
        no = 0
        for s in range(len(p)):
            if p[s] not in self.nodes[no][2].keys():
                if s == len(p)-1: #se a posição em que nos encontramos é a final do sufixo
                    self.add_node(no, p[s], seqnum, sufnum)  #adiciona o ultimo no, ou seja a folha
                else:
                    self.add_node(no, p[s], seqnum)
            no = self.nodes[no][2][p[s]]
            

    def suffix_tree_from_seq(self, s1, s2):
        self.seq1 = s1
        self.seq2 = s2
        seq1 = s1 + "$"
        seq2 = s2 + "#"
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], 0, i)  # i representa a posicao incial do sufixo na sequencia, 0 representa a sequencia 1
        for j in range(len(seq2)):
            self.add_suffix(seq2[j:], 1, j)  # j representa a posicao incial do sufixo na sequencia, 1 representa a sequencia 2


    def find_pattern(self, pattern):
        node = 0
        res1 = []
        res2 = []
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][2].keys():
                node = self.nodes[node][2][pattern[pos]]
            else:
                return None
            if self.nodes[node][0] == 0:
                res1.append(self.get_leafes_below(node))
            else:
                res2.append(self.get_leafes_below(node))
        return res1, res2


    def get_leafes_below(self, node):
        res = [] #posicoes onde ocorre o padrao
        # print(node)
        if self.nodes[node][1] >= 0:  # se esse no, no primeiro elemento do tuplo nao tiver um valor positivo ou zero, quer dizer que é uma folha, e que encontramos o padrao
            # print(node)
            res.append(self.nodes[node][1]) # por isso podemos adicionar o valor desse tuplo, que corresponde ao indice de onde começa o sufixo na sequencia
            # print(res)
        else:  # se o no que veio da função find_pattern ainda nao for uma folha
            for k in self.nodes[node][2].keys():  # k vai tomar o(s) simbolo(s) para o nó atual  
                newnode = self.nodes[node][2][k]  # e o value correspondente ao simbolo de cima, será o proximo nó
                
                leafes = self.get_leafes_below(newnode)  # e vai correr novamente esta função para esse nó, até encontrar um valor negativo, que representa a folha
                res.extend(leafes)
                # print(res)
        return res


    def nodes_below(self, node):
        res = []
        if node in self.nodes.keys():  # verifica se o nó especificado é um nó da arvore
            for value in self.nodes[node][2].values():  # guarda em value os nos que estao no dicionário interior
                res.append(value)
            for nos in res:
                for values in self.nodes[nos][2].values():  # para os nos em res, atribui o no seguinte a values
                    res.append(values)  # e adiciona esse no a res, que por cada valor que adicona a res, permite que haja outro no e haja mais um ciclo
            return sorted(res)
        else:
            return None


    def nodes_below_symb(self, node):
        res = []  # lista de simbolos que aparecem depois do nó especificado
        newnode = 0
        if self.nodes[node][0] < 0:  # tem que ser um nó, ou seja o primeiro elemento do tuplo tem que ser -1
            for sym, no in self.nodes[node][2].items():  # sym vai tomar os simbolos que estao nesse nó, e no vai tomar os nos que estao a seguir do no que se quer 
                res.append(sym)  # adiciona imediatamente o primero simbolo que vê
                newnode = no  # o proximo no a ser visto será o que esta logo a seguir (que é o que esta associado ao simbolo)   
                if self.nodes[newnode][0] >= 0:  # quando chegar a folha
                    continue
                else:
                    while self.nodes[newnode][0] < 0:  # enquanto for um nó
                        for symb in self.nodes[newnode][2].keys():  # este nó agora é analisado, sendo que symb toma o simbolo que está nesse nó
                            res.append(symb)  # adicona-se o simbolo
                        newnode = self.nodes[newnode][2][symb]  # passa-se para o proximo nó
                return res
        else:
            return None


    def largestCommonSubstring(self):
        subseq = ""  # maior sequencia será guardada
        for x in range(len(self.seq1)):  # corre a primeira sequencia
            for y in range(len(self.seq2)):  # corre a segunda sequencia
                c = 1
                while x + c <= len(self.seq1) and y + c <= len(self.seq2):  # ciclo while que vai permitir aumentar a janela a analisar em ambas as sequencias
                    if self.seq1[x:x+c] == self.seq2[y:y+c]:  # se os caracteres fruto deste splicing forem iguais de uma seq para a outra
                        if len(subseq) <= len(self.seq1[x:x+c]):  # e se o tamanho desse for maior ou igual que o tamanho da subsequencia já gravada
                            subseq = self.seq1[x:x+c]  # subsquencia comum passa a ser essa
                    c += 1  # vai correr até que o tamanho da janela supere o tamanha de uma das sequencias
        return subseq


def test():
    seq1 = "TACTA"
    seq2 = "TAGAC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))

def test2():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    # print (st.find_pattern("TA"))

def test3():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.nodes_below(0))

def test4():
    seq1 = "TACTA"
    seq2 = "ATGAC"
    st = SuffixTree_2Seq()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.largestCommonSubstring())

#test()
#print()
#test2()
#test3()
test4()


# 0 -> {'T': 1, 'A': 7, 'C': 12, '$': 18, 'G': 28, '#': 34}
# 1 -> {'A': 2, 'G': 24}
# 2 -> {'C': 3, '$': 16}
# 3 -> {'T': 4}
# 4 -> {'A': 5}
# 5 -> {'$': 6}
# 6 : Seqnum: 0 Sufixnum: 0
# 7 -> {'C': 8, '$': 17, 'T': 19}
# 8 -> {'T': 9, '#': 32}
# 9 -> {'A': 10}
# 10 -> {'$': 11}
# 11 : Seqnum: 0 Sufixnum: 1
# 12 -> {'T': 13, '#': 33}
# 13 -> {'A': 14}
# 14 -> {'$': 15}
# 15 : Seqnum: 0 Sufixnum: 2
# 16 : Seqnum: 0 Sufixnum: 3
# 17 : Seqnum: 0 Sufixnum: 4
# 18 : Seqnum: 0 Sufixnum: 5
# 19 -> {'G': 20}
# 20 -> {'A': 21}
# 21 -> {'C': 22}
# 22 -> {'#': 23}
# 23 : Seqnum: 1 Sufixnum: 0
# 24 -> {'A': 25}
# 25 -> {'C': 26}
# 26 -> {'#': 27}
# 27 : Seqnum: 1 Sufixnum: 1
# 28 -> {'A': 29}
# 29 -> {'C': 30}
# 30 -> {'#': 31}
# 31 : Seqnum: 1 Sufixnum: 2
# 32 : Seqnum: 1 Sufixnum: 3
# 33 : Seqnum: 1 Sufixnum: 4
# 34 : Seqnum: 1 Sufixnum: 5
