from Mazi import Maze
from maze_solver import maze_solver
import numpy as np

# number of iterations to test each maze by every algorythm
iteration_size = 100

# maze sizes low - smallest maze, high - biggest maze
low = 10
high = 101
maze_size = [i for i in range (low,high)]

# experiment data summary matrices
times = np.arange(3*(high-low), dtype='float64').reshape(high-low,3)
iter_times = np.arange(3*(high-low), dtype='float64').reshape(high-low,3)

# algorythm types
algorythm = ['bfs','dfs', 'idfs']

filename_txt = 'maze.txt'
filename_svg = 'maze_gen.svg'


for size in maze_size:

    alg = 0
    for algorythm_type in algorythm:
        tmp_time = 0.0
        tmp_iter = 0.0
        time_passed = 0.0
        stat_vis = 0.0
        
        for iter in range(0, iteration_size):

            maze = Maze(size, size)
            maze.make_maze()

            filename_txt_size = filename_txt[0:-4] + '_' + str(size) + '.txt'
            maze.save_file(filename_txt_size)

            filename_svg_size = filename_svg[0:-4] + '_' + str(size) + '.svg'
            maze.write_svg(filename_svg_size)


            maze = maze_solver(filename_txt_size, algorythm_type, False)
            tmp_time, tmp_iter = maze.find_path()
            time_passed += tmp_time
            stat_vis += tmp_iter
        times[size - low][alg] = time_passed/(iteration_size)
        iter_times[size - low][alg] = stat_vis/(iteration_size)
        alg += 1
        #print('maze of size ' + str(size) +  ', algorythm: ' + algorythm_type +', average time: ' + str(time_passed/iteration_size))



# generate summary files
with open('times_bfs.txt','wb') as f:
    for line in times[:,[0]]:
        np.savetxt(f, line, fmt='%.6f')
with open('times_dfs.txt','wb') as f:
    for line in times[:,[1]]:
        np.savetxt(f, line, fmt='%.6f')
with open('times_idfs.txt','wb') as f:
    for line in times[:,[2]]:
        np.savetxt(f, line, fmt='%.6f')
with open('iter_bfs.txt','wb') as f:
    for line in iter_times[:,[0]]:
        np.savetxt(f, line, fmt='%.6f')
with open('iter_dfs.txt','wb') as f:
    for line in iter_times[:,[1]]:
        np.savetxt(f, line, fmt='%.6f')
with open('iter_idfs.txt','wb') as f:
    for line in iter_times[:,[2]]:
        np.savetxt(f, line, fmt='%.6f')