from durak import *
from game import *

# GLOBAL CONSTANTS
HAND_SIZE = 6
SUITS = ['D', 'C', 'H', 'S']

# Starting a game of Durak
print("\nWelcome to Durak!")
player_count = number_of_players()
print("\nThank you - have a good game!")

# Create deck, shuffle into talon, create hands, instantiate battlefield
talon = card_gen(SUITS)
trump = assign_trump(talon)
hands = create_hands(player_count)
battlefield = {'attack': [], 'defense': []}

# First deal, find out who goes first, assign initial attacker and defender values
dealer(hands, talon, HAND_SIZE)
attacker, low_card = first_to_play(hands, trump)
defender = next_player(attacker, player_count)
print("Player {} has the lowest trump - {} - and will play first.".format(attacker, low_card))
print("---------------------------------\n")

# Initial print of game state
print_seats(player_count, hands, trump, talon)
print_hand(hands[attacker], attacker)

# Begin main game loop
# TODO Make this an actual loop :)

# First attack
played, hands[attacker] = play_card(hands[attacker], attacker)
battlefield['attack'].append(played)

# Print state after first attack
print_seats(player_count, hands, trump, talon)
print_battlefield(battlefield)

# Defense
print_hand(hands[defender], defender)
if to_defend(hands[defender], played, trump):
    print("\nYOU ARE DEFENDING!")
