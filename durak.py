# Global variables
TALON = []
TRUMP = ''
HAND_SIZE = 6
HANDS = {}
SUITS = ['D', 'C', 'H', 'S']
PLAYERS = 0
FIRST_PLAYER = 1
DISCARD = []

class PlayingCard:
    def __init__(self, suit, value):    
        self.suit = suit
        self.value = value

    def card_name(self):
        return str(self.value) + self.suit


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
    i = int(players)
    while i > 0:
        HANDS[i] = []
        i -= 1


def dealer(hands, talon):
    """Brings each hand's card count up to the HAND_SIZE"""
    print("Dealing...")
    print("---------------------------------\n")
    for k, v in hands.items():
        while len(v) < HAND_SIZE and len(talon) > 0:
            v.append(talon.pop())


def print_hand(hand, player, talon=TALON, trump=TRUMP):
    """Takes single list of PlayingCard objects and the player number, prints hand in string format
        Also prints remaining cards in talon and trump card to remind players.
    """
    # TODO replace face card value with letters - not needed in GUI?
    hand_string = "Player {} current hand: ".format(player)
    for card in hand:
        hand_string += "{}  ".format(card.card_name())
    print(hand_string)
    print("Remaining cards: {}".format(len(talon)))
    print("Trump card: {}\n".format(trump.card_name()))
    print("---------------------------------\n")


def print_seats():
    print("PLAYERS = {}".format(PLAYERS))
    if PLAYERS == 2:
        print("     Player 2 ({} cards)    ".format(len(hands[2])))
        print("         |        ")
        print("         |        ")
        print("         |        ")
        print("     Player 1 ({} cards)    ".format(len(hands[1])))


def first_to_play(hands, trump):
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