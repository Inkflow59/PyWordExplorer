"""
Système de traduction et gestion multilingue pour PyWordExplorer.
"""
from typing import Dict, List
import json
import os


class Language:
    """Gestion des langues et traductions."""
    
    # Traductions de l'interface
    TRANSLATIONS = {
        'fr': {
            # Menu principal
            'app_title': 'PyWordExplorer',
            'app_subtitle': 'Jeu de Mots Mêlés',
            'new_game': 'Nouveau Jeu',
            'continue': 'Continuer',
            'load_game': 'Charger une Partie',
            'replay_seed': 'Rejouer avec Seed',
            'quit': 'Quitter',
            'settings': 'Paramètres',
            
            # Niveaux
            'choose_level': 'Choisissez un niveau',
            'level': 'Niveau',
            'beginner': 'Débutant',
            'easy': 'Facile',
            'medium': 'Moyen',
            'hard': 'Difficile',
            'expert': 'Expert',
            'minutes': 'minutes',
            'words': 'mots',
            'back': 'Retour',
            
            # Jeu
            'time_remaining': 'Temps restant',
            'score': 'Score',
            'seed': 'Seed',
            'words_to_find': 'Mots à trouver',
            'pause': 'Pause',
            'resume': 'Reprendre',
            'save': 'Sauvegarder',
            'menu': 'Menu',
            
            # Dialogues
            'load_title': 'Charger une partie',
            'saves_available': 'Sauvegardes disponibles',
            'load': 'Charger',
            'save_dialog': 'Nom de la sauvegarde:',
            'save_success': 'Partie sauvegardée sous',
            'seed_dialog': 'Entrez le seed:',
            'level_dialog': 'Niveau (1-5):',
            'no_saves': 'Aucune sauvegarde trouvée.',
            'no_autosave': 'Aucune sauvegarde automatique trouvée.',
            'error': 'Erreur',
            'success': 'Succès',
            'info': 'Info',
            
            # Fin de jeu
            'level_complete': 'Niveau Terminé',
            'congratulations': 'Félicitations!',
            'level_completed': 'Niveau {} terminé!',
            'final_score': 'Score final: {}',
            'time_used': 'Temps utilisé: {}s',
            'next_level': 'Niveau suivant débloqué!',
            'continue_question': 'Continuer?',
            'time_up': 'Temps Écoulé',
            'time_over': 'Temps écoulé!',
            'words_found': 'Mots trouvés: {}/{}',
            'replay_level': 'Rejouer ce niveau?',
            
            # Menu aide
            'game_menu': 'Jeu',
            'help_menu': 'Aide',
            'help': 'Comment jouer',
            'about': 'À propos',
            'how_to_play': 'Comment jouer',
            'help_text': """Comment jouer:

1. Cliquez sur la première lettre d'un mot
2. Maintenez le clic et glissez jusqu'à la dernière lettre
3. Relâchez le clic pour valider

Les mots peuvent être:
- Horizontaux (→)
- Verticaux (↓)
- Diagonaux (↘ ↗)
- Inversés (selon le niveau)

Trouvez tous les mots avant la fin du temps!""",
            'about_text': """PyWordExplorer v1.0

Un jeu de mots mêlés en Python

Créé par Inkflow59
2025""",
            
            # Paramètres
            'language': 'Langue',
            'select_language': 'Sélectionner la langue',
            'language_changed': 'Langue changée avec succès!',
        },
        
        'en': {
            # Main menu
            'app_title': 'PyWordExplorer',
            'app_subtitle': 'Word Search Game',
            'new_game': 'New Game',
            'continue': 'Continue',
            'load_game': 'Load Game',
            'replay_seed': 'Replay with Seed',
            'quit': 'Quit',
            'settings': 'Settings',
            
            # Levels
            'choose_level': 'Choose a level',
            'level': 'Level',
            'beginner': 'Beginner',
            'easy': 'Easy',
            'medium': 'Medium',
            'hard': 'Hard',
            'expert': 'Expert',
            'minutes': 'minutes',
            'words': 'words',
            'back': 'Back',
            
            # Game
            'time_remaining': 'Time remaining',
            'score': 'Score',
            'seed': 'Seed',
            'words_to_find': 'Words to find',
            'pause': 'Pause',
            'resume': 'Resume',
            'save': 'Save',
            'menu': 'Menu',
            
            # Dialogs
            'load_title': 'Load game',
            'saves_available': 'Available saves',
            'load': 'Load',
            'save_dialog': 'Save name:',
            'save_success': 'Game saved as',
            'seed_dialog': 'Enter seed:',
            'level_dialog': 'Level (1-5):',
            'no_saves': 'No saves found.',
            'no_autosave': 'No autosave found.',
            'error': 'Error',
            'success': 'Success',
            'info': 'Info',
            
            # End game
            'level_complete': 'Level Complete',
            'congratulations': 'Congratulations!',
            'level_completed': 'Level {} completed!',
            'final_score': 'Final score: {}',
            'time_used': 'Time used: {}s',
            'next_level': 'Next level unlocked!',
            'continue_question': 'Continue?',
            'time_up': 'Time Up',
            'time_over': 'Time is up!',
            'words_found': 'Words found: {}/{}',
            'replay_level': 'Replay this level?',
            
            # Help menu
            'game_menu': 'Game',
            'help_menu': 'Help',
            'help': 'How to play',
            'about': 'About',
            'how_to_play': 'How to play',
            'help_text': """How to play:

1. Click on the first letter of a word
2. Hold and drag to the last letter
3. Release to validate

Words can be:
- Horizontal (→)
- Vertical (↓)
- Diagonal (↘ ↗)
- Reversed (depending on level)

Find all words before time runs out!""",
            'about_text': """PyWordExplorer v1.0

A word search game in Python

Created by Inkflow59
2025""",
            
            # Settings
            'language': 'Language',
            'select_language': 'Select language',
            'language_changed': 'Language changed successfully!',
        },
        
        'es': {
            # Menú principal
            'app_title': 'PyWordExplorer',
            'app_subtitle': 'Juego de Sopa de Letras',
            'new_game': 'Nuevo Juego',
            'continue': 'Continuar',
            'load_game': 'Cargar Partida',
            'replay_seed': 'Rejugar con Seed',
            'quit': 'Salir',
            'settings': 'Configuración',
            
            # Niveles
            'choose_level': 'Elige un nivel',
            'level': 'Nivel',
            'beginner': 'Principiante',
            'easy': 'Fácil',
            'medium': 'Medio',
            'hard': 'Difícil',
            'expert': 'Experto',
            'minutes': 'minutos',
            'words': 'palabras',
            'back': 'Volver',
            
            # Juego
            'time_remaining': 'Tiempo restante',
            'score': 'Puntuación',
            'seed': 'Seed',
            'words_to_find': 'Palabras para encontrar',
            'pause': 'Pausa',
            'resume': 'Reanudar',
            'save': 'Guardar',
            'menu': 'Menú',
            
            # Diálogos
            'load_title': 'Cargar partida',
            'saves_available': 'Guardados disponibles',
            'load': 'Cargar',
            'save_dialog': 'Nombre del guardado:',
            'save_success': 'Partida guardada como',
            'seed_dialog': 'Ingrese el seed:',
            'level_dialog': 'Nivel (1-5):',
            'no_saves': 'No se encontraron guardados.',
            'no_autosave': 'No se encontró guardado automático.',
            'error': 'Error',
            'success': 'Éxito',
            'info': 'Info',
            
            # Fin del juego
            'level_complete': 'Nivel Completado',
            'congratulations': '¡Felicitaciones!',
            'level_completed': '¡Nivel {} completado!',
            'final_score': 'Puntuación final: {}',
            'time_used': 'Tiempo usado: {}s',
            'next_level': '¡Siguiente nivel desbloqueado!',
            'continue_question': '¿Continuar?',
            'time_up': 'Tiempo Agotado',
            'time_over': '¡Se acabó el tiempo!',
            'words_found': 'Palabras encontradas: {}/{}',
            'replay_level': '¿Rejugar este nivel?',
            
            # Menú de ayuda
            'game_menu': 'Juego',
            'help_menu': 'Ayuda',
            'help': 'Cómo jugar',
            'about': 'Acerca de',
            'how_to_play': 'Cómo jugar',
            'help_text': """Cómo jugar:

1. Haz clic en la primera letra de una palabra
2. Mantén presionado y arrastra hasta la última letra
3. Suelta para validar

Las palabras pueden estar:
- Horizontales (→)
- Verticales (↓)
- Diagonales (↘ ↗)
- Invertidas (según el nivel)

¡Encuentra todas las palabras antes de que se acabe el tiempo!""",
            'about_text': """PyWordExplorer v1.0

Un juego de sopa de letras en Python

Creado por Inkflow59
2025""",
            
            # Configuración
            'language': 'Idioma',
            'select_language': 'Seleccionar idioma',
            'language_changed': '¡Idioma cambiado con éxito!',
        }
    }
    
    LANGUAGE_NAMES = {
        'fr': 'Français',
        'en': 'English',
        'es': 'Español'
    }
    
    def __init__(self):
        self.current_language = 'fr'
        self.config_file = 'config.json'
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_language = config.get('language', 'fr')
            except (json.JSONDecodeError, IOError):
                pass
    
    def save_config(self):
        """Sauvegarde la configuration."""
        config = {'language': self.current_language}
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def set_language(self, lang_code: str):
        """Change la langue."""
        if lang_code in self.TRANSLATIONS:
            self.current_language = lang_code
            self.save_config()
    
    def get(self, key: str, *args) -> str:
        """
        Récupère une traduction.
        
        Args:
            key: Clé de traduction
            *args: Arguments pour le formatage
            
        Returns:
            Texte traduit
        """
        text = self.TRANSLATIONS.get(self.current_language, {}).get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def get_available_languages(self) -> List[tuple]:
        """Retourne la liste des langues disponibles."""
        return [(code, name) for code, name in self.LANGUAGE_NAMES.items()]


# Instance globale
_language_instance = None

def get_language() -> Language:
    """Retourne l'instance de langue globale."""
    global _language_instance
    if _language_instance is None:
        _language_instance = Language()
    return _language_instance
