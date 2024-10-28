import random
import re
from pyswip import Prolog
import chess
from colors import Colors

# Initialize Prolog
prolog = Prolog()

# Load the knowledge base from a file
prolog.consult("../lab1/chess_facts.pl") 

# Define patterns for matching user input
difficulty_pattern = r'(beginner|novice|easy|simple|intermediate|medium|average|advanced|hard|expert)'
rules_known_pattern = r'(know the rules|knows the rules|understand the rules|familiar with the rules|do not know the rules|does not know the rules|unfamiliar with the rules)'
game_mode_pattern = r'(fast|quick|short|blitz|classic)'

def get_game_mode_and_time(preference):
    query_mode = f"game_mode({preference})"
    query_time = f"game_time({preference}, Time)"
    
    try:
        modes = list(prolog.query(query_mode))
        times = list(prolog.query(query_time))
    except Exception as e:
        print(f"{Colors.RED}Error querying Prolog: {e}{Colors.RESET}")
        return None, None
    
    if modes and times:
        return preference, times[0]['Time']
    else:
        return None, None

def get_rules():
    try:
        rules = list(prolog.query("rule(Name, Description)"))
    except Exception as e:
        print(f"{Colors.RED}Error querying Prolog: {e} {Colors.RESET}")
        return {}
    
    return {rule['Name']: rule['Description'] for rule in rules}

def parse_user_input(user_input):
    """Parse the user input to extract game mode, difficulty, and rules familiarity."""
    knows_rules = True  # Default to true if no specific mention

    # Check for rule familiarity
    rules_known_match = re.search(rules_known_pattern, user_input)
    if rules_known_match:
        knows_rules = 'know' in rules_known_match.group(0).lower()
    else:
        while True:
            rules_response = input(f"{Colors.MAGENTA}Do you know the rules?{Colors.RESET} (yes/no): ").strip().lower()
            if rules_response in ['yes', 'no']:
                knows_rules = rules_response == 'yes'
                break
            else:
                print(f"{Colors.RED}Invalid input. Please enter 'yes' or 'no'.{Colors.RESET}")

    # Check for game mode and difficulty
    mode_match = re.search(game_mode_pattern, user_input)
    difficulty_match = re.search(difficulty_pattern, user_input)

    return mode_match, difficulty_match, knows_rules

def normalize_difficulty(difficulty_match):
    """Normalize difficulty levels based on user input."""
    if difficulty_match:
        difficulty = difficulty_match.group(0).lower()
        if difficulty in ['beginner', 'novice', 'easy', 'simple']:
            return 'easy'
        elif difficulty in ['intermediate', 'medium', 'average']:
            return 'medium'
        else:
            return 'hard'
    else:
        while True:
            difficulty_input = input(f"{Colors.MAGENTA}Please specify your difficulty level {Colors.RESET}(beginner, intermediate, advanced): ")
            difficulty_match = re.search(difficulty_pattern, difficulty_input)
            if difficulty_match:
                return normalize_difficulty(difficulty_match)
            else:
                print(f"{Colors.RED}Invalid input. Please enter a valid difficulty level.{Colors.RESET}")

def get_user_input():
    """Get input from the user with a usage example."""
    usage_example = "blitz easy or classic hard"
    while True:
        user_input = input(f"{Colors.MAGENTA}Enter your preferences. For example:{Colors.RESET} '{usage_example}': ").strip().lower()
        
        if user_input:
            return user_input
        else:
            print(f"{Colors.RED}Input cannot be empty. Please try again.{Colors.RESET}")

def determine_game_mode(mode_match):
    """Determine the game mode based on user input."""
    if mode_match:
        mode_preference = mode_match.group(0)
        if mode_preference in ['fast', 'quick', 'short']:
            return 'fast_chess'
        else:
            return str(mode_preference)
    else:
        while True:
            mode_input = input(f"{Colors.MAGENTA}Please specify your mode preference {Colors.RESET}(blitz, fast chess, classic): ")
            mode_match = re.search(game_mode_pattern, mode_input)
            if mode_match:
                return determine_game_mode(mode_match)
            else:
                print(f"{Colors.RED}Invalid input. Please enter a valid game mode.{Colors.RESET}")

def get_recommended_move(fen_position):
    # Creating a chessboard from a FEN string
    board = chess.Board(fen_position)
    
    # Get all possible moves for the current position
    legal_moves = list(board.legal_moves)
    
    if not legal_moves:
        return "No moves available. The game is over."
    
    move = legal_moves[random.choice([0, 1, 2, 3, 4])]
    
    # Get the start and end squares in coordinate format
    start_square = chess.square_name(move.from_square)
    end_square = chess.square_name(move.to_square)
    
    return f"Recommended move: {start_square} -> {end_square}"

if __name__ == "__main__":
    print(f"{Colors.CYAN}Welcome to the chess game recommendation system!{Colors.RESET}")

    while True:
        user_input = get_user_input()
        mode_match, difficulty_match, knows_rules = parse_user_input(user_input)
        # Provide rules if the user does not know them
        if not knows_rules:
            while True:
                show_rules = input(f"{Colors.MAGENTA}Would you like to know the rules of the game?{Colors.RESET} Enter 'yes' to view the rules: ").strip().lower()
                if show_rules == 'yes':
                    rules = get_rules()
                    for rule, description in rules.items():
                        print(f"{Colors.CYAN}{rule}:{Colors.RESET} {description}")
                    break
                elif show_rules == 'no':
                    break
                else:
                    print(f"{Colors.RED}Invalid input. Please enter 'yes' or 'no'.{Colors.RESET}")

        game_mode = determine_game_mode(mode_match)
        mode, time = get_game_mode_and_time(game_mode)

        if mode and time:
            print(f"Recommended game mode: {Colors.CYAN}{mode.capitalize()}{Colors.RESET}, duration: {Colors.CYAN}{time}{Colors.RESET} minutes.")
        else:
            print(f"{Colors.RED}Sorry, that game mode was not found.{Colors.RESET}")

        difficulty = normalize_difficulty(difficulty_match)

        print(f"Recommended difficulty level: {Colors.CYAN}{difficulty.capitalize()}{Colors.RESET}.")

        # Generate a random FEN position for the game
        player_color_pos = random.choice(['w', 'b'])
        fen_position = f"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR {player_color_pos} KQkq - 0 1"
        
        if player_color_pos =='w':
            player_color = 'white'
        else: player_color = 'black'
        
        if difficulty == 'easy':
            # print(f"{Colors.CYAN}Here's your starting position: {Colors.RESET}{fen_position}")
            print(f"{Colors.CYAN}You are playing as {player_color}.{Colors.RESET}")

            while True:
                ask_for_move = input(f"{Colors.MAGENTA}Would you like a recommended move?{Colors.RESET} (yes/no): ").strip().lower()
                if ask_for_move == 'yes':
                    recommended_move = get_recommended_move(fen_position)
                    print(f"{Colors.CYAN}{recommended_move}{Colors.RESET}")
                    break
                elif ask_for_move == 'no':
                    break
                else:
                    print(f"{Colors.RED}Invalid input. Please enter 'yes' or 'no'.{Colors.RESET}")

        # Ask the user if they want to continue
        while True:
            continue_input = input(f"{Colors.MAGENTA}Do you want to continue?{Colors.RESET}(yes/no): ").strip().lower()
            if continue_input in ['yes', 'no']:
                if continue_input != 'yes':
                    print(f"{Colors.CYAN}Thank you for using the chess game recommendation system! Goodbye!{Colors.RESET}")
                    exit()
                break
            else:
                print(f"{Colors.RED}Invalid input. Please enter 'yes' or 'no'.{Colors.RESET}")