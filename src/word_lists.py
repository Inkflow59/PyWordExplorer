"""
Listes de mots pour le jeu de mots mêlés.
"""

# Liste de mots français pour le jeu
FRENCH_WORDS = [
    # Animaux
    "CHAT", "CHIEN", "LION", "TIGRE", "OURS", "LOUP", "RENARD", "LAPIN",
    "SOURIS", "ELEPHANT", "GIRAFE", "ZEBRE", "SINGE", "PANDA", "KOALA",
    "DAUPHIN", "BALEINE", "REQUIN", "TORTUE", "CROCODILE", "SERPENT",
    "AIGLE", "HIBOU", "CORBEAU", "PIGEON", "CANARD", "CYGNE", "POULE",
    
    # Fruits
    "POMME", "POIRE", "BANANE", "ORANGE", "CITRON", "FRAISE", "CERISE",
    "RAISIN", "PECHE", "ABRICOT", "PRUNE", "KIWI", "ANANAS", "MANGUE",
    "MELON", "PASTEQUE", "FRAMBOISE", "MYRTILLE", "CASSIS",
    
    # Légumes
    "CAROTTE", "TOMATE", "SALADE", "OIGNON", "AIL", "POIREAU", "CHOU",
    "NAVET", "RADIS", "CELERI", "PERSIL", "BASILIC", "THYM",
    
    # Couleurs
    "ROUGE", "BLEU", "VERT", "JAUNE", "ORANGE", "VIOLET", "ROSE", "NOIR",
    "BLANC", "GRIS", "MARRON", "BEIGE", "TURQUOISE", "INDIGO",
    
    # Nature
    "ARBRE", "FLEUR", "FEUILLE", "HERBE", "FORET", "MONTAGNE", "RIVIERE",
    "LAC", "MER", "OCEAN", "PLAGE", "SABLE", "ROCHER", "PIERRE",
    "SOLEIL", "LUNE", "ETOILE", "NUAGE", "PLUIE", "NEIGE", "VENT",
    
    # Corps humain
    "TETE", "BRAS", "JAMBE", "MAIN", "PIED", "DOIGT", "OEIL", "NEZ",
    "BOUCHE", "OREILLE", "DENT", "CHEVEU", "COEUR", "CERVEAU",
    
    # Maison
    "MAISON", "PORTE", "FENETRE", "TOIT", "MUR", "SOL", "PLAFOND",
    "CHAMBRE", "SALON", "CUISINE", "SALLE", "GARAGE", "JARDIN",
    "TABLE", "CHAISE", "LIT", "ARMOIRE", "BUREAU", "LAMPE",
    
    # Transports
    "VOITURE", "TRAIN", "AVION", "BATEAU", "VELO", "MOTO", "BUS",
    "METRO", "CAMION", "FUSEE", "HELICOPTERE", "TAXI",
    
    # Métiers
    "DOCTEUR", "INFIRMIER", "POMPIER", "POLICIER", "PROFESSEUR",
    "BOULANGER", "BOUCHER", "FERMIER", "PEINTRE", "MUSICIEN",
    "CUISINIER", "PILOTE", "MARIN", "COIFFEUR",
    
    # Sports
    "FOOTBALL", "TENNIS", "NATATION", "COURSE", "CYCLISME", "BOXE",
    "JUDO", "KARATE", "BASKET", "VOLLEY", "RUGBY", "GOLF", "SKI",
    
    # Objets quotidiens
    "LIVRE", "STYLO", "CRAYON", "PAPIER", "CAHIER", "SAC", "MONTRE",
    "TELEPHONE", "ORDINATEUR", "CLAVIER", "SOURIS", "ECRAN",
    "LUNETTES", "CHAPEAU", "PARAPLUIE", "CLES", "PORTE", "FENETRE",
]

# Catégories de mots pour des thèmes spécifiques
WORD_CATEGORIES = {
    'animaux': [w for w in FRENCH_WORDS if w in ["CHAT", "CHIEN", "LION", "TIGRE", "OURS", "LOUP", "RENARD", "LAPIN", "SOURIS", "ELEPHANT", "GIRAFE", "ZEBRE", "SINGE", "PANDA", "KOALA", "DAUPHIN", "BALEINE", "REQUIN", "TORTUE", "CROCODILE", "SERPENT", "AIGLE", "HIBOU", "CORBEAU", "PIGEON", "CANARD", "CYGNE", "POULE"]],
    'nature': [w for w in FRENCH_WORDS if w in ["ARBRE", "FLEUR", "FEUILLE", "HERBE", "FORET", "MONTAGNE", "RIVIERE", "LAC", "MER", "OCEAN", "PLAGE", "SABLE", "ROCHER", "PIERRE", "SOLEIL", "LUNE", "ETOILE", "NUAGE", "PLUIE", "NEIGE", "VENT"]],
    'nourriture': [w for w in FRENCH_WORDS if w in ["POMME", "POIRE", "BANANE", "ORANGE", "CITRON", "FRAISE", "CERISE", "RAISIN", "PECHE", "ABRICOT", "PRUNE", "KIWI", "ANANAS", "MANGUE", "MELON", "PASTEQUE", "FRAMBOISE", "MYRTILLE", "CASSIS", "CAROTTE", "TOMATE", "SALADE", "OIGNON", "AIL", "POIREAU", "CHOU", "NAVET", "RADIS", "CELERI", "PERSIL", "BASILIC", "THYM"]],
}


def get_words(category: str = None) -> list:
    """
    Retourne une liste de mots pour le jeu.
    
    Args:
        category: Catégorie optionnelle ('animaux', 'nature', 'nourriture')
        
    Returns:
        Liste de mots
    """
    if category and category in WORD_CATEGORIES:
        return WORD_CATEGORIES[category]
    return FRENCH_WORDS
