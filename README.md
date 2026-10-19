## Project Goal

This project aims to create a single-game Elo performance estimator. Indeed, professional analysis tools often lack full features, preventing players from getting accurate free estimates.

That is why I intend to provide an open-source analyzer under the terms of the GNU General Public License v3.0.

## Project architecture

## Project Structure

```text
/Projet_chess
│
├── assets/                    # Images, sounds, and opening book
├── env1/                      # Python virtual environment
├── stockfish/                 # Stockfish engine binary
│   └── stockfish.exe
│
├── src/                       # Main source code directory
│   ├── __init__.py
│   ├── chess_analyser.py      # Handles moves analysis
│   ├── gui.py                 # Handles the graphical interface
│   ├── parser.py              # Extracts games from PGN files
│   ├── utils.py               # Utilitary methods
│   └── game.py                # Event handling and coordination
│
├── from_games_to_regression/  # Model calibration pipeline
│   ├── dataset.csv            # Extracted data for regression
│   ├── Performance.bin        # Book moves filtered out from analysis
│   ├── games.pgn              # Official games used for calibration
│   ├── from_pgn_to_data.py    # Extracts reliable data into dataset.csv
│   └── from_dataset_to_model.py # Calculates regression coefficients via scipy
│
├── partie.png                 # Sample game / PGN illustration
├── LICENSE                    # GNU GPLv3 License
├── README.md                  # Project documentation
└── run.py                     # Main entry point to launch scripts
```

## Prerequisites and Installation

### 1. Requirements
- **Python 3.10+**
- **Stockfish Engine**: Download the official Stockfish binary corresponding to your operating system from [stockfishchess.org](https://stockfishchess.org/). Extract the folder (rename it `stockfish`) and place it at the root of the project.

### 2. Setup Virtual Environment (Recommended)
*Note: Make sure you are at the root of the project repository before running these commands.*

Create and activate an isolated Python environment:

- **On Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows**
  ```Powershell
  python -m venv venv
  venv/Scripts/activate.ps1
  ```

### 3. Python Dependencies
Install the required packages within your active environment:

```bash
pip install pygame chess pandas numpy scipy
```

## Dependencies and Tools
- **Stockfish**: Used for analyzing positions (`depth=14`, `MultiPV=5`). More information on the engine's official website: [stockfishchess.org](https://stockfishchess.org/).
