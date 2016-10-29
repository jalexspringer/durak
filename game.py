def main_game_loop(player_count, hands, trump, talon, attacker, defender, battlefield, discard):
    # New turn print of game state
    print_seats(player_count, hands, trump, talon, discard)
    first_attack_hand_string = print_hand(hands[attacker], attacker)
    played = ''
    # First attack
    if len(hands[defender]) > 0 and len(hands[attacker]) > 0:
        played, hands[attacker] = play_card(hands[attacker], attacker, first_attack_hand_string)
        battlefield['attack'].append(played)
    elif len(hands[attacker]) == 0:
        attacker = next_player(attacker, player_count)
        defender = next_player(attacker, player_count)
        return attacker, defender
    elif len(hands[defender]) == 0:
        defender = next_player(defender, player_count)
        return attacker, defender

    # Print state after first attack
    print_all(player_count, hands, trump, talon, battlefield, discard)

    # Defense/attack loop
    return internal_game_loop(player_count, hands, trump, talon, attacker, defender, battlefield, discard, played)


def internal_game_loop(player_count, hands, trump, talon, attacker, defender, battlefield, discard, played, press=True):
    while True:
        # Show legal cards, offer a chance to defend or take all cards
        defending, valid_cards = to_defend(hands[defender], played, trump, defender)  # defend or not to defend
        if defending:
            played, hands[defender] = play_card(hands[defender], defender, valid_cards, 'defend')
            battlefield['defense'].append(played)
            print_all(player_count, hands, trump, talon, battlefield, discard)
            # Check to see if the defender has just played their last card. If yes - end of round. Move to main to check
            # if the talon is empty and defender is the winner.
            if len(hands[defender]) == 0:
                attacker = next_player(attacker, player_count)
                defender = next_player(attacker, player_count)
                return attacker, defender

            # Show legal cards, offer a chance to attack or pass and end attack
            attacking, valid_cards = to_attack(hands[attacker], battlefield, attacker)  # attack
            if attacking:
                played, hands[attacker] = play_card(hands[attacker], attacker, valid_cards)
                battlefield['attack'].append(played)
                print_all(player_count, hands, trump, talon, battlefield, discard)
            else:  # pass
                # If the game has 3 or 4 players, the attack can be continued by the player after the defender
                if player_count > 2 and press:
                    press_attack(player_count, hands, trump, talon, attacker, defender, battlefield, discard, played)
                print("PLAYER {} - DISCARDING CARDS - END OF ATTACK".format(attacker))
                for k, v in battlefield.items():
                    for card in v:
                        discard.append(card)
                attacker = next_player(attacker, player_count)
                defender = next_player(attacker, player_count)
                return attacker, defender
        else:  # take all cards
            additional_throws = throw_in(battlefield, hands, attacker)
            if additional_throws:
                for card in additional_throws:
                    battlefield['attack'].append(card)
            print("PLAYER {} - TAKING CARDS AND SKIPPING YO TURN!!".format(defender))
            for k, v in battlefield.items():
                for card in v:
                    hands[defender].append(card)
            for i in range(2):
                attacker = next_player(attacker, player_count)
                defender = next_player(attacker, player_count)
            return attacker, defender


def dealer(hands, talon, hand_size):
    """Brings each hand's card count up to the HAND_SIZE"""
    # TODO make the dealer start with the last attacker. Potentially move to the end of the game loop.
    print("Dealing...")
    print("---------------------------------\n")
    for k, v in hands.items():
        while len(v) < hand_size and len(talon) > 0:
            v.append(talon.pop())

    for k, v in players.items():
        while len(v.hand) <  hand_size


def check_win_condition(hands):
    cards_in_hand = []
    counter = 0
    for k, v in hands.items():
        cards_in_hand.append(len(v))
    cards_in_hand.sort()
    for i in cards_in_hand:
        if i == 0:
            counter += 1
    return counter


def play_card(hand, active_player, valid_cards, state='attack'):
    """Takes a list of cards and user input, returns the card, and the hand minus the card.
       Runs until a card that is in the hand is input.
       Defaults to the attacker dialogue, set 3rd param to False for defender."""
    while True:
        played = input("Player {}, what card would you like to {} with? ".format(active_player, state))
        for idx, card in enumerate(hand):
            if card.card_name() == played.upper() and played.upper() in valid_cards:
                valid_play = hand.pop(idx)
                return valid_play, hand
        print("That card is not an option. Please select a card from your hand and in the list of playable cards.")


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
        elif played.suit == trump.suit and card.suit == trump.suit and card.value > played.value:
            valid_cards += card.card_name() + " "
        elif played.suit != trump.suit and card.suit == trump.suit:
            valid_cards += card.card_name() + " "
    if len(valid_cards) > 0:
        while True:
            print_hand(hand, defender)
            print('Valid card options: {}'.format(valid_cards))
            defending = input("Type 'd' or 'take' to continue: ")
            if defending == 'd':
                return True, valid_cards
            elif defending == 'take':
                return False, valid_cards
            else:
                print('{} is not an option.'.format(defending))
    else:
        print('No valid options - taking cards.')
        return False, valid_cards


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
            print('Valid card options: {}'.format(valid_cards))
            attacking = input('Type "a" or "pass" to continue: ')
            if attacking == 'a':
                return True, valid_cards
            elif attacking == 'pass':
                return False, valid_cards
    elif len(battlefield['attack']) >= 6:
        print('Max rounds (6) completed - discarding cards and ending the turn.')
    else:
        print('No valid options - discarding cards and ending the turn.')
        return False, valid_cards


def throw_in(battlefield, hands, attacker):
    """Prompts to see if the attacker would like to add the rest of the cards with a matching value.
        returns the list of cards."""
    valid_cards = ""
    values = []
    cards = []
    for k, v in battlefield.items():
        for card in v:
            if card.value not in values:
                values.append(card.value)
    for idx, card in enumerate(hands[attacker]):
        if card.value in values:
            valid_cards += card.card_name() + " "
    while len(valid_cards) > 0:
        print('Attacking player - you may throw in the rest of the cards in your hand with matching values.')
        print('Valid cards: {}'.format(valid_cards))
        response = input("THROW IN DOUBLES? (y/n)")
        if response == "y":
            played, hands[attacker] = play_card(hands[attacker], attacker, valid_cards, 'throw in')
            cards.append(played)
            valid_cards = valid_cards.replace(played.card_name(), "").strip()
        else:
            break
    return cards


def press_attack(player_count, hands, trump, talon, attacker, defender, battlefield, discard, played):
    """After to_attack() returns False, next attacker has the option to continue the attack
        """
    thrower = next_player(defender, player_count)
    keep_attacking = input('Player {} has passed on the attack.\n'
                           ' Player {} would you like to continue? (y/n) '.format(attacker, thrower))
    if keep_attacking == 'y':
        internal_game_loop(player_count, hands, trump, talon, thrower, defender, battlefield, discard, played)
    else:
        print("PLAYER {} - DISCARDING CARDS - END OF ATTACK".format(thrower))


def print_all(player_count, hands, trump, talon, battlefield, discard):
    print_seats(player_count, hands, trump, talon, discard)
    print_battlefield(battlefield)


def print_seats(players, hands, trump, talon, discard):
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
    print_state(trump, talon, discard)


def print_state(trump, talon, discard):
    """Prints important game state information"""
    print("Remaining cards: {}".format(len(talon)))
    print("Trump card: {}".format(trump.card_name()))
    print("Total discard: {}".format(len(discard)))
    print("---------------------------------\n")


def print_hand(hand, player):
    """Takes single list of PlayingCard objects and the player number, prints hand in string format
        Also prints remaining cards in talon and trump card to remind players."""
    hand_string = "Player {} current hand: ".format(player)
    sorted_hand = sorted(hand, key=lambda x: (x.suit, x.value))
    for card in sorted_hand:
        hand_string += "{}  ".format(card.card_name())
    print(hand_string)
    return hand_string


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
