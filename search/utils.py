# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from dataclasses import dataclass

from .core import Coord, CellState, PlayerColor, Direction, BOARD_N, MoveAction, EatAction, CascadeAction


def apply_ansi(
    text: str,
    bold: bool = False,
    color: str | None = None
):
    """
    Wraps some text with ANSI control codes to apply terminal-based formatting.
    Note: Not all terminals will be compatible!
    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{text}\033[0m"


def render_board(
    board: dict[Coord, CellState],
    ansi: bool = False
) -> str:
    """
    Visualise the board via a multiline ASCII string, including optional ANSI
    styling for terminals that support this. Cells are displayed as R3, B2, etc.
    """
    output = ""
    for r in range(BOARD_N):
        for c in range(BOARD_N):
            cell = board.get(Coord(r, c), CellState())
            if cell.is_stack:
                color_char = "R" if cell.color == PlayerColor.RED else "B"
                text = f"{color_char}{cell.height}"
                if ansi:
                    ansi_color = "r" if cell.color == PlayerColor.RED else "b"
                    output += apply_ansi(f"{text:>3}", color=ansi_color)
                else:
                    output += f"{text:>3}"
            else:
                output += " . "
            output += " "
        output += "\n"
    return output


def goal_test(state):
    """Test if we have reached the goal state"""
    for cell in state.values():
        if cell.color == PlayerColor.BLUE:
            return False
    return True


def create_root(initial_state):
    return Node(initial_state,None, 0, [])


def in_bounds(coord):
    return 0 <= coord.r < 8 and 0 <= coord.c < 8

def evaluate_heuristic(state): #heuristic based on number of enemy pieces
    heuristic = 0
    for cell in state.values():
        if cell.color == PlayerColor.BLUE:
            heuristic += cell.height
    return heuristic

@dataclass
class Node: #Defining a class for node to make it easier. I don't believe the previous_action is necessary. If it is, we can add it later.
    state: dict[Coord, CellState]
    parent_node: 'Node'
    depth: int
    children: list['Node']

    def __init__(self, state:dict, parent_node: 'Node', depth: int, children):
        self.state = state
        self.parent_node = parent_node
        self.depth = depth
        self.children = children
        
def find_children(node: Node):
    #check all four directions
    
    """
    1. Get a list of all pieces that have possible moves
    2. Iterate through all moves for each piece
    """
    children = []
    for coord in node.state:
        if node.state[coord].color == PlayerColor.RED:

            for direction in Direction:#this code is still wrong, ignore
         #check move first
                move_action = MoveAction(coord,direction)
                new_node = apply(move_action, node)
                if(new_node.state != node.state):
                    children.append(new_node)   

                
        
        #check eat
                eat_action = EatAction(coord, direction)
                new_node = apply(eat_action, node)

                if(new_node.state != node.state):
                    children.append(new_node)
                
                
        #check cascade
                cascade_action = CascadeAction(coord, direction)
                new_node = apply(cascade_action, node)

                if(new_node.state != node.state):
                    children.append(new_node)  
    node.children = children
                

    

def apply(action, node: Node):
    """Takes a node and an action and applies the action to that node. Returns a new node after the action have been applied."""
    state = node.state
    depth = node.depth
    new_state = [] # creates a deep copy of state
    new_state = dict(new_state)
    for coord, cell_state in state.items():
        new_state[coord] = CellState(cell_state.color, cell_state.height)
        
    new_depth = depth + 1
    new_node = Node(new_state, node, new_depth, []) #some redundancy in this

    if isinstance(action, MoveAction):
        try:
            next_coord = action.coord + action.direction
        except ValueError:
            new_node = Node(new_state, node, new_depth, [])
            return new_node
        if next_coord in state:
            if state[next_coord].color == PlayerColor.BLUE: #to disallow moving onto an enemy pieces
                new_node = Node(new_state, node, new_depth, [])
            if state[next_coord].color == PlayerColor.RED:
                del new_state[next_coord]
                new_state[next_coord] = CellState(PlayerColor.RED, state[next_coord].height + state[action.coord].height)
                del new_state[action.coord]
            
        elif in_bounds(next_coord): #why does out of bounds need to be checked twice? Does ValueError do the same thing?
            new_state[next_coord] = state[action.coord]
            del new_state[action.coord]
    

    if isinstance(action, EatAction):
        try:
            next_coord = action.coord + action.direction
        except ValueError:
            new_node = Node(new_state, node, new_depth, [])
            return new_node
        if next_coord in state:
            if state[next_coord].color == PlayerColor.BLUE and state[next_coord].height <= state[action.coord].height:
                del new_state[next_coord]
                new_state[next_coord] = state[action.coord]
                del new_state[action.coord]
    

    if isinstance(action, CascadeAction):
        height = state[action.coord].height
        if height > 1:
            del new_state[action.coord]
            current = action.coord
            for _ in range(height):
                try:
                    next_coord = current + action.direction
                except ValueError:
                    break
                if next_coord not in new_state:
                    new_state[next_coord] = CellState(PlayerColor.RED, 1)
                    current = next_coord
                else:
                    chain = []
                    temp = next_coord
                    while True:
                        if temp not in new_state:
                            break
                        chain.append(temp)
                        try:
                            temp = temp + action.direction
                        except ValueError:
                            break
                    print(chain)
                    for pos in reversed(chain):
                        new_state[temp] = new_state[pos]
                        del new_state[pos]
                        temp = pos
                    new_state[next_coord] = CellState(PlayerColor.RED, 1)
                    current = next_coord
    
                new_node = Node(new_state, node, new_depth, [])

    return new_node
