from Mazi import Cell
from Mazi import Maze
from BFS import BFS
from DFS import DFS
from IDFS import IDFS
import copy

class maze_solver:

    def __init__(self, filename, path):
        self.type = type
        self.filename = filename

    def read_maze(self, filename):
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

    def find_path(self):
        maze = self.read_maze(self.filename)
        maze.write_svg('read.svg')

        if(self.type is 'bfs'):
            algorythm = BFS(maze)
        elif(self.type is 'dfs'):
            algorythm = DFS(maze)
        elif(self.type is 'idfs'):
            algorythm = IDFS(maze)
        else:
            exit('Wrong algorythm type, check spelling')

        path = algorythm.find_path()
        maze.write_svg('path.svg', path)

