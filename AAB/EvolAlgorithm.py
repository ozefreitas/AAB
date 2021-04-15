from Popul import Popul, PopulInt, PopulReal


class EvolAlgorithm:  

    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize


    def initPopul(self, indsize):  # responsável pela geração da população incial
        self.popul = PopulInt(self.popsize, indsize, 50)


    def evaluate(self, indivs):
        for i in range(len(indivs)):  # para cada individuo da populacao
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():  # para o tamanho do individuo
                if x == 1:  # cada gene que seja igual a 1
                    fit += 1.0  # vai aumentar 1 valor ao seu score de aptidão
            ind.setFitness(fit)  # e atribui esse score ao individuo
        return None


    def iteration(self):
        parents = self.popul.selection(self.noffspring)  # parte da população que queremos manter
        offspring = self.popul.recombination(parents, self.noffspring)  # geramos novas soluções
        self.evaluate(offspring)  # avaliamos as novas soluções 
        self.popul.reinsertion(offspring)  # integramos tudo na mesma população

    # ciclo principal do algoritmo evolucionário 

    def run(self):
        self.initPopul(self.indsize)  # cria nova população
        self.evaluate(self.popul.indivs)  # avalia os individuos dessa população
        self.bestsol = self.popul.bestSolution()
        # inicio do processo iterativo
        for i in range(self.numits+1):
            self.iteration()
            bs = self.popul.bestSolution()  # para ver se ha melhoramento do score de aptidão da população
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)


    def printBestSolution(self):
        print("Best solution:", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())
        print("Best fitness:", self.bestsol.getMiltiFitness())


def test():
    ea = EvolAlgorithm(100, 1000, 80, 50)
    ea.run()
    ea.printBestSolution()


if __name__ == "__main__":
    test()
