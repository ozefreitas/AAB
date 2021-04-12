from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt(EvolAlgorithm):

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)  # numero de sequencias a analisar, que será o numero de individuos
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)


    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])


    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


class EAMotifsReal(EvolAlgorithm):

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)


    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize,
                              maxvalue, [])


    def vec_to_pwm(self, v):  # v é o vetor de um "individuo", pelo que para tansformar numa pwm
        tam_alfabeto = len(self.motifs.alphabet)
        tam_motif = self.motifs.motifSize
        pwm = createMatZeros(tam_alfabeto, tam_motif)
        for i in range(0, len(v), tam_alfabeto):
            col_idx = i / tam_alfabeto
            col = v[i : i + tam_alfabeto]
            soma = sum(col)
            for j in range(tam_alfabeto):
                pwm[j][col_idx] = col[j] / soma
        return pwm


    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            self.motifs.pwm = self.vec_to_pwm(sol)
            s = []
            for seq in self.motifs.seqs:
                prob = self.motifs.mostProbableSeq(seq)
                s.append(prob)
            ### Usar score multiplicativo sem atualizar a pwm
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


def test1():
    ea = EAMotifsInt(100, 1000, 50, "C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


test1()
#test2()
