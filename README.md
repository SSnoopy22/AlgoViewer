# AlgoViewer 🧭

*A lightweight, terminal-friendly maze pathfinding visualizer for teaching and experimenting with classic graph search algorithms in Python.*

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Command-Line Usage](#command-line-usage)
- [Maze File Format](#maze-file-format)
- [Sample Mazes](#sample-mazes)
- [Debug Mode Output](#debug-mode-output)
- [Project Structure](#project-structure)
- [Architecture & Key Classes](#architecture--key-classes)
- [Extending: Add Your Own Algorithm](#extending-add-your-own-algorithm)
- [Development Roadmap / TODOs](#development-roadmap--todos)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AlgoViewer** lets you load ASCII mazes, then watch search algorithms work their way from **start** (`A`) to **goal** (`B`). It’s built for learning: code is intentionally readable, debug printouts are color-coded, and the maze controller exposes helper functions (move validation, marking explored cells, goal detection) that make it easy to plug in additional search strategies.

Current implementations: **Breadth-First Search (BFS)** & **Depth-First Search (DFS)**.

---

## Features

- ✅ Parse maze text files from *any* path (absolute, relative, or filename-only) via `FileParser`.
- ✅ Terminal rendering of mazes with ANSI color formatting.
- ✅ Pluggable search algorithms (BFS, DFS implemented; framework supports more).
- ✅ Debug mode: step‑wise state, legal actions, and counts of explored nodes.
- ✅ Handles uneven row lengths (detects and can fill/pad rows; see TODOs).
- ✅ Marks explored states and can render solved mazes.

---

## Quick Start

```bash
# Clone (SSH)
git clone git@github.com:SSnoopy22/AlgoViewer.git

# or HTTPS
git clone https://github.com/SSnoopy22/AlgoViewer.git

cd AlgoViewer/pathFindingAlgosPython

# Run with a sample maze
python main.py mazes/maze1.txt 1   # debug on
```

**Python Version:** 3.7+ recommended.

---

## Command-Line Usage

```bash
python main.py <maze_file> [debug]
```

**Arguments**

| Arg         | Required | Description                                                                                                   | Default     |
| ----------- | -------- | ------------------------------------------------------------------------------------------------------------- | ----------- |
| `maze_file` | ✅        | Path to maze text file. Can be relative, absolute, or just filename; the helper will search the current tree. | `maze1.txt` |
| `debug`     | ❌        | `1` to enable debug mode; `0` or omit for normal mode.                                                        | `0`         |

**Examples**

```bash
python main.py mazes/maze3.txt           # normal run
python main.py /full/path/maze5.txt 1    # debug run, absolute path
python main.py maze2.txt 0               # explicit debug off
```

---

## Maze File Format

A maze is a plain‑text grid of characters. Each character is a cell:

| Char  | Meaning                                     |
| ----- | ------------------------------------------- |
| `A`   | Start position (exactly **one** required)   |
| `B`   | Goal position (exactly **one** required)    |
| `#`   | Wall / impassable                           |
| `_`   | Open traversable cell                       |
| space | Also treated as open (when parsing actions) |

**Rules:**

- Maze *must* contain exactly one `A` and one `B` or initialization will raise `ValueError`.
- Rows may be uneven lengths; internal logic tracks `maxWidth` and can pad/fill (see [Development Roadmap](#development-roadmap--todos)).

---

## Sample Mazes

Sample files live in `mazes/`.

``

```
##___B
##_##_
##_#__
#__###
A_####
```

Try others: `maze2.txt`, `maze3.txt`, `maze4.txt`, `maze5.txt`.

---

## Debug Mode Output

When debug is enabled (`debug=1`):

- Prints the current player position each turn.
- Shows the current maze state rendered in color.
- Displays valid move options from the current cell (up/down/left/right) excluding walls and the start.
- Logs explored node counts during search.

Use this to *see the difference* between DFS’s stack behavior and BFS’s queue ordering.

---

## Project Structure

```
AlgoViewer/
├── pathFindingAlgosPython/
│   ├── main.py                # CLI entry point; runs BFS & DFS
│   ├── pathAlgos.py           # Algorithm classes: bfs, dfs, base class
│   ├── mazeController.py      # Maze class: parsing, printing, moves, marking
│   ├── helper.py              # FileParser + Node + Frontier data structures
│   ├── mazes/                 # Sample maze text files
│   │   ├── maze1.txt
│   │   ├── maze2.txt
│   │   ├── maze3.txt
│   │   ├── maze4.txt
│   │   └── maze5.txt
│   └── LICENSE                # MIT License
└── README.md                  # You are here
```

---

## Architecture & Key Classes

### `Maze` (in `mazeController.py`)

Responsible for parsing maze text, validating the presence of `A` and `B`, tracking dimensions, and rendering output. Provides helpers used by the algorithms:

- `getInitialState()` → `(y, x)` start
- `getEndPosition()` → `(y, x)` goal
- `getActions(state)` → dict of valid moves `{"up": True, ...}`
- `movePlayer(state, direction)` → new `(y, x)`
- `isAtGoal(state)` → bool
- `markExplored(cells)` → returns a maze copy with explored cells marked
- `printMaze(state, ...)` / `printMarkedMaze()` → colorized terminal display

### `Node` (in `helper.py`)

Lightweight search node: `state`, `parent`, `action`.

### Frontier Implementations (in `helper.py`)

- `StackFrontier` → LIFO; used by DFS
- `QueueFrontier` → FIFO; used by BFS

### Algorithms (in `pathAlgos.py`)

Base class `algos` wires up the maze + frontier + debug flags. Subclasses implement `solve()`:

- `bfs` → explores neighbors in breadth-first order using `QueueFrontier`.
- `dfs` → explores depth-first using `StackFrontier`.

Each solver:

1. Initializes from the maze text.
2. Creates the start node from `Maze.getInitialState()`.
3. Expands legal moves via `Maze.getActions()`.
4. Stops when `Maze.isAtGoal()` is true.
5. Reconstructs and prints the solution path + stats.

---

## Extending: Add Your Own Algorithm

Want to implement **A**\*, **Greedy Best‑First**, or **Dijkstra**? Suggested steps:

1. Import or write a **priority frontier** (heap‑based) that stores `(priority, Node)`.
2. Write a subclass (e.g., `astar`) that inherits from `algos` in `pathAlgos.py`.
3. Use `Maze.getActions()` to expand neighbors.
4. Use Manhattan distance (`abs(dy) + abs(dx)`) as a heuristic for grids.
5. Track cost so far (for A\* / Dijkstra) in a dict keyed by state.
6. Reuse `printMaze()` during expansion if `isDebug` is enabled.

If you’d like, open an Issue and I’ll help scaffold the code.

---

## Development Roadmap / TODOs

Pulled from in‑code comments and discussion:

### PathAlgos
- Convert self.maze to take in a maze object instead of a file path so the maze can be a different type of object with the same function names
- Explored States and Frontier does not mark position on map.

### MazeController
- Convert isDebug to an inherited class variable for mazeController class.
- Remove isDebug from the constructor and use a class variable instead

---

## Contributing

Pull requests welcome! Please:

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/my-idea`.
3. Follow PEP‑8 style where practical.
4. Include sample mazes or tests when adding algorithms.
5. Open a descriptive PR.

---

## License

This project is released under the **MIT License**. See the [`LICENSE`](./LICENSE) file for details.

---

**Happy exploring!** If you build a cool maze or implement A\*, tag the repo and share it.

