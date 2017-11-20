# Avancements

## 1.Objectif
* Entree: OK
* Sortie: OK

## 2.Description générale
* Vidéos de Stanford
* *Remarque :* Nous n'avons pas eu de code Python pour commencer.

### 2.1 Collection de pages web
Nous n'avons jamais lancé sur 1.5 millions de docs pour le moment.
Crawler possiblement réalisable (pas encore fait).

### 2.2 Contraintes matérielles
* Moins de **1 Go** de RAM : nous avons besoin de mesurer correctement
* Moins de **60% de la taille collection** pour l'index : nous avons besoin de mesurer correctement
* Moins de **10sec** pour la requête : jamais essayée pour 1.5 million de docs, pour 20 000 on est dans un temps de 0.1sec, qui semble augmenter moins que lineairement avec la taille du corpus... donc à suivre.

## 3. Détails sur le rendu attendu
### 3.1 L’indexation
* Deux techniques possibles : avec ou sans racinisation (stemming)
* Suppression des mots vides effectuée
* Méthode tf*idf employée (diverses méthodes de calcul disponibles)

### 3.2 La recherche
* Modèle vectoriel implémenté
* Similarité cosinus implémentée, orientation du choix vers la mesure bm25
* On peut choisir ou non d'utiliser le stemming.

### 3.3 Evaluation
#### 3.3.1 Pertinence
* **AUCUNE** evaluation de la pertinence n'a été réalisée jusque ici
(méthode à suivre : evaluer la pertinence des 20 premiers documents renvoyés pour 10 requêtes données)

* Pour le rapport il faudra détailler "le choix des métriques" + "la manière de juger la pertinence" + "les limites de cette évaluation"

#### 3.3.2 Performances
Vous fournirez toutes les mesures objectives pertinentes de la performance de votre système. Devront figurer au minimum :

* Le temps de calcul consacré à l’indexation (pour chaque index), et la durée de réponse moyenne à une requête.
* Vous comparerez  ́egalement l’espace disque occupé par les différents index. Vous expliquerez les différences constatées.
* Enfin, vous estimerez la mémoire occupée lors de l’indexation et lors d’une requête.
 
**Idée:** Courbe montrant l’évolution de la consommation mémoire pour l’indexation, par exemple avec l’aide de l’outil jconsole **(besoin d'un équivalent sur python)**.

## 4. Suppléments
* Clustering (etude du corpus)
* Crawler
* positions dans le texte (à utiliser ?)
