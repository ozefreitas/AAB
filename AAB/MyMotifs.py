# -*- coding: utf-8 -*-
"""
@author: miguelrocha
"""

def createMatZeros (nl, nc):
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat):
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:

    def __init__(self, seqs):  # fornece-se um conjunto de subsequencias para construir os perfis (PWM e consensos)
        self.size = len(seqs[0])
        self.seqs = seqs  # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()


    def __len__ (self):
        return self.size


    def doCounts(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)  # cria uma matriz so com zeros de acordo com o tamanho das sequencias e alfabeto 
        for s in self.seqs:
            for i in range(self.size):  # vai preenchendo a matriz de acordo com as ocorrencias de cada nucleoido em cada posição das sequencias 
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1


    def doCounts_pseudo(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)  # cria uma nova matriz de 0
        for i in range(len(self.counts)):
            for j in range(len(self.counts[0])):  # percorre esta nova matriz toda
                self.counts[i][j] += 1  # e adiciona 1 a todos os elementos
        for s in self.seqs:
            for i in range(self.size):  # vai preenchendo a matriz de acordo com as ocorrencias de cada nucleoido em cada posição das sequencias
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1


    def createPWM(self):
        self.doCounts()  # faz a matriz de contagens sem ser pseudo, para trocar caso a que estava guardada anterirormente fosse a de pseudo ontagens
        self.pwm = createMatZeros(len(self.alphabet), self.size)  # cria uma nova matriz de zeros com 4 linhas (alfabeto) e numero de colunas correspondente ao tamanha das sequencias
        for i in range(len(self.alphabet)):  # corre as linhas
            for j in range(self.size):  # corre as colunas
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)  # pega nos valores da correspondentes da matriz de contagem e divide pelo numero total de sequencias, trocando os zeros por esses valores


    def createPWM_pseudo(self):
        self.doCounts_pseudo()  # em vez de fazer a matriz de contagens normais, vai fazer a matriz de pseudo contagens
        self.pwm = createMatZeros(len(self.alphabet), self.size)  # cria uma nova matriz de zeros
        for i in range(len(self.alphabet)):  # corre as linhas
            for j in range(self.size):  # corre as colunas
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)  # pega nos valores correspondentes de pseudo-contagem e divide pelo numero total de sequencias 


    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res


    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res


    def probabSeq (self, seq):  # calcula a probablidade de uma sequencia individual de acordo com a pwm
        res = 1.0
        for i in range(self.size):  # itera sobre as posições da sequencia (motif)
            lin = self.alphabet.index(seq[i])  # de acordo com o alfabeto, vê qual a linha para depois usar na PWM
            res *= self.pwm[lin][i]  # cada valor é multiplicado pelo anterior
        return res


    def probAllPositions(self, seq):  # recebe uma sequencia inteira
        res = []
        for k in range(len(seq) - self.size + 1):
            res.append(self.probabSeq(seq[k : k + self.size]))  # ESTAVA ERRADO, não estava a fazer o splicing da sequencia, nem iteração para fazer avançar a janela
        return res


    def SumprobAllPositions(self, seq):
        res = self.probAllPositions(seq)
        soma = 0
        for x in res:
            soma += x
        return soma


    def mostProbableSeq(self, seq):  # recebe uma sequencia inteira
        maximo = -1.0
        maxind = -1
        for k in range(len(seq) - self.size):  # faz a iteração num range que so vai até ao comprimento da sequencia menos o comprimento do motif
            p = self.probabSeq(seq[k : k + self.size])  # faz a probabilidade de cada subsquencia ocorrer
            if(p > maximo):  # devolve o maior valor de probabilidade
                maximo = p
                maxind = k
        return maxind


def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    print()
    #motifs.doCounts_pseudo()
    printMat(motifs.counts)
    print()
    motifs.createPWM()
    printMat(motifs.pwm)
    print()
    #motifs.createPWM_pseudo()
    #printMat(motifs.pwm)
    #print(motifs.alphabet)
    print()
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.probAllPositions("CTATAAACCTTACATC"))
    print(motifs.SumprobAllPositions("CTATAAACCTTACATC"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
