"""
Générateur de grilles de mots mêlés avec support de seed.
"""
import random
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class GridConfig:
    """Configuration pour la génération de grille."""
    size: int
    num_words: int
    allow_diagonal: bool
    allow_reverse: bool
    

class GridGenerator:
    """Génère des grilles de mots mêlés aléatoires."""
    
    DIRECTIONS = {
        'horizontal': (0, 1),
        'vertical': (1, 0),
        'diagonal_down': (1, 1),
        'diagonal_up': (-1, 1),
        'horizontal_reverse': (0, -1),
        'vertical_reverse': (-1, 0),
        'diagonal_down_reverse': (-1, -1),
        'diagonal_up_reverse': (1, -1)
    }
    
    def __init__(self, seed: int = None):
        """
        Initialise le générateur.
        
        Args:
            seed: Seed pour la génération aléatoire (reproductibilité)
        """
        self.seed = seed if seed is not None else random.randint(0, 999999)
        self.rng = random.Random(self.seed)
        
    def generate_grid(self, config: GridConfig, word_list: List[str]) -> Tuple[List[List[str]], List[Dict]]:
        """
        Génère une grille de mots mêlés.
        
        Args:
            config: Configuration de la grille
            word_list: Liste de mots à placer
            
        Returns:
            Tuple contenant la grille et les informations des mots placés
        """
        # Filtrer les mots qui sont trop longs pour tenir dans la grille
        max_word_length = config.size
        suitable_words = [w for w in word_list if len(w) <= max_word_length and len(w) >= 3]
        
        if len(suitable_words) < config.num_words:
            # Ajuster le nombre de mots si pas assez de mots appropriés
            config.num_words = max(3, len(suitable_words))  # Au minimum 3 mots
        
        # Essayer de générer une grille valide (avec au moins 50% des mots demandés)
        max_grid_attempts = 5
        min_required_words = max(3, config.num_words // 2)
        
        for attempt in range(max_grid_attempts):
            # Initialiser la grille avec des espaces vides
            grid = [[' ' for _ in range(config.size)] for _ in range(config.size)]
            placed_words = []
            
            # Sélectionner les mots à utiliser
            words_to_place = self.rng.sample(suitable_words, min(config.num_words, len(suitable_words)))
            words_to_place.sort(key=len, reverse=True)  # Placer les plus longs d'abord
            
            # Placer chaque mot
            for word in words_to_place:
                word = word.upper()
                placement = self._try_place_word(grid, word, config)
                if placement:
                    placed_words.append(placement)
            
            # Vérifier si assez de mots ont été placés
            if len(placed_words) >= min_required_words:
                # Remplir les cases vides avec des lettres aléatoires
                self._fill_empty_cells(grid)
                return grid, placed_words
        
        # Si après plusieurs tentatives, pas assez de mots, retourner ce qu'on a
        # (ce cas devrait être rare avec les filtres en place)
        if placed_words:
            self._fill_empty_cells(grid)
            return grid, placed_words
        
        # Cas extrême : générer une grille minimale avec des mots courts garantis
        return self._generate_fallback_grid(config, suitable_words)
    
    def _try_place_word(self, grid: List[List[str]], word: str, config: GridConfig, max_attempts: int = None) -> Dict:
        """
        Tente de placer un mot dans la grille.
        
        Args:
            grid: La grille de jeu
            word: Le mot à placer
            config: Configuration de la grille
            max_attempts: Nombre maximum de tentatives
            
        Returns:
            Dictionnaire avec les infos du mot placé, ou None si échec
        """
        # Adapter le nombre de tentatives à la taille de la grille
        if max_attempts is None:
            max_attempts = max(200, config.size * 20)
        
        # Déterminer les directions autorisées (en donnant beaucoup plus de poids aux diagonales si activées)
        available_directions = ['horizontal', 'vertical']
        if config.allow_diagonal:
            # Ajouter les diagonales plusieurs fois pour augmenter significativement leur fréquence (ratio 3:1)
            available_directions.extend(['diagonal_down', 'diagonal_up'] * 3)
        
        # Décider si on inverse le mot (60% de chance si allow_reverse est activé)
        word_to_place = word
        is_reversed = False
        if config.allow_reverse and self.rng.random() < 0.6:
            word_to_place = word[::-1]  # Inverser les lettres
            is_reversed = True
        
        for _ in range(max_attempts):
            # Choisir une position et direction aléatoires
            row = self.rng.randint(0, config.size - 1)
            col = self.rng.randint(0, config.size - 1)
            direction_name = self.rng.choice(available_directions)
            direction = self.DIRECTIONS[direction_name]
            
            # Vérifier si le mot peut être placé
            if self._can_place_word(grid, word_to_place, row, col, direction, config.size):
                # Placer le mot
                self._place_word(grid, word_to_place, row, col, direction)
                return {
                    'word': word,  # On retourne toujours le mot original
                    'start': (row, col),
                    'direction': direction_name,
                    'length': len(word),
                    'reversed': is_reversed
                }
        
        return None
    
    def _can_place_word(self, grid: List[List[str]], word: str, row: int, col: int, 
                       direction: Tuple[int, int], grid_size: int) -> bool:
        """Vérifie si un mot peut être placé à une position donnée."""
        dr, dc = direction
        
        for i, letter in enumerate(word):
            new_row = row + i * dr
            new_col = col + i * dc
            
            # Vérifier les limites
            if not (0 <= new_row < grid_size and 0 <= new_col < grid_size):
                return False
            
            # Vérifier si la case est vide ou contient la même lettre
            current = grid[new_row][new_col]
            if current != ' ' and current != letter:
                return False
        
        return True
    
    def _place_word(self, grid: List[List[str]], word: str, row: int, col: int, 
                   direction: Tuple[int, int]):
        """Place un mot dans la grille."""
        dr, dc = direction
        
        for i, letter in enumerate(word):
            new_row = row + i * dr
            new_col = col + i * dc
            grid[new_row][new_col] = letter
    
    def _fill_empty_cells(self, grid: List[List[str]]):
        """Remplit les cases vides avec des lettres aléatoires."""
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == ' ':
                    grid[i][j] = self.rng.choice(letters)
    
    def _generate_fallback_grid(self, config: GridConfig, word_list: List[str]) -> Tuple[List[List[str]], List[Dict]]:
        """
        Génère une grille de secours avec placement garanti de mots simples.
        Cette méthode est utilisée en dernier recours.
        """
        grid = [[' ' for _ in range(config.size)] for _ in range(config.size)]
        placed_words = []
        
        # Prendre les mots les plus courts pour garantir le placement
        short_words = sorted([w for w in word_list if len(w) <= config.size // 2], key=len)
        words_to_place = short_words[:min(config.num_words, len(short_words))]
        
        # Placer les mots horizontalement en lignes espacées
        row_spacing = max(2, config.size // (len(words_to_place) + 1))
        
        for idx, word in enumerate(words_to_place):
            word = word.upper()
            row = min(idx * row_spacing + 1, config.size - 1)
            col = 0
            
            if len(word) <= config.size:
                # Placer le mot horizontalement
                for i, letter in enumerate(word):
                    if col + i < config.size:
                        grid[row][col + i] = letter
                
                placed_words.append({
                    'word': word,
                    'start': (row, col),
                    'direction': 'horizontal',
                    'length': len(word)
                })
        
        self._fill_empty_cells(grid)
        return grid, placed_words
    
    def get_seed(self) -> int:
        """Retourne le seed utilisé pour la génération."""
        return self.seed
