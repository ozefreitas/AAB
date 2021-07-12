# -*- coding: utf-8 -*-

class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        """
        Função inicializadora

        Parameters
        ----------
        alphabet : String
            String dos simbolos que iram aparecer na sequencia na qual se quer ver os padroes.
        pattern : String
            String do padrao a procurar.

        """
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()  # chama a funçao a baixo

    def preprocess(self):  # esta por sua vez automatimente executa as duas funções a baixo
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):  # cria um dicionário que corresponde ao pre processamento da sequencia para a bcr
        """
        Implementação do pré-processamento do bad caracter rule

        """
        self.occ = {}
        for c in self.alphabet:
            self.occ[c] = -1
        for i in range(len(self.pattern)):
            self.occ[self.pattern[i]] = i

    def process_gsr(self):  # cria 
        """
        Implementação do pré-processamento do good suffix rule

        """
        self.f = [0] * (len(self.pattern) + 1)
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern)
        j = i + 1
        self.f[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i-1] != self.pattern[i-1]:
                if self.s[j] == 0:
                    self.s[j] = j-i
                j = self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j
        j = self.f[0]
        for i in range(0, len(self.pattern)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]

    def search_pattern(self, text):
        res = []
        i = 0  # posição na sequencia
        while i <= (len(text) - len(self.pattern)):  # percorre os simbolos na sequencia
            j = len(self.pattern) - 1  # posição no padrão
            while j >= 0 and self.pattern[j] == text[j + i]:
                j = j - 1 
            if j < 0:  # quando o j passar a ser menor que 0 quer dizer que se encontrou um padrao
                res.append(i)  # adiciona à lista a posição onde começou a analise (i)
                i = i + self.s[0]
            else:  # enquanto o j continuar a ser maior ou igual a 0, mas o simbolo no padrao na posição j deixa de ser igual
            # ao correspondente na sequencia
                c = text[j + i]  # vai buscar o simbolo dessa posição
                i += max(self.s[j+1], j - self.occ[c])  # i vai tomar o valor do maior indice entre as duas regras
                
        return res


def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


if __name__ == "__main__":
    test()

# result: [5, 13, 23, 37]
