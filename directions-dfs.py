### chap11/directions-dfs.py
import maze

# Marks for map, which use color codes for terminal printing
EXPLORED = '\033[34m*\033[0m' # blue *
FRONTIER = '\033[32mf\033[0m' # green f

# Keep track of the tree of explored paths
class TreeNode():
    def __init__(self, state, parent, action):
        self.state = state    # current location 
        self.parent = parent  # previous note in path
        self.action = action  # action that got us to this location


def search(my_map):
    g = my_map.grid
    frontier = []

    # Initialize the variables used in the while-loop
    # with values from the start location
    loc = my_map.start
    row, col = loc
    g[row][col].content = EXPLORED
    cur_node = TreeNode(loc, None, None)

    # Search loop
    while loc != my_map.goal:
        # Build list of unexplored locations. A move is possible if there's not
        # a wall in that direction. We also add unexplored locations only once.
        if not g[row][col].northwall and g[row-1][col].content != EXPLORED and \
            g[row-1][col].content != FRONTIER:
            new_loc = (row-1, col)
            new_node = TreeNode(new_loc, cur_node, 'north')
            frontier.append(new_node)
            g[row-1][col].content = FRONTIER
        if not g[row][col].southwall and g[row+1][col].content != EXPLORED and \
            g[row+1][col].content != FRONTIER:
            new_loc = (row+1, col)
            new_node = TreeNode(new_loc, cur_node, 'south')
            frontier.append(new_node)
            g[row+1][col].content = FRONTIER
        if not g[row][col].eastwall and g[row][col+1].content != EXPLORED and \
            g[row][col+1].content != FRONTIER:
            new_loc = (row, col+1)
            new_node = TreeNode(new_loc, cur_node, 'east')
            frontier.append(new_node)
            g[row][col+1].content = FRONTIER
        if not g[row][col].westwall and g[row][col-1].content != EXPLORED and \
            g[row][col-1].content != FRONTIER:
            new_loc = (row, col-1)
            new_node = TreeNode(new_loc, cur_node, 'west')
            frontier.append(new_node)
            g[row][col-1].content = FRONTIER

        # my_map.print() # uncomment to see the frontier grow

        if len(frontier) == 0:
            print('No solution')
            return

        # Choose a location from the frontier as next to explore
        cur_node = frontier.pop()
        loc = cur_node.state
        row, col = loc
        g[row][col].content = EXPLORED

    # Follow the parent links from cur_node to create
    # the actual driving directions
    ddirections = [cur_node]
    while cur_node.parent:
        cur_node = cur_node.parent
        ddirections.insert(0, cur_node)

    # Print out the driving directions
    print('## Solution ##')
    print(f'Starting at {ddirections[0].state}')
    ddirections.pop(0)
    for n in ddirections:
        print(f'Go {n.action} then')
    print('Arrive at your goal')
    return


def main():
    print('\nBuilding our map')
    my_map = maze.Maze(maze.MAZE_map, maze.MAZE_map_endpts)
    my_map.print()

    print('Starting the search')
    search(my_map)

if __name__ == '__main__':
    main()