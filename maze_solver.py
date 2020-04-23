from Mazi import Cell
from Mazi import Maze
from BFS import BFS
from DFS import DFS
from IDFS import IDFS
import copy
import sys
from timeit import default_timer as timer

class maze_solver:

    def __init__(self, filename, type, print = True):
        self.type = type
        self.filename = filename
        self.print = print


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
        #maze.write_svg('read.svg')


        if(self.type == 'bfs'):
            algorythm = BFS(maze)
        elif(self.type == 'dfs'):
            algorythm = DFS(maze)
        elif(self.type == 'idfs'):
            algorythm = IDFS(maze)
        else:
            sys.exit('Wrong algorythm type, is: ' + self.type + ', should be: bfs or dfs or idfs, check spelling')

        time_start = timer()
        path, state_visited = algorythm.find_path()
        time_stop = timer()
        time_passed = time_stop - time_start
        if self.print == True:
            maze.write_svg(self.filename[0:-4] +'_' + self.type + '.svg', path)

        return time_passed, state_visited


