import os


class FileParser:
    def __init__(self, arg):
        self.arg = arg
        self.file_path = self.find_file()

    def find_file(self):
        # If it's an absolute or relative valid path
        if os.path.isfile(self.arg):
            return os.path.abspath(self.arg)
        
        # Extract just the filename
        filename = os.path.basename(self.arg)

        # Walk the filesystem starting from current directory
        for root, _, files in os.walk('.'):
            if filename in files:
                return os.path.join(root, filename)
        
        raise FileNotFoundError(f"File '{filename}' not found in the current directory or its subdirectories.")

    def parse_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, state):
        """Adds a state to the frontier."""
        self.frontier.append(state)
    
    def contains_state(self, state):
        """Checks if the frontier contains a state."""
        return any(node.state == state for node in self.frontier)

    def is_empty(self):
        """Checks if the frontier is empty."""
        return len(self.frontier) == 0

    def remove(self):
        """Removes and returns a state from the frontier."""
        if self.is_empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        """Removes and returns a state from the frontier."""
        if self.is_empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
