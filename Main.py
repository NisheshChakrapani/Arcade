import sys, pygame
from Games import *
game = raw_input("Play Pong, Breakout or Air Hockey? Other responses will close the game\n> ")
if game != "pong" and game != "breakout" and game != "air hockey":
    sys.exit()
else:
    try:
        difficulty = int(raw_input("Choose a difficulty from 1-3. Other responses will close the game\n> "))
        if difficulty < 1 or difficulty > 3:
            sys.exit()
    except ValueError:
        sys.exit()

print("Click on the new icon on the taskbar and enjoy the game!")

if game == "pong" or game == 1:
    Pong(difficulty)
elif game == "breakout" or game == 2:
    Breakout(difficulty)
elif game == "air hockey" or game == 3:
    AirHockey(difficulty)