import re
from pyswip import Prolog
prolog = Prolog()
prolog.consult("./prolog/lab1/chess_facts.pl")
prolog.consult("./prolog/lab1/chess_rules.pl")

usage_example = str('I am a beginner who knows the rules and wants fast game')
def get_user_input():
    user_input = input(f" Enter your preferences. For example: '{usage_example}'")
    if user_input:
        return user_input
    else: 
        print("Input cannot be empty. Please try again" )

def parse_input(user_input):
    difficulty = None
    rules_known = None
    fast_game = None

    difficulty_pattern = r'(beginner|novice|easy|simple|intermediate|medium|average|advanced|hard|expert)'
    rules_known_pattern = r'(know the rules|knows the rules|understand the rules|familiar with the rules|do not know the rules|does not know the rules|unfamiliar with the rules)'
    fast_game_pattern = r'(fast|quick|short|blitz|)'

    difficulty_match = re.search(difficulty_pattern, user_input, re.IGNORECASE)
    rules_known_match = re.search(rules_known_pattern, user_input, re.IGNORECASE)
    fast_game_match = re.search(fast_game_pattern, user_input, re.IGNORECASE)

    
    if difficulty_match:
        difficulty = difficulty_match.group(0).lower()
        if difficulty in ['beginner', 'notice', 'easy', 'simple']:
            difficulty = 'easy'
        elif difficulty in ['intermediate', 'medium', 'avarage']:
            difficulty = 'medium'
        else:
            difficulty = 'hard'
    else:
        print("Invalid difficulty level. Please specify: \nbeginner\nintermediate\nadvanced'")
    
    if rules_known_match:
        rules_known = 'know' in rules_known_match.group(0).lower()
    else:
        print("Invalid input. Please specify whether you know the rules or not")
    
    if fast_game_match:
        fast_game = True
    else:
        fast_game = False
        
    return str(difficulty), str(rules_known), str(fast_game)

def get_recommendation(difficulty, rules_known, fast_game):
    game_mode = None
    if fast_game:
        game_mode = ['blitz', 'fast_chess']
    else:
        game_mode = 'classic'
    query = f'game_mode(Mode), Mode = {game_mode[0]}, Difficulty = {difficulty}, Rules = {rules_known}, write(', '), write(Difficulty), nl, fail.'
    results = list(prolog.query(query=query))
    if results:
        recommended_game_mode = results[0]["Mode"]
        recommended_difficulty = results[0]["Difficulty"]
        return recommended_game_mode, recommended_difficulty
    else:
        return None, None
    
def print_rules():
    query = "rule(Name, Description), write(Name), write(': '), write(Description), nl, fail."
    print("Chess rules:")
    results = list(prolog.query(query=query))
    for result in results:
        print(f'{result['Name']}: {result['Description']}')

if __name__ == "__main__":
    user_input = get_user_input()
    difficulty, rules_known, fast_game = parse_input(user_input=user_input)
    if difficulty == 'easy':
        remind_rules = input("Do you want us to remind you the rules? (yes/no): ")
        if remind_rules.lower() == 'yes':
            print_rules()
        else:
            rules_known = False
    elif rules_known is None:
        rules_known = input("Do you know the rules? (yes/no): ")
        rules_known = rules_known.lower() == 'yes'

    if difficulty and rules_known and fast_game is not None and fast_game is not None:
        recommended_game_mode, recommended_difficulty = get_recommendation(difficulty, rules_known, fast_game)

        if recommended_game_mode and recommended_difficulty:
            print(f"Based on your preferences, we recommend the following game mode: {recommended_game_mode}")
            print(f"We also recommend the following difficulty level: {recommended_difficulty}")
        else:
            print("No recommendations found based on your preferences.")
    else:
        print("Invalid input. Please specify your difficulty level, whether you know the rules, and whether you want a fast game.")
    