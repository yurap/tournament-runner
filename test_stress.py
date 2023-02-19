#!/usr/bin/env python3
from src.models import TournamentData, Player, Match
from src.swiss import TournamentSwiss
from src.io import TournamentTextStdOutput
import random


def generate_tournament(total_players: int) -> TournamentData:
    t = TournamentData()
    for player_index in range(total_players):
        t.register(Player(
            name=f"Player {chr(ord('A') + player_index)}",
            rating=1800 + random.randrange(400),
            active=True,
        ))
    return t


def _outcome(p1: Player, p2: Player):
    if p1.rating > p2.rating:
        return 1, 0
    elif p1.rating < p2.rating:
        return 0, 1
    return 0.5, 0.5


def _resolve_match(t: TournamentData, m: Match):
    p1 = t.players[m.player_one]
    p2 = t.players[m.player_two]
    m.points_one, m.points_two = _outcome(p1, p2)


def run(system, total_players, total_rounds, attempt, verbose=False):
    t = generate_tournament(total_players)
    if verbose:
        out = TournamentTextStdOutput(separator=' ')

    for round_index in range(total_rounds):
        if verbose:
            print(f"[=======] ROUND {round_index} [=======]")
        matches = system.generate_pairings(t)
        for m in matches:
            _resolve_match(t, m)

        if verbose:
            out.pairings(t, matches)
        t.rounds.append(matches)
        t.eval()

    # the winner of the tournament must have max rating
    vals = sorted([(p.score, p.rating) for p in t.players], key=lambda v: -v[1])
    if max(vals, key=lambda v: v[1]) == max(vals, key=lambda v: v[0]):
        print(f'OK {attempt}')
    else:
        print(vals)
        print(t)
        raise Exception('Oops!')


if __name__ == '__main__':
    for i in range(1000):
        run(system=TournamentSwiss(verbose=False), total_players=20, total_rounds=17, attempt=i)
