from Mazi import Cell
from Mazi import Maze
#from State import State
import copy



class State:
    """
    class State with fields: cell, previous cell, depth
    """
    def __init__(self, current_cell, previous_state=0, depth = 0):
        """

        :type depth: integer - only used in IDFS
        """
        self.cell = Cell(current_cell.x, current_cell.y)
        self.cell.walls = current_cell.walls
        self.previous_state = copy.copy(previous_state)
        self.depth = depth

    def is_checked(self, st_checked):
        """
         Determines if state is already checked - used in BFS
        """

        for i in range(len(st_checked)):
            if st_checked[i].cell.x == self.cell.x and st_checked[i].cell.y == self.cell.y:
                return True
        return False


class DFS:
    def __init__(self, maze):

        self.st_open = []
        self.maze = copy.copy(maze)

    def is_entry(self, state):

        if state.cell.x == self.maze.entry_x and state.cell.y == self.maze.entry_y:
            return True
        else:
            return False

    def is_exit(self, state):

        if state.cell.x == self.maze.exit_x and state.cell.y == self.maze.exit_y:
            return True
        else:
            return False

    def is_previous(self, new_state, current_state):
        """
        check if new state is previous state from current - going backwards
        :param new_state:
        :param current_state:
        :return: true if is previous
        """
        if current_state.previous_state == 0 :
            return False
        if new_state.cell.x == current_state.previous_state.cell.x and new_state.cell.y == current_state.previous_state.cell.y:
            return True
        else:
            return False

    def get_state_at_direction(self, dir, current_state):

        if current_state.cell.walls[dir] == True:
            return 0
        if current_state.previous_state == 0 and dir == 'E':
            return 0

        x = current_state.cell.x
        y = current_state.cell.y

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
        return next_state


    def find_path(self):

        directions = ['N', 'S', 'W', 'E']
        path = []
        path_found = False
        entry_state = State(self.maze.cell_at(self.maze.entry_x, self.maze.entry_y))
        current_state = entry_state
        new_state = 0
        depth = 0

        state_visited = 1

        while True:
            for dir in directions:
                new_state = self.get_state_at_direction(dir, current_state)
                if new_state != 0:
                    if self.is_exit(new_state):
                        path_found = True
                        break
                    #if we're not going backwards - write new state to the beggining of "st_open"
                    if not self.is_previous(new_state, current_state):
                        self.st_open.insert(0, new_state)
                        state_visited += 1

            if path_found:
                current_state = new_state
                break
            current_state = self.st_open.pop(0)

        while current_state != 0:
            path.append(current_state.cell)
            current_state = current_state.previous_state

        return path, state_visited