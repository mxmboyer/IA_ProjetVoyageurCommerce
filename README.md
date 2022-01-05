# IA : ProjetVoyageurCommerce

## Requirements
Pour pouvoir utiliser notre code, il vous faudra installer grâce à la commande pip les bibliothèques listées dans le fichier requirements.txt

Nous avions commencé à coder nos implémentations des algorithmes sur un notebook python au départ.
Il figure dans les fichiers que vous avez et permet de visualiser les graphes grâce à quelques commandes simples.
Pour une meilleure visualisation dans le notebook via jupyter notebook, il vous faudra installer toujours via la commande pip :
- algorithmx ;
- jupyter.

## Exécution
Dans le fichier main.py vous avez 2 fonctions à votre disposition pour générer un graphe.

Une première fonction generate_random_graph() vous permet de générer un graphe complet en précisant le nombre de sommets (par défaut 5) ainsi que le poids maximum que peut avoir une arrête (par défaut 10).

Une deuxième fonction generate_graph() vous montre comment générer un graphe à la main en ajoutant les arrêtes une par une sous le format :

(départ, arrivée, poids)

Enfin, une fois le graphe créé, vous n'avez plus qu'à choisir l'algorithme qui va trouver le meilleur circuit hamiltonien (A*, IDA* ou l'algorithme génétique).
Des exemples de code vous indiquant comment lancer ces algorithmes sont présents dans le fichier main.py
