import unittest

from uno.game import *


class UNOTest(unittest.TestCase):
    def test_card(self):
        card: Card = Card(CardType.CARD_PLUS_2, CardColor.YELLOW)
        second_card: Card = Card(CardType.CARD_5, CardColor.RED)
        self.assertEqual(card.playable(second_card), False)

        card = Card(CardType.CARD_PLUS_4, None)
        second_card = Card(CardType.CARD_PLUS_4, None)
        self.assertEqual(card.playable(second_card), True)

        card = Card(CardType.CARD_PLUS_4, None)
        second_card = Card(CardType.CARD_4, CardColor.BLUE)
        self.assertEqual(card.playable(second_card), True)

        card = Card(CardType.CARD_6, CardColor.GREEN)
        second_card = Card(CardType.CARD_WILDCARD, None)
        self.assertEqual(second_card.playable(card), True)

        card = Card(None, CardColor.GREEN)
        second_card = Card(CardType.CARD_WILDCARD, None)
        self.assertEqual(second_card.playable(card), True)

        card = Card(CardType.CARD_WILDCARD, None)
        second_card = Card(CardType.CARD_7, CardColor.GREEN)
        self.assertEqual(second_card.playable(card), False)

        card = Card(None, CardColor.GREEN)
        second_card = Card(CardType.CARD_7, CardColor.YELLOW)
        self.assertEqual(second_card.playable(card), False)

    def test_card_creation(self):
        self.assertEqual(Card(CardType.CARD_6, CardColor.RED).__repr__(), "6 RED")
        self.assertEqual(Card(CardType.CARD_WILDCARD, None).__repr__(), "WILDCARD")
        self.assertEqual(Card(CardType.CARD_PLUS_4, CardColor.GREEN).__repr__(), "+4")
        self.assertEqual(Card(None, CardColor.GREEN).__repr__(), "* GREEN")
        with self.assertRaises(InvalidCardException):
            self.assertEqual(Card(None, None).__repr__(), "* GREEN")

    def test_card_from_str(self):
        self.assertEqual(Card.from_str('6 BLUE'), Card(CardType.CARD_6, CardColor.BLUE))
        self.assertEqual(Card.from_str('69 GREEN'), None)
        self.assertEqual(Card.from_str('hello'), None)
        self.assertEqual(Card.from_str('3 HELLOW'), None)
        self.assertEqual(Card.from_str('WILDCARD'), Card(CardType.CARD_WILDCARD, None))
        self.assertEqual(Card.from_str('+4'), Card(CardType.CARD_PLUS_4, None))

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

        self.assertEqual(Card(CardType.CARD_WILDCARD, None), Card(CardType.CARD_WILDCARD, None))
        self.assertEqual(
            Card(CardType.CARD_6, None).is_wild,
            Card(CardType.CARD_WILDCARD, None) in (CardType.CARD_WILDCARD, CardType.CARD_PLUS_4)
        )

    def test_drawing(self):  # TODO
        with self.assertRaises(NotImplementedError):
            raise NotImplementedError

    def test_deck(self):
        deck: Deck = Deck()
        deck.draw(10)
        self.assertEqual(len(deck.draw(100)), 100)

    def test_player(self):
        player: Player = Player("Computer")
        self.assertEqual(player.name, 'Computer')
        self.assertEqual(player.hand, [])
        self.assertEqual(player.is_computer, True)

    def test_player_deal(self):
        player: Player = Player("Test")
        player.hand = [Card(CardType.CARD_5, CardColor.GREEN), Card(CardType.CARD_6, CardColor.YELLOW)]
        print(player.hand)
        new_cards: list[Card] = Deck().draw(5)
        for card in new_cards:
            player.hand.append(card)
        self.assertEqual(len(player.hand), 7)
        print(player.hand)

    def test_table(self):
        # Creating a table
        players: list[Player] = [Player("Human"), Player("Computer")]
        rules: dict[str, Any] = {'card_stacking': False,
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
            self.assertEqual(len(table.stack), 2)
            print("The attempt was successful, and the deck size is now 2.")
        except CardNotPlayableError:
            print("The attempt was unsuccessful, and the deck size is still 1.")
            self.assertEqual(len(table.stack), 1)

        self.assertEqual(type(table.turn), Player)

    def test_queue_order_starting_with_human(self):
        table: Table = Table(
            [Player("Human1"), Player("Computer1"), Player("Human2"), Player("Human3"), Player("Computer2")],
            {'card_stacking': True,
             'initial_cards': 10}
        )
        for i in range(10):
            # print(f"Current turn: {table.turn.name}. Next turn...")
            table.set_next_turn()

        table.reverse_queue()
        table.set_next_turn()
        table.set_next_turn()

        self.assertEqual(table.turn.name, "Human3")

    def test_queue_order_starting_with_computer(self):
        table: Table = Table(
            [Player("Computer1"), Player("Computer2"), Player("Human1"), Player("Human2"), Player("Human3")],
            {'card_stacking': True,
             'initial_cards': 10}
        )
        for i in range(10):
            # print(f"Current turn: {table.turn.name}. Next turn...")
            table.set_next_turn()

        table.reverse_queue()
        table.set_next_turn()
        table.set_next_turn()

        self.assertEqual(table.turn.name, "Human2")


if __name__ == '__main__':
    unittest.main()
