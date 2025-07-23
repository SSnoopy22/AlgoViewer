import copy


"""
TODO Fill extra maze space with wall. Basically add walls accounting for max height/width.
TODO Convert isDebug to an inherited class variable
TODO Remove isDebug from the constructor and use a class variable instead
"""


class Maze():
    def __init__(self, mazeText):
        # Parse the maze from a multiline string into a 2D list of characters
        self.maze = [list(mazeLine.strip()) for mazeLine in mazeText.splitlines()]
        
        # Validate that maze has exactly one start 'A' and one goal 'B'
        if mazeText.count('A') != 1:
            raise ValueError("Maze must contain exactly one 'A' (start position)") 
        if mazeText.count('B') != 1:
            raise ValueError("Maze must contain exactly one 'B' (end position)")

        # Define maze element types
        self.hero = "A"
        self.wall = "#"
        self.path = "_"
        self.goal = "B"
        self.explored = "X"

        # Precompute useful properties
        self.goalPosition = self.getEndPosition()
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.maxWidth = max(len(row) for row in self.maze)

        self.fillMaze()
        print("Maze initialized with dimensions: height=", self.height, "width=", self.width, "max width", self.maxWidth)    


    def movePlayer(self, mazeState, direction, marked=False):
        """
        Returns a new mazeState tuple after moving in the specified direction.
        """
        if direction not in ["up", "down", "left", "right"]:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

        new_position = mazeState 
        if direction == "up":
            new_position = (mazeState[0] - 1, mazeState[1])
        elif direction == "down":
            new_position = (mazeState[0] + 1, mazeState[1])
        elif direction == "left":
            new_position = (mazeState[0], mazeState[1] - 1)
        elif direction == "right":
            new_position = (mazeState[0], mazeState[1] + 1)

        return new_position
    
    
    def getActions(self, mazeState, isDebug=False):
        """
        Returns a dictionary of valid move directions from the current mazeState.
        If isDebug is True, prints debugging information.
        """
        moveOptions = {}
        notExplorable = [self.wall, 'A']  # Cells that cannot be entered

        if isDebug:
            print("\nNew Turn:")
            print("Current Player Position:", mazeState)
            print("Current Maze State:")
            self.printMaze(mazeState)

        # Check movement in each direction and whether it's allowed
        if mazeState[0] > 0 :
            if isDebug: print("up:", self.maze[mazeState[0] - 1][mazeState[1]])
            if self.maze[mazeState[0] - 1][mazeState[1]] not in notExplorable:
                moveOptions["up"] = True

        if mazeState[0] < self.height - 1:
            if isDebug: 
                print("down:", self.maze[mazeState[0] + 1][mazeState[1]])
            if self.maze[mazeState[0] + 1][mazeState[1]] not in notExplorable:
                moveOptions["down"] = True

        if mazeState[1] > 0:
            if isDebug: print("left:", self.maze[mazeState[0]][mazeState[1] - 1])
            if self.maze[mazeState[0]][mazeState[1] - 1] not in notExplorable:
                moveOptions["left"] = True

        # BUG: Incorrect index for width checking; should use self.width instead of len(row)
        if mazeState[1] < len(self.maze[mazeState[0]])-1:
            if isDebug: print("right:", self.maze[mazeState[0]][mazeState[1] + 1])
            if self.maze[mazeState[0]][mazeState[1] + 1] not in notExplorable:
                moveOptions["right"] = True

        if isDebug:
            print("Available Actions:", moveOptions)

        return moveOptions


    def getPlayerPosition(self, mazeState):
        """
        Searches the provided mazeState (2D list) for the hero 'A'.
        Returns the position as a (row, col) tuple.
        """
        for i, row in enumerate(mazeState):
            for j, cell in enumerate(row):
                if cell == 'A':
                    return (i, j)
        return None    


    def getEndPosition(self):
        """
        Searches the original maze for the goal 'B'.
        Returns the position as a (row, col) tuple.
        """
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == self.goal:
                    return (i, j)
        return None


    def getInitialState(self):
        """
        Returns the starting position of the hero 'A' in the original maze.
        """
        return self.getPlayerPosition(self.maze)


    def isAtGoal(self, mazeState):
        """
        Checks if the current mazeState is the goal position.
        """
        # TODO: Move this debug print to a controlled debug flag
        if mazeState == self.goalPosition:
            return True


    def fillMaze(self):
        """
        Fills uneven rows in the maze with underscores (_) to make all rows equal in length.
        Returns a list of (y, x) coordinates that were filled.
        """
        fillPoints = []
        for y, row in enumerate(self.maze):
            current_length = len(row)
            if current_length < self.maxWidth:
                # Fill with underscores at the missing x positions
                for x in range(current_length, self.maxWidth):
                    row.append("_")  # or " " if you prefer
                    fillPoints.append((y, x))
            else:
                # Optionally: collect empty spaces within full-width rows
                for x, cell in enumerate(row):
                    if cell == " ":
                        fillPoints.append((y, x))
        for y, x in fillPoints:
            # Ensure the row is long enough
            while len(self.maze[y]) <= x:
                self.maze[y].append(self.wall)  # fill with underscore (or your chosen char)
            # Now set the specific cell to the fill value
            self.maze[y][x] = self.wall


    def printMaze(self, mazeState=None, isSpecial=False, isDebug=False, solved=False):
        """
        Prints the maze to the terminal with optional styling for special/debug/solved views.
        Replaces the current position of the player with 'A'.
        """
        # ANSI color codes for different styles
        COLOR = "\033[92m"
        COLOR_2 = "\033[94m"
        COLOR_SOLVED = "\033[93m"
        END = '\033[0m'
        
        seperator = "+" + "-" * self.maxWidth * 2 + "+"
        if isSpecial:
            print(COLOR + seperator)
        elif isDebug:
            print(COLOR_2 + seperator)
        elif solved:
            print(COLOR_SOLVED + seperator)
        else:   
            print(seperator)

        # Create a copy so original maze isn't modified
        newMaze = copy.deepcopy(self.maze)

        # Replace original 'A' with '_' and put 'A' at the current state
        newMaze[self.getInitialState()[0]][self.getInitialState()[1]] = "_"
        newMaze[mazeState[0]][mazeState[1]] = "A"

        for row in self.maze:
            print("|", ' '.join(row), "|")
        print(seperator + END)


    def printMarkedMaze(self, state, specialOne = False, specialTwo = False):
        """
        Prints a maze with the state position marked with a colored border.
        """
        COLOR_ONE = "\033[92m"
        COLOR_TWO = "\033[94m"
        color = ""
        if specialOne:
            color = COLOR_ONE
        elif specialTwo:
            color = COLOR_TWO
        END = '\033[0m'
        seperator = color + "+" + "-" * self.maxWidth * 2 + "+"
        print(seperator)
        for row in self.maze:
            print("|", ' '.join(row), "|")
        print(seperator + END)

    # TODO FINISH THIS
    def printExploredMaze(self, theMaze):
        """
        Prints a solved or explored maze with a yellow border.
        """
        COLOR_SOLVED = "\033[93m"
        END = '\033[0m'
        seperator = COLOR_SOLVED + "+" + "-" * self.maxWidth * 2 + "+"
        print(seperator)
        for row in theMaze:
            print("|", ' '.join(row), "|")
        print(seperator + END)
    

    def markExplored(self, cells):
        """
        Returns a copy of the maze with the given list of (y,x) positions marked as explored.
        Replaces non-goal cells with 'X', and the goal with 'A' if explored.
        """
        exploredMaze = copy.deepcopy(self.maze)
        for cell in cells:
            if exploredMaze[cell[0]][cell[1]] == self.goal:
                exploredMaze[cell[0]][cell[1]] = self.hero
            else:
                exploredMaze[cell[0]][cell[1]] = str(self.explored)
        return exploredMaze
