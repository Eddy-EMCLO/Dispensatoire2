# persistance.py - À COMPLÉTER (épreuve flotte)
#
# Persistance de la flotte, à transposer de catalogue_persistance (S18).
# Les FONCTIONS de ce module orchestrent fichiers et format (JSON) ; ce
# sont les CLASSES (to_dict / from_dict) qui connaissent leurs attributs.
# Le module vehicule, lui, n'importe pas json.
# Aucune docstring demandée ; test_persistance.py fixe le comportement.
# Complétez les corps « ... ».

import json

from vehicule import Vehicule, VoitureElectrique, Camion


# Registre de reconstruction : associe le discriminateur « type » à la
# classe. Le compléter est ce qui rend la reconstruction polymorphe
# possible. Comme la fabrique du catalogue de livres, il illustre le
# principe ouvert/fermé : ajouter un type = une ligne ici, sans toucher
# à la fabrique (vs une cascade if/elif à éditer en son cœur).
_FABRIQUES = { 
    "Vehicule": Vehicule,
    "VoitureElectrique": VoitureElectrique,
    "Camion": Camion,
}


def vehicule_depuis_dict(donnees):
    # Lire le champ « type », choisir la classe dans le registre, puis
    # déléguer à sa classmethod from_dict. Type absent ou inconnu -> erreur.
    # Même rôle que livre_depuis_dict.
    type_vehicule = donnees.get("type")
    if type_vehicule not in _FABRIQUES:
        raise ValueError(f"Type de véhicule inconnu : {type_vehicule}")
    classe = _FABRIQUES[type_vehicule]
    return classe.from_dict(donnees)


# --- Persistance JSON ---

def sauvegarder_flotte_json(vehicules, chemin):
    # Transformer chaque véhicule par SON to_dict (dispatch polymorphe,
    # sans test de type), puis écrire la liste de dicts en JSON.
    donnees = [v.to_dict() for v in vehicules]
    with open(chemin, "w") as f:
        json.dump(donnees , f)


def charger_flotte_json(chemin):
    # Relire le JSON et confier chaque dict à la fabrique, qui restitue le
    # type exact d'origine. Un parc mélangé revient à l'identique.
    with open(chemin, "r") as f:
        donnees = json.load(f)
    return [vehicule_depuis_dict(d) for d in donnees]
