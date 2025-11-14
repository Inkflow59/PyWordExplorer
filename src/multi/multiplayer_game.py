"""
PyWordExplorer - Fenêtre de jeu multijoueur
Affiche la grille et gère le gameplay en ligne avec sélection visuelle
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Optional, Dict
import time


class MultiplayerGameWindow:
    """Fenêtre de jeu pour le mode multijoueur avec interface de sélection visuelle."""
    
    # Couleurs (reprises du mode solo)
    COLOR_BG = "#2C3E50"
    COLOR_GRID_BG = "#ECF0F1"
    COLOR_CELL = "#FFFFFF"
    COLOR_CELL_BORDER = "#BDC3C7"
    COLOR_SELECTED = "#3498DB"
    COLOR_FOUND = "#2ECC71"
    COLOR_TEXT = "#2C3E50"
    COLOR_WORD_LIST = "#34495E"
    
    # Couleurs pour les mots trouvés (variées)
    WORD_COLORS = [
        "#E74C3C",  # Rouge
        "#3498DB",  # Bleu
        "#2ECC71",  # Vert
        "#F39C12",  # Orange
        "#9B59B6",  # Violet
        "#1ABC9C",  # Turquoise
        "#E67E22",  # Carotte
        "#34495E",  # Gris foncé
        "#16A085",  # Vert turquoise
        "#C0392B",  # Rouge foncé
        "#2980B9",  # Bleu foncé
        "#27AE60",  # Vert foncé
        "#D35400",  # Citrouille
        "#8E44AD",  # Violet foncé
        "#2C3E50",  # Bleu nuit
    ]
    
    def __init__(self, parent, client, game_data, room_data):
        self.parent = parent
        self.client = client
        self.room_data = room_data
        
        self.window = tk.Toplevel(parent)
        mode_text = "DUEL" if room_data['mode'] == 'duel' else "COOP"
        self.window.title(f"PyWordExplorer - Multijoueur {mode_text}")
        self.window.geometry("1200x800")
        self.window.configure(bg=self.COLOR_BG)
        
        # Données de jeu
        self.grid = game_data['grid']
        self.words = game_data['words']
        self.duration = game_data['duration']
        self.seed = game_data['seed']
        self.mode = room_data['mode']
        
        # État du jeu
        self.found_words = []
        self.scores = {}
        self.start_time = time.time()
        
        # État de sélection (comme le mode solo)
        self.selecting = False
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_end: Optional[Tuple[int, int]] = None
        self.current_selection: List[Tuple[int, int]] = []
        self.found_cells: List[Tuple[int, int]] = []
        self.cell_colors: Dict[Tuple[int, int], str] = {}
        self.color_index: int = 0
        
        # UI elements
        self.canvas = None
        self.cell_size = 40
        self.grid_offset_x = 50
        self.grid_offset_y = 50
        self.cell_rects = []
        self.cell_texts = []
        self.word_labels = {}
        
        # Timer
        self.timer_running = True
        
        # Interface
        self.create_widgets()
        self.update_timer()
    
    def create_widgets(self):
        """Crée l'interface de jeu."""
        # Container principal
        main_frame = tk.Frame(self.window, bg=self.COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête
        header = tk.Frame(main_frame, bg=self.COLOR_BG)
        header.pack(fill=tk.X, pady=(0, 20))
        
        mode_emoji = "🆚" if self.mode == "duel" else "🤝"
        mode_text = "DUEL" if self.mode == "duel" else "COOPÉRATION"
        
        self.level_label = tk.Label(
            header,
            text=f"{mode_emoji} {mode_text} - Niveau {self.room_data['level']}",
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
        
        seed_label = tk.Label(
            header,
            text=f"Seed: {self.seed}",
            font=("Arial", 12),
            bg=self.COLOR_BG,
            fg="#95A5A6"
        )
        seed_label.pack(side=tk.LEFT, padx=20)
        
        # Container pour la grille et les infos
        game_container = tk.Frame(main_frame, bg=self.COLOR_BG)
        game_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour la grille (côté gauche)
        canvas_frame = tk.Frame(game_container, bg=self.COLOR_BG)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        grid_size = len(self.grid)
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
        
        # Bindings pour la sélection (comme le mode solo)
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Panel de droite
        right_panel = tk.Frame(game_container, bg=self.COLOR_BG, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        right_panel.pack_propagate(False)
        
        # Scores
        score_frame = tk.LabelFrame(
            right_panel, 
            text="📊 Scores", 
            bg=self.COLOR_WORD_LIST,
            fg="#ECF0F1",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=10
        )
        score_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.score_text = tk.Text(
            score_frame, 
            height=4, 
            width=30, 
            font=('Arial', 12),
            bg=self.COLOR_WORD_LIST,
            fg="#ECF0F1",
            relief=tk.FLAT
        )
        self.score_text.pack()
        self.score_text.config(state=tk.DISABLED)
        
        # Liste des mots à trouver
        words_frame = tk.LabelFrame(
            right_panel,
            text=f"🎯 Mots à trouver ({len(self.words)})",
            bg=self.COLOR_WORD_LIST,
            fg="#ECF0F1",
            font=("Arial", 14, "bold"),
            padx=10,
            pady=10
        )
        words_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
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
        
        # Permettre le défilement avec la molette
        def on_mousewheel(event):
            words_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        words_canvas.bind_all("<MouseWheel>", on_mousewheel)
        words_list.bind("<MouseWheel>", on_mousewheel)
        
        words_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.word_labels = {}
        for word in self.words:
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
        
        # Message de statut
        self.message_label = tk.Label(
            right_panel,
            text="✨ Sélectionnez les mots dans la grille!",
            font=('Arial', 11, 'italic'),
            bg=self.COLOR_BG,
            fg="#3498DB",
            wraplength=280
        )
        self.message_label.pack(pady=10)
        
        # Dessiner la grille initiale
        self.draw_grid()
    
    def draw_grid(self):
        """Dessine la grille de mots mêlés."""
        if not self.canvas or not self.grid:
            return
        
        self.canvas.delete("all")
        self.cell_rects = []
        self.cell_texts = []
        
        grid_size = len(self.grid)
        
        for i in range(grid_size):
            row_rects = []
            row_texts = []
            for j in range(grid_size):
                x = self.grid_offset_x + j * self.cell_size
                y = self.grid_offset_y + i * self.cell_size
                
                # Déterminer la couleur
                if (i, j) in self.found_cells:
                    color = self.cell_colors.get((i, j), self.COLOR_FOUND)
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
                    text=self.grid[i][j],
                    font=("Arial", self.cell_size // 2, "bold"),
                    fill=self.COLOR_TEXT
                )
                
                row_rects.append(rect)
                row_texts.append(text)
            
            self.cell_rects.append(row_rects)
            self.cell_texts.append(row_texts)
    
    def get_cell_from_coords(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Convertit les coordonnées canvas en indices de cellule."""
        if not self.grid:
            return None
        
        grid_size = len(self.grid)
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
        """Gère le relâchement de souris - envoie le mot au serveur."""
        if not self.selecting:
            return
        
        self.selecting = False
        
        # Extraire le mot sélectionné
        if self.current_selection:
            word = ''.join(self.grid[r][c] for r, c in self.current_selection)
            word_reverse = word[::-1]
            
            # Envoyer le mot au serveur (ou son inverse)
            # Le serveur vérifiera si c'est correct
            if word in self.words or word_reverse in self.words:
                # Envoyer le mot qui est dans la liste
                word_to_send = word if word in self.words else word_reverse
                self.client.check_word(word_to_send)
        
        self.current_selection = []
        self.draw_grid()
    
    def mark_word_found(self, word: str, finder: str, cells: Optional[List[Tuple[int, int]]] = None):
        """Marque un mot comme trouvé avec sélection visuelle."""
        if word not in self.found_words:
            self.found_words.append(word)
            
            # Choisir une couleur pour ce mot
            word_color = self.WORD_COLORS[self.color_index % len(self.WORD_COLORS)]
            self.color_index += 1
            
            # Si des cellules sont fournies, les utiliser
            if cells:
                self.found_cells.extend(cells)
                for cell in cells:
                    self.cell_colors[cell] = word_color
            
            # Mettre à jour le label du mot
            if word in self.word_labels:
                if self.mode == "duel":
                    self.word_labels[word].config(
                        text=f"✓ {word} ({finder})",
                        fg=word_color,
                        font=("Arial", 14, "bold", "overstrike")
                    )
                else:
                    self.word_labels[word].config(
                        fg=word_color,
                        font=("Arial", 14, "bold", "overstrike")
                    )
            
            self.draw_grid()
    
    def update_timer(self):
        """Met à jour le chronomètre."""
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            return
        
        if not self.timer_running:
            return
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        color = "#E74C3C" if remaining < 30 else "#F39C12" if remaining < 60 else "#2ECC71"
        self.timer_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}", fg=color)
        
        if remaining > 0:
            self.window.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.show_message("⏱️ Temps écoulé!", '#E74C3C')
    
    def update_scores(self, scores):
        """Met à jour l'affichage des scores."""
        self.scores = scores
        self.score_text.config(state=tk.NORMAL)
        self.score_text.delete('1.0', tk.END)
        
        for player, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            emoji = "🏆" if score == max(scores.values()) and len(scores) > 1 else "👤"
            self.score_text.insert(tk.END, f"{emoji} {player}: {score}\n")
        
        self.score_text.config(state=tk.DISABLED)
    
    def show_message(self, text, color='#3498DB'):
        """Affiche un message temporaire."""
        self.message_label.config(text=text, fg=color)
        self.window.after(3000, lambda: self.message_label.config(text="✨ Sélectionnez les mots dans la grille!"))
    
    # Callbacks réseau
    
    def on_word_found(self, data):
        """Un mot a été trouvé."""
        word = data['word']
        finder = data['finder']
        
        # On peut optionnellement recevoir les cellules du serveur, sinon on devine
        cells = data.get('cells', None)
        
        self.mark_word_found(word, finder, cells)
        self.update_scores(data['scores'])
        
        if self.mode == "duel":
            if finder == self.room_data.get('player_name', ''):
                self.show_message(f"✓ Vous avez trouvé '{word}'! 🎉", '#2ECC71')
            else:
                self.show_message(f"{finder} a trouvé '{word}'", '#F39C12')
        else:
            self.show_message(f"✓ '{word}' trouvé par {finder}! 🎉", '#2ECC71')
    
    def on_word_invalid(self, data):
        """Mot invalide."""
        reason = data['reason']
        word = data.get('word', '')
        
        if reason == 'not_in_list':
            self.show_message(f"✗ '{word}' n'est pas dans la liste", '#E74C3C')
        elif reason == 'already_found':
            if self.mode == "duel" and 'by' in data:
                self.show_message(f"✗ '{word}' déjà trouvé par {data['by']}", '#E67E22')
            else:
                self.show_message(f"✗ '{word}' déjà trouvé", '#E67E22')
    
    def on_game_over(self, data):
        """Partie terminée."""
        self.timer_running = False
        
        winner = data.get('winner', '')
        scores = data.get('scores', {})
        found_words = data.get('found_words', [])
        
        # Créer la fenêtre de résultats
        result_window = tk.Toplevel(self.window)
        result_window.title("Partie terminée!")
        result_window.geometry("450x500")
        result_window.configure(bg=self.COLOR_BG)
        result_window.transient(self.window)
        
        frame = tk.Frame(result_window, bg=self.COLOR_BG, padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        if self.mode == "duel":
            tk.Label(
                frame,
                text=f"🏆 Victoire de {winner}!",
                font=('Arial', 20, 'bold'),
                bg=self.COLOR_BG,
                fg="#F39C12"
            ).pack(pady=15)
        else:
            if len(found_words) == len(self.words):
                tk.Label(
                    frame,
                    text="🎉 Victoire d'équipe!",
                    font=('Arial', 20, 'bold'),
                    bg=self.COLOR_BG,
                    fg="#2ECC71"
                ).pack(pady=15)
            else:
                tk.Label(
                    frame,
                    text="⏱️ Temps écoulé!",
                    font=('Arial', 20, 'bold'),
                    bg=self.COLOR_BG,
                    fg="#E74C3C"
                ).pack(pady=15)
        
        # Scores
        tk.Label(
            frame,
            text="Scores finaux:",
            font=('Arial', 16, 'bold'),
            bg=self.COLOR_BG,
            fg="#ECF0F1"
        ).pack(pady=15)
        
        for player, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            emoji = "🥇" if score == max(scores.values()) else "🥈"
            tk.Label(
                frame,
                text=f"{emoji} {player}: {score} points",
                font=('Arial', 14),
                bg=self.COLOR_BG,
                fg="#ECF0F1"
            ).pack(pady=3)
        
        # Stats
        tk.Label(
            frame,
            text=f"\nMots trouvés: {len(found_words)}/{len(self.words)}",
            font=('Arial', 13),
            bg=self.COLOR_BG,
            fg="#BDC3C7"
        ).pack(pady=10)
        
        # Boutons
        btn_frame = tk.Frame(frame, bg=self.COLOR_BG)
        btn_frame.pack(pady=25)
        
        def close_all():
            result_window.destroy()
            self.window.destroy()
        
        tk.Button(
            btn_frame,
            text="Retour au lobby",
            font=("Arial", 12),
            bg="#3498DB",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=close_all
        ).pack(side=tk.LEFT, padx=8)
        
        tk.Button(
            btn_frame,
            text="Quitter",
            font=("Arial", 12),
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            command=self.parent.quit
        ).pack(side=tk.LEFT, padx=8)
