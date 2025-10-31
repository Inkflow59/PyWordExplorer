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
        # Initialiser la grille avec des espaces vides
        grid = [[' ' for _ in range(config.size)] for _ in range(config.size)]
        placed_words = []
        
        # Sélectionner les mots à utiliser
        words_to_place = self.rng.sample(word_list, min(config.num_words, len(word_list)))
        words_to_place.sort(key=len, reverse=True)  # Placer les plus longs d'abord
        
        # Placer chaque mot
        for word in words_to_place:
            word = word.upper()
            placement = self._try_place_word(grid, word, config)
            if placement:
                placed_words.append(placement)
        
        # Remplir les cases vides avec des lettres aléatoires
        self._fill_empty_cells(grid)
        
        return grid, placed_words
    
    def _try_place_word(self, grid: List[List[str]], word: str, config: GridConfig, max_attempts: int = 100) -> Dict:
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
        # Déterminer les directions autorisées
        available_directions = ['horizontal', 'vertical']
        if config.allow_diagonal:
            available_directions.extend(['diagonal_down', 'diagonal_up'])
        if config.allow_reverse:
            available_directions.extend(['horizontal_reverse', 'vertical_reverse'])
            if config.allow_diagonal:
                available_directions.extend(['diagonal_down_reverse', 'diagonal_up_reverse'])
        
        for _ in range(max_attempts):
            # Choisir une position et direction aléatoires
            row = self.rng.randint(0, config.size - 1)
            col = self.rng.randint(0, config.size - 1)
            direction_name = self.rng.choice(available_directions)
            direction = self.DIRECTIONS[direction_name]
            
            # Vérifier si le mot peut être placé
            if self._can_place_word(grid, word, row, col, direction, config.size):
                # Placer le mot
                self._place_word(grid, word, row, col, direction)
                return {
                    'word': word,
                    'start': (row, col),
                    'direction': direction_name,
                    'length': len(word)
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
    
    def get_seed(self) -> int:
        """Retourne le seed utilisé pour la génération."""
        return self.seed
