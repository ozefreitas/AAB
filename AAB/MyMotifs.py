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
        if self.counts == None: 
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)


    def createPWM_pseudo(self):
        if self.counts == None: 
            self.doCounts_pseudo()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)


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


    def probabSeq (self, seq):  # calcula a probablidade de uma sequencia de acordo com a pwm
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res


    def probAllPositions(self, seq):
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res


    def mostProbableSeq(self, seq):
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
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
    motifs.doCounts_pseudo()
    printMat(motifs.counts)
    print()
    printMat(motifs.pwm)
    print()
    motifs.createPWM_pseudo()
    printMat(motifs.pwm)
    #print(motifs.alphabet)
    print()
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
