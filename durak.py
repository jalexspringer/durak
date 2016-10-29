class PlayingCard:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def card_name(self):
        return str(self.value) + self.suit


class Player:
    def __init__(self, player_number):
        self.player_number = player_number
        self.hand = []
        self.human = True

    def return_hand(self):
        return self.hand

    def replace_hand(self, new_hand):
        self.hand = new_hand


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
    return trump


def create_hands(players):
    """Creates empty list for each player's hand"""
    hands = {}
    i = players
    while i > 0:
        hands[i] = []
        i -= 1
    return hands


def create_players(player_count):
    """Instantiates Player objects for each player"""
    players = {}
    for i in range(player_count):
        players[i] = Player(i+1)
    return players


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
