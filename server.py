"""
PyWordExplorer - Serveur Multijoueur
Gère les parties en ligne (Duel et Coop)
"""
import asyncio
import websockets
import json
import random
from datetime import datetime
from typing import Dict, Set, Optional, Any
from src.word_generator import get_word_generator
from src.grid_generator import GridGenerator, GridConfig


class GameRoom:
    """Représente une salle de jeu multijoueur."""
    
    def __init__(self, room_id: str, host_name: str, mode: str, level: int, seed: Optional[int] = None):
        self.room_id = room_id
        self.host_name = host_name
        self.mode = mode  # "duel" ou "coop"
        self.level = level
        self.seed = seed or random.randint(1000, 9999999)
        self.players: Dict[Any, dict] = {}
        self.max_players = 2
        self.game_started = False
        self.created_at = datetime.now()
        
        # État du jeu
        self.grid = None
        self.words_to_find = []
        self.found_words = {}  # {word: player_name} pour duel, {word: True} pour coop
        self.player_scores = {}  # {player_name: score}
        self.start_time = None
        self.game_duration = self._get_game_duration()
    
    def _get_game_duration(self) -> int:
        """Retourne la durée de jeu en secondes selon le niveau."""
        durations = {1: 180, 2: 240, 3: 300, 4: 360, 5: 480}
        return durations.get(self.level, 300)
    
    def add_player(self, websocket, player_name: str) -> bool:
        """Ajoute un joueur à la room."""
        if len(self.players) >= self.max_players:
            return False
        
        self.players[websocket] = {
            'name': player_name,
            'ready': False
        }
        self.player_scores[player_name] = 0
        return True
    
    def remove_player(self, websocket):
        """Retire un joueur de la room."""
        if websocket in self.players:
            player_name = self.players[websocket]['name']
            del self.players[websocket]
            if player_name in self.player_scores:
                del self.player_scores[player_name]
    
    def is_full(self) -> bool:
        """Vérifie si la room est pleine."""
        return len(self.players) >= self.max_players
    
    def all_players_ready(self) -> bool:
        """Vérifie si tous les joueurs sont prêts."""
        return len(self.players) >= 2 and all(p['ready'] for p in self.players.values())
    
    def start_game(self):
        """Démarre la partie."""
        # Générer la grille et les mots
        word_gen = get_word_generator()
        all_words = word_gen.get_words()
        
        sizes = {1: (8, 5), 2: (10, 7), 3: (12, 9), 4: (14, 11), 5: (16, 14)}
        grid_size, word_count = sizes.get(self.level, (10, 7))
        
        generator = GridGenerator(self.seed)
        selected_words = random.Random(self.seed).sample(all_words, word_count)
        
        config = GridConfig(size=grid_size, num_words=word_count, allow_diagonal=True, allow_reverse=True)
        self.grid, self.words_to_find = generator.generate_grid(config, selected_words)
        self.game_started = True
        self.start_time = datetime.now()
        
        # Initialiser les mots trouvés
        if self.mode == "coop":
            self.found_words = {}
        else:  # duel
            self.found_words = {}
    
    def check_word(self, player_name: str, word: str) -> dict:
        """Vérifie si un mot est valide et met à jour le score."""
        word = word.upper()
        
        # Vérifier si le mot existe dans la liste
        word_data = next((w for w in self.words_to_find if w['word'] == word), None)
        if not word_data:
            return {'valid': False, 'reason': 'not_in_list'}
        
        # Vérifier si le mot a déjà été trouvé
        if word in self.found_words:
            if self.mode == "duel":
                return {'valid': False, 'reason': 'already_found', 'by': self.found_words[word]}
            else:  # coop
                return {'valid': False, 'reason': 'already_found'}
        
        # Mot valide!
        if self.mode == "duel":
            self.found_words[word] = player_name
            self.player_scores[player_name] = self.player_scores.get(player_name, 0) + 100
        else:  # coop
            self.found_words[word] = True
            # En coop, tous les joueurs gagnent des points
            for pname in self.player_scores:
                self.player_scores[pname] = self.player_scores.get(pname, 0) + 50
        
        return {
            'valid': True,
            'word': word,
            'finder': player_name,
            'scores': self.player_scores,
            'found_count': len(self.found_words),
            'total_words': len(self.words_to_find)
        }
    
    def is_game_over(self) -> bool:
        """Vérifie si la partie est terminée."""
        if not self.game_started:
            return False
        
        # Tous les mots trouvés
        if len(self.found_words) >= len(self.words_to_find):
            return True
        
        # Temps écoulé
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            if elapsed >= self.game_duration:
                return True
        
        return False
    
    def get_winner(self) -> Optional[str]:
        """Retourne le nom du gagnant (pour le mode duel)."""
        if self.mode == "coop":
            return "Team"
        
        if not self.player_scores:
            return None
        
        return max(self.player_scores.items(), key=lambda x: x[1])[0]
    
    def to_dict(self) -> dict:
        """Convertit la room en dictionnaire pour l'envoi."""
        return {
            'room_id': self.room_id,
            'host_name': self.host_name,
            'mode': self.mode,
            'level': self.level,
            'seed': self.seed,
            'player_count': len(self.players),
            'max_players': self.max_players,
            'game_started': self.game_started,
            'players': [p['name'] for p in self.players.values()]
        }


class MultiplayerServer:
    """Serveur de jeu multijoueur."""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.rooms: Dict[str, GameRoom] = {}
        self.clients: Set[Any] = set()
    
    async def handle_client(self, websocket: Any):
        """Gère la connexion d'un client."""
        self.clients.add(websocket)
        current_room = None
        
        try:
            async for message in websocket:
                data = json.loads(message)
                action = data.get('action')
                
                if action == 'list_rooms':
                    await self.send_room_list(websocket)
                
                elif action == 'create_room':
                    room = await self.create_room(
                        data['player_name'],
                        data['mode'],
                        data['level'],
                        data.get('seed')
                    )
                    current_room = room.room_id
                    room.add_player(websocket, data['player_name'])
                    await self.broadcast_room_update(room)
                    await websocket.send(json.dumps({
                        'type': 'room_created',
                        'room': room.to_dict()
                    }))
                
                elif action == 'join_room':
                    room = self.rooms.get(data['room_id'])
                    if room and not room.is_full() and not room.game_started:
                        if room.add_player(websocket, data['player_name']):
                            current_room = room.room_id
                            await self.broadcast_to_room(room, {
                                'type': 'player_joined',
                                'player_name': data['player_name'],
                                'room': room.to_dict()
                            })
                            await websocket.send(json.dumps({
                                'type': 'joined_room',
                                'room': room.to_dict()
                            }))
                    else:
                        await websocket.send(json.dumps({
                            'type': 'error',
                            'message': 'Cannot join room'
                        }))
                
                elif action == 'player_ready':
                    if current_room:
                        room = self.rooms[current_room]
                        if websocket in room.players:
                            room.players[websocket]['ready'] = True
                            await self.broadcast_to_room(room, {
                                'type': 'player_ready',
                                'player_name': room.players[websocket]['name']
                            })
                            
                            if room.all_players_ready():
                                room.start_game()
                                await self.broadcast_to_room(room, {
                                    'type': 'game_start',
                                    'grid': room.grid,
                                    'words': [w['word'] for w in room.words_to_find],
                                    'duration': room.game_duration,
                                    'seed': room.seed
                                })
                
                elif action == 'check_word':
                    if current_room:
                        room = self.rooms[current_room]
                        player_name = room.players[websocket]['name']
                        result = room.check_word(player_name, data['word'])
                        
                        if result['valid']:
                            await self.broadcast_to_room(room, {
                                'type': 'word_found',
                                'word': result['word'],
                                'finder': result['finder'],
                                'scores': result['scores'],
                                'found_count': result['found_count'],
                                'total_words': result['total_words']
                            })
                        else:
                            await websocket.send(json.dumps({
                                'type': 'word_invalid',
                                'reason': result['reason'],
                                'word': data['word']
                            }))
                        
                        # Vérifier fin de partie
                        if room.is_game_over():
                            winner = room.get_winner()
                            await self.broadcast_to_room(room, {
                                'type': 'game_over',
                                'winner': winner,
                                'scores': room.player_scores,
                                'found_words': list(room.found_words.keys())
                            })
                
                elif action == 'leave_room':
                    if current_room:
                        room = self.rooms[current_room]
                        player_name = room.players[websocket]['name']
                        room.remove_player(websocket)
                        current_room = None
                        
                        await self.broadcast_to_room(room, {
                            'type': 'player_left',
                            'player_name': player_name
                        })
                        
                        # Supprimer la room si vide
                        if len(room.players) == 0:
                            del self.rooms[room.room_id]
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            if current_room and current_room in self.rooms:
                room = self.rooms[current_room]
                if websocket in room.players:
                    player_name = room.players[websocket]['name']
                    room.remove_player(websocket)
                    await self.broadcast_to_room(room, {
                        'type': 'player_left',
                        'player_name': player_name
                    })
                    if len(room.players) == 0:
                        del self.rooms[room.room_id]
    
    async def create_room(self, host_name: str, mode: str, level: int, seed: Optional[int] = None) -> GameRoom:
        """Crée une nouvelle room."""
        room_id = f"ROOM_{random.randint(1000, 9999)}"
        room = GameRoom(room_id, host_name, mode, level, seed)
        self.rooms[room_id] = room
        return room
    
    async def send_room_list(self, websocket):
        """Envoie la liste des rooms disponibles."""
        available_rooms = [
            room.to_dict()
            for room in self.rooms.values()
            if not room.is_full() and not room.game_started
        ]
        
        await websocket.send(json.dumps({
            'type': 'room_list',
            'rooms': available_rooms
        }))
    
    async def broadcast_to_room(self, room: GameRoom, message: dict):
        """Envoie un message à tous les joueurs d'une room."""
        if room.players:
            message_json = json.dumps(message)
            await asyncio.gather(
                *[ws.send(message_json) for ws in room.players.keys()],
                return_exceptions=True
            )
    
    async def broadcast_room_update(self, room: GameRoom):
        """Notifie tous les clients d'une mise à jour de room."""
        message = json.dumps({
            'type': 'room_updated',
            'room': room.to_dict()
        })
        await asyncio.gather(
            *[client.send(message) for client in self.clients],
            return_exceptions=True
        )
    
    async def start(self):
        """Démarre le serveur."""
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"🎮 Serveur multijoueur démarré sur {self.host}:{self.port}")
            print(f"   Mode Duel: Compétition - le joueur avec le plus de mots trouvés gagne")
            print(f"   Mode Coop: Coopération - trouvez tous les mots ensemble")
            await asyncio.Future()  # Run forever


async def main():
    """Lance le serveur."""
    server = MultiplayerServer(host='0.0.0.0', port=8765)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Serveur arrêté!")
