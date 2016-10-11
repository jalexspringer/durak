def print_hand(hand, player):
    """Takes single list of PlayingCard objects and the player number, prints hand in string format
        Also prints remaining cards in talon and trump card to remind players."""
    hand_string = "Player {} current hand: ".format(player)
    sorted_hand = sorted(hand, key=lambda x: (x.suit, x.value))
    for card in sorted_hand:
        hand_string += "{}  ".format(card.card_name())
    print(hand_string)


def print_battlefield(battlefield):
    """Takes the battlefield and prints to the console"""
    print_string = 'Attacks: '
    for card in battlefield['attack']:
        print_string += card.card_name() + " | "
    print(print_string)
    print_string = 'Defense: '
    for card in battlefield['defense']:
        print_string += card.card_name() + " | "
    print(print_string + "\n")


def play_card(hand, active_player, attacking=True):
    """Takes a list of cards and user input, returns the card, and the hand minus the card.
       Runs until a card that is in the hand is input.
       Defaults to the attacker dialogue, set 3rd param to False for defender."""
    if attacking:
        state = 'attack'
    else:
        state = 'defend'
    while True:
        played = input("Player {}, what card would you like to {} with? ".format(active_player, state))
        for idx, card in enumerate(hand):
            if card.card_name() == played.upper():
                valid_play = hand.pop(idx)
                return valid_play, hand
        print("That card is not in your hand. Please select a card from your hand.")


def next_player(active_player, player_count):
    """Increments active_player to start the next turn
        Also used to assign defender value."""
    if active_player != player_count:
        active_player += 1
    else:
        active_player = 1
    return active_player


def first_attack(valid_play):
    """Plays first valid card to battlefield"""
    return valid_play


def to_defend(hand, played, trump):
    """Checks that the defender has a playable card, returns playable card options.
        Ask if the defender intends to continue the defense or take the cards"""
    valid_cards = ""
    for card in hand:
        if card.suit == played.suit and card.value > played.value:
            valid_cards += card.card_name() + " "
        elif card.suit == trump:
            valid_cards += card.card_name() + " "
    if len(valid_cards) > 0:
        while True:
            print("Valid card options: {}".format(valid_cards))
            defending = input("Type 'defend' or 'take' to continue: ")
            if defending == 'defend':
                return True
            elif defending == 'take':
                return False
            else:
                print("{} is not an option.".format(defending))
    else:
        print("No valid options - taking cards.")
        return False


def to_attack(hand, battlefield):
    """Checks that the attacker has a playable card, returns playable card options.
    Ask if the attacker intends to continue the attack or pass"""
    valid_cards = ""
    values = []
    for k, v in battlefield:
        for card in v:
            if card.value not in values:
                values.append(card.value)
    for card in hand:
        if card.value in values:
            valid_cards += card.card_name() + " "
    if len(valid_cards) > 0:
        while True:
            print("Valid card options: {}".format(valid_cards))
            attacking = input("Type 'attack' or 'pass' to continue: ")
            if attacking == 'attack':
                return True
            elif attacking == 'pass':
                return False
    elif len(battlefield['attack']) >= 6:
        print("Max rounds (6) completed - discarding cards and ending the turn.")
    else:
        print("No valid options - discarding cards and ending the turn.")
        return False


def defense(valid_play, attack):
    """Takes a valid card (in defender's hand) and the attacking card.
    If valid defense, play card to battlefield, return True. If "Take", return False"""


def next_attack(valid_play, battlefield):
    """Checks card against battlefield to ensure that it is legal. Plays card to battlefield."""


def throw_in(valid_play):
    """After defense() returns False, attacker has the option to add in all cards of a certain value
        Presents attacker with a choice - throw in? not throw in? If yes, adds cards to attack side of battlefield"""
