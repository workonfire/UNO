import unittest
from uno.game import *
from uno.exceptions import *


class UNOTest(unittest.TestCase):
    def test_card(self):
        """
        Checks, if we can stack a card on top of another card
        """
        card = Card(CardType.CARD_PLUS_2, CardColor.YELLOW)
        second_card = Card(CardType.CARD_5, CardColor.RED)
        self.assertEqual(card.playable(second_card), False)
        print(f"You cannot stack {second_card} on top of {card}")

        card = Card(CardType.CARD_PLUS_4, CardColor.BLUE)
        second_card = Card(CardType.CARD_PLUS_4, CardColor.GREEN)
        self.assertEqual(card.playable(second_card), True)

        card = Card(CardType.CARD_PLUS_4, CardColor.BLUE)
        second_card = Card(CardType.CARD_4, CardColor.BLUE)
        self.assertEqual(card.playable(second_card), True)

    def test_wildcard(self):
        wildcard = Card(CardType.CARD_WILDCARD, CardColor.GREEN)
        self.assertEqual(wildcard.is_wild, True)
        second_wildcard = Card(CardType.CARD_PLUS_4, CardColor.BLUE)
        self.assertEqual(second_wildcard.is_wild, True)
        not_wildcard = Card(CardType.CARD_4, CardColor.RED)
        self.assertEqual(not_wildcard.is_wild, False)

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
        player.hand = [Card(CardType.CARD_5, CardColor.GREEN), Card(CardType.CARD_6, CardColor.YELLOW)]
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
        players = [Player("Human"), Player("Computer")]
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
            print(table.stack)
            self.assertEqual(len(table.stack), 2)  # FIXME: This test fails. I don't yet know why.
            print("The attempt was successful, and the deck size is now 2.")
        except CardNotPlayableError:
            print("The attempt was unsuccessful, and the deck size is still 1.")
            self.assertEqual(len(table.stack), 1)

        self.assertEqual(type(table.turn), Player)

        # Checks if the queue order is correct
        for i in range(10):
            print(f"Current turn: {table.turn.name}. Next turn...")
            table.next_turn()


if __name__ == '__main__':
    unittest.main()
