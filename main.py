from pathAlgos import bfs, dfs
from helper import FileParser
import sys

""" 
Main script to run pathfinding algorithms on a maze file. 
- This script reads a maze file. 
- It initializes the mazeruns both BFS and DFS algorithms to find a path from the start to the goal.
- Usage: python main.py <maze_file> [debug]
"""

# Handle arg valuess
if len(sys.argv) > 1:
    MAZE_FILE = sys.argv[1]
else:
    MAZE_FILE = "maze1.txt"
isDebug = False
if len(sys.argv)>2:
    if sys.argv[2] is None or sys.argv[2] == 0:
        isDebug = False
    elif sys.argv[2] == 1:
        isDebug = True

fileParser = FileParser(MAZE_FILE) 
text = fileParser.parse_file()

bfsSolver = bfs(text, isDebug=isDebug)  # or dfs() for depth-first search
dfsSolver = dfs(text, isDebug=isDebug)  # or dfs() for depth-first search

print("______________________________________________________________________________________")
print("Starting BFS Solver...")
bfsSolver.solve()

print("\n\n\n______________________________________________________________________________________")
print("Starting DFS Solver...")
dfsSolver.solve()