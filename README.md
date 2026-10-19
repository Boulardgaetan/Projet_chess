## Project Goal

This project aims to create a single-game Elo performance estimator. Indeed, professional analysis tools often lack full features, preventing players from getting accurate free estimates.

That is why I intend to provide an open-source analyzer under the terms of the GNU General Public License v3.0.

## Prerequisites and Installation

### 1. Requirements
- **Python 3.10+**
- **Stockfish Engine**: Download the official Stockfish binary corresponding to your operating system from [stockfishchess.org](https://stockfishchess.org/). Extract the folder (rename it `stockfish`) and place it at the root of the project.

### 2. Python Dependencies
Install the required Python packages using `pip`:

```bash
pip install pygame chess pandas numpy scipy
```

## Dependencies and Tools
- **Stockfish**: Used for analyzing positions (`depth=14`, `MultiPV=5`). More information on the engine's official website: [stockfishchess.org](https://stockfishchess.org/).
