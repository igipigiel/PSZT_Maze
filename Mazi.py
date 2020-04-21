# df_maze.py
import random

# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.

class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y, walls_str = ''):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}


        #set walls when reading from file
        if walls_str != '':
            self.set_walls('N', walls_str)
            self.set_walls('S', walls_str)
            self.set_walls('E', walls_str)
            self.set_walls('W', walls_str)

        #if cell has no walls
        if walls_str == ' ':
            self.walls = {'N': False, 'S': False, 'E': False, 'W': False}


    def set_walls(self, symbol = '', walls_string = ''):
        if walls_string.__contains__(symbol):
            self.walls[symbol] = True
        else:
            self.walls[symbol] = False

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, maze_map = 0, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (self.ix, self.iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        #set entry and exit coordinates
        self.entry_x = self.nx - 1
        self.entry_y = 2
        self.exit_x = 3
        self.exit_y = self.ny - 1

        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

        #generate maze map whe reading from file
        if maze_map != 0 :
            self.maze_map = maze_map
            #set entry and exit
            self.cell_at(self.entry_x, self.entry_y).walls['E'] = False
            if self.exit_x == self.nx - 1:
                self.cell_at(self.exit_x,self.exit_y).walls['E'] = False
            elif self.exit_y == self.ny - 1:
                self.cell_at(self.exit_x, self.exit_y).walls['S'] = False




    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx*2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename, path_found =0):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(f, x1, y1, x2, y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                                .format(x1, y1, x2, y2), file=f)


        def draw_circle(f,x,y):

            print('<circle cx="{}" cy="{}" r="2" stroke="black" stroke-width="0.1" fill="magenta" />'.format(x,y), file =f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                    .format(width+2*padding, height+2*padding,
                        -padding, -padding, width+2*padding, height+2*padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #FF1493;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x,y).walls['S']:
                        x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x,y).walls['E']:
                        x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                        write_wall(f, x1, y1, x2, y2)

            #draw dots in cells on found path
            if path_found != 0:
                for i in range(len(path_found)):
                    xs =  path_found[i].x * scx + scx/2
                    ys = path_found[i].y * scx + scx/2
                    draw_circle(f,xs,ys)

            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height),file=f)
            print('</svg>', file=f)

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1,0)),
                 ('E', (1,0)),
                 ('S', (0,1)),
                 ('N', (0,-1))]
        neighbours = []
        for direction, (dx,dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        # Total number of cells.

        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            #delete walls on entry cell and exit cell
            if current_cell == self.cell_at(self.entry_x, self.entry_y):
                current_cell.walls['E'] = False

            if current_cell == self.cell_at(self.exit_x, self.exit_y):
                current_cell.walls['S'] = False

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1


    def save_file(self, filename):
        """

        :param filename: name of file to save
        :return:

        cell format: |walls| (N if north wall is true etc.)
        """

        maze_string = str(self.nx) + ' ' + str(self.ny) + ' ' + str(self.entry_x) + ' ' + str(self.entry_y) + ' ' +  str(self.exit_x) + ' ' + str(self.exit_y) + '\n'

        for y in range (self.iy, self.ny+self.iy, 1):
            for x in range(self.ix, self.nx + self.ix, 1):
                current_cell = self.cell_at(x, y)
                if current_cell.walls['N'] == True:
                    maze_string = maze_string + 'N'
                if current_cell.walls['S'] == True:
                    maze_string = maze_string + 'S'
                if current_cell.walls['E'] == True:
                    maze_string = maze_string + 'E'
                if current_cell.walls['W'] == True:
                    maze_string = maze_string + 'W'

                maze_string = maze_string + ' |'

            maze_string = maze_string + '\n'

        mazi = open(filename, 'w')
        print(maze_string, file = mazi)
        mazi.close()


# Maze dimensions (ncols, nrows)
nx, ny = 30, 20
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()
maze.save_file('mazik.txt')
maze.write_svg('maze_gen.svg')


