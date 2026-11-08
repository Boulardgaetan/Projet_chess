## Project Goal

This project aims to create a single-game Elo performance estimator. Indeed, professional analysis tools often lack full features, preventing players from getting accurate free estimates.

That is why I intend to provide an open-source analyzer under the terms of the GNU General Public License v3.0.

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
├── calculate_model/           # Model calibration pipeline
│   ├── dataset.csv            # Extracted data for regression
<<<<<<< HEAD
│   ├── progress.json          # Indicates the state of the data acquisition
│   ├── extracted_games.pgn    # Extracted games by the script from_pgn_to_data.py
=======
>>>>>>> 1386e89577a6c9336ca98123e3031b8d626fd861
│   ├── games.pgn              # Official games used for calibration
│   ├── from_pgn_to_data.py    # Extracts reliable data into dataset.csv
│   ├── verify_brackets.py     # Verifies the brackets' homogeneity and the number of games
│   └── from_csv_to_model.py   # Calculates regression coefficients via scipy
│
├── partie.png                 # Sample game / PGN illustration
├── LICENSE                    # GNU GPLv3 License
├── README.md                  # Project documentation
├── run_calculate_model.py     # Runs the script from_pgn_to_data.py
└── run.py                     # Main entry point to launch scripts
```

## Prerequisites and Installation

### 1. Requirements
- **Python 3.10+**
- **Stockfish Engine**: Download the official Stockfish binary corresponding to your operating system from [stockfishchess.org](https://stockfishchess.org/). Extract the folder (rename it `stockfish`) and place it at the root of the project.
- **Opening Book (`Performance.bin`)**: Download the Polyglot opening book from [Chris Whittington's Polyglot Books repository](https://github.com/ChrisWhittington/polyglot-books) and place it inside the `assets/book_moves` directory (`assets/Performance.bin`).
- **Calibration Dataset (`games.pgn`)**: Download the official PGN games from [The Week in Chess - Issue #1666](https://theweekinchess.com/twic) and place it inside the `calculate_model/` directory (`calculate_model/games.pgn`).

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
python -m pip install pygame chess pandas numpy scipy matplotlib
```

## Methodology & Architecture

The pipeline processes raw chess games to estimate player performance through the following steps:

1. **Data Preprocessing & Filtering:**
   * Raw PGN games are parsed from the [TWIC - Issue #1666](https://theweekinchess.com/twic) dataset.
   * Theoretical moves are filtered out using the Polyglot opening book [`Performance.bin`](https://github.com/ChrisWhittington/polyglot-books) (containing 92,954 positions) to ensure that only independent decision-making phases are analyzed.

2. **Engine Evaluation:**
   * Cleaned moves are evaluated using [Stockfish 19](https://stockfishchess.org/) configured at `depth=14` with `MultiPV=5` to extract positional evaluations and centipawn loss metrics.

3. **Statistical Regression:**
   * A regression model is applied using Python's scipy library to map the analyzed metrics and determine the FIDE Elo performance in classic games by minimizing the RMSE.