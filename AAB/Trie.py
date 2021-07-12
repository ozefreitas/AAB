# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = {0: {}}  # dictionary
        self.num = 0

    def print_trie(self):
        for k in self.nodes.keys():
            print(k, "->", self.nodes[k])

    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num  # origin vai buscar o valor da key, e symbol vai buscar o simbolo do dicionário que corresponde a essa key
        self.nodes[self.num] = {}  # o mesmo tempo cria outro key com o numero do nó seguinte, para ser preenchido a seguir

    def add_pattern(self, p):  # p é um novo padrao
        no = 0
        for s in range(len(p)):  # percorre os simbolos do padrao
            if p[s] not in self.nodes[no].keys():  # se esse simbolo não estiver no dicionário que corresponde à key do no que se está a ver
                self.add_node(no, p[s])  # vai se adicionar esse no, em conjunto com o simbolo s 
            no = self.nodes[no][p[s]]  # passa-se depois para esse no, e repete-se o processo para o simbolo seguinte

    def trie_from_patterns(self, patterns):
        for p in patterns:
            self.add_pattern(p)  # vai executar a função de cima para cada padrão que se quiser adicionar

    def prefix_trie_match(self, text):  # quando virmos que nao se consegue ir mais, dá-se return ao match
        match = ""
        no = 0
        for s in range(len(text)):
            if text[s] in self.nodes[no].keys():
                no = self.nodes[no][text[s]]
                match += text[s]  # guarda o caminho da arvore a medida que o padrao vai dando match com a sequencia
                if self.nodes[no] == {}:  #se o nó a que chegamos é uma folha, e se for, damos return ao match que temos ate esse momento
                    return match  # se isto nao se verificar, continua a percorrer a avore
            else:
                return None  #tbm pode acontecer que nao ha qualquer match, por isso nao da return a nada
        return None

    def trie_matches(self, text):  # uma sequencia como argumento, a qual vamos ver se contem qualquer um dos padroes guardados na arvore
        res = []
        for i in range(len(text)):  # percorre a sequencia
            m = self.prefix_trie_match(text[i:]) #vai ver se ha algum match do padrao
            if m is not None:  # se houver um match
                res.append((i, m))  # vai dar append a um tuplo, com o indice da primeria posição na sequencia onde o match foi encontrado e o proprio match
        return res


def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))


# test()
print()
test2()

# 0 -> {'A': 1, 'C': 11, 'G': 19, 'T': 25}
# 1 -> {'G': 2}
# 2 -> {'A': 3, 'C': 7, 'T': 8}
# 3 -> {'G': 4}
# 4 -> {'A': 5}
# 5 -> {'T': 6}
# 6 -> {}
# 7 -> {}
# 8 -> {'C': 9}
# 9 -> {'C': 10}
# 10 -> {}
# 11 -> {'A': 12, 'C': 16}
# 12 -> {'G': 13}
# 13 -> {'A': 14}
# 14 -> {'T': 15}
# 15 -> {}
# 16 -> {'T': 17}
# 17 -> {'A': 18}
# 18 -> {}
# 19 -> {'A': 20}
# 20 -> {'G': 21, 'T': 24}
# 21 -> {'A': 22}
# 22 -> {'T': 23}
# 23 -> {}
# 24 -> {}
# 25 -> {'C': 26}
# 26 -> {}
# GAGAT
# [(0, 'GAGAT')]
