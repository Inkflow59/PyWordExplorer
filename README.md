# 🔤 PyWordExplorer

An interactive word search game in Python with level system, seed-based random generation, and progress saving.

## ✨ Features

- **🌍 Multilingual**: French, English, Spanish with translated interface and words
- **📚 Complete Dictionaries**: Words pulled from real dictionaries (thousands of words per language)
- **🔄 Automatic Download**: Dictionaries are downloaded and cached on first launch
- **🎲 Random Generation**: Grids generated with a seed system for reproducibility
- **📊 5 Difficulty Levels**: From beginner to expert with increasing grids (8×8 to 16×16)
- **⏱️ Dynamic Timer**: Time adapted to each level (3 to 8 minutes)
- **💾 Auto-save**: Resume your game at any time
- **🎯 Scoring System**: Time bonus to reward speed
- **🔄 Replayability**: Replay any grid with its seed
- **🎨 Graphical Interface (Tkinter)**: Modern interface with click-and-drag system
- **🖱️ Intuitive Selection**: Find words by clicking and dragging on the grid
- **✅ Visual Validation**: Found words are highlighted in green
- **⚙️ Customizable Settings**: Change language at any time
- **🌐 Online Multiplayer**: Play with friends in Duel or Coop mode (requires websockets)

## 📋 Requirements

- Python 3.7 or higher
- No external dependencies for single-player (uses only standard library)
- For multiplayer mode: `websockets` library (install with `pip install websockets`)

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/Inkflow59/PyWordExplorer.git
cd PyWordExplorer
```

2. Launch the game:

```bash
python main.py
```

**Note**: On first launch, the game will automatically download word dictionaries from GitHub (about 1-2 MB per language). These dictionaries will be cached in the `dict_cache/` folder for later offline use.

## 🎮 How to Play

### Available Languages

The game is available in **3 languages** with **complete dictionaries**:

- 🇫🇷 **Français**: Over 324,000 French dictionary words
- 🇬🇧 **English**: Over 270,000 English dictionary words
- 🇪🇸 **Español**: Over 635,000 Spanish dictionary words

Words are **randomly selected** from real dictionaries for **infinite variety**!

Change language at any time via **Game → Settings**!

### Graphical Interface

The graphical interface offers an intuitive experience with:

- **Interactive Grid**: Click and drag to select words
- **Word List**: On the right side of the screen, found words are crossed out
- **Real-time Timer**: Display of remaining time with color coding
- **Dynamic Score**: Updated in real-time
- **Translated Interface**: All menus and messages in your language

### Starting a Game

1. **New Game**: Choose a level from 1 to 5
2. **Continue**: Resume your last saved game (if available)
3. **Load**: Select a specific save from the list
4. **Replay with Seed**: Enter a seed to replay an exact grid

### Game Controls

1. **Click** on the first letter of a word
2. **Hold and drag** to the last letter
3. **Release** to validate the selection

If the word is correct:

- ✅ Cells turn **green**
- ✅ The word is **crossed out** in the list
- ✅ Your **score** increases

### In-Game Menu

Use the menu bar at the top to:

- **Save** your game at any time
- **Return to main menu**
- **Access help** and information

### Objective

Find all hidden words in the grid before the timer runs out!

Words can be placed:

- **Horizontally** (→)
- **Vertically** (↓)
- **Diagonally** (↘ ↗) - From level 2
- **Backwards** - From level 4

💡 **Tip**: Words can be selected in both directions!

## 🌐 Multiplayer Mode

PyWordExplorer now supports **online multiplayer**! Play with friends in two exciting modes:

### Game Modes

- **🆚 Duel Mode**: Compete against other players - first to find a word wins the points!
- **🤝 Coop Mode**: Work together to find all words - share the victory!

### Quick Start

1. **Install the websockets library**:
   ```bash
   pip install websockets
   ```

2. **Launch the server** (one player hosts):
   ```bash
   python server.py
   ```

3. **Launch the game** (all players):
   ```bash
   python main.py
   ```

4. **Connect**: Click "🌐 Online Multiplayer" in the main menu

5. **Play**: Create or join a game, select a difficulty level, and start playing!

### Network Setup

- **Local play**: Use `localhost:8765`
- **LAN play**: Use server's local IP (e.g., `192.168.1.100:8765`)
- **Internet play**: Use server's public IP with port forwarding

For detailed multiplayer instructions, see [MULTIPLAYER.md](MULTIPLAYER.md).

## 📊 Levels

| Level | Size | Words | Time | Difficulty |
|-------|------|-------|------|------------|
| 1 - Beginner | 8×8 | 5 | 3 min | Horizontal, Vertical |
| 2 - Easy | 10×10 | 7 | 4 min | + Diagonals |
| 3 - Medium | 12×12 | 9 | 5 min | + Diagonals |
| 4 - Hard | 14×14 | 11 | 6 min | + Reversed words |
| 5 - Expert | 16×16 | 14 | 8 min | + Reversed words |

## 🏗️ Architecture

```
PyWordExplorer/
├── main.py                 # Main entry point
├── config.json             # Configuration (selected language)
├── requirements.txt        # Dependencies (none external!)
├── src/
│   ├── __init__.py
│   ├── gui.py              # Multilingual Tkinter GUI
│   ├── language.py         # Translation system (FR/EN/ES)
│   ├── word_generator.py   # Dynamic generator from dictionaries
│   ├── grid_generator.py   # Grid generation with seed
│   ├── game_logic.py       # Game logic and level system
│   ├── save_manager.py     # Save management (JSON)
│   └── word_lists.py       # [Legacy] French word lists
├── dict_cache/             # Downloaded dictionaries cache
│   ├── fr_words.txt        # ~324K French words
│   ├── en_words.txt        # ~270K English words
│   └── es_words.txt        # ~635K Spanish words
├── saves/                  # Save folder (created automatically)
└── README.md
```

## 💡 Usage Examples

### First Launch

On first startup, the game automatically downloads dictionaries from GitHub:

```
⏳ Downloading dictionary fr...
✓ Dictionary fr downloaded (324290 words)
⏳ Downloading dictionary en...
✓ Dictionary en downloaded (270528 words)
⏳ Downloading dictionary es...
✓ Dictionary es downloaded (635005 words)
```

Dictionaries are then **cached** locally for **offline** use.

### Replay a Specific Grid

If you enjoyed a particular grid, note its **seed** (displayed at the top of the screen) and use the "Replay with seed" option to regenerate it exactly.

### Share a Challenge

Share your seed with friends so they can play the same grid as you!

```
Level 3 | Seed: 123456
```

## 🎯 Scoring System

Score is calculated as follows:

- **100 points** per word found
- **Time bonus**: 2 points per remaining second

Example: 9 words found with 45 seconds remaining = 900 + 90 = **990 points**

## 🔧 Customization

### Add Your Own Words

Edit `src/word_lists.py` to add your own words or create new categories:

```python
FRENCH_WORDS = [
    "YOUR", "NEW", "WORD",
    # ... add your words here
]
```

### Modify Levels

In `src/game_logic.py`, modify the `LEVELS` list:

```python
LEVELS = [
    Level(1, size, nb_words, time, diagonals, reversed),
    # ...
]
```

## 📝 Save Format

Saves are stored in JSON format in the `saves/` folder:

```json
{
  "timestamp": "2025-10-31T12:00:00",
  "version": "1.0",
  "game_state": {
    "level": 3,
    "seed": 123456,
    "found_words": ["CHAT", "CHIEN"],
    "remaining_time": 180.5
  }
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Add word lists
- Improve documentation

## 📜 License

This project is under MIT license. See the `LICENSE` file for more details.

## 📸 Screenshots

### Main Menu

Modern interface with clear buttons to start a new game, continue, load, or replay with a seed.

### Game Screen

- **Interactive Grid** with clickable cells
- **Word List** on the right side
- **Timer** and **score** in real-time
- **Seed display** for replayability

### Visual Feedback

- **Blue**: Selection in progress
- **Green**: Word found and validated
- **White**: Unused letters

## 🎨 Possible Future Improvements

- [x] Graphical interface (Tkinter) ✅
- [x] Multilingual support (FR/EN/ES) ✅
- [x] Dynamic word generator ✅
- [x] Online multiplayer mode ✅
- [ ] Animations when discovering words
- [ ] Sound effects
- [ ] Detailed statistics (progress charts)
- [ ] Selectable word themes in the interface
- [ ] Visual hint system (with penalty)
- [ ] Arcade mode (limited time per word)
- [ ] Online leaderboard with daily seed
- [ ] More languages (German, Italian, Portuguese, etc.)
- [ ] Customizable color themes
- [ ] Integrated dictionary for word definitions

## 👨‍💻 Author

**Inkflow59** - [GitHub](https://github.com/Inkflow59)

## 🙏 Acknowledgments

Thank you for choosing PyWordExplorer! Have fun! 🎉

---

*Created with ❤️ in Python*
