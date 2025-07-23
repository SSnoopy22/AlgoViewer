import sys
from pathAlgos import bfs, dfs
from helper import FileParser

"""
Main script to run pathfinding algorithms on a maze file.

Usage:
    python main.py <maze_file> [debug]

Arguments:
    maze_file : str  - Path to the maze file (required)
    debug     : bool - Optional flag: 1 = debug mode ON, 0 or missing = OFF
"""

def parse_args(args):
    """
    Parse CLI arguments.
    Returns:
        - maze_file: str
        - is_debug: bool
    """
    maze_file = args[1] if len(args) > 1 else "maze1.txt"
    debug_flag = args[2] if len(args) > 2 else "0"
    is_debug = debug_flag == "1"
    return maze_file, is_debug

def run_solver(SolverClass, maze_text, is_debug, label):
    print(f"\n{'='*30} {label} Solver {'='*30}")
    solver = SolverClass(maze_text, isDebug=is_debug)
    solver.solve()

def main():
    maze_file, is_debug = parse_args(sys.argv)

    # Read maze file
    try:
        file_parser = FileParser(maze_file)
        maze_text = file_parser.parse_file()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Debug Mode: {'ON' if is_debug else 'OFF'}")

    # Run Solvers
    run_solver(bfs, maze_text, is_debug, "BFS")
    run_solver(dfs, maze_text, is_debug, "DFS")

if __name__ == "__main__":
    main()
