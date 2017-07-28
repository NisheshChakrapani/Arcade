import sys, pygame
from Games import *
game = ""
while game != "pong" and game != "breakout" and game != "air hockey":
    game = raw_input("Play Pong, Breakout or Air Hockey?\n> ")
difficulty = 0
while difficulty < 1 or difficulty > 3:
    try:
        difficulty = int(raw_input("Choose a difficulty from 1-3.\n> "))
    except ValueError:
        pass

print("Click on the new icon on the taskbar and enjoy the game!")

if game == "pong" or game == 1:
    Pong(difficulty)
elif game == "breakout" or game == 2:
    Breakout(difficulty)
elif game == "air hockey" or game == 3:
    AirHockey(difficulty)