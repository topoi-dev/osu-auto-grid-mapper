# osu! auto grid mapper
this was a small project i wanted to create just to see the possibilities of auto generated mapping in osu!
i do not plan on making this a well maintained project, but i do want to make it accessible.
i am also not very experienced with python or good code so please excuse my mess

# requirements
this program requires python 3.8.x, other versions probably will not work (3.9.x will not). check your python version with:
```
python --version
```

assuming you have pip, simply open the cloned directory and enter this command to install dependencies
```
pip install requirements.txt
```

# usage
as of now all the python files are jumbled into the same directory, sorry
- copy an .mp3 or .wav file that you want to create the map for into the cloned directory and make note of the filename
- next, use the command (keep the exact filename format of title.mp3 and do not add any \'s or .'s)
```
python main.py --filename yourfile.mp3
```
- follow the prompt instructions
- program will output the osu hit objects into a hitobjects.txt
- copy these hitobjects into your .osu map file (slider velocity of 1.3 is required and use only a single red line timing point)

i will make it output an actual map file soon

# about
write here what this program is doing future me (good luck👍)

# references
onset detection: https://github.com/CPJKU/onset_detection/

"Evaluating the Online Capabilities of Onset Detection Methods"
by Sebastian Böck, Florian Krebs and Markus Schedl in Proceedings of the 13th International Society for Music Information Retrieval Conference (ISMIR), 2012

bpm detection: https://github.com/scaperot/the-BPM-detector-python/
