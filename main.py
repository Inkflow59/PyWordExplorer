"""
PyWordExplorer - Jeu de mots mêlés
Point d'entrée principal
"""
import sys
import os
import tkinter as tk
from src.gui import WordSearchGUI
from src.game_logic import GameLogic
from src.save_manager import SaveManager
from src.word_generator import get_word_generator


def main():
    """Lance l'application avec l'interface graphique."""
    try:
        root = tk.Tk()
        app = WordSearchGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir!\n")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# =============================================================================
# ANCIENNE VERSION CONSOLE (conservée pour référence)
# =============================================================================

class ConsoleUI_OLD:
    """Interface utilisateur en mode console."""
    
    def __init__(self):
        word_gen = get_word_generator()
        self.game = GameLogic(word_gen.get_words())
        self.save_manager = SaveManager()
        self.running = True
    
    def clear_screen(self):
        """Efface l'écran de la console."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_grid(self):
        """Affiche la grille de jeu."""
        if not self.game.grid:
            return
        
        print("\n   ", end="")
        for i in range(len(self.game.grid[0])):
            print(f" {i:2}", end="")
        print("\n   " + "---" * len(self.game.grid[0]))
        
        for i, row in enumerate(self.game.grid):
            print(f"{i:2} |", end="")
            for cell in row:
                print(f" {cell} ", end="")
            print("|")
        
        print("   " + "---" * len(self.game.grid[0]))
    
    def display_game_info(self):
        """Affiche les informations de la partie."""
        if not self.game.current_level:
            return
        
        print(f"\n{'='*60}")
        print(f"  NIVEAU {self.game.current_level.number} | Seed: {self.game.seed}")
        print(f"{'='*60}")
        
        remaining = self.game.get_remaining_time()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        if remaining > 0:
            print(f"  ⏱️  Temps restant: {minutes:02d}:{seconds:02d}")
        else:
            print(f"  ⏱️  TEMPS ÉCOULÉ!")
        
        print(f"  ✓ Mots trouvés: {len(self.game.found_words)}/{len(self.game.words_to_find)}")
        print(f"  🎯 Score: {self.game.get_score()}")
        print(f"{'='*60}\n")
    
    def display_words_list(self):
        """Affiche la liste des mots à trouver."""
        print("\nMots à trouver:")
        print("-" * 40)
        
        words_per_line = 4
        words = [w['word'] for w in self.game.words_to_find]
        
        for i in range(0, len(words), words_per_line):
            line_words = words[i:i+words_per_line]
            for word in line_words:
                status = "✓" if word in self.game.found_words else " "
                print(f"  [{status}] {word:12}", end="")
            print()
        print()
    
    def main_menu(self):
        """Affiche le menu principal."""
        self.clear_screen()
        print("\n" + "="*60)
        print("  🔤  PYWORDEXPLORER - Jeu de Mots Mêlés  🔤")
        print("="*60)
        print("\n1. Nouveau jeu")
        print("2. Continuer la dernière partie")
        print("3. Charger une partie")
        print("4. Rejouer avec un seed")
        print("5. Quitter")
        print()
        
        choice = input("Votre choix: ").strip()
        
        if choice == "1":
            self.new_game()
        elif choice == "2":
            self.continue_game()
        elif choice == "3":
            self.load_game_menu()
        elif choice == "4":
            self.replay_with_seed()
        elif choice == "5":
            self.running = False
        else:
            print("Choix invalide!")
            input("\nAppuyez sur Entrée pour continuer...")
    
    def new_game(self):
        """Démarre une nouvelle partie."""
        self.clear_screen()
        print("\n" + "="*60)
        print("  NOUVEAU JEU")
        print("="*60)
        print("\nChoisissez un niveau (1-5):")
        print("  1. Débutant    (8×8,   5 mots,  3 min)")
        print("  2. Facile      (10×10, 7 mots,  4 min)")
        print("  3. Moyen       (12×12, 9 mots,  5 min)")
        print("  4. Difficile   (14×14, 11 mots, 6 min)")
        print("  5. Expert      (16×16, 14 mots, 8 min)")
        print()
        
        try:
            level = int(input("Niveau: ").strip())
            info = self.game.start_level(level)
            print(f"\nNiveau {level} démarré! (Seed: {info['seed']})")
            input("\nAppuyez sur Entrée pour commencer...")
            self.play_game()
        except (ValueError, Exception) as e:
            print(f"Erreur: {e}")
            input("\nAppuyez sur Entrée pour continuer...")
    
    def continue_game(self):
        """Continue la dernière partie sauvegardée."""
        if not self.save_manager.has_autosave():
            print("\nAucune sauvegarde automatique trouvée.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        state = self.save_manager.load_game("autosave")
        if state:
            self.game.load_game_state(state)
            print(f"\nPartie chargée! Niveau {state['level']}")
            input("\nAppuyez sur Entrée pour continuer...")
            self.play_game()
    
    def load_game_menu(self):
        """Affiche le menu de chargement."""
        self.clear_screen()
        saves = self.save_manager.list_saves()
        
        if not saves:
            print("\nAucune sauvegarde trouvée.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print("\n" + "="*60)
        print("  SAUVEGARDES DISPONIBLES")
        print("="*60)
        
        for i, save in enumerate(saves, 1):
            print(f"\n{i}. {save['name']}")
            print(f"   Niveau: {save['level']} | Date: {save['timestamp'][:19]}")
        
        print("\n0. Retour")
        print()
        
        try:
            choice = int(input("Choisir une sauvegarde: ").strip())
            if choice > 0 and choice <= len(saves):
                save_name = saves[choice - 1]['name']
                state = self.save_manager.load_game(save_name)
                if state:
                    self.game.load_game_state(state)
                    print(f"\nPartie '{save_name}' chargée!")
                    input("\nAppuyez sur Entrée pour continuer...")
                    self.play_game()
        except (ValueError, IndexError):
            print("Choix invalide!")
            input("\nAppuyez sur Entrée pour continuer...")
    
    def replay_with_seed(self):
        """Rejoue une partie avec un seed spécifique."""
        self.clear_screen()
        print("\n" + "="*60)
        print("  REJOUER AVEC UN SEED")
        print("="*60)
        
        try:
            seed = int(input("\nEntrez le seed: ").strip())
            level = int(input("Niveau (1-5): ").strip())
            
            info = self.game.start_level(level, seed)
            print(f"\nNiveau {level} démarré avec le seed {seed}!")
            input("\nAppuyez sur Entrée pour commencer...")
            self.play_game()
        except (ValueError, Exception) as e:
            print(f"Erreur: {e}")
            input("\nAppuyez sur Entrée pour continuer...")
    
    def play_game(self):
        """Boucle principale du jeu."""
        while self.running and self.game.current_level:
            self.clear_screen()
            self.display_game_info()
            self.display_grid()
            self.display_words_list()
            
            # Vérifier les conditions de fin
            if self.game.is_level_complete():
                self.level_complete()
                return
            
            if self.game.is_time_up():
                self.game_over()
                return
            
            print("\nCommandes: [mot] pour trouver un mot | 'pause' | 'menu' | 'save'")
            command = input(">>> ").strip().upper()
            
            if command == "MENU":
                self.save_manager.save_game(self.game.get_game_state(), "autosave")
                print("\nPartie sauvegardée automatiquement.")
                input("\nAppuyez sur Entrée pour continuer...")
                return
            elif command == "PAUSE":
                self.pause_menu()
            elif command == "SAVE":
                save_name = input("Nom de la sauvegarde: ").strip()
                if save_name:
                    self.save_manager.save_game(self.game.get_game_state(), save_name)
                    print(f"\nPartie sauvegardée sous '{save_name}'!")
                    input("\nAppuyez sur Entrée pour continuer...")
            elif command:
                if self.game.check_word(command):
                    print(f"\n✓ Bravo! '{command}' trouvé!")
                else:
                    print(f"\n✗ '{command}' n'est pas dans la liste ou déjà trouvé.")
                input("\nAppuyez sur Entrée pour continuer...")
    
    def pause_menu(self):
        """Menu de pause."""
        self.game.pause()
        
        while True:
            self.clear_screen()
            print("\n" + "="*60)
            print("  JEU EN PAUSE")
            print("="*60)
            print("\n1. Reprendre")
            print("2. Sauvegarder")
            print("3. Menu principal")
            print()
            
            choice = input("Votre choix: ").strip()
            
            if choice == "1":
                self.game.resume()
                return
            elif choice == "2":
                save_name = input("Nom de la sauvegarde: ").strip()
                if save_name:
                    self.save_manager.save_game(self.game.get_game_state(), save_name)
                    print(f"\nPartie sauvegardée sous '{save_name}'!")
                    input("\nAppuyez sur Entrée pour continuer...")
            elif choice == "3":
                self.save_manager.save_game(self.game.get_game_state(), "autosave")
                self.game.resume()
                return
    
    def level_complete(self):
        """Affiche l'écran de niveau terminé."""
        if not self.game.current_level:
            return
            
        self.clear_screen()
        print("\n" + "="*60)
        print("  🎉 NIVEAU TERMINÉ! 🎉")
        print("="*60)
        print(f"\n  Score final: {self.game.get_score()}")
        print(f"  Temps utilisé: {int(self.game.elapsed_time)}s")
        print(f"  Niveau: {self.game.current_level.number}")
        print(f"  Seed: {self.game.seed}")
        
        if self.game.current_level.number < len(GameLogic.LEVELS):
            print(f"\n  Niveau suivant débloqué!")
        
        print("\n" + "="*60)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def game_over(self):
        """Affiche l'écran de game over."""
        self.clear_screen()
        print("\n" + "="*60)
        print("  ⏱️  TEMPS ÉCOULÉ!")
        print("="*60)
        print(f"\n  Mots trouvés: {len(self.game.found_words)}/{len(self.game.words_to_find)}")
        print(f"  Score: {self.game.get_score()}")
        print(f"  Seed: {self.game.seed}")
        print("\n" + "="*60)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def run(self):
        """Lance l'application."""
        while self.running:
            self.main_menu()
        
        print("\n👋 Merci d'avoir joué! À bientôt!\n")
