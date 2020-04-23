from Mazi import Cell
from Mazi import Maze
#from State import State
import copy



class State:
    """
    class State with fields: cell, previous cell, depth
    """
    def __init__(self, current_cell, previous_state=0):
        """

        :type depth: integer - only used in IDFS
        """
        self.cell = Cell(current_cell.x, current_cell.y)
        self.cell.walls = current_cell.walls
        self.previous_state = copy.copy(previous_state)

    def is_checked(self, st_checked):
        """
         Determines if state is already checked - used in BFS
        """

        for i in range(len(st_checked)):
            if st_checked[i].cell.x == self.cell.x and st_checked[i].cell.y == self.cell.y:
                return True
        return False

class BFS:
    """
    class realizes BFS algorythm
    fields: states open, states checked, maze
    """
    def __init__(self, maze):

        self.st_open = []
        self.st_checked = []
        self.maze = copy.copy(maze)
        self.visited = [[False for i in range(self.maze.nx)] for i in range(self.maze.ny)]

    def is_entry(self, state):
        """
        check if state is the first state - at maze entry
        :param state:
        :return:
        """
        if state.cell.x == self.maze.entry_x and state.cell.y == self.maze.entry_y:
            return True
        else:
            return False

    def is_exit(self, state):
        """
        check if state is terminal - at maze exit
        :param state:
        :return:
        """
        if state.cell.x == self.maze.exit_x and state.cell.y == self.maze.exit_y:
            return True
        else:
            return False

    def get_state_at_direction(self, dir, current_state):

        """
        :param dir: direction
        :param current_state:
        :return: next state in direction if possible, otherwise 0
        """
        #if there is a wall at this direction - next move not possible
        if current_state.cell.walls[dir] == True:
            return 0, self.maze.nx, self.maze.ny
        #if current state is entry state - don't return state in the east - it's outside the maze
        if current_state.previous_state == 0 and dir == 'E':
            return 0, self.maze.nx, self.maze.ny

        x = current_state.cell.x
        y = current_state.cell.y

        # h - move in horizontal direction (-1 West; 1 East)
        # v - move in vertical direction (-1 North; 1 South)
        if dir == 'N':
            h = 0
            v = -1

        if dir == 'S':
            h = 0
            v = 1

        if dir == 'E':
            h = 1
            v = 0

        if dir == 'W':
            h = -1
            v = 0

        next_state = State(self.maze.cell_at(x + h, y + v), current_state)
        return (next_state, x + h, y + v)

    def find_path(self):
        """
        finds path from entry to exit
        :return: list of cells from entry to exit
        """

        directions = ['N', 'S', 'W', 'E']
        path = []
        path_found = False
        entry_state= State(self.maze.cell_at(self.maze.entry_x, self.maze.entry_y))

        current_state = entry_state

        # added
        x,y = self.maze.entry_x, self.maze.entry_y

        # matrix of visited states
        self.visited[x][y] = True

        states_visited = 1
        while len(self.st_checked) < (self.maze.nx * self.maze.ny):
            for dir in directions:
                #get new state at direction if possible
                new_state, x, y = self.get_state_at_direction(dir, current_state)


                if new_state != 0:
                    if self.visited[x][y] == True:
                        continue
                    #check if state is terminal
                    if self.is_exit(new_state):
                        path_found = True
                        break
                    #if state was checked - do nothing
                    if self.visited[x][y] == False:
                        self.st_open.append(new_state)
                        states_visited += 1

            if path_found:
                current_state = new_state
                break
            x,y = current_state.cell.x, current_state.cell.y
            self.visited[x][y] = True
            self.st_checked.append(current_state)
            current_state = self.st_open.pop(0)


        #write path to list
        while current_state != 0:
            path.append(current_state.cell)
            current_state = current_state.previous_state

        return path, states_visited - len(self.st_open)


