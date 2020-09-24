#!/usr/bin/env python

"""replay-player.py: Replays games in a flexible way"""

__author__ = "Thomas"
__copyright__ = "Copyright 2020, itsjfx"
__repo__ = "https://github.com/itsjfx/pacman-contest-replay-player"
__contributors__ = ["Sebastan Sardina"]

import os
import sys
import argparse
import re

# Settings
REPLAYS_FOLDER = "replays"
PYTHON_BIN = "python"

# Constants
DIR_SCRIPT = sys.path[0]
REPLAYS_FOLDER = os.path.join(DIR_SCRIPT, REPLAYS_FOLDER)

# Arg parsing
parser = argparse.ArgumentParser(
    description="Replays specific games from a set of replays. \n"
                "\n"
                "Replay a specific replay file: \n"
                "\n\n"
                "\t\t python replay.py -f replays/BBC_vs_It_depends_contest18Capture.replay --delay-step 0.5"
                "\n\n"
                "List all replays available with their ids:"
                "\n\n"
                "\t\t python replay.py"
                "\n\n"
                "List all replays between two teams:"
                "\n\n"
                "\t\t python replay.py -t team1 team2"
                "\n\n"
                "Replay game 3 between team1 and team2:"
                "\n\n"
                "\t\t python replay-player.py --team TEAM1 TEAM2 -n 3 --delay-step 0.5"
                "", formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('-f', '--file', dest='file', nargs='?', help='Replay file to replay')
parser.add_argument('-t', '--teams', dest='teams', nargs='+', help='Set teams to filter by <team1> [team2]')
parser.add_argument('-n', '--number', dest='number', nargs='?', type=int,
                    help='Set replay to run. Omit to list all replays')
parser.add_argument('-s', '--delay-step', type=float, dest='delay_step', help='Delay step in a play or replay.',
                    default=0.03)
args = parser.parse_args()


def main():
    if args.file:
        cmd = f'{PYTHON_BIN} {os.path.join(DIR_SCRIPT, "capture.py")} --replay {args.file} --delay-step {args.delay_step}'
        os.system(cmd)
        exit(0)

    if not os.path.exists(REPLAYS_FOLDER):
        print('No replays folder found with path "{}". This can be edited in the script under REPLAYS_FOLDER'.format(
            REPLAYS_FOLDER))
        exit(1)

    all_files = [f for f in os.listdir(REPLAYS_FOLDER) if os.path.isfile(os.path.join(DIR_SCRIPT, REPLAYS_FOLDER, f))]

    # Team name filtering code
    if args.teams and len(args.teams) == 1:  # 1 team given
        files = [k for k in all_files if args.teams[0] in k]
    elif args.teams and len(args.teams) > 1:  # 2 teams given
        files = [k for k in all_files if args.teams[0] in k and args.teams[1] in k]
    else:  # No team filtering
        files = all_files

    if len(files) == 0:
        print("ERROR: No files found")
    elif args.number:  # We are selecting a replay to play
        if args.number < len(files) + 1:
            found_file = files[args.number - 1]
            match = re.match("(.*)_vs_(.*)_.*", found_file)
            red = match[1]
            blue = match[2]
            os.system("{} {} --red-name {} --blue-name {} --replay {}/{} --delay-step {}".format(PYTHON_BIN,
                                                                                                 os.path.join(
                                                                                                     DIR_SCRIPT,
                                                                                                     "capture.py"), red,
                                                                                                 blue, REPLAYS_FOLDER,
                                                                                                 found_file,
                                                                                                 str(args.delay_step)))
        else:
            print("ERROR: Invalid replay ID. {} replays found (select from 1 - {}).".format(len(files), len(files)))
    else:  # No number given, list the IDs
        print("{} Files found:".format(len(files)))
        for i, f in enumerate(files):
            print("ID {}: {}".format(i + 1, f))


if __name__ == "__main__":
    main()
