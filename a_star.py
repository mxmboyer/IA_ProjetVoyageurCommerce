import networkx as nx
import sys

class Etat:
    # constructeur de la classe Etat
    # pere : un Etat
    # etat : un entier pour le numéro du sommet correspondant à l'Etat
    # distance : somme des distances depuis le départ jusqu'à cette ville
    def __init__(self, pere, etat, distance):
        self.pere = pere
        self.etat = etat
        self.distance = distance #distance parcourue du début jusqu'à cet état -> g(n)
    
    # return True si toutes les villes ont été parcourues pour cet Etat en remontant sur tous les pères
    def is_solved(self, graphe):
        path = self.liste_peres()
        if(set(path) == set(list(graphe.nodes()))):
            return True
        return False
    
    # retourne la listes de toutes les villes précédents cet Etat
    def liste_peres(self):
        e = self
        path = [e.etat]
        while(e.pere != -1):
            path.append(e.pere.etat)
            e = e.pere
        return path

class AStar2:
    # constructeur de la classe AStar2, prend un graphe G d networkx en paramètre
    def __init__(self, G):
        self.graphe = G.copy()
        #chemin + court le même peu importe le sommet de départ car boucle
        self.racine = Etat(-1, list(self.graphe.nodes)[0], 0)
        # frontier = dict(n, f(n))
        self.frontier = {self.racine: self.f(self.racine)}
    
    # retourne le résultat de f(n) = g(n) + h(n)
    def f(self, n):
        return self.g(n) + self.heuristique(n)
    
    # retourne le résultat de g(n) soit la somme des distances précédentes d'un état n depuis le départ
    def g(self, n):
        return n.distance
    
    # retourne la valeur de l'heuristique h(n) pour un état n
    def heuristique(self, n):
        G = self.graphe.copy()
        path = n.liste_peres()
        path.remove(0)
        if(n.etat != 0):
            path.remove(n.etat)
        for node in path:
            G.remove_node(node)
        mst_graph = nx.minimum_spanning_tree(G, weight='weight', algorithm='prim')
        distance = 0
        for edge in mst_graph.edges(data=True):
            distance += edge[2]["weight"]
        return distance
    
    # retourne le meilleur élément de frontier tout en le retirant
    def my_pop(self):
        mini = sys.maxsize
        i = -1
        for f in self.frontier.items():
            if f[1] < mini:
                mini = f[1]
                i = f[0]
        self.frontier.pop(i)
        return i
    
    # retourne une liste d'actions possibles et leurs valeurs f(n) associées étant donné l'état actuel
    # contenu dans self.racine
    def actions(self):
        actions = {}
        for edge in self.graphe.edges(self.racine.etat, data=True):
            if(edge[1] not in self.racine.liste_peres()):
                action = Etat(self.racine, edge[1], self.racine.distance + edge[2]["weight"])
                actions.update({action: self.f(action)})
        return actions
    
    # la fonction result met à jour un état de la frontier si on a trouvé un état identique
    # avec un meilleur f(n)
    def result(self, action, f_n):
        self.frontier.update({action: f_n})
    
    # fonction principale de la classe qui exécute l'algorithme A* 
    def solve(self):
        #tant qu'il y a des villes dans frontier c'est qu'on a pas parcouru toutes les villes
        while(not self.racine.is_solved(self.graphe) and len(self.frontier) > 0):
            self.racine = self.my_pop()
            for action, f_n in self.actions().items():
                etat_in_front = []
                for etat_f in list(self.frontier.keys()): #on récupère les états des actions
                    etat_in_front.append(etat_f.etat)
                if(action.etat not in etat_in_front): #si pas dans frontier, on rajoute
                    self.result(action, f_n)
                elif(action.etat in etat_in_front): #màj dans frontier si action mieux que celle dans frontier
                    for key in self.frontier.keys():
                        if(key.etat == action.etat):
                            frontier_fn = self.frontier[key]
                            key_f = key
                            break
                    if(frontier_fn > f_n):
                        self.frontier.pop(key_f)
                        self.result(action, f_n)
        if(self.racine.is_solved(self.graphe)):
            e = self.racine
            path = self.racine.liste_peres()
            path.insert(0, 0) #on rajoute le sommet de départ qui est 0 dans le trajet
            distance = nx.path_weight(self.graphe, path, weight="weight") #pour récupérer la bonne distance
            print("Le meilleur chemin avec l'algorithme A* est " + str(path) + " ce chemin a une distance totale de " + str(distance))
