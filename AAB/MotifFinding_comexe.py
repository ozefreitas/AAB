# -*- coding: utf-8 -*-
"""

"""

from MySeq import MySeq
from MyMotifs_comexe import MyMotifs

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
        for i,ind in enumerate(indexes):  # i toma o indice para fazer a iteração das sequencias, e ind toma os valores de posições iniciais
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )   # por cada valor presente no vetor
            # vai buscar a sequencia correspondente, e dentro dessa dar slice à subsequencia do tamanho do motif especificado ao inicio
        return MyMotifs(seqs=pseqs)  # cria um objeto MyMotifs com os motifs resultantes

    # SCORES

    def score(self, s): 
        """
        Recebe um vetor de posições inicias, que depois vai usar para criar os motifs (com a função
        createMotifFromIndexes) em cada sequencia já proporcionada na inicialização do MotiFinding
        """
        score = 0
        motif = self.createMotifFromIndexes(s)  # o objeto MyMotifs é atribuido a motif
        motif.doCounts()  # função da classe MyMotifs
        mat = motif.counts  # a matriz de contagem dos motifs 
        for j in range(len(mat[0])):  # itera sobre todas as colunas
            maxcol = mat[0][j]
            for i in range(1, len(mat)):  # itera sobre as linhas
                if mat[i][j] > maxcol:  # e para dentro da mesma coluna, vê todas as linhas para ver qual dos nucleotidos aparece mais vezes
                    maxcol = mat[i][j]  # quando encontrar o maior valor,
            score += maxcol  # vai adicionar ao score
        return score


    def pseudo_score(self, s):
        """
        Igual a função score mas calcula este de acordo com a matriz de pseudo-contagem
        """
        score = 0
        motif = self.createMotifFromIndexes(s)  # o objeto MyMotifs é atribuido a motif
        motif.doCounts_pseudo()  # função da classe MyMotifs
        mat = motif.counts  # a matriz de pseudo-contagem dos motifs 
        for j in range(len(mat[0])):  # itera sobre todas as colunas
            maxcol = mat[0][j]
            for i in range(1, len(mat)):  # itera sobre as linhas
                if mat[i][j] > maxcol:  # e para dentro da mesma coluna, vê todas as linhas para ver qual dos nucleotidos aparece mais vezes
                    maxcol = mat[i][j]  # quando encontrar o maior valor,
            score += maxcol  # vai adicionar ao score
        return score


    def scoreMult(self, s, pwm = None):
        """
        Igual a função score, só que em vez de se somar os consecutivos scores, multiplicam-se
        Usa a PWM, ou seja, a frequencia de cada nucleotido a dividir pelo numero de sequencias 
        """
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        mat = pwm  # matriz pwm fornecida
        if pwm is None:
            motif.createPWM()
            mat = motif.pwm  # matriz PWM
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     


    def pseudo_scoreMult(self, s):
        """
        Igual a função scoreMult mas calcula este de acordo com a PWM de pseudo contagem
        """
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM_pseudo()
        mat = motif.pwm  # matriz PWM proveniente da matriz de pseudo contagens
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score

    # EXHAUSTIVE SEARCH

    def nextSol (self, s):  # vai iterar sobre o vetor de posicoes inciais 
        nextS = [0] * len(s)
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
        s = [0] * len(self.seqs)  # vetor de posições iniciais
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
            if pos < 0: 
                res = None # last solution
            else:
                for i in range(pos): 
                    res.append(s[i])
                res.append(s[pos]+1)
        return res


    def bypass (self, s): # s é o mesmo que nextvertex
        res =  []
        pos = len(s) -1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: 
            res = None 
        else:
            for i in range(pos): 
                res.append(s[i])
            res.append(s[pos] + 1)
        return res


    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0] * size  # no inicio será (0,0,0)
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
                    melhorMotif = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        mf = MotifFinding(self.motifSize, self.seqs[:2])  # cria um objeto MotifFinding apenas para as primeiras duas sequencias
        s = mf.exhaustiveSearch()  # nas quais fazemos uma procura exaustiva entre as duas para determinar S1 e S2 
        for i in range(2, len(self.seqs)):  # para as restantes sequencias
            s.append(0)
            melhorScore = -1
            melhorposicao = 0
            for j in range(self.seqSize(i) - self.motifSize + 1):  # vai correr as posições da sequencia i até ao comprimento do motif
                s[i] = j  # adiciona essa posição ao vetor de posições iniciais
                scoreatual = self.score(s)  # faz o score para o vetor em cada momento
                if scoreatual > melhorScore:  # se o score melhorar
                    melhorScore = scoreatual  # o melhor score passa a ser esse
                    melhorposicao = j  # e o indice respetivo de onde começa essa subsquencia na sequencia i
                s[i] = melhorposicao  # adiciona esse indice ao vetor de posições iniciais
        return s

    # Consensus (heuristic estocastico)

    def heuristicStochastic(self):
        from random import randint
        s = [0] * len(self.seqs)  # vetor de posições iniciais
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  # preenche o vetor com posições aleatorias
        bestscore = self.score(s)  # a função score cria os motifs e a matriz de contagem e assim faz o score para o vetor criado aleatoriamente
        improve = True
        while improve:  # enquanto improve for True
            motif = self.createMotifFromIndexes(s)  # cria os motifs a partir do vetor de posições iniciais
            motif.createPWM()  # faz a PWM de acordo com os motifs criados
            for i in range(len(self.seqs)):  # para todas as sequencias 
                s[i] = motif.mostProbableSeq(self.seqs[i])  # ve qual o segmento mais provavel em cada uma de acordo com a PWM, e muda a posição incial dessa sequencia para a posição encontrada
            scr = self.score(s)  # calcula o score desse segmento
            if scr > bestscore:  # se esse score for melhor que o anterior
                bestscore = scr  # passa a ser o melhor score
            else:
                improve = False  # quando o score não aumentar, improve passa a ser False e o ciclo acaba
        return s

    # Gibbs sampling 

    def gibbs(self, n):  # n é o numero de iterações
        from random import randint
        s = [0] * len(self.seqs)  # vetor de posições iniciais so com zeros
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  # criar vetor de posições iniciais aleatorias
        vector = s  # variavel que vai receber o vetor de posições iniciais com o melhor score mais tarde
        bestscore = self.score(s)  # faz o score de s com as posições iniciais aleatórias 
        i = 0
        while i <= n:
            seq_idx = randint(0, len(self.seqs) - 1)  # escolher uma das sequencias aleatoriamente
            igno_seq = self.seqs.pop(seq_idx)  # remover a sequencia selecionada e atribuila a uma variavel, assim, self.seqs ficará apenas com 4 sequencias
            #print(self.seqs)
            #print(igno_seq)
            s.pop(seq_idx)  # retirar do vetor de posições o valor da posição inicial que seria para a sequencia retirada
            motif = self.createMotifFromIndexes(s)  # fazer os motifs para as restantes sequencias em self.seqs, de acordo com os indices restantes em s
            motif.createPWM()  # fazer a pwm para depois poder fazer as probabilidades de todas as subsquencias do tamanho do motif
            probs = motif.probAllPositions(igno_seq)  # devolve uma lista de sequencias com as probabilidades de todas as subsquencias 
            new_ind = self.roulette(probs)  # a função roulet escolhe um indice de acordo com as probabilidades de cada posiçao inicial obtida pela função anterior
            self.seqs.insert(seq_idx, igno_seq)  # adicionamos novamente e no mesmo local, a sequencia que foi retirada antes
            s.insert(seq_idx, new_ind)  # adiciona-se agora, tambem no mesmo local de onde foi retirado o valor de inicio do motif, o novo indice que vem da roulette
            sc = self.score(s)  # faz novamente o score para o novo vetor de posições inicias
            if sc > bestscore:  # se esse score for melhor que o anterior
                bestscore = sc  # atualiza-se o melhor score
                vector = s  # e o vetor de posições iniciais correspondente é dado a uma variavel
            i += 1  # continua-se o ciclo até ao fim das iteações que foi dado
        return vector


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: 
            tot += (0.01 + x)
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind - 1

    # Consensus (heuristic estocastico) with pseudo 

    def heuristicStochastic_pseudo(self):  # igual a anterior
        from random import randint
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        bestscore = self.pseudo_score(s)  # muda o metodo de score, para passar a calcular o score de acordo com a matriz de pseudo-contagem
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM_pseudo()  # cria a PWM a partir das pseudocontagens
            for i in range(len(self.seqs)):
                s[i] = motif.mostProbableSeq(self.seqs[i])
            scr = self.pseudo_score(s)  # a mesma coisa que em cima
            if scr > bestscore:
                bestscore = scr
            else:
                improve = False
        return s

    # Gibbs sampling with pseudo 

    def gibbs_pseudo(self, n):
        from random import randint
        s = [0] * len(self.seqs)  # vetor de posições iniciais so com zeros
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  # criar vetor de posições iniciais aleatorias
        vector = s  # variavel que vai receber o vetor de posições iniciais com o melhor score mais tarde
        bestscore = self.pseudo_score(s)  # faz o score de s com as posições aleatórias 
        i = 0
        while i <= n:
            seq_idx = randint(0, len(self.seqs) - 1)
            igno_seq = self.seqs.pop(seq_idx)
            s.pop(seq_idx)  
            motif = self.createMotifFromIndexes(s) 
            motif.createPWM_pseudo()  # passa a usar a pseudo pwm para depois fazer as probabilidades
            probs = motif.probAllPositions(igno_seq) 
            new_ind = self.roulette(probs)  
            self.seqs.insert(seq_idx, igno_seq) 
            s.insert(seq_idx, new_ind)  
            sc = self.pseudo_score(s)  
            if sc > bestscore: 
                bestscore = sc 
                vector = s  
            i += 1  
        return vector

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("c:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt","dna")
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
    print ("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print ("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("c:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("c:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print ("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    print()
    print("Gibbs sampling:")
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

def test5():
    mf = MotifFinding()
    mf.readFile("c:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt","dna")
    print("Heuristic stochastic with pseudo matrix:")
    sol = mf.heuristicStochastic_pseudo()
    print ("Solution: " , sol)
    print ("Score:" , mf.pseudo_score(sol))
    print ("Score mult:" , mf.pseudo_scoreMult(sol))
    print ("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    print()
    print("Gibbs sampling with pseudo matrix:")
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.pseudo_score(sol2))
    print ("Score mult:" , mf.pseudo_scoreMult(sol2))


#test1()
#test2()
#test3()
#test4()
#test5()
