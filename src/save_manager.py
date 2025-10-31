"""
Gestionnaire de sauvegarde des parties.
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime


class SaveManager:
    """Gère la sauvegarde et le chargement des parties."""
    
    def __init__(self, save_directory: str = "saves"):
        """
        Initialise le gestionnaire de sauvegarde.
        
        Args:
            save_directory: Répertoire où stocker les sauvegardes
        """
        self.save_directory = save_directory
        self._ensure_save_directory()
    
    def _ensure_save_directory(self):
        """Crée le répertoire de sauvegarde s'il n'existe pas."""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def save_game(self, game_state: Dict, save_name: str = "autosave") -> str:
        """
        Sauvegarde l'état du jeu.
        
        Args:
            game_state: État du jeu à sauvegarder
            save_name: Nom de la sauvegarde
            
        Returns:
            Chemin du fichier de sauvegarde
        """
        # Ajouter des métadonnées
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0',
            'game_state': game_state
        }
        
        # Générer le nom du fichier
        filename = f"{save_name}.json"
        filepath = os.path.join(self.save_directory, filename)
        
        # Sauvegarder en JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_game(self, save_name: str = "autosave") -> Optional[Dict]:
        """
        Charge l'état d'un jeu sauvegardé.
        
        Args:
            save_name: Nom de la sauvegarde à charger
            
        Returns:
            État du jeu ou None si la sauvegarde n'existe pas
        """
        filename = f"{save_name}.json"
        filepath = os.path.join(self.save_directory, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return save_data.get('game_state')
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement: {e}")
            return None
    
    def list_saves(self) -> list:
        """
        Liste toutes les sauvegardes disponibles.
        
        Returns:
            Liste des noms de sauvegarde avec leurs informations
        """
        saves = []
        
        if not os.path.exists(self.save_directory):
            return saves
        
        for filename in os.listdir(self.save_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(self.save_directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        save_data = json.load(f)
                    
                    save_name = filename[:-5]  # Enlever .json
                    timestamp = save_data.get('timestamp', 'Inconnu')
                    level = save_data.get('game_state', {}).get('level', 'N/A')
                    
                    saves.append({
                        'name': save_name,
                        'timestamp': timestamp,
                        'level': level,
                        'filepath': filepath
                    })
                except (json.JSONDecodeError, IOError):
                    continue
        
        # Trier par date (plus récent en premier)
        saves.sort(key=lambda x: x['timestamp'], reverse=True)
        return saves
    
    def delete_save(self, save_name: str) -> bool:
        """
        Supprime une sauvegarde.
        
        Args:
            save_name: Nom de la sauvegarde à supprimer
            
        Returns:
            True si supprimé avec succès, False sinon
        """
        filename = f"{save_name}.json"
        filepath = os.path.join(self.save_directory, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                return True
            except IOError:
                return False
        
        return False
    
    def has_autosave(self) -> bool:
        """
        Vérifie si une sauvegarde automatique existe.
        
        Returns:
            True si une autosave existe
        """
        return self.load_game("autosave") is not None
