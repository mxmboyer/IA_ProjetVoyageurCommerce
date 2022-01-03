import networkx as nx
import matplotlib.pyplot as plt
from random import randint

from first_try import *
from a_star import *
from ida_star import *
from genetic_algorithm import *

# Fonction pour générer un graphe complet aléatoire avec la possibilité de spécifier un nombre de sommets ainsi
# qu'une borne supérieur pour le poids aléatoire de chaque arrête
def generate_random_graph(nbr_sommets=5, max_poids=10):
    graphe = nx.complete_graph(nbr_sommets)
    nx.set_edge_attributes(graphe, {e: {'weight': randint(1, max_poids)} for e in graphe.edges})
    return graphe

# Fonction avec un exemple de graphe généré à la main
# Il est possible de changer les valeurs des poids et de rajouter d'autres arrêtes en suivant la même syntaxe
# Ajouter une arrête entre le sommet 0 et le sommet 1 rajoutera les sommets au graphe s'ils n'existent pas encore
# dans le graphe
def generate_graph():
    graphe = nx.Graph()
    graphe.add_weighted_edges_from([(0, 1, 2), #(départ, arrivée, poids)
                                    (0, 2, 4),
                                    (1, 2, 8),
                                    (0, 3, 9),
                                    (1, 3, 3),
                                    (2, 3, 1),
                                    (0, 4, 4),
                                    (1, 4, 3),
                                    (2, 4, 10),
                                    (3, 4, 6)])
    return graphe

#visualisation
graphe = generate_graph()
nx.draw(graphe, with_labels=True, node_size=1000)
plt.show()

for t in graphe.edges(data=True):
    print(t)

a_star = AStar(graphe)
a_star.solve()

a_star2 = AStar2(graphe)
a_star2.solve()

ida_star = IDA_star(graphe)
ida_star.solve()

genetic_algorithm = Genetic(graphe)
genetic_algorithm.solve()
