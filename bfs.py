from helper import Node, StackFrontier, QueueFrontier
from mazeGenerator import Maze

# Generate the maze
maze = Maze('maze1.txt')

"""Initialize BFS variables"""
num_explored = 0 # Create a variable to count the number of explored nodes

start = Node(maze.getInitialState(), parent=None, action=None) # Create Start Node
frontier = StackFrontier() # Initialize Frontier
frontier.add(start) # Add the start node to the frontier

explored = [] # Create a set to keep track of explored nodes

while True:
    print("\n\n---------------------------------------------------")  # Print the current state of the frontier
    print("Current Frontier:")  # Print the Frontier
    for state in frontier.frontier:
        maze.printMaze(state.state, debug=True)
    print("Explored States:")  # Print the current state of the maze
    for state in explored:
        maze.printMaze(state, isSpecial=True)
    if frontier.is_empty():
        raise Exception("No solution found")  # If the frontier is empty, no solution exists
    node = frontier.remove()  # Remove a node from the frontier
    num_explored += 1  # Increment the number of explored nodes

    if maze.isAtGoal(node.state):
        actions = []
        cells = []
        while node.parent is not None:
            actions.append(node.action)
            cells.append(maze.getPlayerPosition(node.state))
            node = node.parent
        actions.reverse()
        cells.reverse()

        print("Solution found!")
        print("Initial State:")
        maze.printMaze(maze.getInitialState())
        print("Solved Path:")
        maze.printMaze(node.state, solved=True)
        print("Actions:", actions)
        print("Cells:", cells)
        print(f"Explored nodes: {num_explored}")
        print(f"Path: {cells}")
        break
    
    explored.append(node.state)  # Add the current state to the explored set
    # maze.printMaze(node.state, isSpecial=True)
    for action in maze.getActions(node.state, debug=True):
        child_state = maze.movePlayer(node.state, action)
        child = Node(state=child_state, parent=node, action=action)
        isExplored = False
        for i in explored:
            if i == child_state:
                print("Already explored action:", action)
                isExplored = True
        if not isExplored and not frontier.contains_state(child_state):
            frontier.add(child)

