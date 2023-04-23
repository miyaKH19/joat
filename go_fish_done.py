from enum import Enum
import os
import sys
import random

##############################################################################
# "Go Fish" Game Logic
#
# 
#
#
##############################################################################

########################## Classes START ##############################

# A card is a tuple of (Suit,Value)
class Suit(Enum):
    HEARTS = 14
    SPADES = 15
    CLUBS = 16
    DIAMONDS = 17
class Value(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

####################
### Game Class ##
# (array of Players, ordered by turn) playerlist
class Game:
    def __init__(self):
        self.playerlist = []

    def add_player(self, player):
        #index into the player list
        self.playerlist.append(player)
        print(f'Player {len(self.playerlist)} has been added')

####################
### Player Class ###
# (str) name
# (int) id
# (dictionary) hand =  {(int) value : (str) suit}
# (int) points
class Player:
    def __init__(self, name):
        self.name = name
        self.id = 0
        self.hand = {}
        self.points = 0

    def receive_card(self,card):
        suit = card[0]
        rank = card[1]
        print(f">> {self.name} received {rank} of {suit}!\n")
        if rank in self.hand:
            self.hand[rank].append(suit)
        else:
            self.hand[rank] = [suit]

########################## Classes END ##############################

########################## Card Functions START ##############################

# deals (int)n cards from the (card array)deck to add to the (dict)player's hand
def deal_cards(deck, player, n):
    if n <= len(deck):
        #make sure that there are no sizing conflicts
        for i in range(n):
            card = deck.pop()
            player.receive_card(card)
    elif len(deck) == 0:
        print("Deck is empty!")

# prints all the cards in the deck ex. "2 of SPADES"
def print_deck(deck):
    print("Current deck: ")
    for i in range(len(deck)):
        card = deck[i]
        print(f'{Value(card[1]).name} of {card[0]}')
    print('\n')

# prints all the cards in the player's hand
def print_hand(player):
    print(f"{player.name}'s hand: ")
    
    hand = player.hand
    for rank in hand:
        for suit in hand[rank]:
            print(f'{Value(rank).name} of {suit}')
    print('\n')

# creates a shuffled deck of cards
# a card is a tuple of (Suit,Value)
# a deck is an array of tuples
def make_shuffled_deck():
    deck = []
    for s in Suit:
        for v in Value:
            card = (s.name, v.value)
            deck.append(card)
    random.shuffle(deck)
    return deck

########################## Card Functions END ##############################

########################## Game Functions START ##############################
# checks if the player has all suits of the specified value
def check_match(player, match_value):
    value = int(match_value)
    if value in player.hand:
        if len(player.hand[value]) == 4:
            return True
    return False

# removes cards of match_value from hand and increases player's points
def make_match(player, match_value):
    value = int(match_value)    
    player.hand.pop(value)
    player.points += 1

# checks if opponent has the requested value
def check_request(opponent, request_value):
    value = int(request_value)
    if(value in opponent.hand) and len(opponent.hand[value]) > 0:
        print(f">> {opponent.name} has {len(opponent.hand[value])} x {Value(value).name}'s \n")
        return True
    else:
        return False
# adds the requested cards to player's hands, and removes from opponent's hand
def make_request(player, opponent, request_value):
    value = int(request_value)
    if(value not in player.hand):
        player.hand[value] = []
    # add the card(s) to the player's hand
    for suit in opponent.hand[value]:
        player.hand[value].append(suit)
    # remove the card(s) from opponent's hand
    opponent.hand.pop(value)

# checks if there are no cards left to play
def check_game_over(deck, curr_player, opp_player):
    if(len(deck) == 0) and len(curr_player.hand) == 0 and len(opp_player.hand) == 0:
        return True
    else:
        return False

########################## Game Functions END ##############################

def main():
    # ################# Initialize Game #################################
    # Add options to specify how many players per lobby
    # For now, assume this is a game of 2
    print("You can decide who goes first by who is Player 1 and who is Player 2.")
    p1_name = input("Player 1 name: ")
    p2_name = input("Player 2 name: ")

    p1 = Player(p1_name)
    p2 = Player(p2_name)

    game = Game()
    game.add_player(p1)
    game.add_player(p2)

    start_game = False
    while(not start_game):
        game_ready = input("\n>> Ready to start the game? Enter 'y' to begin: ")
        if (game_ready == 'y'):
            start_game = True
            break
        else:
            continue

    # MAKE the deck 
    deck = make_shuffled_deck()
    print(f'Deck size: {len(deck)} \n')

    # DEAL starting hand (print for testing purposes)
    deal_cards(deck, p1, 4)
    deal_cards(deck, p2, 4)
    
    game_over = False
    player_turn = 0

    # ################## GAME PLAY ################################
    print("Game Start ##############################################\n")
    print(f">> It's {game.playerlist[player_turn].name}'s turn! \n")

    while(not game_over):
        turn_over = False

        while(not turn_over):
            
            # set who is the current player and who is the opponent
            curr_player = game.playerlist[player_turn]
            if player_turn == len(game.playerlist) - 1:
                opp_player =  game.playerlist[0]
            else:
                opp_player = game.playerlist[player_turn+1]

            # print all the cards in player's hand
            print_hand(curr_player)

            # continuous video streaming from camera 
            # if four cards of same rank detected --> match
            # if keyboard input to request card --> display to opponent

            # Ask for a card,  (Assume only 2 players here)
            requested_value = input(f">> It's {curr_player.name}'s move! \n What value are you asking for? (1-13): ")
            print("\n")
            # Opponent has that value
            if check_request(opp_player, requested_value):
                make_request(curr_player, opp_player, requested_value)

                # ask player to make matches
                ask_match = input(">> Any value matches? 'y' for yes: ")
                print("\n")
                if ask_match == 'y':
                    value_match = input(">> Type value to make a set: ")
                    print("\n")
                    if check_match(curr_player, value_match):
                        make_match(curr_player,value_match)
                        print(f">> You made a set of {value_match}. Your points: {curr_player.points}")
                        # check if game over
                        if(check_game_over(deck, curr_player, opp_player)):
                            game_over = True
                            break
                    else:
                        print(f">> You do not have all suits of {value_match}")
            # Go Fish!, draw a card from the deck
            else:
                print("\n >> Go Fish!\n")
                deal_cards(deck, curr_player, 1)
                print_hand(curr_player)
                print_deck(deck)
                # check for more matches?
                # 
                # ask player to make matches
                ask_match = input(">> Any value matches? 'y' for yes: ")
                print("\n")
                if ask_match == 'y':
                    value_match = input(">> Type value to make a set: ")
                    print("\n")
                    if check_match(curr_player, value_match):
                        make_match(curr_player,value_match)
                        print(f">> You made a set of {value_match}. Your points: {curr_player.points}")
                        # check if game over
                        if(check_game_over(deck, curr_player, opp_player)):
                            game_over = True
                            break
                    else:
                        print(f">> You do not have all suits of {value_match}")
                # 
                turn_over =  True

        # CHECK if game over
        if(check_game_over(deck, curr_player, opp_player)):
            game_over = True
        else:
            # end of turn go back to player 1
            player_turn += 1
            if player_turn == len(game.playerlist):
                player_turn = 0
            print("New turn! ##############################################\n")
            print(f"It's {game.playerlist[player_turn].name}'s turn! \n") 
    
    # ##################################################
    # print the results
    print("Game over!! \n")
    for player in game.playerlist:
        print(f"{player.name} has {player.points} points!\n")
    


if __name__ == '__main__':
    main()
