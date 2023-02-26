from dataclasses import dataclass, field
from typing import List, Set, Dict


@dataclass
class Player:
    """must be unique per player"""
    name: str

    """may be used for pairing, e.g. swiss system likes to pair weaker with stronger"""
    rating: int

    """sometimes a player leaves the tournament, we still need to keep them for point calc"""
    active: bool

    """intermediate data"""
    opponents: Set[int] = field(default_factory=set)
    points_per_round: List[str] = field(default_factory=list)
    score: int = 0


@dataclass
class Match:
    """index of first player"""
    player_one: int
    """points for first player"""
    points_one: float
    """index of second player"""
    player_two: int
    "points of second player"
    points_two: float


class PlayerNotRegisteredException(Exception):
    pass


class PlayerAlreadyRegisteredException(Exception):
    pass


@dataclass
class TournamentData:
    name_to_index: Dict[str, int] = field(default_factory=dict)
    players: List[Player] = field(default_factory=list)
    rounds: List[List[Match]] = field(default_factory=list)

    def register(self, p: Player):
        """register a player and assign them an id"""
        if p.name in self.name_to_index:
            raise PlayerAlreadyRegisteredException()
        self.name_to_index[p.name] = len(self.players)
        self.players.append(p)

    def get_player_id(self, player_name):
        if player_name not in self.name_to_index:
            raise PlayerNotRegisteredException(player_name)
        return self.name_to_index[player_name]

    def eval(self):
        """eval intermediate data"""
        for p in self.players:
            p.points_per_round = []
            p.score = 0
            p.opponents = set()

        for round_matches in self.rounds:
            for m in round_matches:
                p1 = self.players[m.player_one]
                p2 = self.players[m.player_two]
                p1.score += m.points_one
                p2.score += m.points_two
                p1.opponents.add(m.player_two)
                p2.opponents.add(m.player_one)
            for p in self.players:
                p.points_per_round.append(f'{p.score}')


class TournamentCreator:
    def __init__(self):
        self.t = TournamentData()

    def next_round(self):
        """declares a new round, all matches will be created there"""
        self.t.rounds.append([])

    def register(self, name, rating=1600, is_active=True):
        self.t.register(Player(name, rating, is_active))

    def add_match(self, p1: str, score: str, p2: str):
        """
        register a match in the current round
        :param p1: name of player one
        :param score: score in format <points player one>:<points player two>, e.g. 0.5:1.5
        :param p2: name of player two
        :return: none
        """
        id_one, id_two = self.t.get_player_id(p1), self.t.get_player_id(p2)
        points_one, points_two = map(float, score.split(':'))
        self.t.rounds[-1].append(Match(id_one, points_one, id_two, points_two))

    def build(self):
        """calc intermediate data and return the tournament object"""
        self.t.eval()
        return self.t
