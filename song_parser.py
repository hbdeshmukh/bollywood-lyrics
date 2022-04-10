import argparse
import glob
import os
import pandas as pd
import pathlib
import re
import string

TITLE = '\stitle'
FILM = '\\film'
YEAR = '\year'
LYRICIST = '\lyrics'
SINGER = '\singer'
COMPOSER = '\music'
IGNORE_PREFIX = ['%', '#', '\starring', '\printtitle', '\startsong', '\endsong']

class Song:
	def __init__(self):
		self.title = ''
		self.film = ''
		self.year = 0
		self.singer = ''
		self.composer = ''
		self.lyricist = ''
		self.lyrics = ''
		self.fname = ''

	def clean(self):
		self.title = self.title.lower()
		self.film = self.film.lower()
		self.singer = self.singer.lower()
		self.composer = self.composer.lower()
		self.lyricist = self.lyricist.lower()
		self.lyrics = self.lyrics.lower()
		# Remove punctuations
		punct = set(string.punctuation)	
		self.title = "".join([ch for ch in self.title if ch not in punct])
		self.film = "".join([ch for ch in self.film if ch not in punct])
		self.singer = "".join([ch for ch in self.singer if ch not in punct])
		self.composer = "".join([ch for ch in self.composer if ch not in punct])
		self.lyricist = "".join([ch for ch in self.lyricist if ch not in punct])
		self.lyrics = "".join([ch for ch in self.lyrics if ch not in punct])

	def to_dict(self):
		# We don't export fname in the output. It is meant for debugging purposes. 
		return {
			'Title' : self.title,
			'Film' : self.film,
			'Year' : self.year,
			'Singer' : self.singer,
			'Composer' : self.composer,
			'Lyricist' : self.lyricist,
			'Lyrics' : self.lyrics,
		}

def validateYear(year_text):
	if len(year_text) == 0:
		return False
	return year_text.isnumeric()
	
def isComment(line):
	for p in IGNORE_PREFIX:
		if line.startswith(p):
			return True
	return False

def checkPrefix(line, prefix):
	return line.startswith(prefix) 

def extractText(line):
	res = re.findall(r'\{.*?\}', line)
	if len(res) == 0:
		return '' 
	return res[0][1:-1]

def readFile(filename):
	with open(filename, encoding="utf8", errors='ignore') as f:
		lines = f.read().splitlines()
		return lines

def getFilename(filename):
	return pathlib.Path(filename).name
	
def createSong(filename):
	lines = readFile(filename)
	song = Song()
	setattr(song, 'fname', getFilename(filename))
	for l in lines:
		if isComment(l):
			continue
		if checkPrefix(l, TITLE):
			setattr(song, 'title', extractText(l))
			continue
		if checkPrefix(l, FILM):
			setattr(song, 'film', extractText(l))
			continue
		if checkPrefix(l, YEAR):
			year_text = extractText(l)
			if not validateYear(year_text):
				year_text = -1
			setattr(song, 'year', int(year_text))
			continue
		if checkPrefix(l, SINGER):
			setattr(song, 'singer', extractText(l))
			continue
		if checkPrefix(l, COMPOSER):
			setattr(song, 'composer', extractText(l))
			continue
		if checkPrefix(l, LYRICIST):
			setattr(song, 'lyricist', extractText(l))
			continue
		# All previous checks failed, this line is part of the lyrics.
		song.lyrics = song.lyrics + ' ' + l
	song.clean()
	return song

def getSongsDf(base_dir):
	all_files_path = os.path.join(base_dir, '*.txt')
	all_files = glob.glob(all_files_path) 
	songs = []
	for f in all_files:
		song = createSong(f)
		songs.append(song)

	return pd.DataFrame().from_records([s.to_dict() for s in songs])

def main():
	# Read the input arguments. 
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--input', help='Input path for the directory with the lyrics files',  type=pathlib.Path)
	arg_parser.add_argument('--output', help='Filename for the CSV output', type=argparse.FileType('w')) 
	args = arg_parser.parse_args()
	# Create the dataframe. 
	df = getSongsDf(args.input)
	# Export the dataframe as a CSV file. 
	df.to_csv(args.output, header=True, index=False)

if __name__ == "__main__":
	main()
