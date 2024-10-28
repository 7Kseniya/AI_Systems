import random
from colors import Colors
from script import get_user_input, parse_user_input, get_rules, determine_game_mode, normalize_difficulty, get_recommended_move, get_game_mode_and_time
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