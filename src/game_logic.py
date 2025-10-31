"""
Logique du jeu de mots mêlés avec système de niveaux.
"""
import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from src.grid_generator import GridGenerator, GridConfig


@dataclass
class Level:
    """Configuration d'un niveau."""
    number: int
    grid_size: int
    num_words: int
    time_limit: int  # en secondes
    allow_diagonal: bool
    allow_reverse: bool
    

class GameLogic:
    """Gère la logique du jeu."""
    
    LEVELS = [
        Level(1, 8, 5, 180, False, False),          # Niveau 1: 8×8, 5 mots, 3 min
        Level(2, 10, 7, 240, True, False),          # Niveau 2: 10×10, 7 mots, 4 min
        Level(3, 12, 9, 300, True, False),          # Niveau 3: 12×12, 9 mots, 5 min
        Level(4, 14, 11, 360, True, True),          # Niveau 4: 14×14, 11 mots, 6 min
        Level(5, 16, 14, 480, True, True),          # Niveau 5: 16×16, 14 mots, 8 min
    ]
    
    def __init__(self, word_list: List[str]):
        """
        Initialise le jeu.
        
        Args:
            word_list: Liste des mots disponibles
        """
        self.word_list = [word.upper() for word in word_list]
        self.current_level: Optional[Level] = None
        self.grid: Optional[List[List[str]]] = None
        self.words_to_find: List[Dict] = []
        self.found_words: List[str] = []
        self.seed: Optional[int] = None
        self.start_time: Optional[float] = None
        self.elapsed_time: float = 0
        self.is_paused: bool = False
        self.pause_start: Optional[float] = None
        self.total_pause_time: float = 0
    
    def start_level(self, level_number: int, seed: int = None) -> Dict:
        """
        Démarre un niveau.
        
        Args:
            level_number: Numéro du niveau (1-5)
            seed: Seed optionnel pour la génération
            
        Returns:
            Informations sur le niveau démarré
        """
        if level_number < 1 or level_number > len(self.LEVELS):
            raise ValueError(f"Niveau invalide: {level_number}")
        
        self.current_level = self.LEVELS[level_number - 1]
        self.found_words = []
        self.elapsed_time = 0
        self.total_pause_time = 0
        self.is_paused = False
        
        # Générer la grille
        generator = GridGenerator(seed)
        self.seed = generator.get_seed()
        
        config = GridConfig(
            size=self.current_level.grid_size,
            num_words=self.current_level.num_words,
            allow_diagonal=self.current_level.allow_diagonal,
            allow_reverse=self.current_level.allow_reverse
        )
        
        self.grid, self.words_to_find = generator.generate_grid(config, self.word_list)
        self.start_time = time.time()
        
        return {
            'level': level_number,
            'grid_size': self.current_level.grid_size,
            'num_words': len(self.words_to_find),
            'time_limit': self.current_level.time_limit,
            'seed': self.seed,
            'words': [w['word'] for w in self.words_to_find]
        }
    
    def check_word(self, word: str) -> bool:
        """
        Vérifie si un mot est correct et non déjà trouvé.
        
        Args:
            word: Le mot à vérifier
            
        Returns:
            True si le mot est valide et trouvé pour la première fois
        """
        word = word.upper().strip()
        
        if word in self.found_words:
            return False
        
        for word_info in self.words_to_find:
            if word_info['word'] == word:
                self.found_words.append(word)
                return True
        
        return False
    
    def get_remaining_time(self) -> float:
        """
        Calcule le temps restant.
        
        Returns:
            Temps restant en secondes (peut être négatif)
        """
        if not self.start_time or not self.current_level:
            return 0
        
        if self.is_paused:
            elapsed = self.elapsed_time
        else:
            elapsed = (time.time() - self.start_time) - self.total_pause_time
            self.elapsed_time = elapsed
        
        return self.current_level.time_limit - elapsed
    
    def pause(self):
        """Met le jeu en pause."""
        if not self.is_paused and self.start_time:
            self.is_paused = True
            self.pause_start = time.time()
    
    def resume(self):
        """Reprend le jeu après une pause."""
        if self.is_paused and self.pause_start:
            self.total_pause_time += time.time() - self.pause_start
            self.is_paused = False
            self.pause_start = None
    
    def is_level_complete(self) -> bool:
        """Vérifie si tous les mots ont été trouvés."""
        return len(self.found_words) == len(self.words_to_find)
    
    def is_time_up(self) -> bool:
        """Vérifie si le temps est écoulé."""
        return self.get_remaining_time() <= 0
    
    def get_score(self) -> int:
        """
        Calcule le score basé sur le temps restant et les mots trouvés.
        
        Returns:
            Score du joueur
        """
        if not self.current_level:
            return 0
        
        base_score = len(self.found_words) * 100
        time_bonus = max(0, int(self.get_remaining_time() * 2))
        
        return base_score + time_bonus
    
    def get_game_state(self) -> Dict:
        """
        Retourne l'état actuel du jeu.
        
        Returns:
            Dictionnaire contenant l'état du jeu
        """
        return {
            'level': self.current_level.number if self.current_level else None,
            'seed': self.seed,
            'grid': self.grid,
            'words_to_find': [w['word'] for w in self.words_to_find],
            'found_words': self.found_words,
            'remaining_time': self.get_remaining_time(),
            'is_paused': self.is_paused,
            'elapsed_time': self.elapsed_time,
            'total_pause_time': self.total_pause_time
        }
    
    def load_game_state(self, state: Dict):
        """
        Charge un état de jeu sauvegardé.
        
        Args:
            state: État du jeu à charger
        """
        level_number = state.get('level')
        if level_number:
            self.current_level = self.LEVELS[level_number - 1]
        
        self.seed = state.get('seed')
        self.grid = state.get('grid')
        self.found_words = state.get('found_words', [])
        self.elapsed_time = state.get('elapsed_time', 0)
        self.total_pause_time = state.get('total_pause_time', 0)
        self.is_paused = state.get('is_paused', False)
        
        # Reconstruire words_to_find
        words_list = state.get('words_to_find', [])
        self.words_to_find = [{'word': word, 'start': (0, 0), 'direction': 'horizontal', 'length': len(word)} 
                              for word in words_list]
        
        # Ajuster le temps de début
        if self.current_level:
            self.start_time = time.time() - self.elapsed_time - self.total_pause_time
