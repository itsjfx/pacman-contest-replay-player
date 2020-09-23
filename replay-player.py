from os import listdir
from os.path import isfile, join, exists
import sys
import argparse
import os
import re

# Settings
REPLAYS_FOLDER = "replays"
PYTHON = "python"

# Constants
DIR_SCRIPT = sys.path[0]
REPLAYS_FOLDER = join(DIR_SCRIPT, REPLAYS_FOLDER)

# Arg parsing
parser = argparse.ArgumentParser()
parser.add_argument('-t','--teams', dest='teams', nargs='+', help='Set teams to filter by <team1> [team2]')
parser.add_argument('-n','--number', dest='number', nargs='?', type=int, help='Set replay to run. Omit to list all replays')
parser.add_argument('-s', '--delay-step', type=float, dest='delay_step', help='Delay step in a play or replay.', default=0.03)
args = parser.parse_args()

def main():
	if not exists(REPLAYS_FOLDER):
		return print('No replays folder found with path "{}". This can be edited in the script under REPLAYS_FOLDER'.format(REPLAYS_FOLDER))

	all_files = [f for f in listdir(REPLAYS_FOLDER) if isfile(join(DIR_SCRIPT, REPLAYS_FOLDER, f))]
	
	# Team name filtering code
	if args.teams and len(args.teams) == 1: # 1 team given
		files = [k for k in all_files if args.teams[0] in k]
	elif args.teams and len(args.teams) > 1: # 2 teams given
		files = [k for k in all_files if args.teams[0] in k and args.teams[1] in k]
	else: # No team filtering
		files = all_files

	if len(files) == 0:
		print("ERROR: No files found")
	elif args.number: # We are selecting a replay to play
		if args.number < len(files) + 1:
			found_file = files[args.number - 1]
			match = re.match("(.*)_vs_(.*)_.*", found_file)
			red = match[1]
			blue = match[2]
			os.system("{} {} --red-name {} --blue-name {} --replay {}/{} --delay-step {}".format(PYTHON, join(DIR_SCRIPT, "capture.py"), red, blue, REPLAYS_FOLDER, found_file, str(args.delay_step)))
		else:
			print("ERROR: Invalid replay ID. {} replays found (select from 1 - {}).".format(len(files), len(files)))
	else: # No number given, list the IDs
		print("{} Files found:".format(len(files)))
		for i, f in enumerate(files):
			print("ID {}: {}".format(i + 1, f))

if __name__ == "__main__":
    main()
