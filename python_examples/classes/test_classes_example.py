"""Testing unit for classes_example."""
import unittest
from classes_example import Clan, Race, Player

clan1 = Clan(name="Warriors")
clan2 = Clan(name="Shields", motto="We defend the people")
clan3 = Clan("The Wild Bunch", "No idea")
clanempty1 = Clan("Empty1", "----")
clanempty2 = Clan("Empty2", "----")
race1 = Race(name="Humans")
race2 = Race(name="Orcs", power=600)
race3 = Race("White Walkers", 1000)
player1 = Player(name="Mad King", motto="Burn them all")
player2 = Player(name="Cormoran Strike", race=race1)
player3 = Player("Pennywise", clan=clan3, motto="You'll die if you try!")
player2update = Player("Pennywise II", clan=clanempty1,
                       motto="You'll die if you try!")
player2update.clan = clanempty2
player2update.race = race1
player2update.motto = "you'll float too!"


class ClanTest(unittest.TestCase):
    """Testing Clan."""

    def test_00_clanname(self):
        """Basic test for clan name."""
        self.assertEqual(clan1.name, "Warriors")
        self.assertEqual(clan2.name, "Shields")
        self.assertEqual(clan3.name, "The Wild Bunch")

    def test_01_clanmotto(self):
        """Basic test for clan motto."""
        self.assertEqual(clan1.motto, "Disbanded")
        self.assertEqual(clan2.motto, "We defend the people")
        self.assertEqual(clan3.motto, "No idea")


class RaceTest(unittest.TestCase):
    """Testing Race."""

    def test_02_racename(self):
        """Basic test for race name."""
        self.assertEqual(race1.name, "Humans")
        self.assertEqual(race2.name, "Orcs")
        self.assertEqual(race3.name, "White Walkers")

    def test_03_racepower(self):
        """Basic test for race power."""
        self.assertEqual(race1.power, 500)
        self.assertEqual(race2.power, 600)
        self.assertEqual(race3.power, 1000)


class PlayerTest(unittest.TestCase):
    """Testing Player."""

    def test_04_playername(self):
        """Basic test for player name."""
        self.assertEqual(player1.name, "Mad King")
        self.assertEqual(player2.name, "Cormoran Strike")
        self.assertEqual(player3.name, "Pennywise")

    def test_05_playerpower(self):
        """Basic test for player individual power."""
        self.assertEqual(player1.power, 100)

    def test_06_playermotto(self):
        """Basic test for player personal motto."""
        self.assertEqual(player1.motto, "Burn them all")
        self.assertEqual(player2.motto, None)
        self.assertEqual(player3.motto, "You'll die if you try!")

    def test_07_layerfullpower(self):
        """Basic test for plater full power."""
        self.assertEqual(player1.fullpower(), 100)
        self.assertEqual(player2.fullpower(), 600)
        self.assertEqual(player3.fullpower(), 160)

    def test_08_playerrace(self):
        """Basic test for player race."""
        self.assertEqual(player1.race, "unknown info")
        self.assertEqual(player2.race, "Humans")
        self.assertEqual(player3.race, "unknown info")

    def test_09_playerclan(self):
        """Basic test for player clan."""
        self.assertEqual(player1.clan, "Not Assigned")
        self.assertEqual(player2.clan, "Not Assigned")
        self.assertEqual(player3.clan, "The Wild Bunch")

    def test_10_playerownmotto(self):
        """Basic test for player own motto."""
        self.assertEqual(player1.ownmotto(), "Burn them all")
        self.assertEqual(player2.ownmotto(), None)
        self.assertEqual(player3.ownmotto(), "No idea. You'll die if you try!")


class PlayerTestAdvanced(unittest.TestCase):
    """
    Test for player with updated info.

    This will change clan info (members) as well.
    """

    def test_11_updatedplayerclan(self):
        """Test clan for updated player."""
        self.assertEqual(player2update.clan, "Empty2")

    def test_12_updatedplayerrace(self):
        """Test race for updated player."""
        self.assertEqual(player2update.race, "Humans")

    def test_13_updatedplayerfullpower(self):
        """Test full power for updated player."""
        self.assertEqual(player2update.fullpower(), 670)

    def test_14_updatedclanmenbers(self):
        """Test clan members after a player clan update."""
        self.assertEqual(clanempty1.members, [])
        self.assertEqual(clanempty2.members, ['Pennywise II'])


if __name__ == "__main__":
    unittest.main()
