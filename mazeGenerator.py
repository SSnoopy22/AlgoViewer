import copy

class Maze():
    def __init__(self, filename):
        with open (filename, 'r') as f:
            self.maze = [list(line.strip()) for line in f.readlines()]
        with open (filename, 'r') as f:
            contents = f.read()
            # print(contents.count('A'), contents.count('B'))
            if contents.count('A') != 1:
                raise ValueError("Maze must contain exactly one 'A' (start position)") 
            if contents.count('B') != 1:
                raise ValueError("Maze must contain exactly one 'B' (end position)")
        self.wall = "#"
        self.path = "_"
        self.explored = "X"
        self.height = len(self.maze)
        self.width = len(self.maze[0])
    
    
    def movePlayer(self, mazeState, direction, marked=False):
        if marked:
            self.explored = "X"
        else:
            self.explored = self.path
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")
        new_position = self.getPlayerPosition(mazeState) 
        if direction == "up":
            new_position = (self.getPlayerPosition(mazeState)[0] - 1, self.getPlayerPosition(mazeState)[1])
        elif direction == "down":
            new_position = (self.getPlayerPosition(mazeState)[0] + 1, self.getPlayerPosition(mazeState)[1])
        elif direction == "left":
            new_position = (self.getPlayerPosition(mazeState)[0], self.getPlayerPosition(mazeState)[1] - 1)
        elif direction == "right":
            new_position = (self.getPlayerPosition(mazeState)[0], self.getPlayerPosition(mazeState)[1] + 1)
        # print("player pos", self.getPlayerPosition(mazeState))
        mazeStateCopy = copy.deepcopy(mazeState)
        mazeStateCopy[self.getPlayerPosition(mazeState)[0]][self.getPlayerPosition(mazeState)[1]] = self.explored
        mazeStateCopy[new_position[0]][new_position[1]] = 'A'
        # print(mazeStateCopy)
        return mazeStateCopy
    
    
    def getActions(self, mazeState, debug=False):
        moveOptions = {}
        notExplorable = [self.wall, 'A']  # Cells that cannot be moved into
        if debug:
            print("New Turn:")
            print("Current Player Position:", self.getPlayerPosition(mazeState))
            print("Current Maze State:")
            self.printMaze(mazeState)
        # Check Above
        if self.getPlayerPosition(mazeState)[0] > 0 :
            if debug: print("up:", mazeState[self.getPlayerPosition(mazeState)[0] - 1][self.getPlayerPosition(mazeState)[1]])
            if mazeState[self.getPlayerPosition(mazeState)[0] - 1][self.getPlayerPosition(mazeState)[1]] not in notExplorable:
                moveOptions["up"] = True
        # Check Below
        if self.getPlayerPosition(mazeState)[0] < self.height-1:
            if debug: print("down:", mazeState[self.getPlayerPosition(mazeState)[0] + 1][self.getPlayerPosition(mazeState)[1]])
            if mazeState[self.getPlayerPosition(mazeState)[0] + 1][self.getPlayerPosition(mazeState)[1]] not in notExplorable:
                moveOptions["down"] = True
        # Check Left
        if self.getPlayerPosition(mazeState)[1] > 0:
            if debug: print("left:", mazeState[self.getPlayerPosition(mazeState)[0]][self.getPlayerPosition(mazeState)[1] - 1])
            if mazeState[self.getPlayerPosition(mazeState)[0]][self.getPlayerPosition(mazeState)[1] - 1] not in notExplorable:
                moveOptions["left"] = True
        # Check Right
        if self.getPlayerPosition(mazeState)[1] < len(mazeState[1])-1:
            if debug: print("right:", mazeState[self.getPlayerPosition(mazeState)[0]][self.getPlayerPosition(mazeState)[1] + 1])
            if mazeState[self.getPlayerPosition(mazeState)[0]][self.getPlayerPosition(mazeState)[1] + 1] not in notExplorable:
                moveOptions["right"] = True
        if(debug):
            print("Available Actions:", moveOptions)
        return moveOptions
    
    def getPlayerPosition(self, mazeState):
        for i, row in enumerate(mazeState):
            for j, cell in enumerate(row):
                if cell == 'A':
                    return (i, j)
        return None    
    
    def getEndPosition(self):
        for i, row in enumerate(self.getInitialState()):
            for j, cell in enumerate(row):
                if cell == 'B':
                    return (i, j)
        return None
    
    def  getInitialState(self):
        return self.maze.copy()
    
    def isAtGoal(self, mazeState):
        if self.getPlayerPosition(mazeState) == self.getEndPosition():
            return True

    def printMaze(self, mazeState, isSpecial=False, debug=False, solved=False):
        COLOR = "\033[92m"
        COLOR_2 = "\033[94m"
        COLOR_SOLVED = "\033[93m"
        END = '\033[0m'
        seperator = "+" + "-" * len(mazeState[0]) * 2 + "+"
        if isSpecial:
            print(COLOR + seperator)
        elif debug:
            print(COLOR_2 + seperator)
        elif solved:
            print(COLOR_SOLVED + seperator)
        else:
            print(seperator)
        for row in mazeState:
            print("|", ' '.join(row), "|")
        print(seperator + END)
    
    def markExplored(self, actions):
        """Marks the actions taken as explored."""
        exploredMaze = copy.deepcopy(self.maze)
        for action in actions:
            exploredMaze = self.movePlayer(exploredMaze, action, marked=True)
        return exploredMaze