import numpy as np
import random 

class Genetic:

    #constructeur de la classe
    def __init__(self, G):
        self.graphe = G.copy()
        
    #definir le score de chaque chemin
    def fitness(self, chemin):
        score = 0
        for i in range(len(chemin)-1):
            score += self.graphe[chemin[i]][chemin[i+1]]['weight']
        score += self.graphe[chemin[len(chemin)-1]][chemin[0]]['weight']
        return score 

    #choix des reproducteurs : on prend ceux qui ont le meilleur score
    #on prend 1/3 de la population pour la reproduction
    def selection(self, pop):
        selec_pop = []
        scores = []
        for i in range(len(pop)):
            data = []
            data.append(i)
            data.append(self.fitness(pop[i]))
            scores.append(data)
        scores_tries = sorted(scores, key=lambda item:(item [1]))
        for i in range(round(len(pop)/3)):
            selec_pop.append(pop[scores_tries[i][0]])
        return selec_pop

    #on prend au hasard un individu dans les sélectionnés pour être reproducteurs
    def random_selec(self, pop):
        i = random.randint(0, len(pop)-1)
        return pop[i]

    #on prend les caracteristiques du pere jusqu'au point de croisement ici (sommet/3)
    def reproduce(self, pere, mere):
        point_crois = round(len(self.graphe.nodes)/3)
        child = []
        sommets = np.arange(len(self.graphe.nodes)) 
        for i in range(point_crois):
            child.append(pere[i])
            sommets = np.setdiff1d(sommets, pere[i])
        for i in range(point_crois, len(mere)):
            if(mere[i] in sommets):
                child.append(mere[i])
                sommets = np.setdiff1d(sommets, mere[i])
            else :
                s = sommets[random.randint(0, len(sommets)-1)]
                child.append(s)
                sommets = np.setdiff1d(sommets, s)
        return child

    #on applique la mutation on inversant 2 sommets voisins
    def mutate(self, individu):
        i = random.randint(0, len(individu)-1)
        temp = individu[i]
        if(i+1==len(individu)):
            individu[i] = individu[0]
            individu[0] = temp
        else: 
            individu[i] = individu[i+1]
            individu[i+1] = temp
        return individu 

    def solve(self):
        #size of the population : nbr arretes
        size_pop = len(self.graphe.edges)
        population = []

        #generation de la population initiale  
        for i in range(size_pop):
            sommets = np.arange(len(self.graphe.nodes)) 
            np.random.shuffle(sommets)
            chemin = sommets.tolist()
            population.append(chemin)

        #evolution de la population
        iterations = 0
        while(iterations < 10):
            new_population = []
            selec_pop = self.selection(population)
            for i in range(size_pop):
                pere = self.random_selec(selec_pop)
                mere = self.random_selec(selec_pop)
                child = self.reproduce(pere, mere)
                proba_mutation = random.randint(1, 100)
                if(proba_mutation<10):
                    child = self.mutate(child)
                new_population.append(child)
            population = new_population
            iterations += 1


        #on prend le meilleur individu
        meilleure_pop = self.selection(population)
        #on sélectionne celui qui est en haut du classement
        print("Le meilleur chemin avec l'algorithme génétique est " + str(meilleure_pop[0]) + ". Ce chemin a une distance totale de " + str(self.fitness(meilleure_pop[0])))
