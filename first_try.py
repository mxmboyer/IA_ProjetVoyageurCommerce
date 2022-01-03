import networkx as nx
import sys

class AStar:
    # constructeur
    def __init__(self, G):
        self.graphe = G
    
    # retourne la liste des actions possibles = les ville dans frontier
    def actions(self):
        return list(self.frontier.keys())
    
    # retourne le coût f(n) associé à une action avec f(n) = total distance + nouvelle distance + heuristique
    def result(self, action):
        for l in list(self.graphe.edges(self.node, data=True)):
            if (l[1] == action):
                self.frontier[action] = self.g_n + l[2]['weight'] + self.result_mst(action)
                break
    
    # retourne le résultat de l'heuristique pour 1 action
    # le minimum spanning tree est créé à la main en prenant toutes les villes sauf celles explorées (dont le départ)
    # et sans celle de où va l'action considérée
    def result_mst(self, action):
        mst_graph = nx.Graph()
        mst_graph.add_node(action)
        unexplored = list(self.frontier.keys())
        for j in range(len(self.frontier) - 1):
            mini = sys.maxsize
            i = -1
            for k in list(mst_graph.nodes()):
                for l in list(self.graphe.edges(k, data=True)):
                    if(l[2]["weight"] < mini and l[0] == k and l[1] not in list(mst_graph.nodes()) and l[1] in unexplored):
                        mini = l[2]["weight"]
                        i = l[1]
                    elif(l[2]["weight"] < mini and l[1] == k and l[0] not in list(mst_graph.nodes()) and l[0] in unexplored):
                        mini = l[2]["weight"]
                        i = l[0]
            unexplored.remove(i)
            mst_graph.add_weighted_edges_from([(0, i, mini)])
        total_weight = 0
        for e in list(mst_graph.edges(data=True)):
            total_weight += e[2]["weight"]
        return total_weight
    
    # fonction qui initialise la frontier au début de solve()
    def initiate_frontier(self):
        self.frontier = {list(self.graphe.edges(self.node))[i][1]: list(self.graphe.edges(self.node, data=True))[i][2]['weight'] for i in range(self.graphe.number_of_nodes()-1)}
    
    # retourne le meilleur élément de la frontier tout en le retirant de frontier et met à jour la distance total g_n
    def my_pop(self):
        mini = sys.maxsize
        i = -1
        for f in self.frontier.items():
            if f[1] < mini:
                mini = f[1]
                i = f[0]
        self.frontier.pop(i)
        for j in range(len(self.graphe.edges(self.node))):
            if(list(self.graphe.edges(self.node, data=True))[j][1] == i):
                self.g_n += list(self.graphe.edges(0, data=True))[j][2]['weight']
                break
        return i
    
    # fonction principale qui gère l'algorithme
    def solve(self):
        self.node = list(self.graphe.nodes)[0]
        self.initiate_frontier()
        self.explored = [self.node]
        self.g_n = 0
        for action in self.actions():
            self.result(action)
        while(len(self.frontier) > 0):
            self.node = self.my_pop()
            self.explored.append(self.node)
            for action in self.actions():
                self.result(action)
        self.explored.append(self.explored[0])
        self.g_n = nx.path_weight(self.graphe, self.explored, weight="weight")
        print("Le meilleur chemin avec cet algorithme est " + str(self.explored) + " ce chemin a une distance totale de " + str(self.g_n))
