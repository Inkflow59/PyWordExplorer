"""
PyWordExplorer - Interface Multijoueur
Interface graphique pour le mode multijoueur en ligne
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.network_client import NetworkClient
import time


class MultiplayerGUI:
    """Interface graphique pour le multijoueur."""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("PyWordExplorer - Multijoueur")
        self.window.geometry("800x600")
        
        self.client = NetworkClient()
        self.current_room = None
        self.player_name = ""
        self.game_window = None
        
        # Configuration des callbacks réseau
        self.setup_network_callbacks()
        
        # Afficher l'écran de connexion
        self.show_connection_screen()
    
    def setup_network_callbacks(self):
        """Configure les callbacks pour les événements réseau."""
        self.client.on('room_list', self.on_room_list)
        self.client.on('room_created', self.on_room_created)
        self.client.on('joined_room', self.on_joined_room)
        self.client.on('player_joined', self.on_player_joined)
        self.client.on('player_left', self.on_player_left)
        self.client.on('player_ready', self.on_player_ready)
        self.client.on('game_start', self.on_game_start)
        self.client.on('word_found', self.on_word_found)
        self.client.on('word_invalid', self.on_word_invalid)
        self.client.on('game_over', self.on_game_over)
        self.client.on('error', self.on_error)
        self.client.on('disconnected', self.on_disconnected)
    
    def show_connection_screen(self):
        """Affiche l'écran de connexion."""
        for widget in self.window.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="🌐 Connexion Multijoueur", font=('Arial', 20, 'bold')).pack(pady=20)
        
        # Nom du joueur
        ttk.Label(frame, text="Nom du joueur:").pack(pady=5)
        name_entry = ttk.Entry(frame, width=30, font=('Arial', 12))
        name_entry.pack(pady=5)
        name_entry.insert(0, self.player_name or "Joueur1")
        
        # Adresse du serveur
        ttk.Label(frame, text="Serveur:").pack(pady=5)
        server_entry = ttk.Entry(frame, width=30, font=('Arial', 12))
        server_entry.pack(pady=5)
        server_entry.insert(0, "localhost:8765")
        
        def connect():
            self.player_name = name_entry.get().strip()
            server = server_entry.get().strip()
            
            if not self.player_name:
                messagebox.showerror("Erreur", "Veuillez entrer un nom de joueur")
                return
            
            # Construire l'URL du serveur
            if ':' in server:
                host, port = server.split(':')
                self.client.server_url = f"ws://{host}:{port}"
            else:
                self.client.server_url = f"ws://{server}:8765"
            
            # Se connecter
            self.client.connect()
            time.sleep(0.5)  # Attendre la connexion
            
            if self.client.connected:
                self.show_lobby()
            else:
                messagebox.showerror("Erreur", "Impossible de se connecter au serveur")
        
        ttk.Button(frame, text="Se connecter", command=connect).pack(pady=20)
        ttk.Button(frame, text="Retour", command=self.window.destroy).pack(pady=5)
    
    def show_lobby(self):
        """Affiche le lobby avec la liste des parties."""
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # En-tête
        header = ttk.Frame(self.window)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header, text=f"🎮 Lobby - {self.player_name}", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header, text="Actualiser", command=self.refresh_rooms).pack(side=tk.RIGHT, padx=5)
        ttk.Button(header, text="Déconnexion", command=self.disconnect).pack(side=tk.RIGHT)
        
        # Boutons de création
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="🆚 Créer partie DUEL", 
                  command=lambda: self.show_create_room_dialog("duel")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🤝 Créer partie COOP", 
                  command=lambda: self.show_create_room_dialog("coop")).pack(side=tk.LEFT, padx=5)
        
        # Liste des parties
        list_frame = ttk.LabelFrame(self.window, text="Parties disponibles", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer le Treeview
        columns = ('room_id', 'host', 'mode', 'level', 'players')
        self.room_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.room_tree.heading('room_id', text='ID')
        self.room_tree.heading('host', text='Hôte')
        self.room_tree.heading('mode', text='Mode')
        self.room_tree.heading('level', text='Niveau')
        self.room_tree.heading('players', text='Joueurs')
        
        self.room_tree.column('room_id', width=100)
        self.room_tree.column('host', width=150)
        self.room_tree.column('mode', width=100)
        self.room_tree.column('level', width=80)
        self.room_tree.column('players', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.room_tree.yview)
        self.room_tree.configure(yscroll=scrollbar.set)
        
        self.room_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton rejoindre
        ttk.Button(self.window, text="Rejoindre la partie sélectionnée", 
                  command=self.join_selected_room).pack(pady=10)
        
        # Charger les parties
        self.refresh_rooms()
    
    def show_create_room_dialog(self, mode):
        """Affiche le dialogue de création de partie."""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Créer une partie {mode.upper()}")
        dialog.geometry("400x250")
        dialog.transient(self.window)
        
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Mode info
        mode_text = "🆚 DUEL: Compétition - le joueur avec le plus de mots gagne!" if mode == "duel" else "🤝 COOP: Coopération - trouvez tous les mots ensemble!"
        ttk.Label(frame, text=mode_text, wraplength=350).pack(pady=10)
        
        # Niveau
        ttk.Label(frame, text="Niveau de difficulté:").pack(pady=5)
        level_var = tk.IntVar(value=2)
        level_frame = ttk.Frame(frame)
        level_frame.pack(pady=5)
        
        for i in range(1, 6):
            ttk.Radiobutton(level_frame, text=str(i), variable=level_var, value=i).pack(side=tk.LEFT, padx=5)
        
        # Seed (optionnel)
        ttk.Label(frame, text="Seed (optionnel):").pack(pady=5)
        seed_entry = ttk.Entry(frame, width=20)
        seed_entry.pack(pady=5)
        
        def create():
            level = level_var.get()
            seed_text = seed_entry.get().strip()
            seed = int(seed_text) if seed_text.isdigit() else None
            
            self.client.create_room(self.player_name, mode, level, seed)
            dialog.destroy()
        
        ttk.Button(frame, text="Créer", command=create).pack(pady=10)
        ttk.Button(frame, text="Annuler", command=dialog.destroy).pack()
    
    def refresh_rooms(self):
        """Actualise la liste des parties."""
        self.client.list_rooms()
    
    def join_selected_room(self):
        """Rejoint la partie sélectionnée."""
        selection = self.room_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une partie")
            return
        
        room_id = self.room_tree.item(selection[0])['values'][0]
        self.client.join_room(room_id, self.player_name)
    
    def show_waiting_room(self, room_data):
        """Affiche la salle d'attente."""
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.current_room = room_data
        
        frame = ttk.Frame(self.window, padding=20)
        frame.pack(expand=True)
        
        # Info partie
        mode_emoji = "🆚" if room_data['mode'] == "duel" else "🤝"
        ttk.Label(frame, text=f"{mode_emoji} Salle d'attente - {room_data['mode'].upper()}", 
                 font=('Arial', 18, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text=f"ID: {room_data['room_id']}", font=('Arial', 12)).pack()
        ttk.Label(frame, text=f"Niveau: {room_data['level']}", font=('Arial', 12)).pack()
        ttk.Label(frame, text=f"Seed: {room_data['seed']}", font=('Arial', 12)).pack(pady=10)
        
        # Liste des joueurs
        ttk.Label(frame, text="Joueurs:", font=('Arial', 14, 'bold')).pack(pady=10)
        self.players_label = ttk.Label(frame, text="\n".join(room_data['players']), font=('Arial', 12))
        self.players_label.pack(pady=10)
        
        # Boutons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="✓ Prêt!", command=self.mark_ready).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Quitter", command=self.leave_room).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(frame, text="En attente des joueurs...", font=('Arial', 11, 'italic'))
        self.status_label.pack(pady=10)
    
    def mark_ready(self):
        """Marque le joueur comme prêt."""
        self.client.player_ready()
        self.status_label.config(text="✓ Vous êtes prêt! En attente des autres joueurs...")
    
    def leave_room(self):
        """Quitte la salle d'attente."""
        self.client.leave_room()
        self.current_room = None
        self.show_lobby()
    
    def disconnect(self):
        """Déconnexion du serveur."""
        self.client.disconnect()
        self.show_connection_screen()
    
    # Callbacks réseau
    
    def on_room_list(self, data):
        """Reçoit la liste des parties."""
        if hasattr(self, 'room_tree'):
            # Effacer la liste actuelle
            for item in self.room_tree.get_children():
                self.room_tree.delete(item)
            
            # Ajouter les parties
            for room in data['rooms']:
                mode_icon = "🆚" if room['mode'] == "duel" else "🤝"
                self.room_tree.insert('', tk.END, values=(
                    room['room_id'],
                    room['host_name'],
                    f"{mode_icon} {room['mode']}",
                    room['level'],
                    f"{room['player_count']}/{room['max_players']}"
                ))
    
    def on_room_created(self, data):
        """Partie créée avec succès."""
        self.show_waiting_room(data['room'])
    
    def on_joined_room(self, data):
        """Rejoint une partie avec succès."""
        self.show_waiting_room(data['room'])
    
    def on_player_joined(self, data):
        """Un joueur a rejoint la partie."""
        if self.current_room and hasattr(self, 'players_label'):
            self.current_room = data['room']
            self.players_label.config(text="\n".join(data['room']['players']))
    
    def on_player_left(self, data):
        """Un joueur a quitté la partie."""
        if hasattr(self, 'players_label'):
            messagebox.showinfo("Info", f"{data['player_name']} a quitté la partie")
    
    def on_player_ready(self, data):
        """Un joueur est prêt."""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"{data['player_name']} est prêt!")
    
    def on_game_start(self, data):
        """La partie démarre."""
        # Fermer la fenêtre d'attente et ouvrir la fenêtre de jeu
        from src.multiplayer_game import MultiplayerGameWindow
        self.game_window = MultiplayerGameWindow(self.window, self.client, data, self.current_room)
    
    def on_word_found(self, data):
        """Un mot a été trouvé."""
        if self.game_window:
            self.game_window.on_word_found(data)
    
    def on_word_invalid(self, data):
        """Mot invalide."""
        if self.game_window:
            self.game_window.on_word_invalid(data)
    
    def on_game_over(self, data):
        """Partie terminée."""
        if self.game_window:
            self.game_window.on_game_over(data)
    
    def on_error(self, data):
        """Erreur réseau."""
        messagebox.showerror("Erreur", data.get('message', 'Erreur inconnue'))
    
    def on_disconnected(self, data):
        """Déconnecté du serveur."""
        messagebox.showwarning("Déconnexion", "Connexion au serveur perdue")
        self.show_connection_screen()
