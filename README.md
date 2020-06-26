# Balloon Platoon!  

This game is my first game ever created. In this game, you must type in the correct vocab translation before the balloon reaches the top of the screen. This is a basic game for testing one's vocabulary skills.  You can create your own custom vocabulary by modifying the 'germanvocab.csv' file found in the 'vocab' folder.  The keyword for custom vocabulary selection is an 'M' in the 'Type' column.

# Running
## Command Window
To run, open your command prompt / console and set your base directory to the folder where you saved this repository.  Then run 'script.py' with python. For me, this looks like (Windows):
```
(base) C:\Users\Patrick\Documents\PythonExercise\vocabgame>python script.py
```
Please note that this repository is saved in the 'vocabgame' folder for me.  If the correct base path is not initiated, then there may be a 'file-not-found' error raised.  If there is, then it is likely because you are in the wrong base path.

## Dependencies
This was developed using Python 3.7 (Anaconda) with pygame v1.9.6. The following dependencies are shown:

pygame
xlrd
random
numpy
pandas
csv
datetime
sys
os


# Reflection on this project:
## Art

Due to this being my first game ever created, there are naturally some things I would do different the 2nd time around. 

For me, the most difficult part was the art creation.  Most of the art was created by me, and I am no artist. The few sprites that were not created by me are linked below:

Night Sky: https://www.deviantart.com/zlzhang/art/Night-Sky-Pixel-Art-573693193  <-- Great art, my man!!

Red Balloon: https://www.reddit.com/r/PixelArt/comments/6txnez/ocnewbieballoon_pixel_art_criticism_welcome/

Hot Air Balloon: https://en.clipdealer.com/vector/media/A:79145295

Goku P1: https://www.pinterest.com/pin/302233824995446924/

Goku P2: https://www.funidelia.de/goku-kostum-dragon-ball-80213.html

Eventually, I was forced to stop making progress on this game, as creating the art was taking too much time (I am currently in a neuroscience master's program, and need to focus on studies). Please do not judge me too hard for the artwork I created, it is definitely incomplete. 

## Improvements
1. Set a limit on the # of characters that can be entered.
2. Make an English -> German vocab direction.  (This is why I created GermBot! My other GitHub repository!)
3. Improve the artwork.
4. Find better heuristics for sprite placement.
5. My run-time efficient sprite read-in function unfortunately requires me to have multiple copies of the same picture in the sprites folder.
6. I need to comment this code MUCH BETTER. Code in my later projects are commented better.
7. Screen resizing is not available.
8. Add vocab from the GUI.
9. Overall organization of code could be better.
10. Score tracking in this game is not ideal. The game should set a limit on the number of vocab words that are played each round. Right now, it is set up to run through the entire vocab list in 'germanvocab.csv' that meets the type and level reqs. Unfortunately, this means that as new words are added, the game duration increases, and naturally the scores will keep increasing too.  







