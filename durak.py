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
    # shuffle(deck)
    return deck


def assign_trump(talon):
    """sets global trump variable - use at the start of each game"""
    trump = talon[0]
    return trump


def create_hands(players):
    """Creates empty list for each player's hand"""
    hands = {}
    i = players
    while i > 0:
        hands[i] = []
        i -= 1
    return hands


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
    return first_player, low_card
