#!/usr/bin/env python

import re
from os.path import isfile
from subprocess import check_output
from random import shuffle
from time import sleep

SAY_CMD = "/usr/bin/say"
DEFAULT_DICT_FILE = "/usr/share/dict/words"
DEFAULT_DELAY = 2.0
ENDING_PHRASES = [
	"That's all folks",
	"Over and out",
	"The end",
	"Okee dokee"
]

def say(thing, voice=None, rate=None):
	args = [SAY_CMD]
	if voice:
		args.extend(["-v", voice])
	if rate:
		args.extend(["-r", rate])
	args.append(thing)
	check_output(args)


def get_entries(dict_file, randomize, letter_filter_regex=None, suffix_filter_regex=None, min_length=None, max_length=None, limit=None):
	entries = []
	with open(dict_file, "r") as fh:
		for line in fh:
			l = line.rstrip()
			if letter_filter_regex and not re.match(letter_filter_regex, l):
				continue
			if suffix_filter_regex and not re.match(suffix_filter_regex, l):
				continue
			if min_length and len(l) < min_length:
				continue
			if max_length and len(l) > max_length:
				continue
			entries.append(l)

	if randomize:
		shuffle(entries)

	if limit:
		return entries[:limit]

	return entries


def main(args):
	letter_filter_regex = r"^[{}]+$".format(args.letter_filter) if args.letter_filter else None
	suffix_filter_regex = r".*{}(\W|$)".format(args.suffix_filter) if args.suffix_filter else None

	entries = get_entries(args.dict_file, not args.in_order, letter_filter_regex, suffix_filter_regex, args.min_length, args.max_length, args.limit)
	for e in entries:
		print(e)
		if args.word_delay == 0:
			say(e, args.voice, args.rate)
		else:
			bits = re.split(r"\s+", e)
			for i, b in enumerate(bits):
				say(b, args.voice, args.rate)
				if i < len(bits) - 1:
					sleep(args.word_delay)
		sleep(args.line_delay)

	if args.the_end:
		shuffle(ENDING_PHRASES)
		say(ENDING_PHRASES[0], args.voice)


if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-D', '--dict_file', help="Dictionary file to use (default: {})".format(DEFAULT_DICT_FILE), default=DEFAULT_DICT_FILE)
	parser.add_argument('-d', '--delay', default=DEFAULT_DELAY, type=float, help="Seconds of delay between items (default: {})".format(DEFAULT_DELAY))
	parser.add_argument('--line_delay', type=float, help="Delay between lines, defaults to value of --delay")
	parser.add_argument('--word_delay', type=float, help="Delay between words in a line, defaults to value of --delay")
	parser.add_argument('-l', '--limit', help="Limit to N words (default is all of them)", type=int)
	parser.add_argument('--in_order', default=False, help='Play dictionary in order (default is to randomize)', action='store_true')
	parser.add_argument('-v', '--voice', help="Specify the voice to use (type 'say --voice ?') to see your options")
	parser.add_argument('-r', '--rate', help="Specify the rate in words per minute (try -r 100)")
	parser.add_argument('-L', '--letter_filter', help="Only use words that contain the specified letters (eg: -L asfx would use fax but not fox)")
	parser.add_argument('-S', '--suffix_filter', help="Only use lines that have a word with the suffix (eg: -S tion would use lines with 'action')")
	parser.add_argument('--max_length', type=int, help="Max length of word")
	parser.add_argument('--min_length', type=int, help="Min length of word")
	parser.add_argument('--the_end', default=False, action="store_true", help="Announce the end of the list")
	parser.add_argument('-I', '--initial_delay', type=int, help="Delay start for N seconds")
	args = parser.parse_args()

	if args.line_delay == None:
		args.line_delay = args.delay

	if args.word_delay == None:
		args.word_delay = args.delay

	if not isfile(SAY_CMD):
		print("Uh oh, can't find 'say' command at {}".format(SAY_CMD))
		exit(1)

	if not isfile(args.dict_file):
		print("Uh oh, can't find dictionary file at {}".format(args.dict_file))
		exit(1)

	if args.initial_delay:
		sleep(args.initial_delay)

	main(args)