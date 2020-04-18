from Mazi import Cell
from Mazi import Maze
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


def read_maze(filename):
    """
    Read and create maze from text file
    :param filename: name of file with maze
    :return: maze created from file
    """
    maze_file = open(filename, 'r')
    line = maze_file.readline()
    params = line.split(' ')
    nx = int(params[0])
    ny = int(params[1])
    entry_x = int(params[2])
    entry_y = int(params[3])
    exit_x = int(params[4])
    exit_y = int(params[5])

    cells = [[0 for y in range(ny)] for x in range(nx)]

    for y in range(ny):
        mazi = maze_file.readline()
        row = mazi.split('|')
        for x in range(nx):
            cells[x][y] = row[x]

    maze_file.close()

    maze_map = [[Cell(x, y, cells[x][y]) for y in range(ny)] for x in range(nx)]

    maze = Maze(nx, ny, maze_map)
    return maze


class BFS_algorythm:
    """
    class realizes BFS algorythm
    fields: states open, states checked, maze
    """
    def __init__(self, maze):

        self.st_open = []
        self.st_checked = []
        self.maze = copy.copy(maze)

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
            return 0
        #if current state is entry state - don't return state in the east - it's outside the maze
        if current_state.previous_state == 0 and dir == 'E':
            return 0

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
        return next_state

    def find_path(self):
        """
        finds path from entry to exit
        :return: list of cells from entry to exit
        """

        directions = ['N', 'S', 'W', 'E']
        path = []
        path_found = False
        entry_state = State(self.maze.cell_at(self.maze.entry_x, self.maze.entry_y))
        current_state = entry_state


        while len(self.st_checked) < (self.maze.nx * self.maze.ny):

            for dir in directions:
                #get new state at direction if possible
                new_state = self.get_state_at_direction(dir, current_state)
                if new_state != 0:
                    #check if state is terminal
                    if self.is_exit(new_state):
                        path_found = True
                        break
                    #if state was checked - do nothing
                    if new_state.is_checked(self.st_checked) == False:
                        self.st_open.append(new_state)

            if path_found:
                current_state = new_state
                break
            self.st_checked.append(current_state)
            current_state = self.st_open.pop(0)
        #write path to list
        while current_state != 0:
            path.append(current_state.cell)
            current_state = current_state.previous_state

        return path


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

            if path_found:
                current_state = new_state
                break
            current_state = self.st_open.pop(0)

        while current_state != 0:
            path.append(current_state.cell)
            current_state = current_state.previous_state

        return path


class IDFS:
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

        next_state = State(self.maze.cell_at(x + h, y + v), current_state, current_state.depth + 1)
        return next_state

    def find_path(self):

        directions = ['N', 'S', 'W', 'E']
        path = []
        path_found = False
        entry_state = State(self.maze.cell_at(self.maze.entry_x, self.maze.entry_y))
        current_state = entry_state
        new_state = 0
        depth = 10
        d = 0
        i = 0

        while not path_found:
            while current_state.depth < depth:
                for dir in directions:
                    new_state = self.get_state_at_direction(dir, current_state)
                    if new_state != 0:
                        if self.is_exit(new_state):
                            path_found = True
                            break
                        if not self.is_previous(new_state, current_state):
                            self.st_open.insert(0, new_state)
                if path_found:
                    current_state = new_state
                    break
                current_state = self.st_open.pop(0)

            depth = depth + 1

        while current_state != 0:
            path.append(current_state.cell)
            current_state = current_state.previous_state
        return path





maze = read_maze('mazik.txt')
maze.write_svg('read.svg')
#bfs = BFS_algorythm(maze)
#path = bfs.find_path()
#maze.write_svg('pathBFS.svg', path)
#dfs = DFS(maze)
#path = dfs.find_path()
#maze.write_svg('pathDFS.svg', path)

idfs = IDFS(maze)
path = idfs.find_path()
maze.write_svg('pathIDFS.svg', path)
