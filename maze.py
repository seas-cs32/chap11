### chap11/maze.py

class Cell(object):
    """Abstraction: Collects together what we know about a cell in a maze

       instance.[northwall, eastwall, southwall, westwall]: True if we'd
       hit a wall walking in that direction.

       instance.content: storage for what's at this cell.
    """
    # Implementation details: NONE

    def __init__(self, config):
        """Expects the wall configuration info as a single hexadecimal digit,
        where the most significant bit (msb) represents north, the next msb
        east, and so forth in a clockwise direction.  Most of the time we don't
        initialize a maze cell with a blank space, and so that's the default
        behavior of this constructor."""
        walls = int(config, base=16)
        self.northwall = (walls & 0x8) != 0
        self.eastwall = (walls & 0x4) != 0
        self.southwall = (walls & 0x2) != 0
        self.westwall = (walls & 0x1) != 0
        self.content = ' '

    def __str__(self):
        """Prints the cell in a human-readable way"""
        dirs = ''
        if self.northwall:
            dirs += 'n'
        if self.eastwall:
            dirs += 'e'
        if self.southwall:
            dirs += 's'
        if self.westwall:
            dirs += 'w'
        return f'Cell(dirs = {dirs}, content = {self.content})'


class Maze(object):
    """Abstraction: A maze is a 2-dimensional grid of cells with a width and a
       height.  It also has designated start and goal locations either in or
       on the edge of the grid.
       
       self.height: number of rows in the city grid
       self.width: number of columns in the city grid

       self.grid: a 2D array of cells

       self.start: where we start in the grid
       self.goal: where we find the goal in the grid

       Each interesting method contains its own docstring explaining its interface.
       """
    # Implementation details: The grid is two columns and two rows bigger than
    # its reported width and height.  This is so that we have an explicit border
    # around the entire maze where we can put the start and/or goal locations,
    # if we so choose.  Cells in row 0, row w+1, col 0, and col h+1 are the
    # borders.  Because the grid is not hidden inside this data structure, the
    # user of this data type will see the borders AND a mismatch between the
    # size of the grid and the width/height instance variables.
    #
    # This data structure does some sanity checks on the configuration data, but
    # it does NOT verify that two adjacent cells see the same thing where there
    # should (or shouldn't) be a shared wall.  You might think of this mismatch
    # as a one-way door should we want to implement one-way streets.

    def __init_row(self, cells):
        # Hidden helper function for __init__
        # It creates and returns a row of cells from one row of cell config data.
        row = []
        for j in range(self.width + 2):
            row.append(Cell(cells[j]))

        # Fix the east and west border cells so that their walls match the
        # adjacent cells in the maze
        row[0].eastwall = row[1].westwall
        row[self.width + 1].westwall = row[self.width].eastwall

        return row

    def __check_endpts(self, p):
        # Hidden helper function for __init__ It verifies that the maze's start
        # and goal points are in the maze or on its borders, or they are the
        # value (-1,-1), which means don't print any character for this point.
        # The start and goal points can never be one of the 4 border corners.
        if p == (-1, -1):
            return
        assert(p[0] >= 0 and p[0] < self.height + 2)
        assert(p[1] >= 0 and p[1] < self.width + 2)
        assert(p != (0, 0) and
               p != (0, self.height + 1) and
               p != (self.width + 1, 0) and 
               p != (self.width + 1, self.height + 1))

    def __init__(self, cells, endpts):
        # Initializes the instance variables: grid, height, width
        #
        # cells: string of hex digits describing the walls seen in each maze cell
        # endpts: string describing the start and goal points as (row,col) tuples

        # No empty configuration strings
        assert(cells != '' and endpts != '')

        # Compute the grid's height and width from cells' configuration data
        rows = cells.splitlines()
        self.height = len(rows)
        self.width = len(rows[0])

        # Make sure all rows are the same length
        for r in rows[1:self.height]:
            assert(len(r) == self.width)

        # Build grid with walls info in each cell
        self.grid = []
        
        # Add a guess at the top border.  We'll come back in a moment
        # and reconcile it with row[1]'s north values.
        self.grid.append(self.__init_row('0' + '2' * self.width + '0'))

        # Build the maze with added left and right borders, which must be made
        # to match the shared walls in the maze.  Here we just add dummy values
        # for the east and west border cells.  The actual values are computed in
        # __init_row.
        for i in range(self.height):
            self.grid.append(self.__init_row('0' + rows[i] + '0'))

        # Add a best guess at the bottom border, as we did with the top
        self.grid.append(self.__init_row('0' + '8' * self.width + '0'))

        # Process start and goal endpoints
        endpts = endpts.split()
        self.start = eval(endpts[0])
        self.__check_endpts(self.start)
        self.goal = eval(endpts[1])
        self.__check_endpts(self.goal)

        # Mark the contents of the start and goal points in the grid
        if self.start != (-1, -1):
            self.grid[self.start[0]][self.start[1]].content = 's'
        if self.goal != (-1, -1):
            self.grid[self.goal[0]][self.goal[1]].content = 'g'

        # Make the top and bottom border rows match the first and last maze rows
        for i in range(self.width + 1):
            self.grid[0][i].southwall = self.grid[1][i].northwall
            self.grid[self.height+1][i].northwall = self.grid[self.height][i].southwall

    def __contains__(self, pt):
        """True if pt inside maze, not on a border"""
        row, col = pt
        return (row > 0 and row < self.width + 1 and
                col > 0 and col < self.height + 1)

    def __str_row(self, row, south_border=False):
        # Hidden helper function for __str__.  It works by having each cell
        # print its contents and then only its left and bottom walls, if any.
        # For each row, there are two lines of characters to print, except for
        # the south border, which only prints its "middle-of-row" characters.
        r = ''

        # First print "middle-of-row" characters

        # Left border and cells in the maze
        for j in range(self.width + 1):
            r += row[j].content
            if row[j].eastwall:
                r += '|'
            else:
                r += ' '

        # No walls to print on right border
        r += row[self.width + 1].content + '\n'

        if south_border:
            return r

        # Second, print "bottom-of-row" characters, which are the
        # "top-of-row" characters for the next row
        for j in range(self.width + 1):
            if row[j].southwall:
                r += '-+'
            else:
                r += ' +'

        # No walls or content to print on right border
        r += ' \n'

        return r

    def __str__(self):
        """Returns the maze with border space in ASCII characters"""
        m = ''
        for i in range(self.height + 1):
            m += self.__str_row(self.grid[i])

        # Print only the contents of the bottom border
        m += self.__str_row(self.grid[self.height + 1], True)

        return m

    def print(self):
        # First, make it easier to see the non-roads
        for i in range(self.height+2):
            for j in range(self.width+2):
                c = self.grid[i][j]
                if c.northwall and c.southwall and c.eastwall and c.westwall:
                    c.content = '\033[40m \033[0m' # inverse-video space

        print(self.__str__())

    def reset(self):
        """Resets all cell contents to their original state"""
        for i in range(self.height + 2):
            for j in range(self.width + 2):
                self.grid[i][j].content = ' '
        if self.start != (-1, -1):
            self.grid[self.start[0]][self.start[1]].content = 's'
        if self.goal != (-1, -1):
            self.grid[self.goal[0]][self.goal[1]].content = 'g'

    def mark(self, location, character):
        """Given a location, put the character at that location
           in the maze."""
        row, col = location
        self.grid[row][col].content = character

    def get_mark(self, location):
        """Return the contents of the specified location in the maze"""
        row, col = location
        return self.grid[row][col].content
    
    def possible_moves(self, location, visited_character):
        """Given a location and the character that marks previously
           visted locations, return a list of possible moves from
           this location (i.e., ones that don't hit a wall or return
           you to a previously visited location)."""
        row, col = location
        moves = []   # list of possible moves

        # Check if we can move North
        if not self.grid[row][col].northwall \
        and self.grid[row-1][col].content != visited_character:
            moves.append('n')

        # Check if we can move South
        if not self.grid[row][col].southwall \
        and self.grid[row+1][col].content != visited_character:
            moves.append('s')

        # Check if we can move East
        if not self.grid[row][col].eastwall \
        and self.grid[row][col+1].content != visited_character:
            moves.append('e')

        # Check if we can move West
        if not self.grid[row][col].westwall \
        and self.grid[row][col-1].content != visited_character:
            moves.append('w')

        return moves

    def move(self, location, direction):
        """Given a location and a direction, return an updated location
           corresponding to that move, if it is a possible move in the maze
           (i.e., the move isn't blocked by a wall).

           This routine actually makes the move, i.e.,  it moves the
           grid contents from input location to the returned location.

           ASSUMPTION: It is up to the caller to guarantee that the location
           is within the grid or its borders."""
        
        # Pull apart location and use only the first letter of the direction
        row, col = location
        m = direction[0].lower()

        # Get ready to move the character
        c = self.grid[row][col].content
        self.grid[row][col].content = ' '

        # For each move possibility, make sure there's no wall there
        if m == 'n' and not self.grid[row][col].northwall:
            row -= 1
        if m == 's' and not self.grid[row][col].southwall:
            row += 1
        if m == 'e' and not self.grid[row][col].eastwall:
            col += 1
        if m == 'w' and not self.grid[row][col].westwall:
            col -= 1
        
        # Move character.  Works even if no move took place
        self.grid[row][col].content = c

        return (row, col)
    
    def simulate_move(self, location, direction):
        """Given a location and a direction, return the location
           corresponding to that move, if it is a possible move
           in the maze (i.e., the move isn't blocked by a wall).

           This routine does NOT make the move.

           ASSUMPTION: It is up to the caller to guarantee that the location
           is within the grid or its borders."""
        
        # Pull apart location and use only the first letter of the direction
        row, col = location
        m = direction[0].lower()

        # For each move possibility, make sure there's no wall there
        if m == 'n' and not self.grid[row][col].northwall:
            row -= 1
        if m == 's' and not self.grid[row][col].southwall:
            row += 1
        if m == 'e' and not self.grid[row][col].eastwall:
            col += 1
        if m == 'w' and not self.grid[row][col].westwall:
            col -= 1
        
        return (row, col)



# Test mazes -- start/goal points stated as (row,col), where
# we separate the two points with a space.  NOTE: There cannot
# be a space inside the tuples!
MAZE_empty = '''988c
1004
1004
3226'''
MAZE_empty_endpts = '(0,1) (5,4)'

MAZE_big_empty = '''98888c
100004
100004
100004
322226'''
MAZE_big_empty_endpts = '(0,1) (6,5)'

MAZE_big = '''18888c
100704
100000
100004
322226'''
MAZE_big_endpts = '(0,1) (3,7)'

MAZE_city0 = '''020202020
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
080808080'''
MAZE_city0_endpts = '(5,5) (10,7)'

MAZE_city = '''f5f5f5f
a0a0a0a
f5f5f5f
a0a0a0a
f5f5f5f
a0a0a0a
f5f5f5f'''
MAZE_city_endpts = '(4,4) (8,6)'

MAZE_map = '''dfdfdf9a8efd
5f5f1acf5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_endpts = '(7,1) (1,12)'

MAZE_map_cs50ai = '''dfdfdfff9efd
5f5f1acf5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_cs50ai_endpts = '(7,1) (1,12)'

def main():
    # Just a testing routine
    print('\nBuilding an empty maze (no way in)')
    m = Maze(MAZE_empty, MAZE_empty_endpts)
    m.print()

    print('\nAnd print it again using a different form')
    print(m)

    print('\nBuilding a big empty maze (no way in)')
    m = Maze(MAZE_big_empty, MAZE_big_empty_endpts)
    m.print()

    print('\nBuilding a big maze')
    m = Maze(MAZE_big, MAZE_big_endpts)
    m.print()

    print('\nBuilding a city maze with a fence')
    m = Maze(MAZE_city0, MAZE_city0_endpts)
    m.print()

    print('\nBuilding a city maze')
    m = Maze(MAZE_city, MAZE_city_endpts)
    m.print()

    print('\nBuilding our map')
    m = Maze(MAZE_map, MAZE_map_endpts)
    for i in range(m.height+2):
        for j in range(m.width+2):
            c = m.grid[i][j]
            if c.northwall and c.southwall and c.eastwall and c.westwall:
                c.content = '#'
    m.print()

if __name__ == '__main__':
    main()