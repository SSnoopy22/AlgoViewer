from helper import Node, StackFrontier, QueueFrontier
from mazeGenerator import Maze


class algos():
    def __init__(self, MAZEFILE, isDebug=False):
        self.maze = Maze(MAZEFILE)
        self.isDebug = isDebug
    
class bfs(algos):
    def __init__(self, MAZEFILE, isDebug=False):
        """Initialize BFS variables"""
        super().__init__(MAZEFILE, isDebug)
        self.num_explored = 0
        self.frontier = self.create_frontier()
        self.start = Node(self.maze.getInitialState(), parent=None, action=None)  # Create Start Node
        self.explored = [] # Create a set to keep track of self.explored nodes
        self.limit = 1000000
        
    def create_frontier(self):
        """Create and return a new frontier."""
        return QueueFrontier()
    
    def solve(self):
        self.frontier.add(self.start) # Add the start node to the frontier
        print("Initial State:")
        self.maze.printMaze(self.maze.getInitialState())
        while True or self.num_explored < self.limit:
            if(self.isDebug):
                print("Current Frontier:")  # Print the Frontier
                for state in self.frontier.frontier:
                    self.maze.printMaze(state.state, debug=True)
                print("Explored States:")  # Print the current state of the maze
                for state in self.explored:
                    self.maze.printMaze(state, isSpecial=True)
            if self.frontier.is_empty():
                print("No solution found")  # If the frontier is empty, no solution exists
                print(f"Explored nodes: {self.num_explored}")
                return
            node = self.frontier.remove()  # Remove a node from the frontier
            self.num_explored += 1  # Increment the number of self.explored nodes

            if self.maze.isAtGoal(node.state):
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(self.maze.getPlayerPosition(node.state))
                    node = node.parent
                actions.reverse()
                cells.reverse()

                print("Solution found!")
                print("Solved Path:")
                self.maze.printMaze(self.maze.markExplored(actions), solved=True)
                print("Actions:", actions)
                print("Cells:", cells)
                print(f"Explored nodes: {self.num_explored}")
                print(f"Path: {cells}")
                break
            
            self.explored.append(node.state)  # Add the current state to the self.explored set
            # maze.printMaze(node.state, isSpecial=True)
            for action in self.maze.getActions(node.state, debug=self.isDebug):
                child_state = self.maze.movePlayer(node.state, action)
                child = Node(state=child_state, parent=node, action=action)
                isExplored = False
                for i in self.explored:
                    if i == child_state:
                        isExplored = True
                if not isExplored and not self.frontier.contains_state(child_state):
                    self.frontier.add(child)
            
            if self.num_explored == self.limit-1:
                print(f"Explore Limit Reached: {self.limit}")

class dfs(bfs):
    def create_frontier(self):
        """Create and return a new frontier."""
        return StackFrontier()  # Use StackFrontier for DFS

