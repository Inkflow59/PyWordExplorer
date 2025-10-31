"""
Générateur de mots dynamique pour différentes langues.
Utilise des dictionnaires aléatoires via des bibliothèques externes.
"""
import random
from typing import List, Set
import os
import urllib.request
import ssl


class WordGenerator:
    """Génère des listes de mots pour différentes langues depuis des dictionnaires."""
    
    # URLs des dictionnaires en ligne
    DICT_URLS = {
        'fr': 'https://raw.githubusercontent.com/lorenbrichter/Words/master/Words/fr.txt',
        'en': 'https://raw.githubusercontent.com/lorenbrichter/Words/master/Words/en.txt',
        'es': 'https://raw.githubusercontent.com/lorenbrichter/Words/master/Words/es.txt',
    }
    
    # Cache local des dictionnaires
    DICT_CACHE_DIR = 'dict_cache'
    
    # Mots de secours si le téléchargement échoue
    FALLBACK_FRENCH_WORDS = [
        # Animaux
        "CHAT", "CHIEN", "LION", "TIGRE", "OURS", "LOUP", "RENARD", "LAPIN",
        "SOURIS", "ELEPHANT", "GIRAFE", "ZEBRE", "SINGE", "PANDA", "KOALA",
        "DAUPHIN", "BALEINE", "REQUIN", "TORTUE", "CROCODILE", "SERPENT",
        "AIGLE", "HIBOU", "CORBEAU", "PIGEON", "CANARD", "CYGNE", "POULE",
        "VACHE", "MOUTON", "CHEVRE", "COCHON", "ANE", "CHEVAL", "CHAMEAU",
        
        # Fruits et légumes
        "POMME", "POIRE", "BANANE", "ORANGE", "CITRON", "FRAISE", "CERISE",
        "RAISIN", "PECHE", "ABRICOT", "PRUNE", "KIWI", "ANANAS", "MANGUE",
        "MELON", "PASTEQUE", "FRAMBOISE", "MYRTILLE", "CASSIS",
        "CAROTTE", "TOMATE", "SALADE", "OIGNON", "POIREAU", "CHOU",
        "NAVET", "RADIS", "CELERI", "PERSIL", "BASILIC", "THYM",
        
        # Couleurs
        "ROUGE", "BLEU", "VERT", "JAUNE", "ORANGE", "VIOLET", "ROSE", "NOIR",
        "BLANC", "GRIS", "MARRON", "BEIGE", "TURQUOISE", "INDIGO",
        
        # Nature
        "ARBRE", "FLEUR", "FEUILLE", "HERBE", "FORET", "MONTAGNE", "RIVIERE",
        "LAC", "MER", "OCEAN", "PLAGE", "SABLE", "ROCHER", "PIERRE",
        "SOLEIL", "LUNE", "ETOILE", "NUAGE", "PLUIE", "NEIGE", "VENT",
        
        # Corps
        "TETE", "BRAS", "JAMBE", "MAIN", "PIED", "DOIGT", "OEIL", "NEZ",
        "BOUCHE", "OREILLE", "DENT", "CHEVEU", "COEUR", "CERVEAU",
        
        # Maison
        "MAISON", "PORTE", "FENETRE", "TOIT", "MUR", "SOL", "PLAFOND",
        "CHAMBRE", "SALON", "CUISINE", "SALLE", "GARAGE", "JARDIN",
        "TABLE", "CHAISE", "LIT", "ARMOIRE", "BUREAU", "LAMPE",
        
        # Autres
        "LIVRE", "STYLO", "CRAYON", "PAPIER", "CAHIER", "SAC", "MONTRE",
        "TELEPHONE", "ORDINATEUR", "CLAVIER", "SOURIS", "ECRAN",
        "VOITURE", "TRAIN", "AVION", "BATEAU", "VELO", "MOTO",
    ]
    
    FALLBACK_ENGLISH_WORDS = [
        # Animals
        "CAT", "DOG", "LION", "TIGER", "BEAR", "WOLF", "FOX", "RABBIT",
        "MOUSE", "ELEPHANT", "GIRAFFE", "ZEBRA", "MONKEY", "PANDA", "KOALA",
        "DOLPHIN", "WHALE", "SHARK", "TURTLE", "CROCODILE", "SNAKE",
        "EAGLE", "OWL", "CROW", "PIGEON", "DUCK", "SWAN", "CHICKEN",
        "COW", "SHEEP", "GOAT", "PIG", "DONKEY", "HORSE", "CAMEL",
        
        # Fruits and vegetables
        "APPLE", "PEAR", "BANANA", "ORANGE", "LEMON", "STRAWBERRY", "CHERRY",
        "GRAPE", "PEACH", "APRICOT", "PLUM", "KIWI", "PINEAPPLE", "MANGO",
        "MELON", "WATERMELON", "RASPBERRY", "BLUEBERRY", "BLACKBERRY",
        "CARROT", "TOMATO", "LETTUCE", "ONION", "LEEK", "CABBAGE",
        "TURNIP", "RADISH", "CELERY", "PARSLEY", "BASIL", "THYME",
        
        # Colors
        "RED", "BLUE", "GREEN", "YELLOW", "ORANGE", "PURPLE", "PINK", "BLACK",
        "WHITE", "GRAY", "BROWN", "BEIGE", "TURQUOISE", "INDIGO",
        
        # Nature
        "TREE", "FLOWER", "LEAF", "GRASS", "FOREST", "MOUNTAIN", "RIVER",
        "LAKE", "SEA", "OCEAN", "BEACH", "SAND", "ROCK", "STONE",
        "SUN", "MOON", "STAR", "CLOUD", "RAIN", "SNOW", "WIND",
        
        # Body
        "HEAD", "ARM", "LEG", "HAND", "FOOT", "FINGER", "EYE", "NOSE",
        "MOUTH", "EAR", "TOOTH", "HAIR", "HEART", "BRAIN",
        
        # House
        "HOUSE", "DOOR", "WINDOW", "ROOF", "WALL", "FLOOR", "CEILING",
        "BEDROOM", "LIVING", "KITCHEN", "BATHROOM", "GARAGE", "GARDEN",
        "TABLE", "CHAIR", "BED", "CLOSET", "DESK", "LAMP",
        
        # Others
        "BOOK", "PEN", "PENCIL", "PAPER", "NOTEBOOK", "BAG", "WATCH",
        "PHONE", "COMPUTER", "KEYBOARD", "MOUSE", "SCREEN",
        "CAR", "TRAIN", "PLANE", "BOAT", "BIKE", "MOTORCYCLE",
    ]
    
    FALLBACK_SPANISH_WORDS = [
        # Animales
        "GATO", "PERRO", "LEON", "TIGRE", "OSO", "LOBO", "ZORRO", "CONEJO",
        "RATON", "ELEFANTE", "JIRAFA", "CEBRA", "MONO", "PANDA", "KOALA",
        "DELFIN", "BALLENA", "TIBURON", "TORTUGA", "COCODRILO", "SERPIENTE",
        "AGUILA", "BUHO", "CUERVO", "PALOMA", "PATO", "CISNE", "GALLINA",
        "VACA", "OVEJA", "CABRA", "CERDO", "BURRO", "CABALLO", "CAMELLO",
        
        # Frutas y verduras
        "MANZANA", "PERA", "PLATANO", "NARANJA", "LIMON", "FRESA", "CEREZA",
        "UVA", "MELOCOTON", "ALBARICOQUE", "CIRUELA", "KIWI", "PINA", "MANGO",
        "MELON", "SANDIA", "FRAMBUESA", "ARANDANO", "MORA",
        "ZANAHORIA", "TOMATE", "LECHUGA", "CEBOLLA", "PUERRO", "COL",
        "NABO", "RABANO", "APIO", "PEREJIL", "ALBAHACA", "TOMILLO",
        
        # Colores
        "ROJO", "AZUL", "VERDE", "AMARILLO", "NARANJA", "MORADO", "ROSA", "NEGRO",
        "BLANCO", "GRIS", "MARRON", "BEIGE", "TURQUESA", "INDIGO",
        
        # Naturaleza
        "ARBOL", "FLOR", "HOJA", "HIERBA", "BOSQUE", "MONTANA", "RIO",
        "LAGO", "MAR", "OCEANO", "PLAYA", "ARENA", "ROCA", "PIEDRA",
        "SOL", "LUNA", "ESTRELLA", "NUBE", "LLUVIA", "NIEVE", "VIENTO",
        
        # Cuerpo
        "CABEZA", "BRAZO", "PIERNA", "MANO", "PIE", "DEDO", "OJO", "NARIZ",
        "BOCA", "OREJA", "DIENTE", "PELO", "CORAZON", "CEREBRO",
        
        # Casa
        "CASA", "PUERTA", "VENTANA", "TECHO", "PARED", "SUELO", "TECHO",
        "DORMITORIO", "SALON", "COCINA", "BANO", "GARAJE", "JARDIN",
        "MESA", "SILLA", "CAMA", "ARMARIO", "ESCRITORIO", "LAMPARA",
        
        # Otros
        "LIBRO", "PLUMA", "LAPIZ", "PAPEL", "CUADERNO", "BOLSA", "RELOJ",
        "TELEFONO", "ORDENADOR", "TECLADO", "RATON", "PANTALLA",
        "COCHE", "TREN", "AVION", "BARCO", "BICICLETA", "MOTOCICLETA",
    ]
    
    def __init__(self, language: str = 'fr'):
        """
        Initialise le générateur.
        
        Args:
            language: Code de langue ('fr', 'en', 'es')
        """
        self.language = language
        self.word_cache: dict = {}  # Cache des mots chargés
        self._ensure_cache_dir()
        self._load_dictionaries()
    
    def _ensure_cache_dir(self):
        """Crée le dossier de cache s'il n'existe pas."""
        if not os.path.exists(self.DICT_CACHE_DIR):
            os.makedirs(self.DICT_CACHE_DIR)
    
    def _get_cache_path(self, lang: str) -> str:
        """Retourne le chemin du fichier de cache pour une langue."""
        return os.path.join(self.DICT_CACHE_DIR, f'{lang}_words.txt')
    
    def _download_dictionary(self, lang: str) -> Set[str]:
        """
        Télécharge un dictionnaire depuis GitHub.
        
        Args:
            lang: Code de langue
            
        Returns:
            Ensemble de mots
        """
        cache_path = self._get_cache_path(lang)
        
        # Vérifier si le cache existe
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    words = set(line.strip().upper() for line in f if line.strip())
                if words:
                    print(f"✓ Dictionnaire {lang} chargé depuis le cache ({len(words)} mots)")
                    return words
            except Exception as e:
                print(f"⚠ Erreur lecture cache {lang}: {e}")
        
        # Télécharger depuis GitHub
        if lang in self.DICT_URLS:
            try:
                print(f"⏳ Téléchargement du dictionnaire {lang}...")
                
                # Contourner la vérification SSL pour les anciens systèmes
                context = ssl._create_unverified_context()
                
                with urllib.request.urlopen(self.DICT_URLS[lang], context=context, timeout=10) as response:
                    content = response.read().decode('utf-8')
                    words = set()
                    
                    for line in content.split('\n'):
                        word = line.strip().upper()
                        # Filtrer les mots valides (3-15 lettres, alphabétiques)
                        if 3 <= len(word) <= 15 and word.isalpha():
                            words.add(word)
                    
                    # Sauvegarder dans le cache
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        for word in sorted(words):
                            f.write(word + '\n')
                    
                    print(f"✓ Dictionnaire {lang} téléchargé ({len(words)} mots)")
                    return words
                    
            except Exception as e:
                print(f"⚠ Erreur téléchargement {lang}: {e}")
        
        return set()
    
    def _load_dictionaries(self):
        """Charge tous les dictionnaires disponibles."""
        for lang in ['fr', 'en', 'es']:
            words = self._download_dictionary(lang)
            
            if not words:
                # Utiliser les mots de secours
                print(f"⚠ Utilisation des mots de secours pour {lang}")
                if lang == 'fr':
                    words = set(self.FALLBACK_FRENCH_WORDS)
                elif lang == 'en':
                    words = set(self.FALLBACK_ENGLISH_WORDS)
                elif lang == 'es':
                    words = set(self.FALLBACK_SPANISH_WORDS)
            
            self.word_cache[lang] = list(words)
    
    def set_language(self, language: str):
        """Change la langue."""
        self.language = language
    
    def get_words(self, count: int = None) -> List[str]:
        """
        Retourne une liste de mots dans la langue courante.
        
        Args:
            count: Nombre de mots à retourner (None = tous)
            
        Returns:
            Liste de mots en majuscules
        """
        # Récupérer les mots du cache
        if self.language not in self.word_cache or not self.word_cache[self.language]:
            print(f"⚠ Aucun mot disponible pour {self.language}, utilisation du français")
            words = self.word_cache.get('fr', self.FALLBACK_FRENCH_WORDS.copy())
        else:
            words = self.word_cache[self.language].copy()
        
        # Mélanger pour varier
        random.shuffle(words)
        
        if count and count < len(words):
            return words[:count]
        return words
    
    def get_random_words(self, count: int) -> List[str]:
        """
        Retourne un nombre spécifique de mots aléatoires.
        
        Args:
            count: Nombre de mots à générer
            
        Returns:
            Liste de mots aléatoires
        """
        all_words = self.get_words()
        return random.sample(all_words, min(count, len(all_words)))


# Instance globale
_word_generator_instance = None

def get_word_generator() -> WordGenerator:
    """Retourne l'instance globale du générateur."""
    global _word_generator_instance
    if _word_generator_instance is None:
        _word_generator_instance = WordGenerator()
    return _word_generator_instance
