from random import randint, random, uniform, shuffle


class Indiv:

    def __init__(self, size, genes=[], lb=0, ub=1):  # primeira abordagem, so vamos usar 0 e 1's, por isso lb = 0 e up = 1 por default
        self.lb = lb
        self.ub = ub  # intervalo de valores que cada gene pode ter
        self.genes = genes  # caracteristicas do indivduo, representação da solução
        self.fitness = None  # guarda os valores de aptidão
        if not self.genes:
            self.initRandom(size)

    # comparadores.
    # Permitem usar sorted, max, min

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size):  # gera individuos de forma aleatória
        self.genes = []  # não ha qualquer "gene" (neste caso nem 1's nem 0's)
        for _ in range(size):  # de acordo com o tamanho da população parametrizado
            self.genes.append(randint(self.lb, self.ub))  # gera-se valores de individuos de acordo com os limites

    def mutation(self):
        s = len(self.genes)  # tamanho da população
        pos = randint(0, s-1)  # variavel que toma um valor aleatorio no range do numero de genes em self.genes
        if self.genes[pos] == 0:  # se o gene que corresponde ao indice da posição que calhou for um 0
            self.genes[pos] = 1  # passamos esse 0 para 1
        else:  # caso já fosse 1
            self.genes[pos] = 0  # passamos a 0

    def crossover(self, indiv2):  # ja temos o primeiro individuo que vem e cima
        return self.one_pt_crossover(indiv2)  # e vamos querer criar o segundo, indiv2

    def one_pt_crossover(self, indiv2):
        offsp1 = []
        offsp2 = []  # dois vetores de descendentes 
        s = len(self.genes)
        pos = randint(0, s-1)  # gera uma posição aleatório onde se vai dar o crossover e que depende do numero de genes do primeiro individuo
        for i in range(pos):  # o iterador toma os valores de 0 até ao valor criado aleatoriamente 
            offsp1.append(self.genes[i])  # adiciona ao descenente1 todos os genes que estão antes da posição que foi selecionada aleatoriamente
            offsp2.append(indiv2.genes[i])  # o mesmo para o descendente2
        for i in range(pos, s):  # para as posições seguintes
            offsp2.append(self.genes[i])  # os genes que estavam no progenitor1 passam para o 2 
            offsp1.append(indiv2.genes[i])  # e vice versa
        res1 = self.__class__(s, offsp1, self.lb, self.ub)
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt (Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1):  # neste caso já podemos alterar os valores de lower e upper bound para os que quisermos
        self.lb = lb
        self.ub = ub  # intervalo de valores que cada gene pode ter
        self.genes = genes  # caracteristicas do indivduo, representação da solução
        self.fitness = None  # guarda os valores de aptidão
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size):  # gera individuos de forma aleatória
        self.genes = []  # não ha qualquer "gene" (nenhum valor entre lb e ub)
        for _ in range(size):  # de acordo com o tamanho da população parametrizado
            self.genes.append(randint(0, self.ub))  # gera-se valores de individuos de acordo com os limites

    def mutation(self):
        s = len(self.genes)  # numero de genes do individuo
        pos = randint(0, s-1)  # indice no qual vai ser mudado 
        self.genes[pos] = randint(0, self.ub)  # gera um novo número aleatório para ir para essa posição


class IndivReal(Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1):  # neste caso já podemos alterar os valores de lower e upper bound para os que quisermos
        # self.lb = lb  ## faltava guadar as lb e ub para usar nas duas funções seguintes ???????
        # self.ub = ub
        Indiv.__init__(self, size, genes, lb, ub)


    def initRandom(self, size):  # override
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub))
        

    def mutation(self):  # override
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = uniform(self.lb, self.ub)
