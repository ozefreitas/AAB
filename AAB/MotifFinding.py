# -*- coding: utf-8 -*-
"""

"""

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):  # fornecer um conjunto de sequencias, assim como o tamanho do motif
        self.motifSize = size
        if seqs is not None:
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []


    def __len__ (self):
        return len(self.seqs)


    def __getitem__(self, n):
        return self.seqs[n]


    def seqSize (self, i):
        return len(self.seqs[i])


    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()


    def createMotifFromIndexes(self, indexes):  # calcular o motif a parir de um vetor de posições iniciais 
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)

    # SCORES

    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score


    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     

    # EXHAUSTIVE SEARCH

    def nextSol (self, s):  # vai iterar sobre o vetor de posicoes inciais 
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:  # enquanto nao chegar ao fim das combinacoes de posicoes iniciais
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while s is not None:
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

    # BRANCH AND BOUND     

    def nextVertex (self, s):  # posições parciais, pode ser um tuplo de 2 ou mais elementos
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res


    def bypass (self, s): # s é o mesmo que nextvertex
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res


    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size  # no inicio será (0,0,0)
        while s is not None:
            if len(s) < size:  # a partir dai vai avaliar segundo o bypass, quando chegar a conclusao que o contributo dado pelas folhas
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore:  # se este for pior que o maior score
                    s = self.bypass(s)  # irá saltar para o proximo
                else: 
                    s = self.nextVertex(s)
            else:  # avalia todas as folhas iniciais 
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        mf = MotifFinding(self.motifSize, self.seqs[:2])
        s = mf.exhaustiveSearch()
        for i in range(2, len(self.seqs)):
            s.append(0)
            melhorScore = -1
            melhorposicao = 0
            for j in range(self.seqSize(i)-self.motifSize+1):
                s[i] = j
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorposicao = j
                s[i] = melhorposicao
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * self.seqs
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i)-self.motifSize)
        bestscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
            scr = self.score(s)
            if scr > bestscore:
                bestscore = scr
            else:
                improve = False
        return s

    # Gibbs sampling 

    def gibbs (self):
        from random import randint
        s = [0] * self.seqs
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i)-self.motifSize)
        seq_idx = (0, len(self.seqs)-1)
        seq = self.seqs.pop(seq_idx)
        s_partial = s.copy().remove(seq_idx)
        motif = self.createMotifFromIndexes(s_partial)
        motif.createPWM()
        s[seq_idx] = motif.mostProbableSeq(seq)
        return s


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    #sol2 = mf.gibbs(1000)
    #print ("Score:" , mf.score(sol2))
    #print ("Score mult:" , mf.scoreMult(sol2))

test4()
