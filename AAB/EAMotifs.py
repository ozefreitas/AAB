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
            multifit = self.motifs.scoreMult(sol)
            ind.setFitness(fit)
            ind.setMultiFitness(multifit)


class EAMotifsReal(EvolAlgorithm):  # Herda todas as funções de EvolAlgorithm

    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()  # inicialização do classe MotifFinding
        self.motifs.readFile(filename, "dna")  # automaticamente guarda as sequencias
        # print(self.motifs.seqs)
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)  # o tamanho dos individuos será um vetor do tamanho da pwm, ou seja, tamanho do motif (coluans) * tamanho do alfabeto (linhas)
        # print(indsize)  que depois será usado para construir a propria pwm com a função vec_to_pwm
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)


    def initPopul(self, indsize):  # override da função que está na classe EvolAlgorithm
        minvalue = 0
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize  # a upper bound será o indice máximo que o vetor de posições iniciais pode tomar, ou seja, o tamanho da sequencia menos o tamanho do motif
        self.popul = PopulReal(self.popsize, indsize, minvalue,
                              maxvalue, [])  # faltava a lower bound


    def vec_to_pwm(self, v):  # v é o vetor de um "individuo", pelo que para tansformar numa pwm:
        tam_alfabeto = len(self.motifs.alphabet)
        tam_motif = self.motifs.motifSize
        pwm = createMatZeros(tam_alfabeto, tam_motif)  # criar uma matriz de zeros de acordo com os paramtros que vem da classe MotifFinding
        for i in range(0, len(v), tam_alfabeto):  # correr o vetor com incrementos do tamanho do alfabeto
            col_idx = int(i / tam_alfabeto)  # o indice da coluna irá incrementar 1 a 1, int para poder ser um indice da matriz
            col = v[i : i + tam_alfabeto]  # dar splice aos elementos do vetor do tamanho do alfabeto
            soma = sum(col)  # soma dos elementos retirados do vetor
            for j in range(tam_alfabeto):  # j será a linha da pwm
                pwm[j][col_idx] = col[j] / soma  # nessa coluna e para cada linha do tamanho do alfabeto, adicionar o valor correspondente
        return pwm  # e tem-se a pwm


    def probabSeq (self, seq):  # calcula a probablidade de uma sequencia individual de acordo com a pwm
        res = 1.0
        for i in range(self.motifs.motifSize):  # itera sobre as posições da sequencia (motif)
            lin = self.motifs.alphabet.index(seq[i])  # de acordo com o alfabeto, vê qual a linha para depois usar na PWM
            res *= self.motifs.pwm[lin][i]  # cada valor é multiplicado pelo anterior
        return res  # é a probabilidade da subsequencia fornecida ter sido gerada pelo perfil da pwm


    def mostProbableSeq(self, seq):  # recebe uma sequencia inteira
        maximo = -1.0
        maxind = -1
        for k in range(len(seq) - self.motifs.motifSize):  # faz a iteração num range que so vai até ao comprimento da sequencia menos o comprimento do motif
            p = self.probabSeq(seq[k : k + self.motifs.motifSize])  # faz a probabilidade de cada subsquencia ocorrer
            if(p > maximo):  # devolve o maior valor de probabilidade
                maximo = p
                maxind = k
        return maxind


#    def evaluate(self, indivs):
#        for i in range(len(indivs)):  # para cada individuo
#            ind = indivs[i]
#            sol = ind.getGenes()
#            self.motifs.pwm = self.vec_to_pwm(sol)  # construir a pwm a partir do vetor, que é atribuida a self.motifs.pwm
#            s = []  # vetor de posições iniciais
#            for seq in self.motifs.seqs:  # para cada sequencia que está guardada
#                prob = self.mostProbableSeq(seq)  # calcular o indice onde começa a sequencia mais provavel de acordo com a pwm
#                s.append(prob)  # adicionar esse indice ao vetor de posições iniciais
#            fit = self.motifs.score(s)  # ver qual o score 
#            multifit = self.motifs.scoreMult(s, self.motifs.pwm)  # não queremos que a pwm seja atualizada ao fazer o score, por isso dá-mos como parametro a pwm que acabamos de criar atraves da função vec_to_pwm
#            ind.setFitness(fit)  # associar esse socre ao individuo
#            ind.setMultiFitness(multifit)


    def evaluate(self, indivs):
        for i in range(len(indivs)):  # para cada individuo
            ind = indivs[i]  # atribuir a ind cada individuo
            sol = ind.getGenes()  # retira os "genes" desse individuo, que neste caso sao os valores que vao compor a pwm
            self.motifs.pwm = self.vec_to_pwm(sol)  # construir a pwm a partir do vetor, que é atribuida a self.motifs.pwm, que na classe MotifFinding é self.pwm
            n = MyMotifs(pwm=self.motifs.pwm, alphabet=self.motifs.alphabet)  # inicializar a classe MyMotifs com a pwm criada e alfabeto antes para poder fazer as probabilidades 
            s = []  # vetor de posições iniciais
            for seq in self.motifs.seqs:  # para cada sequencia que está guardada
                prob = n.mostProbableSeq(seq)  # calcular o indice onde começa a sequencia mais provavel de acordo com a pwm que foi fornecida ao inicializar a classe, e que vem da função vec_to_pwm
                s.append(prob)  # adicionar esse indice ao vetor de posições iniciais
            fit = self.motifs.score(s)  # ver qual o score 
            ind.setFitness(fit)  # associar esse score ao individuo
            ### Calcular o score multiplicativo sem atualizar a pwm
            multifit = self.motifs.scoreMult(s, self.motifs.pwm)  # não queremos que a pwm seja atualizada ao fazer o score multiplo, por isso dá-mos como parametro a pwm que acabamos de criar atraves da função vec_to_pwm
            ind.setMultiFitness(multifit)  # e associamos o valor do score multiplicativo a esse individuo da mesma maneira que se fez para o score 


def test1():
    ea = EAMotifsInt(100, 1000, 50, "C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 200, 50, "C:/Users/Zé Freitas/Desktop/Mestrado/2ºSemestre/Algoritmos Avancados/Portfolio/AAB/AAB/exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()
    printMat(ea.motifs.pwm)

#test1()
test2()
