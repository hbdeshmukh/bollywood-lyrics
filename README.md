# bollywood-lyrics

A comprehensive collection of lyrics and other metadata for bollywood and non-bollywod songs starting from 1940s all the way to 2000s. 

## Credits 

The data for this collection comes from https://www.giitaayan.com/. 
Giitayan's data files are stored here - https://github.com/v9y/giit.
Thanks to the maintainers and contributors of Giitayan. 

## Instructions

Download the lyrics.csv file and use it. 

### Advanced usage

To play with the parser, use these steps: 

1. Clone the giit repo - https://github.com/v9y/giit
2. Note the path to the docs/ directory from the cloned git repo. (say docs_path)
3. python3 song_parser.py --input docs_path --output lyrics.csv
