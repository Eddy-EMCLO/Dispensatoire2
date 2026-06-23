# vehicule.py - À COMPLÉTER (épreuve flotte)
#
# Hiérarchie Vehicule / VoitureElectrique / Camion, à transposer de la
# hiérarchie Livre / LivreNumerique / LivreAudio (S11-S18).
# Pour cette épreuve, aucune docstring n'est demandée : les indices «#»
# donnent le RÔLE (et parfois le cas analogue à transposer), et les
# tests (test_vehicule.py) fixent les valeurs et exceptions exactes.
# Complétez les corps « ... ».


class Vehicule:
    # ENTITE largement immuable. Identité métier : le numéro de châssis
    # (qui ne change jamais, contrairement à la plaque). Seule la
    # disponibilité évolue. Transposé de Livre (identité par ISBN).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):
        # Valider chaque caractéristique avant de la stocker :
        #   - marque, modèle : chaînes non vides ;
        #   - châssis : utiliser la méthode de validation dédiée ;
        #   - nb_places, année : entiers, bornes exactes dans les tests.
        # Distinguer TypeError (mauvais type) et ValueError (mauvaise valeur).
        # À la création, le véhicule est disponible.
        if not isinstance(marque, str) or not marque.strip():
            raise TypeError("c'est une chaîne non vide")
        if not isinstance(modele, str) or not modele.strip():
            raise TypeError("c'est une chaîne non vide")
        if not self.chassis_valide(numero_chassis):
            raise ValueError("Le numéro de châssis n'est pas valide")
        if not isinstance(nb_places, int):
            raise TypeError("ca doit être un entier")
        if not isinstance(annee, int):
            raise TypeError("L'année doit être un entier")

        self._marque = marque
        self._modele = modele
        self._numero_chassis = numero_chassis
        self._nb_places = nb_places
        self._annee = annee
        self._disponible = True
    # --- Propriétés en lecture seule ---

    @property
    def marque(self):
        return self._marque

    @property
    def modele(self):
        return self._modele

    @property
    def numero_chassis(self):
        return self._numero_chassis
    @property
    def nb_places(self):
        return self._nb_places

    @property
    def annee(self):
        return self._annee

    @property
    def disponible(self):
        return self._disponible

    # --- Méthode statique ---

    @staticmethod
    def chassis_valide(chaine):
        # Vrai si la chaîne a exactement la bonne longueur et n'est faite
        # que de caractères alphanumériques. Longueur et nature exactes :
        # déductibles des tests. Une entrée non-str renvoie False.
        if not isinstance(chaine, str) or len(chaine) != 17 :
            return False    
        return chaine.isalnum()

    # --- Constructeur alternatif ---

    @classmethod
    def depuis_csv(cls, ligne):
        # Découper la ligne, vérifier le nombre de champs, construire via
        # cls(...). Même rôle que Livre.depuis_chaine_csv : utiliser cls
        # (et non Vehicule) est ce qui donnera le TYPE EXACT dans les
        # sous-classes.
        champs = ligne.split(",")
        if len(champs) != 5:
            raise ValueError("Le nombre de champs different de 5")
        marque, modele, numero_chassis, nb_places_str, annee_str = champs
        return cls(marque, modele, numero_chassis, int(nb_places_str), int(annee_str))

    # --- Sérialisation JSON ---

    def to_dict(self):
        # Produire un dict marqué d'un champ « type » (le discriminateur
        # qui guidera la reconstruction). Clés attendues : voir les tests.
        return {
            "type": "vehicule", 
            "marque" : self.marque,
            "modele": self.modele,
            "numero_chassis": self.numero_chassis,
            "nb_places": self.nb_places,
            "annee": self.annee,
            "disponible": self.disponible,
        }

    @classmethod
    def from_dict(cls, donnees):
        # Pendant de to_dict : reconstruire via cls(...), puis restaurer la
        # disponibilité par l'API publique (jamais en écrivant l'attribut
        # privé). Même logique que Livre.from_dict.
        vehicule = cls(
                       donnees["marque"], 
                       donnees["modele"], 
                       donnees["numero_chassis"],
                       donnees["nb_places"],
                       donnees["annee"],
                       )
        vehicule._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    @staticmethod
    def _restaurer_disponibilite(vehicule, donnees):
        # Si l'objet était loué, le replacer dans cet état via la méthode
        # métier. Factorisé : toutes les sous-classes restaurent pareil.
        if not donnees.get("disponible", True):
            vehicule.louer()

    # --- Méthodes métier ---

    def louer(self):
        # Bascule vers « loué » ; refuser si déjà loué.
        if not self._disponible:
            raise ValueError("vehicule deja loué")
        self._disponible = False

    def restituer(self):
        # Bascule vers « disponible » ; refuser si déjà disponible.
        if self._disponible:
            raise ValueError("vehicule disponible")
        self._disponible = True
    def fiche_resume(self):
        # Description de la capacité d'un véhicule générique. Format exact :
        # voir les tests. (Transposé de Livre.taille_estimee.)
        return f"{self.nb_places} places"

    # --- Représentations ---

    def __str__(self):
        etat = "disponible" if self.disponible else "loué"
        return f"{self.marque} modele :{self.modele},chassis : {self.numero_chassis} de {self.annee},{etat}"

    def __repr__(self):
        return f"Vehicule(marque='{self.marque}', modele='{self.modele}', numero_chassis='{self.numero_chassis}', nb_places={self.nb_places},annee={self.annee})"

    # --- Identité (entité) ---

    def __eq__(self, autre):
        # Vehicule est une ENTITE : égalité par numéro de châssis (comme
        # Livre par ISBN). NotImplemented si « autre » n'est pas un Vehicule.
        if not isinstance(autre, Vehicule):
            return NotImplemented
        return self.numero_chassis == autre.numero_chassis

    def __hash__(self):
        # Cohérent avec __eq__ : fondé sur le châssis.
        return hash(self.numero_chassis)


class VoitureElectrique(Vehicule):
    # Enrichit Vehicule d'une autonomie. Transposé de LivreNumerique.

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 autonomie_km):
        # Déléguer la validation héritée au parent, puis valider l'attribut
        # propre (autonomie : entier strictement positif).
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        if not isinstance(autonomie_km, int) or autonomie_km <= 0:
            raise ValueError("faut un entier strictement positif")
        self._autonomie_km = autonomie_km

    @property
    def autonomie_km(self):
        return self._autonomie_km

    @classmethod
    def depuis_csv(cls, ligne):
        # Comme Vehicule.depuis_csv, mais un champ de plus (l'autonomie).
        champs = ligne.split(",")
        if len(champs) != 6:    
            raise ValueError("le nombre de champs different de 6")
        marque, modele, numero_chassis, nb_places_str, annee_str, autonomie_str = champs
        return cls(marque, modele, numero_chassis, int(nb_places_str), int(annee_str), int(autonomie_str))

    def to_dict(self):
        # ENRICHIR le dictionnaire hérité du parent (ne pas le réécrire) :
        # corriger « type » et ajouter l'attribut propre. (Geste de
        # LivreNumerique.to_dict.)
        donnees = super().to_dict()
        donnees["type"] = "voiture_electrique"
        donnees["autonomie_km"] = self.autonomie_km
        return donnees
        
    @classmethod
    def from_dict(cls, donnees):
        ...

    def fiche_resume(self):
        # On REPREND la fiche de base et on la complète : la capacité reste
        # un préfixe (ENRICHISSEMENT). Format exact : voir les tests.
        ...

    def __str__(self):
        ...

    def __repr__(self):
        ...


class Camion(Vehicule):
    # La mesure pertinente est la charge utile, pas le nombre de places.
    # Transposé de LivreAudio (durée d'écoute plutôt que pages).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 charge_utile_t):
        # Déléguer au parent, puis valider l'attribut propre (charge :
        # nombre strictement positif, stocké en float).
        ...

    @property
    def charge_utile_t(self):
        ...

    @classmethod
    def depuis_csv(cls, ligne):
        ...

    def to_dict(self):
        ...

    @classmethod
    def from_dict(cls, donnees):
        ...

    def fiche_resume(self):
        # Ici la mesure pertinente n'est PAS le nombre de places : on ne
        # réutilise donc PAS la fiche de base (REMPLACEMENT). Format exact :
        # voir les tests.
        ...

    def __str__(self):
        ...

    def __repr__(self):
        ...
