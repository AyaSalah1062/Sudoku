# Sudoku Solver

Welcome to the Sudoku Solver project! This application allows you to play Sudoku puzzles interactively or let the AI solve them for you.

## Table of Contents
- [Features](#features)
- [Game Information](#game-information)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
### Mode Selection
Choose between two modes to interact with the Sudoku Solver:
- **AI Mode**: Let the AI solve Sudoku puzzles automatically.
- **User Mode**: Play Sudoku puzzles interactively by manually entering numbers.

### Puzzle Difficulty Levels
Select from three difficulty levels for generated puzzles:
- **Easy**: Suitable for beginners.
- **Intermediate**: Moderate challenge.
- **Hard**: Challenging for experienced players.

### Sudoku Grid Interaction
- **Manual Input**:
  - Click on cells to input numbers during User mode.
  - Real-time validation ensures adherence to Sudoku rules.
- **Puzzle Generation**:
  - Generate puzzles manually by inputting numbers.
  - Randomly generate puzzles based on the selected difficulty level.

### Solver
- **Constraint Satisfaction Problem (CSP) Solver**:
  - Uses an efficient CSP algorithm to solve Sudoku puzzles.
  - Displays solver time upon successful completion of puzzles.

## Game Information
Sudoku is a logic-based, combinatorial number-placement puzzle. The objective is to fill a 9x9 grid with digits (1-9) so that each column, each row, and each of the nine 3x3 subgrids (also called "regions", "boxes", or "blocks") contain all of the digits from 1 to 9.

The game begins with some cells already filled; these are the "givens". The player needs to complete the grid while following the standard Sudoku rules:
- Each row must contain all digits from 1 to 9 without repetition.
- Each column must contain all digits from 1 to 9 without repetition.
- Each 3x3 subgrid (box) must contain all digits from 1 to 9 without repetition.

## Usage
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/AyaSalah1062/sudoku.git
