"""
PyWordExplorer - Client Réseau
Gère la communication avec le serveur multijoueur
"""
import asyncio
import websockets
import json
from typing import Callable, Optional, Any
import threading


class NetworkClient:
    """Client pour la communication avec le serveur multijoueur."""
    
    def __init__(self, server_url='ws://localhost:8765'):
        self.server_url = server_url
        self.websocket: Optional[Any] = None
        self.connected = False
        self.callbacks = {}
        self.receive_task = None
        self.loop = None
        self.thread = None
    
    def on(self, event_type: str, callback: Callable):
        """Enregistre un callback pour un type d'événement."""
        self.callbacks[event_type] = callback
    
    async def _connect(self):
        """Établit la connexion avec le serveur."""
        try:
            print(f"🔄 Tentative de connexion à {self.server_url}...")
            self.websocket = await asyncio.wait_for(
                websockets.connect(self.server_url),
                timeout=10.0
            )
            self.connected = True
            print(f"✓ Connecté au serveur {self.server_url}")
            return True
        except asyncio.TimeoutError:
            print(f"✗ Timeout: impossible de joindre le serveur {self.server_url}")
            self.connected = False
            if 'connection_failed' in self.callbacks:
                self.callbacks['connection_failed']({'error': 'timeout'})
            return False
        except ConnectionRefusedError:
            print(f"✗ Connexion refusée: le serveur n'est pas accessible sur {self.server_url}")
            self.connected = False
            if 'connection_failed' in self.callbacks:
                self.callbacks['connection_failed']({'error': 'refused'})
            return False
        except Exception as e:
            print(f"✗ Erreur de connexion: {type(e).__name__}: {e}")
            self.connected = False
            if 'connection_failed' in self.callbacks:
                self.callbacks['connection_failed']({'error': str(e)})
            return False
    
    async def _receive_messages(self):
        """Boucle de réception des messages du serveur."""
        if not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                event_type = data.get('type')
                
                if event_type in self.callbacks:
                    # Exécuter le callback dans le thread principal (GUI)
                    callback = self.callbacks[event_type]
                    if asyncio.iscoroutinefunction(callback):
                        await callback(data)
                    else:
                        callback(data)
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
            if 'disconnected' in self.callbacks:
                self.callbacks['disconnected']({})
        except Exception as e:
            print(f"Erreur de réception: {e}")
            self.connected = False
    
    async def _send(self, data: dict):
        """Envoie un message au serveur."""
        if self.websocket and self.connected:
            try:
                await self.websocket.send(json.dumps(data))
            except Exception as e:
                print(f"Erreur d'envoi: {e}")
                self.connected = False
    
    def _run_event_loop(self):
        """Exécute la boucle d'événements asyncio dans un thread séparé."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def run():
            if await self._connect():
                self.receive_task = asyncio.create_task(self._receive_messages())
                await self.receive_task
        
        try:
            self.loop.run_until_complete(run())
        except Exception as e:
            print(f"Erreur dans la boucle d'événements: {e}")
        finally:
            self.loop.close()
    
    def connect(self):
        """Démarre la connexion dans un thread séparé."""
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self.thread.start()
            # Attendre que la connexion s'établisse
            import time
            max_wait = 3.0  # Attendre jusqu'à 3 secondes
            elapsed = 0.0
            while elapsed < max_wait and not self.connected:
                time.sleep(0.1)
                elapsed += 0.1
    
    def send(self, data: dict):
        """Envoie un message de manière thread-safe."""
        if self.loop and self.connected:
            asyncio.run_coroutine_threadsafe(self._send(data), self.loop)
    
    def disconnect(self):
        """Ferme la connexion."""
        if self.loop:
            async def close():
                if self.websocket:
                    await self.websocket.close()
            
            asyncio.run_coroutine_threadsafe(close(), self.loop)
            self.connected = False
    
    # Méthodes pratiques pour les actions communes
    
    def list_rooms(self):
        """Demande la liste des rooms disponibles."""
        self.send({'action': 'list_rooms'})
    
    def create_room(self, player_name: str, mode: str, level: int, seed: Optional[int] = None):
        """Crée une nouvelle room."""
        data = {
            'action': 'create_room',
            'player_name': player_name,
            'mode': mode,
            'level': level
        }
        if seed:
            data['seed'] = seed
        self.send(data)
    
    def join_room(self, room_id: str, player_name: str):
        """Rejoint une room existante."""
        self.send({
            'action': 'join_room',
            'room_id': room_id,
            'player_name': player_name
        })
    
    def player_ready(self):
        """Indique que le joueur est prêt."""
        self.send({'action': 'player_ready'})
    
    def check_word(self, word: str):
        """Vérifie un mot."""
        self.send({
            'action': 'check_word',
            'word': word
        })
    
    def leave_room(self):
        """Quitte la room actuelle."""
        self.send({'action': 'leave_room'})
