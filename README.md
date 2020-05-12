# stenoSpeak
Script for TTSing words on the mac for use in Steno practice.

This python script assumes access to the "say" command, provided on macOS to convert text to speech.

By default, the system dictionary of words is used. Alternate dictionaries can be used which can be lines of words or sentences.

## Usage
Type `./stenospeak --help` to see all of the options.

Here are some examples:

##### Use alternate dictionary file of words

	./stenospeak.py -D words.txt

##### Use alternate dictionary file of sentences and no delay between words.
	
	./stenospeak.py -D sentences.txt --word_delay 0

##### Include information about hitting the end of the file and some params to change the TTS voice and speech rate

	./stenospeak.py --the_end -v Samantha -r 100 --limit 10

##### Only use entries that have words ending in "tion"

	./stenospeak.py -S tion