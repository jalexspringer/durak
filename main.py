from durak import *
from game import *

# GLOBAL CONSTANTS
HAND_SIZE = 6
SUITS = ['D', 'C', 'H', 'S']

# Starting a game of Durak
print("Welcome to Durak!")
player_count = number_of_players()
print("Thank you - have a good game!")

# Create deck, shuffle into talon, create hands, instantiate battlefield
talon = card_gen(SUITS)
trump = assign_trump(talon)
hands = create_hands(player_count)
battlefield = {'attack': [], 'defense': []}

# First deal, find out who goes first
dealer(hands, talon, HAND_SIZE)
active_player = first_to_play(hands, trump)
attacker = first_to_play(hands, trump)

# Initial print of game state
print_seats(player_count, hands, trump, talon)
for player, hand in hands.items():
    print_hand(hand, player)

# Begin main game loop
# TODO Make this an actual loop :)
# First attack
played, hands[active_player] = play_card(hands[active_player], active_player, attacker)
battlefield['attack'].append(played)

# Print state after first attack
print_seats(player_count, hands, trump, talon)
print_battlefield(battlefield)
print_hand(hands[active_player], active_player)

# Defense
