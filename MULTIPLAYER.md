# 🌐 Multiplayer Mode - PyWordExplorer

## 📋 Overview

Multiplayer mode allows you to play online with other players in two different modes:

- **🆚 Duel Mode**: Competition - Each player earns points for the words they find. The player with the most points wins!
- **🤝 Coop Mode**: Cooperation - Players work together to find all the words. All players earn points together.

## 🚀 Installation

### Prerequisites

Multiplayer mode requires the `websockets` library:

```bash
pip install websockets
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## 🎮 How to Play

### Step 1: Launch the Server

**Important**: The server must be launched **before** players can connect.

Open a terminal and run:

```bash
python server.py
```

You should see:

```
🎮 Multiplayer server started on 0.0.0.0:8765
   Duel Mode: Competition - player with most words found wins
   Coop Mode: Cooperation - find all words together
```

The server is now listening on port **8765**.

### Step 2: Launch the Game

Each player launches the game normally:

```bash
python main.py
```

### Step 3: Access Multiplayer

1. In the main menu, click on **🌐 Online Multiplayer**
2. Enter your **player name**
3. Enter the **server address**:
   - If playing locally: `localhost:8765`
   - If playing on network: `SERVER_IP:8765` (e.g., `192.168.1.100:8765`)
4. Click **Connect**

### Step 4: Create or Join a Game

#### Create a Game

1. Click on **🆚 Create DUEL game** or **🤝 Create COOP game**
2. Select the **difficulty level** (1 to 5)
3. (Optional) Enter a **seed** to generate a specific grid
4. Click **Create**
5. Wait for another player to join
6. Click **✓ Ready!** when you're ready to start

#### Join a Game

1. Available games are displayed in the list
2. Select a game
3. Click **Join selected game**
4. Click **✓ Ready!** when you're ready to start

### Step 5: Play

The game starts automatically when all players are ready!

#### Duel Mode 🆚

- Search and enter words as quickly as possible
- Each word found earns you **100 points**
- The player with the most points at the end wins
- Words already found by the opponent can no longer be found

#### Coop Mode 🤝

- Work together to find all the words
- Each word found earns **50 points for each player**
- Goal: find all words before time runs out
- Found words are shared among all players

## 🖥️ Network Configuration

### Playing Locally (same computer)

Server: `localhost:8765`

### Playing on the Same Local Network (LAN)

1. **On the server computer**:
   - Note your local IP address:
     - Windows: `ipconfig` → Look for "IPv4 Address"
     - Mac/Linux: `ifconfig` or `ip addr`
   - Example: `192.168.1.100`

2. **On client computers**:
   - Use the server's IP: `192.168.1.100:8765`

### Playing Over the Internet

To play over the Internet, you must:

1. **Configure the firewall** to allow port 8765
2. **Port forward** port 8765 on your router to the server computer
3. Clients use your **public IP**: `YOUR_PUBLIC_IP:8765`
   - Find your public IP at: https://www.whatismyip.com/

⚠️ **Warning**: Exposing a server on the Internet poses security risks. For private use, prefer local networks or use a VPN.

## 🔧 Advanced Options

### Change Server Port

Edit `server.py`, final line:

```python
server = MultiplayerServer(host='0.0.0.0', port=YOUR_PORT)
```

### Replay with a Specific Seed

When creating a game, you can enter a **seed** to generate exactly the same grid as a previous game. The seed is displayed during the game.

### Number of Players

Currently, multiplayer mode is configured for **2 players per game**. You can modify `max_players` in `server.py` to allow more players.

## ❓ Troubleshooting

### "Unable to connect to server"

- Verify that the server is running (`python server.py`)
- Check the IP address and port
- Check the firewall (Windows, antivirus, router)

### "Connection to server lost"

- The server may have crashed or been stopped
- Network connection problem
- Restart the server and reconnect

### Game doesn't start

- Verify that **all players** have clicked **✓ Ready!**
- The game must have exactly 2 players

## 📝 Technical Architecture

The multiplayer system uses:

- **WebSockets** for real-time communication
- **Client-server architecture**
- **Server.py**: Manages games, players, and game logic
- **NetworkClient**: Manages connection to the server from the client
- **MultiplayerGUI**: Lobby interface and game creation
- **MultiplayerGameWindow**: Multiplayer game interface

### Communication

Messages exchanged between client and server:
- `create_room`: Create a new game
- `join_room`: Join a game
- `player_ready`: Indicate you're ready
- `check_word`: Verify a word
- `game_start`: Game start
- `word_found`: A word has been found
- `game_over`: Game over

## 🎯 Gameplay Tips

### Duel Mode
- Be fast! The first one to find the word gets the points
- Scan the grid systematically
- Remember words already found by your opponent

### Coop Mode
- Communicate with your teammate (Discord, phone, etc.)
- Divide the grid to avoid searching for the same words
- Share your discoveries

## 🎊 Enjoy!

Have fun with PyWordExplorer's multiplayer mode!

For any questions or issues, consult the main README.md or open an issue on GitHub.
