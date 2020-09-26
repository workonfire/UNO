import unittest
from game import *
from exceptions import *


class UNOTest(unittest.TestCase):
    def test_card(self):
        """
        Checks, if we can stack a card on top of another card
        """
        with self.assertRaises(InvalidCardException):
            Card('69', 'GREEN')
        card = Card('+2', 'YELLOW')
        second_card = Card('5', 'RED')
        self.assertEqual(card.playable(second_card), False)
        print(f"You cannot stack {second_card} on top of {card}")

        card = Card('+4', 'BLUE')
        second_card = ('4', 'GREEN')
        self.assertEqual(card.playable(second_card), True)

        card = Card('+4', 'BLUE')
        second_card = ('4', 'BLUE')
        self.assertEqual(card.playable(second_card), True)

    def test_drawing(self):  # TODO
        with self.assertRaises(NotImplementedError):
            raise NotImplementedError

    def test_deck(self):
        """
        Tries to draw some cards from a deck
        """
        deck = Deck(50)
        print(f"Current deck contents: {deck.stack}")
        print("Trying to draw 10 cards...")
        deck.draw(10)
        print(f"Current deck contents: {deck.stack}")
        print("Trying to draw 100 cards...")
        with self.assertRaises(IndexError):
            print("Drawing failed successfully.")
            deck.draw(100)

    def test_player(self):
        """
        Tries to create a player etc.
        """
        player = Player()
        print(f"Player name: {player.name}")
        self.assertEqual(player.hand, [], "The player's hand is empty.")

    def test_player_deal(self):
        player = Player("Test")
        player.hand = [Card('5', 'GREEN'), Card('6', 'YELLOW')]
        print(player.hand)
        new_cards = Deck(50).draw(5)
        for card in new_cards:
            player.hand.append(card)
        self.assertEqual(len(player.hand), 7)
        print(player.hand)

    def test_table(self):
        """
        Actual game mechanics tests
        """

        # Creating a table
        players = [Player("Human"),
                   Player("Computer1"),
                   Player("Computer2"),
                   Player("Computer3")]
        rules = {'card_stacking': False,
                 'deck_size': 50,
                 'initial_cards': 10}
        table = Table(players, rules)
        print(f"Current players: {table.players}")
        print(f"Deck contents: {table.deck.stack}")
        print(f"Table stack: {table.stack}")
        print(f"First turn: {table.turn}")

        # Giving all players an initial set of cards
        try:
            # Trying to play a random card and checking the deck size
            card = random.choice(table.turn.hand)
            print(f"Trying to play with {card} on {table.last_played_card}...")
            table.play(card, table.turn)
            self.assertEqual(len(table.stack), 2)
            print("The attempt was successful, and the deck size is now 2.")
        except CardNotPlayableError:
            print("The attempt was unsuccessful, and the deck size is still 1.")
            self.assertEqual(len(table.stack), 1)

        self.assertEqual(type(table.turn), Player)

        # Checks if the queue order is correct
        for i in range(10):
            table.next_turn()
            print(f"Current turn: {table.turn.name}. Next turn...")

        table.reverse()
        print("The turn got reversed.")

        for i in range(10):
            table.next_turn()
            print(f"Current turn: {table.turn.name}. Next turn...")


if __name__ == '__main__':
    unittest.main()
