#!/usr/bin/env python3
from src.io import TournamentTextFileInput, TournamentTextFileOutput, TournamentTextStdOutput
from src.swiss import TournamentSwiss
from src.tournament import Tournament
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Read the state of the tournament and generate standings and pairings for the next round')
    parser.add_argument('--players-file', '-p', type=str, required=True, help='list of players')
    parser.add_argument('--round-file', '-r', default=[], action='append', help='round results, specify for each round')
    parser.add_argument('--output-standings', '-s', type=str, help='output current standings')
    parser.add_argument('--output-pairings', '-o', type=str, help='output pairings for the next round')
    parser.add_argument('--verbose', '-v', action='store_true', help='be verbose about decisions')
    args = parser.parse_args()

    out = TournamentTextStdOutput() \
        if args.output_standings is None or args.output_pairings is None \
        else TournamentTextFileOutput(args.output_standings, pairings_file=args.output_pairings)

    t = Tournament(
        pairing=TournamentSwiss(verbose=args.verbose),
        input_io=TournamentTextFileInput(
            players_file=args.players_file,
            rounds_files=args.round_file,
        ),
        output_io=out,
    )
    t.output_standings()
    t.output_pairings()
