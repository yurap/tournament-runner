from .models import TournamentData, Match
from dataclasses import dataclass
from typing import List


class PairingSystemInterface:
    def generate_pairings(self) -> List[Match]:
        pass


class TournamentInputInterface:
    def load(self) -> TournamentData:
        pass


class TournamentOutputInterface:
    def standings(self, t: TournamentData):
        pass

    def pairings(self, t: TournamentData, pairings: List[Match]):
        pass


@dataclass
class Tournament:
    t: TournamentData

    """main api that marries used algorithms via dependency injection"""
    def __init__(self, pairing: PairingSystemInterface,
                 input_io: TournamentInputInterface,
                 output_io: TournamentOutputInterface):
        self.pairing_system = pairing
        self.input_io = input_io
        self.output_io = output_io
        self.t = self.input_io.load()

    def output_pairings(self):
        self.output_io.pairings(self.t, self.pairing_system.generate_pairings(self.t))

    def output_standings(self):
        self.output_io.standings(self.t)
