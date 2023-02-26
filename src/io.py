from src.models import TournamentCreator, TournamentData, Match
from src.tournament import TournamentInputInterface, TournamentOutputInterface


class TournamentTextFileInput(TournamentInputInterface):
    """load tournament data from text file"""
    def __init__(self, players_file, rounds_files, separator=','):
        self.separator = separator
        self.players_file = players_file
        self.rounds_files = rounds_files
        self.builder = TournamentCreator()

    def load(self):
        self._load_players()
        self._load_rounds()
        return self.builder.build()

    def _load_players(self):
        # TODO: support ratings and if players are still active
        with open(self.players_file) as f:
            players = f.readlines()
        for p in players:
            self.builder.register(p.rstrip())

    def _load_rounds(self):
        for file_name in self.rounds_files:
            with open(file_name) as f:
                lines = f.readlines()

            self.builder.next_round()
            for line in lines[1:]:
                (_, p1, score, p2) = line.rstrip().split(self.separator)
                # remove points
                p1, p2 = p1.split('(')[0].rstrip(), p2.split('(')[0].rstrip()
                self.builder.add_match(p1, score, p2)


class TournamentTextFileOutput(TournamentOutputInterface):
    """write tournament pairings and standings to text file"""
    def __init__(self, standings_file, pairings_file, verbose=True, separator=','):
        self.standings_file = standings_file
        self.pairings_file = pairings_file
        self.verbose = verbose
        self.separator = separator

    def standings(self, t: TournamentData):
        if self.verbose:
            print("== STANDINGS ==")
        with open(self.standings_file, 'w') as out:
            for p in t.players:
                s = self.separator.join([p.name] + list(map(str, p.points_per_round)))
                if self.verbose:
                    print(s)
                out.write(s + '\n')

    def pairings(self, t: TournamentData, pairings: list[Match]):
        if self.verbose:
            print("== PAIRINGS ==")
        with open(self.pairings_file, 'w') as out:
            for m in pairings:
                p1 = t.players[m.player_one]
                p2 = t.players[m.player_two]
                s = self.separator.join([f'{p1.name} ({p1.score})', f'{m.points_one}:{m.points_two}', f'{p2.name} ({p2.score})'])
                if self.verbose:
                    print(s)
                out.write(s + '\n')


class TournamentTextStdOutput(TournamentOutputInterface):
    """write tournament pairings and standings to stdout"""
    def __init__(self, separator='\t'):
        self.separator = separator

    def standings(self, t: TournamentData):
        print("== STANDINGS ==")
        for p in t.players:
            columns = [p.name, f'({p.rating})']
            columns += list(map(str, p.points_per_round))
            print(self.separator.join(columns))

    def pairings(self, t: TournamentData, pairings: list[Match]):
        print("== PAIRINGS ==")
        for m in pairings:
            p1 = t.players[m.player_one]
            p2 = t.players[m.player_two]
            print(self.separator.join([f'{p1.name} ({p1.score})', f'{m.points_one}:{m.points_two}', f'{p2.name} ({p2.score})']))
