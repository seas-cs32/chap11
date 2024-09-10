### chap11/maze.py

# Useful globals
NO_LOC = (-1,-1)

class Cell(object):
    """Abstraction: Collects together everything about a maze cell

       instance.[northwall, eastwall, southwall, westwall]: True if we'd
       hit a wall walking in that direction.

       instance.content: storage for what's at this cell.
    """
    # Implementation details: NONE
    
    def __init__(self, config):
        """Expects the wall configuration info as a single hexadecimal digit,
        where the most significant bit (msb) represents north, the next msb
        east, and so forth in a clockwise direction.  Most of the time we
        initialize a maze cell with a blank space, and so that's the default
        behavior of this constructor."""
        walls = int(config, base=16)
        self.northwall = (walls & 0x8) != 0
        self.eastwall = (walls & 0x4) != 0
        self.southwall = (walls & 0x2) != 0
        self.westwall = (walls & 0x1) != 0
        self.content = ' '
    
    def __repr__(self):
        """Prints the cell in a human-readable way"""
        walls = ''
        if self.northwall:
            walls += 'n'
        if self.eastwall:
            walls += 'e'
        if self.southwall:
            walls += 's'
        if self.westwall:
            walls += 'w'
        if walls == '':
            walls = 'x'
        return f'Cell({walls}, "{self.content}")'


class Maze(object):
    """Abstraction: A maze is a 2-dimensional grid of cells. It has a width
       and a height.  It also has designated start and goal locations either
       in the grid or on its edge.
       
       self.height: number of north-to-south blocks (rows) in the city grid
       self.width: number of east-to-west blocks (columns) in the city grid

       self.grid: a 2D array of cells

       To identify a **location** in the grid, we use x-y coordinates. The
       grid's coordinates resemble a Cartesian plane with location (0,0)
       being in the lower lefthand corner of the maze. The upper righthand
       corner is (width+1, height+1). These coordinates include the border
       locations that exists around every maze.

       self.start: grid location where we start
       self.goal: grid location where we find the goal

       Each method contains its own docstring explaining its interface.
       """
    # Implementation details: The grid is two rows and two columns bigger
    # than its reported height and width.  This creates a border around
    # the maze where we can put the start and/or goal locations, if we so
    # choose.  Cells in row 0 (south border), row h+1 (north border),
    # column 0 (west border), and column w+1 (east border) are the borders.
    # Because the grid is not hidden inside this data structure, the user
    # of this data type will see the borders AND a mismatch between the
    # size of the grid and the height/width instance variables.
    #
    # This data structure does some sanity checks on the configuration
    # data, but it does NOT verify that two adjacent cells see the same
    # thing with their shared wall.  This mismatch allows for the
    # implementation of one-way streets.
    #
    # The hardest part of the following implementation is the layout
    # conflict between the map configuration strings (and also the
    # top-left-to-bottom-right printing of a map) and the 2D grid that
    # counts from bottom-left-to-top-right. This mismatch makes the
    # implementation of `__init__` and `__str__` tricky.

    def __check_endpt(self, pt):
        # Hidden helper function for __init__ that verifies that the maze's
        # start and goal are in the maze or on its borders, or they are
        # equal to NO_LOC, which means don't print any character at this
        # location.  The start and goal points shouldn't be one of the four
        # border corners.
        if pt == NO_LOC:
            return
        assert pt[0] >= 0 and pt[0] < self.width + 2
        assert pt[1] >= 0 and pt[1] < self.height + 2
        assert pt != (0, 0) and \
               pt != (0, self.height + 1) and \
               pt != (self.width + 1, 0) and \
               pt != (self.width + 1, self.height + 1)

    def __init__(self, cells, endpts):
        # Initializes the instance variables: grid, height, width
        #
        # cells: string of hex digits describing the walls seen in each maze cell
        # endpts: string describing the start and goal points as (x,y) tuples
        #
        # Note that the configuration data in `cells` describes only the
        # walls seen in the maze. This function creates the walls seen in
        # each border cell, which requires some trickiness to be able to
        # access a maze cell that defines a border cell's wall.
        
        # No empty configuration strings
        assert cells != '' and endpts != ''
        
        # Compute the grid's height and width from cells' configuration data
        rows = cells.splitlines()
        self.height = len(rows)
        self.width = len(rows[0])
        
        # Make sure all rows are the same length
        for r in rows:
            assert len(r) == self.width
        
        # Build grid with walls info in each cell
        self.grid = []
        
        # Guess the configuration of the south border.  We'll come back
        # in a moment and reconcile it with rows[1]'s south values.
        self.grid.append([Cell('0')])                 # SW corner
        for _ in range(1, self.width + 1):
            self.grid.append([Cell('8')])
        self.grid.append([Cell('0')])                 # SE corner
        
        for j in range(1, self.height + 1):
            # Transfer row configuration data
            row_config_codes = rows[self.height - j]
            for i in range(1, self.width + 1):
                cell_config_code = row_config_codes[i-1]
                self.grid[i].append(Cell(cell_config_code))

            # Create this row's west and east border cells
            if self.grid[1][j].westwall:
                self.grid[0].append(Cell('4'))
            else:
                self.grid[0].append(Cell('0'))
            if self.grid[self.width][j].eastwall:
                self.grid[self.width+1].append(Cell('1'))
            else:
                self.grid[self.width+1].append(Cell('0'))

        # Configure north border
        self.grid[0].append(Cell('0'))              # NW corner

        j = self.height      # previous row
        for i in range(1, self.width + 1):
            # Create a default north border cell and then
            # reconcile it with the previous row's northwall.
            self.grid[i].append(Cell('2'))
            self.grid[i][j+1].southwall = self.grid[i][j].northwall

        self.grid[self.width+1].append(Cell('0'))   # NE corner

        # Fix walls between south border and row[1]'s cells
        for i in range(1, self.width + 1):
            self.grid[i][0].northwall = self.grid[i][1].southwall

        # Process start and goal endpoints. There should be no spaces except
        # between the two endpoint tuples, e.g., '(1,7) (12,1)'.
        endpts = endpts.split()
        self.start = eval(endpts[0])    # From string to tuple
        self.__check_endpt(self.start)
        self.goal = eval(endpts[1])
        self.__check_endpt(self.goal)

        # Mark the contents of the start and goal points in the grid
        if self.start != NO_LOC:
            x, y = self.start
            self.grid[x][y].content = 's'
        if self.goal != NO_LOC:
            x, y = self.goal
            self.grid[x][y].content = 'g'

    def __contains__(self, loc):
        """True if loc inside maze, not on a border"""
        x, y = loc
        return (x > 0 and x < self.width + 1 and
                y > 0 and y < self.height + 1)

    def __str_row(self, row, row_next):
        # Hidden helper function for __str__.  It works by having each
        # cell print its contents and then only its left and bottom walls,
        # if any.
        #
        # You should think of each row of cells as requiring the printing
        # of three lines of characters: the row's north wall; the row's
        # east wall, contents, and west wall; and the row's south wall.
        # Because a row shares its south wall with the next row (i.e., its
        # north wall), each row prints only the first two of these lines
        # of characters.  The exceptions are the north border, which never
        # needs to print its non-existent north wall, and the south border,
        # which only prints its "middle-of-row" characters.  These the
        # north border is handled entirely by this routine; the south
        # border exception is handled in cooperation with __str__.
        r = ''

        # First print "middle-of-row" characters

        # For the west border and maze cells, print each cell's content
        # and east wall. The west border's west wall is never printed.
        for i in range(self.width + 1):
            r += row[i].content
            if row[i].eastwall:
                if row[i+1].westwall:
                    r += '|'
                else:
                    r += '<'
            else:
                if row[i+1].westwall:
                    r += '>'
                else:
                    r += ' '

        # No east walls to print on east border
        r += row[self.width + 1].content + '\n'

        if row_next == None:
            # Because we need only print the south border's contents,
            # we're done!
            return r

        # Second, print south-wall characters, which are the
        # north-wall characters for the next row.
        for i in range(self.width + 1):
            if row[i].southwall:
                if row_next[i].northwall:
                    r += '-+'
                else:
                    r += '^+'
            else:
                if row_next[i].northwall:
                    r += 'v+'
                else:
                    r += ' +'

        # No walls or content to print on right border
        r += ' \n'

        return r

    def __str__(self):
        """Returns the maze with border space in ASCII characters"""
        m = ''

        # Build the north border row
        row_to_print = []
        for i in range(self.width + 2):
            row_to_print.append(self.grid[i][self.height+1])

        # Print all but south border
        for j in range(self.height, -1, -1):
            # Build next row
            row_next = []
            for i in range(self.width + 2):
                row_next.append(self.grid[i][j])

            # Print row_to_print
            m += self.__str_row(row_to_print, row_next)

            row_to_print = row_next

        # Print the bottom border row
        m += self.__str_row(row_to_print, None)

        return m

    def print(self):
        # First, make it easier to see the non-roads
        for i in range(self.width+2):
            for j in range(self.height+2):
                c = self.grid[i][j]
                if c.northwall and c.southwall and c.eastwall and c.westwall:
                    c.content = '\033[40m \033[0m' # inverse-video space

        print(self.__str__())

    def mark(self, location, character):
        """Given a location, put the character there
           in the maze."""
        x, y = location
        assert x >= 0 and x < self.width + 2, f'bad x in {location}'
        assert y >= 0 and y < self.height + 2, f'bad y in {location}'
        self.grid[x][y].content = character

    def get_mark(self, location):
        """Return the contents of the specified location in the maze"""
        x, y = location
        assert x >= 0 and x < self.width + 2, f'bad x in {location}'
        assert y >= 0 and y < self.height + 2, f'bad y in {location}'
        return self.grid[x][y].content
    
    def reset(self):
        """Resets all cell contents to their original state"""
        for i in range(self.width + 2):
            for j in range(self.height + 2):
                self.mark((i,j), ' ')
        if self.start != NO_LOC:
            self.mark(self.start, 's')
        if self.goal != NO_LOC:
            self.mark(self.goal, 'g')

    def possible_moves(self, location, visited_character):
        """Given a location and the character that marks previously
           visted locations, return a list of possible moves from
           this location (i.e., ones that don't hit a wall or return
           you to a previously visited location)."""
        x, y = location
        assert x >= 0 and x < self.width + 2, f'bad x in {location}'
        assert y >= 0 and y < self.height + 2, f'bad y in {location}'
        moves = []   # list of possible moves

        # Check if we can move North
        if not self.grid[x][y].northwall and y != self.height + 2 \
        and self.grid[x][y+1].content != visited_character:
            moves.append('n')

        # Check if we can move South
        if not self.grid[x][y].southwall and y != 0 \
        and self.grid[x][y-1].content != visited_character:
            moves.append('s')

        # Check if we can move East
        if not self.grid[x][y].eastwall and x != self.width + 2 \
        and self.grid[x+1][y].content != visited_character:
            moves.append('e')

        # Check if we can move West
        if not self.grid[x][y].westwall and x != 0 \
        and self.grid[x-1][y].content != visited_character:
            moves.append('w')

        return moves

    def move(self, location, direction, make_move=True):
        """Given a location and a direction, return the location
           corresponding to that move, if it is a possible move
           in the maze (i.e., the move isn't blocked by a wall).

           By default, this routine makes the move, i.e., it
           moves the grid contents from input location to the
           returned location.

           ASSUMPTION: It is up to the caller to guarantee that the location
           is within the grid or its borders."""
        
        # Get ready to move the character
        c = self.get_mark(location)

        # Pull apart location and use only the first letter of the direction
        x, y = location
        m = direction[0].lower()

        # For each move possibility, make sure there's no wall there
        # and the move won't leave the grid.
        if m == 'n' and not self.grid[x][y].northwall and y != self.height + 1:
            y += 1
        if m == 's' and not self.grid[x][y].southwall and y != 0:
            y -= 1
        if m == 'e' and not self.grid[x][y].eastwall and x != self.width + 1:
            x += 1
        if m == 'w' and not self.grid[x][y].westwall and x != 0:
            x -= 1
        
        new_loc = (x, y)

        if make_move:
            # Move character.  Works even if no move took place
            self.mark(location, ' ')
            self.mark(new_loc, c)

        return new_loc
    
    def simulate_move(self, location, direction):
        """Given a location and a direction, return the location
           corresponding to that move, if it is a possible move
           in the maze (i.e., the move isn't blocked by a wall).

           This routine does NOT make the move.

           ASSUMPTION: It is up to the caller to guarantee that the location
           is within the grid or its borders."""
        return self.move(location, direction, False)


# Test mazes -- start/goal points stated as (x,y), where
# we separate the two points with a space.  NOTE: There cannot
# be a space inside the tuples!
MAZE_test = '''988c
3226'''
MAZE_test_endpts = '(1,0) (0,1)'

MAZE_empty = '''988c
1004
1004
3226'''
MAZE_empty_endpts = '(1,5) (4,0)'

MAZE_big_empty = '''98888c
100004
100004
100004
322226'''
MAZE_big_empty_endpts = '(0,1) (6,5)'

MAZE_big = '''98888c
100704
100000
100004
122226'''
MAZE_big_endpts = '(1,0) (7,3)'

MAZE_blackhole = '''98888c
104f14
100800
100004
122226'''
MAZE_blackhole_endpts = '(1,0) (7,3)'

MAZE_city_fence = '''020202020
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
0a0a0a0a0
4f5f5f5f1
080808080'''
MAZE_city_fence_endpts = '(5,5) (10,7)'

MAZE_city = '''f5f5f5f
a0a0a0a
f5f5f5f
a0a0a0a
f5f5f5f
a0a0a0a
f5f5f5f'''
MAZE_city_endpts = '(4,4) (8,6)'

MAZE_map = '''dfdfdf9a8efd
5f5f1a4f5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_endpts = '(1,1) (12,7)'

MAZE_map_1way = '''dfdfdf9a8efd
5f5f1acf5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_1way_endpts = '(1,1) (12,7)'

MAZE_map_cs50ai = '''dfdfdfff9efd
5f5f1acf5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_cs50ai_endpts = '(1,1) (12,7)'

MAZE_map_nosoln = '''dfdfdf9a8efd
5f5f1a4f5ff5
386f5f1a6ff5
f5ff5f5fdff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_nosoln_endpts = '(1,1) (12,7)'

MAZE_map_ale04 = '''dfdfd9aa8efd
5f5f12cf5ff5
386f5f1a4ff5
f5ff5f5f5ff5
f3a86f5f3aa6
fff5ff5fffff
baa6ff3aaaae'''
MAZE_map_ale04_endpts = '(12,1) (1,7)'

def main():
    # Just a testing routine
    print('\nBuilding a 4x2 TEST maze (no way in)')
    m = Maze(MAZE_test, MAZE_test_endpts)
    m.print()

    print('\nBuilding an 4x4 EMPTY maze (no way in)')
    m = Maze(MAZE_empty, MAZE_empty_endpts)
    m.print()

    print('\nAnd print it again using a different form')
    print(m)

    print('\nBuilding a 6x5 BIG EMPTY maze (no way in)')
    m = Maze(MAZE_big_empty, MAZE_big_empty_endpts)
    m.print()

    print(f'\nBuilding a 6x5 BIG maze')
    m = Maze(MAZE_big, MAZE_big_endpts)
    m.print()

    print(f'\nBuilding a 6x5 BLACKHOLE maze')
    m = Maze(MAZE_blackhole, MAZE_blackhole_endpts)
    m.print()

    print('\nBuilding a CITY maze with a FENCE')
    m = Maze(MAZE_city_fence, MAZE_city_fence_endpts)
    m.print()

    print('\nBuilding a CITY maze')
    m = Maze(MAZE_city, MAZE_city_endpts)
    m.print()

    print('\nBuilding a MAP for cs32')
    m = Maze(MAZE_map, MAZE_map_endpts)
    m.print()

    print('\nBuilding a MAP for cs32 with 1-way')
    m = Maze(MAZE_map_1way, MAZE_map_1way_endpts)
    m.print()

    print('\nBuilding the MAP from cs50ai')
    m = Maze(MAZE_map_cs50ai, MAZE_map_cs50ai_endpts)
    m.print()

    print('\nBuilding a MAP without a solution')
    m = Maze(MAZE_map_nosoln, MAZE_map_nosoln_endpts)
    m.print()

if __name__ == '__main__':
    main()