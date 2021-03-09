class Automata:

    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)

    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):  # toma os valores para o numero de estados
            for a in self.alphabet:  # toma os caracteres do alfabeto
                prefix = pattern[:q] + a  # adiciona o caracter do alfabeto atribuido a "a" no final do prefixo
                self.transitionTable[(q, a)] = self.overlap(prefix, pattern)  # para depois poder dizer qual é o estado seguinte
                # adiciona ao dicionário uma chave em tuplo com o numero do estado atual e o simbolo seguinte, e value o estado para o qual se deve ir a seguir

    def printAutomata(self):
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]  # vai buscar o valor que corresponde à chave no dicionário (que é um tuplo), e que diz qual o estado para o qual se deve ir a seguir

    def applySeq(self, seq):
        """
        Devolve a sequencia dos estados que foram tomados ao longo da análise

        seq: String
        Sequencia na qual se pretende ver se o padrão ocorre
        """
        q = 0
        res = [q]
        for c in seq:
            q = self.nextState(q, c)  # O estado atual varia consoante o simbolo seguinte, e guarda em q
            res.append(q)
        return res

    def occurencesPattern(self, text):  # vai buscar os values correspondentes na tabela de transição
        """
        No caso de ocorrer o padrao na sequencia, devolve os indices da sequencia
        onde o padrao tem inicio

        seq: String
        Sequencia na qual se pretende ver se o padrão ocorre
        """
        q = 0
        res = []
        for i in range(len(text)):
            q = self.nextState(q, text[i])  # correspondentes ao estado atual e o symbolo seguinte (que é exatamente o que a função nextState faz)
            if q == self.numstates - 1:  # quando ve que chegou ao estado final, quer dizer que encontrou o padrao na sequencia e...
                res.append(i - self.numstates + 2)  # vai adicionar o indice da sequencia onde o padrao começou
        return res

    def overlap(self, s1, s2):  # verifica se o prefixo é igual ao padrao até a posição final
        maxov = min(len(s1), len(s2))
        for i in range(maxov, 0, -1):
            if s1[-i:] == s2[:i]:  # dá return ao numero da ultima posição do padrao que foi igual
                return i
        return 0  # caso contrário volta ao incio


def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print(auto.applySeq("CACAACAA"))
    print(auto.occurencesPattern("CACAACAA"))


test()

# States:  4
# Alphabet:  AC
# Transition table:
# 0 , A  ->  1
# 0 , C  ->  0
# 1 , A  ->  1
# 1 , C  ->  2
# 2 , A  ->  3
# 2 , C  ->  0
# 3 , A  ->  1
# 3 , C  ->  2
# [0, 0, 1, 2, 3, 1, 2, 3, 1]
# [1, 4]
