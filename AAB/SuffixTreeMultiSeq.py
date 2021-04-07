# -*- coding: utf-8 -*-

class SuffixTreeMultiSeq:
    
    def __init__(self, seqlist, finishchars):
        self.nodes = { 0:(-1, -1,{}) }  # {root node:(numero da sequencia entre 0 e numero de sequencia dadas - 1, se for nó será -1, {simbolo: nó seguinte})}
        self.num = 0  # contador de nós
        self.seqs = seqlist  # lista de sequencias para construir a arvore de sufixos
        self.char = finishchars  # lista de caracteres de terminação, que cada um corresponde à sequencia com o mesmo indice em seqlist


    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][1] < 0:
                print (k, "->", self.nodes[k][2]) 
            else:
                print (k, ": Seqnum:", self.nodes[k][0],"Sufixnum:", self.nodes[k][1])


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
                    self.add_node(no, p[s], seqnum)  # caso contrário, adiciona um nó, e o quarto argumento mantem o default na função de cima, ou seja, fica -1
            no = self.nodes[no][2][p[s]]  # passar ao proximo nó
            

    def suffix_tree_from_seq(self):
        for seq in range(len(self.seqs)):
            sequence = self.seqs[seq] + self.char[seq]
            for i in range(len(sequence)):
                self.add_suffix(sequence[i:], seq, i)  # i representa a posicao incial do sufixo na sequencia, seq representa o numero da sequencia


    def find_pattern(self, pattern):  # completar
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][2].keys():
                node = self.nodes[node][2][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)


    def get_leafes_below(self, node):  # completar
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
    lst = ["TACAG", "TACTG", "AGTCG", "CTAGC"]
    lst2 = ["$", "#", "*", "%"]
    st = SuffixTreeMultiSeq(lst, lst2)
    st.suffix_tree_from_seq()
    st.print_tree()

test()