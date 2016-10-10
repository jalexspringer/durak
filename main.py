from durak import *

"""Starting a game of Durak"""
print("Welcome to Durak!")
PLAYERS = input("How many players? (2, 3, or 4) ")
# TODO implement error handling for incorrect inputs - move intro to module?

"""Create deck, shuffle into talon, create hands"""
TALON = card_gen(SUITS)
create_hands(PLAYERS)

print("Have a good game!")
TRUMP = assign_trump(TALON)

"""First deal, find out who goes first"""
dealer(HANDS, TALON)
FIRST_PLAYER = first_to_play(HANDS, TRUMP)

# TODO this line will eventually only show Player 1's hand (human)
for player, hand in HANDS.items():
    print_hand(hand, player, TALON, TRUMP)
print_seats()
