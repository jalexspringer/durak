class PlayingCard:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def card_name(self):
        return str(self.value) + self.suit


def number_of_players():
    """Take player input to create the number of players in the game - 2, 3, 4"""
    player_count = int(input("How many players? (2, 3, or 4) "))
    acceptable = [2, 3, 4]
    while player_count not in acceptable:
        player_count = int(input("{} is not a valid answer. Please enter 2, 3, or 4. ".format(player_count)))
    return player_count


def card_gen(suits):
    """Takes a list of suits and returns a shuffled 36 card deck (values 6 - Ace(14))"""
    from random import shuffle
    deck = []
    for suit in suits:
        for value in range(6, 15):
            deck.append(PlayingCard(suit, value))
    shuffle(deck)
    return deck


def assign_trump(talon):
    """sets global trump variable - use at the start of each game"""
    trump = talon[0]
    print("Trump card is {}".format(trump.card_name()))
    return trump


def create_hands(players):
    """Creates empty list for each player's hand"""
    hands = {}
    i = players
    while i > 0:
        hands[i] = []
        i -= 1
    return hands


def dealer(hands, talon, hand_size):
    """Brings each hand's card count up to the HAND_SIZE"""
    print("Dealing...")
    print("---------------------------------\n")
    for k, v in hands.items():
        while len(v) < hand_size and len(talon) > 0:
            v.append(talon.pop())


def first_to_play(hands, trump):
    """Checks each hand for the lowest trump card and returns who goes first."""
    lowest = 15
    first_player = 1
    low_card = 0
    for player, hand in hands.items():
        for card in hand:
            if card.suit == trump.suit and card.value < lowest:
                lowest = card.value
                first_player = player
                low_card = card.card_name()
    print("Player {} has the lowest trump - {} - and will play first.".format(first_player, low_card))
    print("---------------------------------\n")
    return first_player


def print_hand(hand, player):
    """Takes single list of PlayingCard objects and the player number, prints hand in string format
        Also prints remaining cards in talon and trump card to remind players.
    """
    hand_string = "Player {} current hand: ".format(player)
    for card in hand:
        hand_string += "{}  ".format(card.card_name())
    print(hand_string)


def print_seats(players, hands, trump, talon):
    """Generates a simple display to keep the player updated. Varies based on number of players.
        Shows total card count for each player, and whose turn it is."""
    if players == 2:
        print("     Player 2 ({} cards)    ".format(len(hands[2])))
        print("         |        ")
        print("         |        ")
        print("         |        ")
        print("         |        ")
        print("     Player 1 ({} cards)    \n".format(len(hands[1])))
    elif players == 3:
        print("     Player 3 ({} cards)    ".format(len(hands[3])))
        print("      /             |   ")
        print("     /              |   ")
        print("Player 2 ({} cards)  |".format(len(hands[2])))
        print("     \              |   ")
        print("      \             |   ")
        print("     Player 1 ({} cards)    \n".format(len(hands[1])))
    elif players == 4:
        print("      Player 3 ({} cards)    ".format(len(hands[3])))
        print("      /                 \ ")
        print("     /                   \ ")
        print("Player 2 ({} cards)    Player 4 ({} cards)".format(len(hands[2]), len(hands[4])))
        print("     \                   /")
        print("      \                 / ")
        print("      Player 1 ({} cards)    \n".format(len(hands[1])))
    print_state(trump, talon)


def print_state(trump, talon):
    """Prints important game state information"""
    print("Remaining cards: {}".format(len(talon)))
    print("Trump card: {}".format(trump.card_name()))
    print("---------------------------------\n")