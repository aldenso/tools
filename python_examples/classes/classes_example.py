"""My notes to remember classes."""

NOTASSIGNED = "Not Assigned"
UNKNOWN = "unknown info"


class Clan:
    """Base class for Clan and player."""

    # value will be added to the players power.
    Bonus = 10

    def __init__(self, name, motto="Disbanded"):
        """Create clan."""
        self.name = name
        self.motto = motto
        self._influence = 50
        self.members = []

    @property
    def influence(self):
        """Influence property for the clan.

        Sums the default influence with 10 points per member.
        """
        return self._influence + (len(self.members) * 10)


class Race:
    """Base class for Race and player."""

    def __init__(self, name, power=500):
        """Create a Race."""
        self.name = name
        self.power = power


class Player(Clan, Race):
    """docstring for ClassName."""

    def __init__(self, name, clan=None, race=None, motto=None):
        """Create player."""
        self.name = name
        self._power = 100
        self._clan = clan
        self._race = race
        self.motto = motto
        self.__updateinitclan()

    def fullpower(self):
        """Full power for player."""
        if self._clan is None and self._race is None:
            return self.power
        elif self._clan is None and self._race is not None:
            return self.power + self._race.power
        elif self._clan is not None and self._race is None:
            return self.power + self._clan.influence
        else:
            return self.power + self._clan.influence + self._clan.Bonus +\
                self._race.power

    def ownmotto(self):
        """Create clan motto plus personal motto."""
        if self._clan is not None:
            return "{}. {}".format(self._clan.motto, self.motto)
        return self.motto

    def __updateinitclan(self):
        if self._clan is None:
            return
        self._clan.members.append(self.name)

    @property
    def power(self):
        """Power property, we don't want people changing this."""
        return self._power

    @property
    def clan(self):
        """Clan property."""
        if self._clan is not None:
            return self._clan.name
        return NOTASSIGNED

    @clan.setter
    def clan(self, clan):
        if self._clan is not None and clan is None:
            self._clan.members.remove(self.name)
            self._clan = None
        elif self._clan is not None and clan is not None:
            self._clan.members.remove(self.name)
            self._clan = clan
            self._clan.members.append(self.name)
        elif self._clan is None and clan is not None:
            self._clan = clan
            self._clan.members.append(self.name)
        else:
            pass

    @property
    def race(self):
        """Clan property."""
        if self._race is not None:
            return self._race.name
        return UNKNOWN

    @race.setter
    def race(self, race):
        self._race = race


if __name__ == "__main__":
    warrios = Clan("The conquerors", "We come to conquer")
    wizards = Clan("The fearless", "You shall not pass")
    print("=" * 79)
    print("Clan Name: {:20}Motto: {:40}\nBonus: {:^5}Influence: {:^5}\
          Members: {}"
          .format(warrios.name, warrios.motto,
                  warrios.Bonus, warrios.influence,
                  warrios.members))
    print("=" * 79)
    print("Clan Name: {:20}Motto: {:40}\nBonus: {:^5}Influence: {:^5}\
          Members: {}"
          .format(wizards.name, wizards.motto,
                  wizards.Bonus, wizards.influence,
                  wizards.members))
    print("=" * 79)

    orcs = Race("orcs", power=600)
    humans = Race("humans")
    print("Race Name: {:10}Power: {:^5}"
          .format(humans.name, humans.power))
    print("=" * 79)
    player1 = Player("aldenso", warrios, humans, "veni, vidi, vici")
    print("Name: {:10}Race: {:10}Power: {:^5}FullPower: {:^5}\nMotto: {:50}"
          .format(player1.name, player1.race,
                  player1.power, player1.fullpower(),
                  player1.ownmotto()))
    print("=" * 79)
    print("Warrios members: {}\nwizards members: {}"
          .format(warrios.members, wizards.members))

# output:
# ===============================================================================
# Clan Name: The conquerors      Motto: We come to conquer
# Bonus:  10  Influence:  50            Members: []
# ===============================================================================
# Clan Name: The fearless        Motto: You shall not pass
# Bonus:  10  Influence:  50            Members: []
# ===============================================================================
# Race Name: humans    Power:  500
# ===============================================================================
# Name: aldenso   Race: humans    Power:  100 FullPower:  670
# Motto: We come to conquer. veni, vidi, vici
# ===============================================================================
# Warrios members: ['aldenso']
# wizards members: []
