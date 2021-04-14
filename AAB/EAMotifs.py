from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding_comexe import MotifFinding
from MyMotifs_comexe import MyMotifs


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
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize  # a upper bound será o indice máximo que o vetor de posições iniciais pode tomar, ou seja, o tamanho da sequencia menos o tamanho do motif
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
        # print(self.motifs.seqs)
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)  # o tamanho dos individuos será um vetor do tamanho da pwm, ou seja, tamanho do motif (coluans) * tamanho do alfabeto (linhas)
        # print(indsize)  que depois será usado para construir a propria pwm com a função vec_to_pwm
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)


    def initPopul(self, indsize):  # override da funçãoq que está na classe EvolAlgorithm
        minvalue = 0
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulReal(self.popsize, indsize, minvalue,
                              maxvalue, [])  # faltava a lower bound


    def vec_to_pwm(self, v):  # v é o vetor de um "individuo", pelo que para tansformar numa pwm 
        tam_alfabeto = len(self.motifs.alphabet)
        tam_motif = self.motifs.motifSize
        pwm = createMatZeros(tam_alfabeto, tam_motif)  # criar uma matriz de zeros de acordo com os paramtros que vem da classe MotifFinding
        for i in range(0, len(v), tam_alfabeto):  # correr o vetor com incrementos do tamanho do alfabeto
            col_idx = i / tam_alfabeto  # o indice da coluna irá incrementar 1 a 1
            col = v[i : i + tam_alfabeto]  # dar splice aos elementos do vetor do tamanho do alfabeto
            soma = sum(col)  # soma dos elementos retirados do vetor
            for j in range(tam_alfabeto):  # j será a linha da pwm
                pwm[j][col_idx] = col[j] / soma  # nessa coluna e para cada linha do tamanho do alfabeto, adicionar o valor correspondente
        return pwm  # e tem-se a pwm


    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            self.motifs.pwm = self.vec_to_pwm(sol)
            s = []
            for seq in self.motifs.seqs:
                prob = self.motifs.mostProbableSeq(seq)  # ????? esta função pertence a MyMotifs, a qual nunca é inicializada ????
                s.append(prob)
            fit = self.motifs.score(s)
            ind.setFitness(fit)

    ### Usar score multiplicativo sem atualizar a pwm

    def evaluate_mult(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            self.motifs.pwm = self.vec_to_pwm(sol)
            s = []
            for seq in self.motifs.seqs:
                prob = self.motifs.mostProbableSeq(seq)
                s.append(prob)
            fit = self.motifs.scoreMult(s)
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
