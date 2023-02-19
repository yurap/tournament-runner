from src.models import TournamentData, Match
from src.tournament import PairingSystemInterface
from random import choice


class PairingException(Exception):
    pass


def _pick_top_score_players(t, indexes):
    max_score = max(t.players[i].score for i in indexes)
    return [i for i in indexes if t.players[i].score == max_score]


def _desc(t, player_index):
    return f'{t.players[player_index].name} ({t.players[player_index].score})'


class TournamentSwiss(PairingSystemInterface):
    def __init__(self, verbose=True):
        self.verbose = verbose

    def generate_pairings(self, t: TournamentData):
        # TODO: support ratings and if players are still active
        pairings = []
        remaining = set(i for i in range(len(t.players)))
        if not self._find(t, pairings, remaining):
            raise PairingException("Cannot build pairings!")

        if len(pairings) != len(t.players)//2 + len(t.players)%2:
            raise PairingException(
                f"We created incorrect number of matches! Players: {len(t.players)}, Matches: {len(pairings)}")

        if self.verbose:
            print('== PAIRINGS ==')
        for (one, two) in pairings:
            if self.verbose:
                print(f"{_desc(t, one)} - {_desc(t, two)}")
        return [Match(one, 0, two, 0) for (one, two) in pairings]

    def _find(self, t, pairings, remaining):
        if len(remaining) == 0:
            return True

        p = choice(_pick_top_score_players(t, remaining))
        if self.verbose:
            indent = '  ' * (len(t.players) - len(remaining))
            print(f"{indent}Seeking opponent for {_desc(t, p)} ...")

        remaining.remove(p)
        candidates = set(i for i in remaining if i not in t.players[p].opponents)
        # print(f"All possible opponents are: {', '.join([_desc(t, c) for c in candidates])}")

        while len(candidates) > 0:
            top_score_candidates = _pick_top_score_players(t, candidates)
            c = choice(top_score_candidates)

            if self.verbose:
                print(f"{indent}| Top score candidates are: {', '.join([_desc(t, c) for c in top_score_candidates])}")
                print(f"{indent}| Past opponents are: {', '.join([_desc(t, c) for c in t.players[p].opponents])}")
                print(f"{indent}> Selected: {_desc(t, p)} - {_desc(t, c)}")

            remaining.remove(c)
            pairings.append((p, c))

            if self._find(t, pairings, remaining):
                return True

            if self.verbose:
                print(f"{_desc(t, p)} - {_desc(t, c)} failed!")
            remaining.add(c)
            candidates.remove(c)
            pairings.pop()

        remaining.add(p)
        return False
