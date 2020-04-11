from Mazi import Cell
from Mazi import Maze

mazifile = open('mazik.txt', 'r')
mazi = mazifile.readline()
#print(mazi)
params = mazi.split(' ')
nx = int(params[0])
ny = int(params[1])
entry_x = int(params[2])
entry_y = int(params[3])
exit_x = int(params[4])
exit_y = int(params[5])

cells = [[0 for y in range(ny)] for x in range(nx)]

for y in range (ny) :
    mazi = mazifile.readline()
    row = mazi.split('|')
    for x in range(nx) :
        cells[x][y] = row[x]

mazifile.close()

maze_map  = [[Cell(x, y, cells[x][y]) for y in range(ny)] for x in range(nx)]

maziek = Maze(nx, ny, maze_map)
print(maziek)
maziek.write_svg('maziek.svg')













