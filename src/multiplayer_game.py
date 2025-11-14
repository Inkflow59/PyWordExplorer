"""
PyWordExplorer - Fenêtre de jeu multijoueur
Affiche la grille et gère le gameplay en ligne
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
import time


class MultiplayerGameWindow:
    """Fenêtre de jeu pour le mode multijoueur."""
    
    def __init__(self, parent, client, game_data, room_data):
        self.parent = parent
        self.client = client
        self.room_data = room_data
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"PyWordExplorer - {room_data['mode'].upper()}")
        self.window.geometry("1000x700")
        
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
        
        # Interface
        self.create_widgets()
        self.update_timer()
    
    def create_widgets(self):
        """Crée l'interface de jeu."""
        # En-tête
        header = ttk.Frame(self.window)
        header.pack(fill=tk.X, padx=10, pady=5)
        
        mode_emoji = "🆚" if self.mode == "duel" else "🤝"
        ttk.Label(header, text=f"{mode_emoji} {self.mode.upper()} - Niveau {self.room_data['level']}", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(header, text="⏱️ 00:00", font=('Arial', 14))
        self.timer_label.pack(side=tk.RIGHT)
        
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Partie gauche: Grille
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_grid(left_frame)
        
        # Partie droite: Infos
        right_frame = ttk.Frame(main_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Scores
        score_frame = ttk.LabelFrame(right_frame, text="📊 Scores", padding=10)
        score_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.score_text = tk.Text(score_frame, height=4, width=30, font=('Arial', 11))
        self.score_text.pack()
        self.score_text.config(state=tk.DISABLED)
        
        # Mots à trouver
        words_frame = ttk.LabelFrame(right_frame, text=f"🎯 Mots ({len(self.words)})", padding=10)
        words_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.words_listbox = tk.Listbox(words_frame, font=('Arial', 11), height=15)
        scrollbar = ttk.Scrollbar(words_frame, orient=tk.VERTICAL, command=self.words_listbox.yview)
        self.words_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.words_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for word in self.words:
            self.words_listbox.insert(tk.END, f"  {word}")
        
        # Zone de saisie
        input_frame = ttk.LabelFrame(right_frame, text="✍️ Entrer un mot", padding=10)
        input_frame.pack(fill=tk.X)
        
        self.word_entry = ttk.Entry(input_frame, font=('Arial', 12))
        self.word_entry.pack(fill=tk.X, pady=(0, 5))
        self.word_entry.bind('<Return>', lambda e: self.submit_word())
        
        ttk.Button(input_frame, text="Valider", command=self.submit_word).pack(fill=tk.X)
        
        # Message
        self.message_label = ttk.Label(right_frame, text="", font=('Arial', 10, 'italic'), foreground='blue')
        self.message_label.pack(pady=10)
        
        # Info seed
        ttk.Label(right_frame, text=f"Seed: {self.seed}", font=('Arial', 9), foreground='gray').pack()
    
    def create_grid(self, parent):
        """Crée la grille de jeu."""
        grid_frame = ttk.Frame(parent)
        grid_frame.pack(expand=True)
        
        grid_size = len(self.grid)
        cell_size = min(500 // grid_size, 40)
        
        self.grid_labels = []
        
        for i, row in enumerate(self.grid):
            row_labels = []
            for j, letter in enumerate(row):
                label = tk.Label(
                    grid_frame,
                    text=letter,
                    font=('Arial', cell_size // 2, 'bold'),
                    width=2,
                    height=1,
                    relief=tk.RAISED,
                    borderwidth=2,
                    bg='white'
                )
                label.grid(row=i, column=j, padx=1, pady=1)
                row_labels.append(label)
            self.grid_labels.append(row_labels)
    
    def submit_word(self):
        """Soumet un mot."""
        word = self.word_entry.get().strip().upper()
        if word:
            self.client.check_word(word)
            self.word_entry.delete(0, tk.END)
    
    def update_timer(self):
        """Met à jour le chronomètre."""
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            return
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        self.timer_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}")
        
        if remaining > 0:
            self.window.after(1000, self.update_timer)
        else:
            self.show_message("⏱️ Temps écoulé!", 'red')
    
    def update_scores(self, scores):
        """Met à jour l'affichage des scores."""
        self.scores = scores
        self.score_text.config(state=tk.NORMAL)
        self.score_text.delete('1.0', tk.END)
        
        for player, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            self.score_text.insert(tk.END, f"{player}: {score}\n")
        
        self.score_text.config(state=tk.DISABLED)
    
    def mark_word_found(self, word, finder):
        """Marque un mot comme trouvé."""
        if word not in self.found_words:
            self.found_words.append(word)
            
            # Mettre à jour la liste
            for i in range(self.words_listbox.size()):
                item = self.words_listbox.get(i).strip()
                if item == word:
                    self.words_listbox.delete(i)
                    if self.mode == "duel":
                        self.words_listbox.insert(i, f"✓ {word} ({finder})")
                    else:
                        self.words_listbox.insert(i, f"✓ {word}")
                    self.words_listbox.itemconfig(i, foreground='green')
                    break
    
    def show_message(self, text, color='blue'):
        """Affiche un message temporaire."""
        self.message_label.config(text=text, foreground=color)
        self.window.after(3000, lambda: self.message_label.config(text=""))
    
    # Callbacks réseau
    
    def on_word_found(self, data):
        """Un mot a été trouvé."""
        word = data['word']
        finder = data['finder']
        
        self.mark_word_found(word, finder)
        self.update_scores(data['scores'])
        
        if self.mode == "duel":
            self.show_message(f"✓ {word} trouvé par {finder}!", 'green')
        else:
            self.show_message(f"✓ {word} trouvé! 🎉", 'green')
    
    def on_word_invalid(self, data):
        """Mot invalide."""
        reason = data['reason']
        word = data['word']
        
        if reason == 'not_in_list':
            self.show_message(f"✗ '{word}' n'est pas dans la liste", 'red')
        elif reason == 'already_found':
            if self.mode == "duel" and 'by' in data:
                self.show_message(f"✗ '{word}' déjà trouvé par {data['by']}", 'orange')
            else:
                self.show_message(f"✗ '{word}' déjà trouvé", 'orange')
    
    def on_game_over(self, data):
        """Partie terminée."""
        winner = data['winner']
        scores = data['scores']
        found_words = data['found_words']
        
        # Créer la fenêtre de résultats
        result_window = tk.Toplevel(self.window)
        result_window.title("Partie terminée!")
        result_window.geometry("400x400")
        result_window.transient(self.window)
        
        frame = ttk.Frame(result_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        if self.mode == "duel":
            ttk.Label(frame, text=f"🏆 Victoire de {winner}!", 
                     font=('Arial', 18, 'bold')).pack(pady=10)
        else:
            if len(found_words) == len(self.words):
                ttk.Label(frame, text="🎉 Victoire d'équipe!", 
                         font=('Arial', 18, 'bold')).pack(pady=10)
            else:
                ttk.Label(frame, text="⏱️ Temps écoulé!", 
                         font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Scores
        ttk.Label(frame, text="Scores finaux:", font=('Arial', 14, 'bold')).pack(pady=10)
        for player, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            ttk.Label(frame, text=f"{player}: {score}", font=('Arial', 12)).pack()
        
        # Stats
        ttk.Label(frame, text=f"\nMots trouvés: {len(found_words)}/{len(self.words)}", 
                 font=('Arial', 12)).pack(pady=10)
        
        # Boutons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        def close_all():
            result_window.destroy()
            self.window.destroy()
        
        ttk.Button(btn_frame, text="Retour au lobby", command=close_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Quitter", command=self.parent.quit).pack(side=tk.LEFT, padx=5)
