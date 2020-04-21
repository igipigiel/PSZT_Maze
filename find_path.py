from Mazi import Maze
from maze_solver import maze_solver

# number of iterations to test each maze by every algorythm
iteration_size = 30
# maze sizes
maze_size = [10, 30, 50]
# algorythm types
algorythm = ['bfs', 'dfs', 'idfs']

filename_txt = 'maze.txt'
filename_svg = 'maze_gen.svg'


for size in maze_size:


    maze = Maze(size, size)
    maze.make_maze()

    filename_txt_size = filename_txt[0:-4] + '_' + str(size) + '.txt'
    maze.save_file(filename_txt_size)

    filename_svg_size = filename_svg[0:-4] + '_' + str(size) + '.svg'
    maze.write_svg(filename_svg_size)

    for algorythm_type in algorythm:
        time_passed = 0.0
        for iter in range(0, iteration_size):
            maze = maze_solver(filename_txt_size, algorythm_type)
            time_passed += maze.find_path()
        print('maze of size ' + str(size) +  ', algorythm: ' + algorythm_type +', average time: ' + str(time_passed/iteration_size))

