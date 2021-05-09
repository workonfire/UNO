import unittest
from uno.game import *
from uno.exceptions import *


class UNOTest(unittest.TestCase):
    def test_card(self):
        """
        Checks, if we can stack a card on top of another card
        """
        card: Card = Card(CardType.CARD_PLUS_2, CardColor.YELLOW)
        second_card: Card = Card(CardType.CARD_5, CardColor.RED)
        self.assertEqual(card.playable(second_card), False)
        print(f"You cannot stack {second_card} on top of {card}")

        card = Card(CardType.CARD_PLUS_4, None)
        second_card = Card(CardType.CARD_PLUS_4, None)
        self.assertEqual(card.playable(second_card), True)

        card = Card(CardType.CARD_PLUS_4, None)
        second_card = Card(CardType.CARD_4, CardColor.BLUE)
        self.assertEqual(card.playable(second_card), True)

    def test_wildcard(self):
        for _ in range(50):
            self.assertEqual(Card(CardType.CARD_WILDCARD, CardColor.GREEN).color, None)
            self.assertEqual(Card(CardType.CARD_WILDCARD, CardColor.BLUE).card_type, CardType.CARD_WILDCARD)

        wildcard: Card = Card(CardType.CARD_WILDCARD, None)
        self.assertEqual(wildcard.is_wild, True)
        second_wildcard: Card = Card(CardType.CARD_PLUS_4, None)
        self.assertEqual(second_wildcard.is_wild, True)
        not_wildcard: Card = Card(CardType.CARD_4, CardColor.RED)
        self.assertEqual(not_wildcard.is_wild, False)

    def test_drawing(self):  # TODO
        with self.assertRaises(NotImplementedError):
            raise NotImplementedError

    def test_deck(self):
        """
        Tries to draw some cards from a deck
        """
        deck: Deck = Deck(50)
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
        player: Player = Player()
        self.assertEqual(player.name, None)
        self.assertEqual(player.hand, [], "The player's hand is empty.")

    def test_player_deal(self):
        player: Player = Player("Test")
        player.hand = [Card(CardType.CARD_5, CardColor.GREEN), Card(CardType.CARD_6, CardColor.YELLOW)]
        print(player.hand)
        new_cards: List[Card] = Deck(50).draw(5)
        for card in new_cards:
            player.hand.append(card)
        self.assertEqual(len(player.hand), 7)
        print(player.hand)

    def test_table(self):
        """
        Actual game mechanics tests
        """

        # Creating a table
        players: List[Player] = [Player("Human"), Player("Computer")]
        rules: Dict[str, Any] = {'card_stacking': False,
                                 'deck_size': 50,
                                 'initial_cards': 10}
        table: Table = Table(players, rules)
        print(f"Current players: {table.players}")
        print(f"Deck contents: {table.deck.stack}")
        print(f"Table stack: {table.stack}")
        print(f"First turn: {table.turn}")

        # Giving all players an initial set of cards
        try:
            # Trying to play a random card and checking the deck size
            card: Card = random.choice(table.turn.hand)
            print(f"Trying to play with {card} on {table.last_played_card}...")
            table.play(card, table.turn)
            print(table.stack)
            self.assertEqual(len(table.stack), 2)  # FIXME: This test fails. I don't yet know why.
            print("The attempt was successful, and the deck size is now 2.")
        except CardNotPlayableError:
            print("The attempt was unsuccessful, and the deck size is still 1.")
            self.assertEqual(len(table.stack), 1)

        self.assertEqual(type(table.turn), Player)

    def test_queue_order_starting_with_human(self):
        """
        Checks if the queue order is correct
        """
        table: Table = Table(
            [Player("Human"), Player("Computer")],
            {'card_stacking': False,
             'deck_size': 50,
             'initial_cards': 10}
        )
        human_turn_stack: List[str] = [table.turn.name]
        for i in range(10):
            # print(f"Current turn: {table.turn.name}. Next turn...")
            table.next_turn()
            human_turn_stack.append(table.turn.name)

        self.assertEqual(human_turn_stack, [
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human"
        ])

    def test_queue_order_starting_with_computer(self):
        table: Table = Table(
            [Player("Computer"), Player("Human")],
            {'card_stacking': False,
             'deck_size': 50,
             'initial_cards': 10}
        )
        computer_turn_stack: List[str] = [table.turn.name]
        for i in range(10):
            # print(f"Current turn: {table.turn.name}. Next turn...")
            table.next_turn()
            computer_turn_stack.append(table.turn.name)

        self.assertEqual(computer_turn_stack, [
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer",
            "Human",
            "Computer"
        ])

    def test_queue_order_with_many_players(self):
        table: Table = Table(
            [
                Player("Wzium1"),
                Player("Human"),
                Player("Computer"),
                Player("Wzium69")
            ],
            {'card_stacking': False,
             'deck_size': 50,
             'initial_cards': 10}
        )
        turn_stack: List[str] = [table.turn.name]
        for i in range(10):
            # print(f"Current turn: {table.turn.name}. Next turn...")
            if i == 5:
                self.assertEqual(table.reverse_queue(), NotImplemented)
            table.next_turn()
            turn_stack.append(table.turn.name)
        # TODO: Test the queue system
        """
        self.assertEqual(turn_stack, [
            "Wzium1",
            "Human",
            "Computer",
            "Wzium69",
            "Wzium1",
            "Wzium69",
            "Computer",
            "Human",
            "Wzium1",
            "Wzium69",
            "Computer"
        ])
        """


if __name__ == '__main__':
    unittest.main()
