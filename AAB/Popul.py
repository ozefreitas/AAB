# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import random


class Popul:  # conjunto de individuos

    def __init__(self, popsize, indsize, indivs=[]):  
        self.popsize = popsize  # numero de individuos dentro da população
        self.indsize = indsize  # tamanho desses individuos (numero de genes por exemplo)
        if indivs:  # podem ser logo fornecidos uma lista de individuos
            self.indivs = indivs  
        else:  # se não for, vai ser criado aleatoriamente
            self.initRandomPop()


    def getIndiv(self, index):  # vai buscar individuos por indice na lista
        return self.indivs[index]


    def initRandomPop(self):
        self.indivs = []  # so se vai fazer para quando nao houver individuos
        for _ in range(self.popsize):  # queremos criar um numero de individuos igual ao tamanho da população que foi fornecido aquando da inicialização da classe
            indiv_i = Indiv(self.indsize, [])  # por cada iteração, vai criar um objeto Indiv com o tamanho já estipulado no incio da classe Popul, 
            # sem atribuir o parametro genes, para dessa forma criar um individuo aleatorio na classe Indiv
            self.indivs.append(indiv_i)  # adiciona-se cada novo individuo a variável


    def getFitnesses(self, indivs=None):  # vai buscar os valores de aptidao para todos os individuos
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses


    def bestSolution(self): 
        return max(self.indivs)


    def bestFitness(self):  # devolve o melhor valor de aptidão 
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None):  # mecanismo de seleção para reprodução, onde n é o numero de individuos que vao ser selecionados
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))  # normaliza os scores de aptidão (fitness)
        for _ in range(n):
            sel = self.roulette(fitnesses)  # usa a roleta para seleccionar os individuos que vao gerar novas soluções, de acordo com o ser fitness 
            # (quanto maior, mais provável será que seja selecionado)
            fitnesses[sel] = 0.0  # o score de aptidão do individuo selecionada passa a ser 0
            res.append(sel)  # e adiciona o indice do individuo selecionado
        return res


    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1


    def linscaling(self, fitnesses):
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses:
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res


    def recombination(self, parents, noffspring):  # parents são os individuos que foram selecionados no processo de seleção
        offspring = []  # descendente
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]  # vai buscar os individuos que foram selecionados ao self.indivs que os guarda
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2)  # aplica o crossover nos 2, o que faz criar dois novos descendentes
            offsp1.mutation()
            offsp2.mutation()  # a cada descendente criado, aplica uma mutação
            offspring.append(offsp1)
            offspring.append(offsp2)  # e estes novos individuos vao ser adicionados a uma lista que os detem todos
            new_inds += 2  # por cada iteração vai aumentar 2, pq estão sempre aos pares
        return offspring


    def reinsertion(self, offspring):  # mecanismo que tem a ver com a selacao dos inividuos que vao constitui a população seguinte 
        tokeep = self.selection(self.popsize-len(offspring))  # com a roleta seleciona individuos da população anterior que vao ser mantidos
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep: # se esse i nao estiver na lista dos que sao para manter
                self.indivs[i] = offspring[ind_offsp]  # preenche com um novo individuo
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)


    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):  # Herda todas as funções de Popul

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]):
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)


    def initRandomPop(self):  # override
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivReal(self.indsize, [], lb=self.lb, ub=self.ub)
            self.indivs.append(indiv_i)
