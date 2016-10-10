from durak import *

# GLOBAL CONSTANTS
HAND_SIZE = 6
SUITS = ['D', 'C', 'H', 'S']

"""Starting a game of Durak"""
print("Welcome to Durak!")
player_count = number_of_players()

"""Create deck, shuffle into talon, create hands"""
talon = card_gen(SUITS)
trump = assign_trump(talon)
hands = create_hands(player_count)

"""First deal, find out who goes first"""
dealer(hands, talon, HAND_SIZE)
first_player = first_to_play(hands, trump)

print("Have a good game!")

print_seats(player_count, hands, trump, talon)
for player, hand in hands.items():
    print_hand(hand, player)
