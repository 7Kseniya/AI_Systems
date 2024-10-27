from pyswip import Prolog
from main import Colors

# Initialize Prolog
prolog = Prolog()

# Load the knowledge base from a file
prolog.consult("../lab1/chess_facts.pl")  

def get_game_modes():
    return list(prolog.query("game_mode(Mode)"))

def get_game_time(mode):
    return list(prolog.query(f"game_time({mode}, Time)"))

def get_rules():
    return list(prolog.query("rule(Name, Description)"))

def get_starting_position(piece, color):
    return list(prolog.query(f"position({piece}, {color}, Position)"))

def get_piece_color(piece):
    return list(prolog.query(f"color_piece({piece}, Color)"))

# Example usage
if __name__ == "__main__":
    modes = get_game_modes()
    print(f"{Colors.MAGENTA}Game Modes:{Colors.RESET}")
    for mode in modes:
        print(mode['Mode'])

    time = get_game_time("classic")
    print(f"{Colors.MAGENTA}Classic Game Time:{Colors.RESET}")
    for t in time:
        print(t['Time'])

    rules = get_rules()
    print(f"{Colors.MAGENTA}Game Rules:{Colors.RESET}")
    for rule in rules:
        print(f"{rule['Name']}: {rule['Description']}")

    position = get_starting_position("king", "white")
    print(f"{Colors.MAGENTA}White King's Position:{Colors.RESET}")
    for pos in position:
        print(pos['Position'])

    color = get_piece_color("queen")
    print(f"{Colors.MAGENTA}Queen's Colors:{Colors.RESET}")
    for c in color:
        print(c['Color'])