from algos import bfs, dfs
import sys

isDebug = False

if len(sys.argv) > 1:
    MAZE_FILE = sys.argv[1]
    if sys.argv[2] is None or sys.argv[2] == 0:
        isDebug = False
    elif sys.argv[2] is not None and sys.argv[2] == 1:
        isDebug = True
else:
    MAZE_FILE = "maze1.txt"

print(sys.argv[2])

bfsSolver = bfs(MAZE_FILE, isDebug=isDebug)  # or dfs() for depth-first search
dfsSolver = dfs(MAZE_FILE, isDebug=isDebug)  # or dfs() for depth-first search

print("______________________________________________________________________________________")
print("Starting BFS Solver...")
bfsSolver.solve()

print("\n\n\n______________________________________________________________________________________")
print("Starting DFS Solver...")
dfsSolver.solve()