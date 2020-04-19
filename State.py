

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