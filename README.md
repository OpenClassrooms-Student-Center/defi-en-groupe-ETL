# Défi: construire une interface web de gestion de notes

Début 2021, les universités de Mufflins, Chichigneux, et Grapencourt ont décidé de fusionner: le GRUT (Groupement Régional des Universités Techniques) a été créé. Il délivre un diplôme commun à toutes les universités de la région.

L'université de Mufflins offre depuis toujours un programme complet de formation informatique, comprenant à la fois des cours d'informatique et des cours non techniques.

Les universités de Chichigneux et Grapencourt sont elles jumelées et offrent une formation plus orientée "Web". Les étudiants suivent les cours d'informatique à Grapencourt, et les autres cours à Chichigneux. 

Pour éviter que les validations de diplômes ne prennent trop de temps, les services universitaires ont décidé d'utiliser un système centralisé de gestion des notes et de suivi des étudiants. Certains processus sont déjà en place: chaque étudiant possède un identifiant unique.

Suite à la crise sanitaire du Covid-19, les règles suivantes de gestion des notes ont été mises en place:
* les notes vont de 0 à 100
* les absences sont notées avec la note `A`
* les absences aux contrôles et aux examens ne sont pas sanctionnées (l'étudiant ne reçoit pas 0)
* les notes sont organisées en deux groupes:
  * les notes correspondant aux cours techniques / informatique (coefficient 2)
  * les notes correspondant aux cours non techniques (coefficient 1)
  * la moyenne générale est donc: `(2 * moyenne_technique + moyenne_non_technique) / 3`
* dans chaque groupe de notes, s'il y a plus de trois notes valides (pas d'absence), on supprime la plus basse
* pour obtenir le diplôme, les étudiants doivent avoir une moyenne générale supérieure ou égale à 50

En tant qu'étudiants du GRUT, votre projet de fin d'études est de concevoir une plateforme ETL (Extract Transform Load) qui permettra aux jurys de valider les notes et les diplômes des étudiants.

Un groupe d'étudiants a déjà réalisé l'application web permettant de visualiser les données. Ils ont également commencé à implémenter l'étape de transformation, mais ils ont reçu leur diplôme et ont déjà été embauchés dans l'industrie! Votre mission est de livrer la plateforme complète et fonctionnelle.

### Extraction des données (EXTRACT)

L'extraction des données se fait à partir des fichiers fournis dans le répertoire `data`. L'objectif de cette étape est de préparer les données pour qu'elles puissent être transformées à l'étape suivante.

Les fichiers suivants sont disponibles:

| Fichier           | Commentaire                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `mufflins.json`   | Fichier de notes pour l'université de Mufflins (JSON)                        |
| `students.csv`    | Liste des étudiants pour les universités de Chichigneux et Grapencourt (CSV) |
| `chichigneux.csv` | Liste des notes non techniques pour l'université de Chichigneux              |
| `grapencourt.txt` | Notes d'informatique de l'université de Grapencourt                          |

* Les données disponibles dans le fichier `mufflins.json` peut être directement utilisé par l'étape suivante (Transform).
* Le fichier `students.csv` permet d'associer un nom à un identifiant étudiant.
* Le fichier `chichigneux.csv` contient les notes au format CSV.
* Le fichier `grapencourt.txt` contient les notes au format TXT, séparées par des espaces.

À l'issue de l'extraction des données, une structure similaire est disponible pour chaque étudiant:
```python
{
    "id": 123456,                   # Identifiant étudiant
    "name": "Timothee G",           # Nom de l'étudiant
    "sections": {
        "computing": {              # Notes d'informatique
            # Nom des matières
            "labels": ("Python 1", "Python 2", "Python 3", "Java", "Algorithms"),
            # Notes
            "grades": (100, 90, "A", 73, 60),
        },
        "other": {                  # Autres notes
            "labels": ("English", "Economy", "Communication")
            "grades": (53, 61, "A"),
        }
    }
}
```

### Transformation des données (Transform)

Le but de cette étape est de transformer les données obtenues pour les enrichir.

Les opérations suivantes vont être effectuées sur les données:
* suppression éventuelle de la note la plus basse (la note est remplacée par `None`): `remove_lowest`
* les absences (notées `A`) sont remplacées par `None`: `make_absent_none`
* la moyenne de chaque section est calculée via la fonction `average`
* la moyenne générale de chaque section est calculée dans la fonction `gpa`

> À vous de jouer! Implémentez ces fonctions.

A l'issue de cette étape, les données précédentes sont transformées de la manière suivante:
```python
{
    "id": 123456,
    "name": "Timothee G",
    "sections": {
        "computing": {
            "labels": ("Python 1", "Python 2", "Python 3", "Java", "Algorithms"),
            "grades": (100, 90, "A", 73, 60),
            # La note la plus basse est supprimée, l'absence est remplacée par None
            "final_grades": (100, 90, None, 73, None),
            # La moyenne est 100+90+80/3 (les None sont ignorés dans le calcul)
            # La moyenne est arrondie à deux chiffres après la virgule
            "average": 80.75,
        },
        "other": {
            "labels": ("English", "Economy", "Communication")
            "grades": (53, 61, "A"),
            # L'absence est transformée en None, mais la note la plus basse n'est pas supprimée
            # Il y a moins de 3 notes valides dans le groupe
            "final_grades": (54, 61, None),
            "average": 57.50,
        }
    },
    # La moyenne générale est également calculée
    # Les notes d'informatique ont coefficient 2: (80.75 * 2 + 57.50)/3
    "average": 73.00,
    # L'étudiant a obtenu plus de la moyenne: il est diplômé
    "graduated": True,
}
```

### Chargement et visualisation des données (Load)

Cette interface est construite avec Flask. L'objectif de cette interface est simplement de charger des données correctement formatées, et de les afficher dans une interface web. Les données doivent avoir été au préalable Extraites, et Transformées.

> Pas de panique, il n'est pas nécessaire de connaître Flask pour faire fonctionner l'interface web!

* Pour charger les données, il faut appeler la fonction `load` du module `load`. Cette fonction reçoit une liste de dictionnaires (voir étape précédente).
* Pour lancer le service, il suffit d'appeler la fonction `run_web_service` du module `load`. Cette fonction démarre le serveur Web automatiquement.

### Installation des dépendances

Le programme se lance après installation des dépendances (idéalement dans un environnement virtuel).
En utilisant le module `venv` de Python:
* `py -m venv venv` sous Windows
* `python3 -m venv venv` sous macOS / Linux

L'environnement virtuel s'active:
* `.\venv\Scripts\activate.bat` sous Windows (ligne de commande)
* `.\venv\Scripts\activate.ps1` sous Windows (PowerShell)
* `./venv/bin/activate` (macOS / Linux)

Lorsque l'environnement virtuel est activé, l'installation des dépendances se fait via `pip install -r requirements.txt`.

Le processus ETL complet se lance via la commande `python run.py` (ou `python -m etl`).

L'interface de visualisation est disponible par défaut en local sur l'ordinateur: [http://localhost:5000/](http://localhost:5000/).