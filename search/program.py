# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from .core import CellState, Coord, Action
from .utils import render_board, create_root, goal_test, find_children, evaluate_heuristic, serialize, get_path
import heapq

def search(
    board: dict[Coord, CellState]
) -> list[Action] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to `CellState` instances (each with a `.color` and
            `.height` attribute).

    Returns:
        A list of actions (MoveAction, EatAction, or CascadeAction), or `None`
        if no solution is possible.
    """



    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Each node is represented as a tuple: (state, parent, action, depth, children)

    # Do some impressive AI stuff here to find the solution...

    visited = set()

    heap_list = []
    root_node = create_root(board)

    heapq.heappush(heap_list, (evaluate_heuristic(root_node.state), 0, root_node))
    counter = 1
    while heap_list:
        _, _, current = heapq.heappop(heap_list)

        key = serialize(current.state)
        if key in visited:
            continue
        visited.add(key)
        
        if goal_test(current.state):
            return get_path(current)
        
        find_children(current)

        for child in current.children:

            key = serialize(child.state)
            if key in visited:
                continue

            g = child.depth
            h = evaluate_heuristic(child.state)
            f = g + h
            
            heapq.heappush(heap_list, (f, counter, child))
            counter += 1
    
    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.

    # python -m search < test-vis5.csv
    return None
