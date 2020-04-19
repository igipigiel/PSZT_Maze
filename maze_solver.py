from Mazi import Cell
from Mazi import Maze
from BFS import BFS
from DFS import DFS
from IDFS import IDFS
import copy
import sys
from timeit import default_timer as timer

class maze_solver:

    def __init__(self, filename, type_):
        self.type_ = type_
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
        #maze.write_svg('read.svg')


        if(self.type_ == 'bfs'):
            algorythm = BFS(maze)
        elif(self.type_ == 'dfs'):
            algorythm = DFS(maze)
        elif(self.type_ == 'idfs'):
            algorythm = IDFS(maze)
        else:
            sys.exit('Wrong algorythm type, is: ' + self.type_ + ', should be: bfs or dfs or idfs, check spelling')

        time_start = timer()
        path = algorythm.find_path()
        time_stop = timer()
        time_passed = time_stop - time_start
        maze.write_svg(self.filename[0:-4] +'_' + self.type_ + '.svg', path)

        return time_passed

