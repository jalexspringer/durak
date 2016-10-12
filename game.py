def main_game_loop(player_count, hands, trump, talon, attacker, defender, battlefield):
    # New turn print of game state
    print_seats(player_count, hands, trump, talon)
    print_hand(hands[attacker], attacker)

    # First attack
    played, hands[attacker] = play_card(hands[attacker], attacker)
    battlefield['attack'].append(played)

    # Print state after first attack
    print_all(player_count, hands, trump, talon, battlefield)

    # Defense/attack loop
    while True:
        # Show legal cards, offer a chance to defend or take all cards
        if to_defend(hands[defender], played, trump, defender):  # defend
            played, hands[defender] = play_card(hands[defender], defender, False)
            battlefield['defense'].append(played)
            print_all(player_count, hands, trump, talon, battlefield)

            # Show legal cards, offer a chance to attack or pass and end attack
            if to_attack(hands[attacker], battlefield, attacker):  # attack
                played, hands[attacker] = play_card(hands[attacker], attacker)
                battlefield['attack'].append(played)
                print_all(player_count, hands, trump, talon, battlefield)
            else:  # pass
                # If the game has 3 or 4 players, the attack can be continued by the player after the defender
                # if player_count > 2 and press:
                #    press_attack(player_count, hands, trump, talon, attacker, defender, battlefield, hand_size)
                print("PLAYER {} - DISCARDING CARDS - END OF ATTACK".format(attacker))
                # TODO Discard cards list
                attacker = next_player(attacker, player_count)
                defender = next_player(defender, player_count)
                return attacker, defender
        else:  # take all cards
            battlefield['attack'].append(throw_in(battlefield, hands[attacker]))
            print("PLAYER {} - TAKING CARDS AND SKIPPING YO TURN!!".format(defender))
            for k, v in battlefield.items():
                for card in v:
                    hands[defender].append(card)
            for i in range(2):
                attacker = next_player(attacker, player_count)
                defender = next_player(defender, player_count)
            return attacker, defender


def dealer(hands, talon, hand_size):
    """Brings each hand's card count up to the HAND_SIZE"""
    print("Dealing...")
    print("---------------------------------\n")
    for k, v in hands.items():
        while len(v) < hand_size and len(talon) > 0:
            v.append(talon.pop())


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


def to_defend(hand, played, trump, defender):
    """Checks that the defender has a playable card, returns playable card options.
        Ask if the defender intends to continue the defense or take the cards"""
    valid_cards = ""
    for card in hand:
        if card.suit == played.suit and card.value > played.value:
            valid_cards += card.card_name() + " "
        if card.suit == trump:
            valid_cards += card.card_name() + " "
    if len(valid_cards) > 0:
        while True:
            print_hand(hand, defender)
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


def to_attack(hand, battlefield, attacker):
    """Checks that the attacker has a playable card, returns playable card options.
    Ask if the attacker intends to continue the attack or pass"""
    valid_cards = ""
    values = []
    for k, v in battlefield.items():
        for card in v:
            if card.value not in values:
                values.append(card.value)
    for card in hand:
        if card.value in values:
            valid_cards += card.card_name() + " "
    if len(valid_cards) > 0:
        while True:
            print_hand(hand, attacker)
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


def throw_in(battlefield, hand):
    valid_cards = ""
    values = []
    cards = []
    for k, v in battlefield.items():
        for card in v:
            if card.value not in values:
                values.append(card.value)
    for card in hand:
        if card.value in values:
            valid_cards += card.card_name() + " "
            cards.append(card)
    if len(valid_cards) > 0:
        response = input("THROW IN DOUBLES? (y/n)")
        if response == "y":
            # TODO implement the throw-in process
            return cards


def print_all(player_count, hands, trump, talon, battlefield):
    print_seats(player_count, hands, trump, talon)
    print_battlefield(battlefield)


def print_seats(players, hands, trump, talon):
    """Generates a simple display to keep the player updated. Varies based on number of players.
        Shows total card count for each player, and whose turn it is."""
    if players == 2:
        print("\n     Player 2 ({} cards)    ".format(len(hands[2])))
        print("         |        ")
        print("         |        ")
        print("         |        ")
        print("         |        ")
        print("     Player 1 ({} cards)    \n".format(len(hands[1])))
    elif players == 3:
        print("\n     Player 3 ({} cards)    ".format(len(hands[3])))
        print("      /             |   ")
        print("     /              |   ")
        print("Player 2 ({} cards)  |".format(len(hands[2])))
        print("     \              |   ")
        print("      \             |   ")
        print("     Player 1 ({} cards)    \n".format(len(hands[1])))
    elif players == 4:
        print("\n      Player 3 ({} cards)    ".format(len(hands[3])))
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
    print(battlefield)
    print_string = 'Attacks: '
    for card in battlefield['attack']:
        print_string += card.card_name() + " | "
    print(print_string)
    print_string = 'Defense: '
    for card in battlefield['defense']:
        print_string += card.card_name() + " | "
    print(print_string + "\n")
