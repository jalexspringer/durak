from durak import *
from game import *

# GLOBAL CONSTANTS
HAND_SIZE = 6
SUITS = ['D', 'C', 'H', 'S']
# SUITS = ['H', 'S'] # Limited suits for testing.

# Starting a game of Durak
print("\nWelcome to Durak!")
player_count = number_of_players()
print("\nThank you - have a good game!")

# Create deck, shuffle into talon, create hands, instantiate battlefield
talon = card_gen(SUITS)
trump = assign_trump(talon)
hands = create_hands(player_count)
players = create_players(player_count)
battlefield = {'attack': [], 'defense': []}
discard = []

# First deal, find out who goes first, assign initial attacker and defender values
dealer(hands, talon, HAND_SIZE)
attacker, low_card = first_to_play(hands, trump)
defender = next_player(attacker, player_count)
print("Player {} has the lowest trump - {} - and will play first.".format(attacker, low_card))
print("---------------------------------\n")


# Run the main game loop until only one hand has cards left.
counter = 0
while counter < player_count - 1:
    # MAIN GAME LOOP
    dealer(hands, talon, HAND_SIZE)
    if len(hands[attacker]) > 0:
        attacker, defender = main_game_loop(player_count, hands, trump, talon, attacker, defender, battlefield, discard)
        battlefield = {'attack': [], 'defense': []}
        counter = check_win_condition(hands)
    else:
        attacker = next_player(attacker, player_count)
        defender = next_player(attacker, player_count)

loser = 0
for k, v in hands.items():
    if len(v) > 0:
        loser = k
print("Game over! Player {} is the durak and worthy of much derision.".format(loser))
