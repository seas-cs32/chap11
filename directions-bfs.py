### chap11/directions-bfs.py
import maze

# Marks for map, which use color codes for terminal printing
EXPLORED = '\033[34m*\033[0m' # blue *
FRONTIER = '\033[32mf\033[0m' # green f

# Keep track of the tree of explored paths
class TreeNote():
    def __init__(self, state, parent, action):
        self.state = state    # current location 
        self.parent = parent  # previous note in path
        self.action = action  # action that got us to this location


def search(my_map):
    # Set the current state and mark the map location explored
    cur_loc = my_map.start
    my_map.mark(cur_loc, EXPLORED)
    cur_note = TreeNote(cur_loc, None, None)

    # Build a list on which to keep known but unexplored locations
    frontier = []

    while cur_loc != my_map.goal:    # search loop
        # What unexplored next steps are possible?
        moves = my_map.possible_moves(cur_loc, EXPLORED)

        # Add moves not already on the frontier to the frontier
        for a_move in moves:
            loc = my_map.simulate_move(cur_loc, a_move)
            if loc not in frontier:
                new_note = TreeNote(loc, cur_note, a_move)
                frontier.append(new_note)
                my_map.mark(loc, FRONTIER)

        # DEBUG: Uncomment to watch the frontier grow
        # print(my_map)
        # input('Ready to move on? ')

        if len(frontier) == 0:
            print('No solution')
            return

        # Choose a note from the frontier as next to explore
        next_note = frontier.pop(0)
        next_loc = next_note.state
        my_map.mark(next_loc, EXPLORED)

        # Update current state
        cur_note = next_note
        cur_loc = next_loc

    # Follow the parent links from cur_note to create
    # the actual driving directions
    ddirections = [cur_note]
    while cur_note.parent:
        cur_note = cur_note.parent
        ddirections.insert(0, cur_note)

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