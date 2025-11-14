# type: ignore
"""
Interface graphique pour PyWordExplorer avec Tkinter.
FICHIER DE BACKUP - Peut contenir des avertissements de type
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Tuple, Optional
import math
from src.solo.game_logic import GameLogic
from src.solo.save_manager import SaveManager
from src.word_generator import get_word_generator
from src.language import get_language


class WordSearchGUI:
    """Interface graphique du jeu de mots mêlés."""
    
    # Couleurs
    COLOR_BG = "#2C3E50"
    COLOR_GRID_BG = "#ECF0F1"
    COLOR_CELL = "#FFFFFF"
    COLOR_CELL_BORDER = "#BDC3C7"
    COLOR_SELECTED = "#3498DB"
    COLOR_FOUND = "#2ECC71"
    COLOR_TEXT = "#2C3E50"
    COLOR_WORD_LIST = "#34495E"
    COLOR_WORD_FOUND = "#27AE60"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("1200x800")
        self.root.configure(bg=self.COLOR_BG)
        
        # Language and word generator
        self.lang = get_language()
        self.word_gen = get_word_generator()
        self.word_gen.set_language(self.lang.current_language)
        
        # Game logic
        self.game = GameLogic(self.word_gen.get_words())
        self.save_manager = SaveManager()
        
        # Update title
        self.update_title()
        
        # Selection state
        self.selecting = False
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_end: Optional[Tuple[int, int]] = None
        self.current_selection: List[Tuple[int, int]] = []
        self.found_cells: List[Tuple[int, int]] = []
        
        # UI elements
        self.canvas = None
        self.cell_size = 40
        self.grid_offset_x = 50
        self.grid_offset_y = 50
        self.cell_rects = []
        self.cell_texts = []
        self.timer_label = None
        self.score_label = None
        self.level_label = None
        self.word_labels = {}
        
        # Timer
        self.timer_running = False
        self.timer_id = None
        
        self.create_menu()
        self.show_main_menu()
    
    def update_title(self):
        """Met à jour le titre de la fenêtre."""
        self.root.title(f"{self.lang.get('app_title')} - {self.lang.get('app_subtitle')}")
    
    def create_menu(self):
        """Crée la barre de menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Jeu
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('game_menu'), menu=game_menu)
        game_menu.add_command(label=self.lang.get('new_game'), command=self.new_game_dialog)
        game_menu.add_command(label=self.lang.get('continue'), command=self.continue_game)
        game_menu.add_command(label=self.lang.get('load_game'), command=self.load_game_dialog)
        game_menu.add_command(label=self.lang.get('save'), command=self.save_game_dialog)
        game_menu.add_separator()
        game_menu.add_command(label=self.lang.get('replay_seed'), command=self.replay_seed_dialog)
        game_menu.add_separator()
        game_menu.add_command(label=self.lang.get('settings'), command=self.show_settings)
        game_menu.add_separator()
        game_menu.add_command(label=self.lang.get('quit'), command=self.root.quit)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('help_menu'), menu=help_menu)
        help_menu.add_command(label=self.lang.get('help'), command=self.show_help)
        help_menu.add_command(label=self.lang.get('about'), command=self.show_about)
    
    def clear_window(self):
        """Efface tous les widgets de la fenêtre."""
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
    
    def show_main_menu(self):
        """Affiche le menu principal."""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg=self.COLOR_BG)
        frame.pack(expand=True)
        
        # Titre
        title = tk.Label(
            frame,
            text=f"🔤 {self.lang.get('app_title')} 🔤",
            font=("Arial", 36, "bold"),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        )
        title.pack(pady=30)
        
        subtitle = tk.Label(
            frame,
            text=self.lang.get('app_subtitle'),
            font=("Arial", 18),
            bg=self.COLOR_BG,
            fg="#BDC3C7"
        )
        subtitle.pack(pady=10)
        
        # Boutons
        button_style = {
            "font": ("Arial", 14),
            "width": 25,
            "height": 2,
            "bg": "#3498DB",
            "fg": "white",
            "relief": "flat",
            "cursor": "hand2"
        }
        
        tk.Button(frame, text=self.lang.get('new_game'), command=self.new_game_dialog, **button_style).pack(pady=10)
        
        if self.save_manager.has_autosave():
            tk.Button(frame, text=self.lang.get('continue'), command=self.continue_game, **button_style).pack(pady=10)
        
        tk.Button(frame, text=self.lang.get('load_game'), command=self.load_game_dialog, **button_style).pack(pady=10)
        tk.Button(frame, text=self.lang.get('replay_seed'), command=self.replay_seed_dialog, **button_style).pack(pady=10)
        tk.Button(frame, text=self.lang.get('settings'), command=self.show_settings, **button_style).pack(pady=10)
        tk.Button(frame, text=self.lang.get('quit'), command=self.root.quit, bg="#E74C3C", fg="white", 
                 font=("Arial", 14), width=25, height=2, relief="flat").pack(pady=20)
    
    def new_game_dialog(self):
        """Affiche le dialogue de sélection de niveau."""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg=self.COLOR_BG)
        frame.pack(expand=True)
        
        title = tk.Label(
            frame,
            text=self.lang.get('choose_level'),
            font=("Arial", 24, "bold"),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        )
        title.pack(pady=30)
        
        # Descriptions des niveaux
        levels_info = [
            (f"1. {self.lang.get('beginner')}", f"8×8, 5 {self.lang.get('words')}, 3 {self.lang.get('minutes')}"),
            (f"2. {self.lang.get('easy')}", f"10×10, 7 {self.lang.get('words')}, 4 {self.lang.get('minutes')}"),
            (f"3. {self.lang.get('medium')}", f"12×12, 9 {self.lang.get('words')}, 5 {self.lang.get('minutes')}"),
            (f"4. {self.lang.get('hard')}", f"14×14, 11 {self.lang.get('words')}, 6 {self.lang.get('minutes')}"),
            (f"5. {self.lang.get('expert')}", f"16×16, 14 {self.lang.get('words')}, 8 {self.lang.get('minutes')}"),
        ]
        
        for i, (level_name, level_desc) in enumerate(levels_info, 1):
            level_frame = tk.Frame(frame, bg=self.COLOR_BG)
            level_frame.pack(pady=5)
            
            btn = tk.Button(
                level_frame,
                text=level_name,
                font=("Arial", 14, "bold"),
                width=15,
                height=2,
                bg="#3498DB",
                fg="white",
                relief="flat",
                cursor="hand2",
                command=lambda lvl=i: self.start_level(lvl)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            desc = tk.Label(
                level_frame,
                text=level_desc,
                font=("Arial", 12),
                bg=self.COLOR_BG,
                fg="#BDC3C7"
            )
            desc.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            frame,
            text="Retour",
            font=("Arial", 12),
            width=15,
            bg="#95A5A6",
            fg="white",
            relief="flat",
            command=self.show_main_menu
        ).pack(pady=30)
    
    def start_level(self, level: int, seed: Optional[int] = None):
        """Démarre un niveau."""
        try:
            info = self.game.start_level(level, seed)
            self.found_cells = []
            self.show_game_screen()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer le niveau: {e}")
    
    def continue_game(self):
        """Continue la dernière partie sauvegardée."""
        state = self.save_manager.load_game("autosave")
        if state:
            self.game.load_game_state(state)
            self.found_cells = []
            self.show_game_screen()
        else:
            messagebox.showinfo("Info", "Aucune sauvegarde automatique trouvée.")
    
    def load_game_dialog(self):
        """Affiche le dialogue de chargement."""
        saves = self.save_manager.list_saves()
        
        if not saves:
            messagebox.showinfo("Info", "Aucune sauvegarde trouvée.")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Charger une partie")
        dialog.geometry("500x400")
        dialog.configure(bg=self.COLOR_BG)
        
        tk.Label(
            dialog,
            text="Sauvegardes disponibles",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        ).pack(pady=20)
        
        listbox = tk.Listbox(dialog, font=("Arial", 12), height=10)
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for save in saves:
            listbox.insert(tk.END, f"{save['name']} - Niveau {save['level']} - {save['timestamp'][:19]}")
        
        def load_selected():
            selection = listbox.curselection()
            if selection:
                save_name = saves[selection[0]]['name']
                state = self.save_manager.load_game(save_name)
                if state:
                    self.game.load_game_state(state)
                    self.found_cells = []
                    dialog.destroy()
                    self.show_game_screen()
        
        tk.Button(
            dialog,
            text="Charger",
            font=("Arial", 12),
            bg="#3498DB",
            fg="white",
            command=load_selected
        ).pack(pady=10)
    
    def save_game_dialog(self):
        """Dialogue pour sauvegarder la partie."""
        save_name = simpledialog.askstring("Sauvegarder", "Nom de la sauvegarde:")
        if save_name:
            self.save_manager.save_game(self.game.get_game_state(), save_name)
            messagebox.showinfo("Succès", f"Partie sauvegardée sous '{save_name}'!")
    
    def replay_seed_dialog(self):
        """Dialogue pour rejouer avec un seed."""
        seed = simpledialog.askinteger("Rejouer", "Entrez le seed:")
        if seed is not None:
            level = simpledialog.askinteger("Niveau", "Niveau (1-5):", minvalue=1, maxvalue=5)
            if level:
                self.start_level(level, seed)
    
    def show_game_screen(self):
        """Affiche l'écran de jeu."""
        self.clear_window()
        
        # Container principal
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête
        header = tk.Frame(main_frame, bg=self.COLOR_BG)
        header.pack(fill=tk.X, pady=(0, 20))
        
        self.level_label = tk.Label(
            header,
            text=f"Niveau {self.game.current_level.number}",
            font=("Arial", 20, "bold"),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        )
        self.level_label.pack(side=tk.LEFT)
        
        self.timer_label = tk.Label(
            header,
            text="⏱️ 00:00",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BG,
            fg="#E74C3C"
        )
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        
        self.score_label = tk.Label(
            header,
            text="🎯 Score: 0",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BG,
            fg="#F39C12"
        )
        self.score_label.pack(side=tk.RIGHT)
        
        seed_label = tk.Label(
            header,
            text=f"Seed: {self.game.seed}",
            font=("Arial", 12),
            bg=self.COLOR_BG,
            fg="#95A5A6"
        )
        seed_label.pack(side=tk.LEFT, padx=20)
        
        # Container pour la grille et la liste
        game_container = tk.Frame(main_frame, bg=self.COLOR_BG)
        game_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour la grille
        canvas_frame = tk.Frame(game_container, bg=self.COLOR_BG)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        grid_size = len(self.game.grid)
        self.cell_size = min(40, 600 // grid_size)
        canvas_width = grid_size * self.cell_size + 2 * self.grid_offset_x
        canvas_height = grid_size * self.cell_size + 2 * self.grid_offset_y
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg=self.COLOR_GRID_BG,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Bindings pour la sélection
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Liste des mots à droite
        words_frame = tk.Frame(game_container, bg=self.COLOR_WORD_LIST, width=250)
        words_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        words_frame.pack_propagate(False)
        
        tk.Label(
            words_frame,
            text="Mots à trouver",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_WORD_LIST,
            fg="#ECF0F1"
        ).pack(pady=20)
        
        # Scrollable frame pour les mots
        words_canvas = tk.Canvas(words_frame, bg=self.COLOR_WORD_LIST, highlightthickness=0)
        scrollbar = ttk.Scrollbar(words_frame, orient="vertical", command=words_canvas.yview)
        words_list = tk.Frame(words_canvas, bg=self.COLOR_WORD_LIST)
        
        words_list.bind(
            "<Configure>",
            lambda e: words_canvas.configure(scrollregion=words_canvas.bbox("all"))
        )
        
        words_canvas.create_window((0, 0), window=words_list, anchor="nw")
        words_canvas.configure(yscrollcommand=scrollbar.set)
        
        words_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.word_labels = {}
        for word_info in self.game.words_to_find:
            word = word_info['word']
            label = tk.Label(
                words_list,
                text=f"  {word}",
                font=("Arial", 14),
                bg=self.COLOR_WORD_LIST,
                fg="#ECF0F1",
                anchor="w"
            )
            label.pack(fill=tk.X, pady=5, padx=10)
            self.word_labels[word] = label
        
        self.draw_grid()
        self.start_timer()
    
    def draw_grid(self):
        """Dessine la grille de mots mêlés."""
        if not self.canvas or not self.game.grid:
            return
        
        self.canvas.delete("all")
        self.cell_rects = []
        self.cell_texts = []
        
        grid_size = len(self.game.grid)
        
        for i in range(grid_size):
            row_rects = []
            row_texts = []
            for j in range(grid_size):
                x = self.grid_offset_x + j * self.cell_size
                y = self.grid_offset_y + i * self.cell_size
                
                # Déterminer la couleur
                if (i, j) in self.found_cells:
                    color = self.COLOR_FOUND
                elif (i, j) in self.current_selection:
                    color = self.COLOR_SELECTED
                else:
                    color = self.COLOR_CELL
                
                # Dessiner la cellule
                rect = self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size,
                    fill=color,
                    outline=self.COLOR_CELL_BORDER,
                    width=2
                )
                
                # Dessiner la lettre
                text = self.canvas.create_text(
                    x + self.cell_size // 2,
                    y + self.cell_size // 2,
                    text=self.game.grid[i][j],
                    font=("Arial", self.cell_size // 2, "bold"),
                    fill=self.COLOR_TEXT
                )
                
                row_rects.append(rect)
                row_texts.append(text)
            
            self.cell_rects.append(row_rects)
            self.cell_texts.append(row_texts)
    
    def get_cell_from_coords(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Convertit les coordonnées canvas en indices de cellule."""
        if not self.game.grid:
            return None
        
        grid_size = len(self.game.grid)
        col = (x - self.grid_offset_x) // self.cell_size
        row = (y - self.grid_offset_y) // self.cell_size
        
        if 0 <= row < grid_size and 0 <= col < grid_size:
            return (row, col)
        return None
    
    def get_cells_in_line(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retourne toutes les cellules dans une ligne entre start et end."""
        cells = []
        row1, col1 = start
        row2, col2 = end
        
        # Calculer la direction
        dr = row2 - row1
        dc = col2 - col1
        
        # Normaliser la direction pour avoir -1, 0 ou 1
        steps = max(abs(dr), abs(dc))
        if steps == 0:
            return [start]
        
        dr = dr / steps
        dc = dc / steps
        
        # Vérifier si c'est une ligne valide (horizontale, verticale ou diagonale)
        if abs(dr) not in [0, 1] or abs(dc) not in [0, 1]:
            return [start]
        
        # Construire la liste des cellules
        for i in range(steps + 1):
            row = int(row1 + i * dr)
            col = int(col1 + i * dc)
            cells.append((row, col))
        
        return cells
    
    def on_mouse_down(self, event):
        """Gère le clic de souris."""
        cell = self.get_cell_from_coords(event.x, event.y)
        if cell:
            self.selecting = True
            self.selection_start = cell
            self.selection_end = cell
            self.current_selection = [cell]
            self.draw_grid()
    
    def on_mouse_drag(self, event):
        """Gère le glissement de souris."""
        if not self.selecting or not self.selection_start:
            return
        
        cell = self.get_cell_from_coords(event.x, event.y)
        if cell and cell != self.selection_end:
            self.selection_end = cell
            self.current_selection = self.get_cells_in_line(self.selection_start, self.selection_end)
            self.draw_grid()
    
    def on_mouse_up(self, event):
        """Gère le relâchement de souris."""
        if not self.selecting:
            return
        
        self.selecting = False
        
        # Extraire le mot sélectionné
        if self.current_selection:
            word = ''.join(self.game.grid[r][c] for r, c in self.current_selection)
            word_reverse = word[::-1]
            
            # Vérifier si le mot ou son inverse est correct
            if self.game.check_word(word):
                self.on_word_found(word, self.current_selection)
            elif self.game.check_word(word_reverse):
                self.on_word_found(word_reverse, self.current_selection)
        
        self.current_selection = []
        self.draw_grid()
    
    def on_word_found(self, word: str, cells: List[Tuple[int, int]]):
        """Appelé quand un mot est trouvé."""
        # Ajouter les cellules aux cellules trouvées
        self.found_cells.extend(cells)
        
        # Mettre à jour le label du mot
        if word in self.word_labels:
            self.word_labels[word].config(
                fg=self.COLOR_WORD_FOUND,
                font=("Arial", 14, "bold", "overstrike")
            )
        
        # Mettre à jour le score
        self.update_score()
        
        # Vérifier si le niveau est terminé
        if self.game.is_level_complete():
            self.timer_running = False
            self.level_complete()
        
        self.draw_grid()
    
    def start_timer(self):
        """Démarre le chronomètre."""
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Met à jour l'affichage du chronomètre."""
        if not self.timer_running:
            return
        
        remaining = self.game.get_remaining_time()
        
        if remaining <= 0:
            self.timer_running = False
            self.game_over()
            return
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        color = "#E74C3C" if remaining < 30 else "#F39C12" if remaining < 60 else "#2ECC71"
        self.timer_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}", fg=color)
        
        self.timer_id = self.root.after(100, self.update_timer)
    
    def update_score(self):
        """Met à jour l'affichage du score."""
        score = self.game.get_score()
        self.score_label.config(text=f"🎯 Score: {score}")
    
    def level_complete(self):
        """Affiche l'écran de niveau terminé."""
        score = self.game.get_score()
        level = self.game.current_level.number
        
        msg = f"🎉 Félicitations! 🎉\n\n"
        msg += f"Niveau {level} terminé!\n\n"
        msg += f"Score final: {score}\n"
        msg += f"Temps utilisé: {int(self.game.elapsed_time)}s\n"
        msg += f"Seed: {self.game.seed}"
        
        if level < len(GameLogic.LEVELS):
            msg += f"\n\nNiveau suivant débloqué!"
        
        result = messagebox.askquestion("Niveau Terminé", msg + "\n\nContinuer?")
        
        if result == 'yes' and level < len(GameLogic.LEVELS):
            self.start_level(level + 1)
        else:
            self.show_main_menu()
    
    def game_over(self):
        """Affiche l'écran de game over."""
        score = self.game.get_score()
        found = len(self.game.found_words)
        total = len(self.game.words_to_find)
        
        msg = f"⏱️ Temps écoulé! ⏱️\n\n"
        msg += f"Mots trouvés: {found}/{total}\n"
        msg += f"Score: {score}\n"
        msg += f"Seed: {self.game.seed}"
        
        result = messagebox.askquestion("Temps Écoulé", msg + "\n\nRejouer ce niveau?")
        
        if result == 'yes':
            self.start_level(self.game.current_level.number, self.game.seed)
        else:
            self.show_main_menu()
    
    def show_settings(self):
        """Affiche le dialogue des paramètres."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Paramètres")
        dialog.geometry("400x300")
        dialog.configure(bg=self.COLOR_BG)
        
        tk.Label(
            dialog,
            text="Paramètres",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        ).pack(pady=20)
        
        # Sélecteur de langue
        lang_frame = tk.Frame(dialog, bg=self.COLOR_BG)
        lang_frame.pack(pady=20)
        
        tk.Label(
            lang_frame,
            text=self.lang.get('language') + ":",
            font=("Arial", 14),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        ).pack(side=tk.LEFT, padx=10)
        
        lang_var = tk.StringVar(value=self.lang.current_language)
        
        for lang_code, lang_name in self.lang.get_available_languages():
            rb = tk.Radiobutton(
                lang_frame,
                text=lang_name,
                variable=lang_var,
                value=lang_code,
                font=("Arial", 12),
                bg=self.COLOR_BG,
                fg="#ECF0F1",
                selectcolor=self.COLOR_WORD_LIST,
                activebackground=self.COLOR_BG,
                activeforeground="#ECF0F1"
            )
            rb.pack(anchor=tk.W, padx=20)
        
        def apply_settings():
            new_lang = lang_var.get()
            if new_lang != self.lang.current_language:
                self.lang.set_language(new_lang)
                self.word_gen.set_language(new_lang)
                messagebox.showinfo(
                    "Succès",
                    self.lang.get('language_changed')
                )
                dialog.destroy()
                # Rafraîchir l'interface
                self.update_title()
                self.create_menu()
                self.show_main_menu()
            else:
                dialog.destroy()
        
        tk.Button(
            dialog,
            text="OK",
            font=("Arial", 12),
            width=15,
            bg="#3498DB",
            fg="white",
            relief="flat",
            command=apply_settings
        ).pack(pady=20)
    
    def show_help(self):
        """Affiche l'aide."""
        help_text = """
Comment jouer:

1. Cliquez sur la première lettre d'un mot
2. Maintenez le clic et glissez jusqu'à la dernière lettre
3. Relâchez le clic pour valider

Les mots peuvent être:
- Horizontaux (→)
- Verticaux (↓)
- Diagonaux (↘ ↗)
- Inversés (selon le niveau)

Trouvez tous les mots avant la fin du temps!
        """
        messagebox.showinfo("Comment jouer", help_text)
    
    def show_about(self):
        """Affiche les informations."""
        about_text = """
PyWordExplorer v1.0

Un jeu de mots mêlés en Python

Créé par Inkflow59
2025
        """
        messagebox.showinfo("À propos", about_text)


def main():
    """Lance l'application."""
    root = tk.Tk()
    app = WordSearchGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
