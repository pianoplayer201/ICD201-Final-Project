"""
Programmer: Ryan Mehrian
Date: December 12, 2023
Last Modified:
-----
This program is a game emulating a casino's slot machine. The user will start with 100
"credits", and they will be given the choice to bet 1, 2, 5, or 10 credits, with each
spin having 3 slots with 6 different possibilities (Cherry, Lemon, Lucky 7, Bar, Diamond,
and Jackpot). The player will receive a reward depending on what they roll, and the bet
they inputted at the start. When a player loses, their lost credits accrue in the jackpot
that will be given back to them if the user rolls a jackpot. The player may also choose
to hold 2 out of 3 slots if they do not get a winning combination.
"""
# Imports
import os
import random


# Constant Declaration
class style:
    # All styles use ANSI COLORS CODES
    DIAMOND = '\033[1;30;44m'
    SEVEN_NUM = '\033[1;30;41m'
    SEVEN = '\033[0;34;41m'
    FRUIT = '\033[0;30;107m'
    BAR = '\033[1;37;40m'
    DEFAULT = '\033[0m'


SLOT_OPTIONS = [style.FRUIT + "   CH🍒RRY  " + style.DEFAULT, style.FRUIT + "   LEM🍋N   " + style.DEFAULT, style.SEVEN
                + "   SE" + style.SEVEN_NUM + '7' + style.SEVEN + "EN    " + style.DEFAULT, style.BAR + "    BAR!    " +
                style.DEFAULT, style.DIAMOND + "  DIA💎OND  " + style.DEFAULT, " JACKPOT "]

# ^ Each entry has a field-with of 9.

TITLE = """
|==================================|
|   Welcome to the Slot Machine!   |
|----------------------------------|
|  You have %-3d credits to start   |
|----------------------------------|
| Press ENTER to start the game!   |
|==================================|
"""
OPTIONS = """
|==================================|
|   You have %-3d credits           |
|==================================|
|  What would you like to do?      |
|----------------------------------|
|  [B]et                           |   
|  [H]old                          | 
|  [Q]uit                          |
|==================================|
"""
GOODBYE = """
|==================================|
|   Game Over, Thanks for Playing! |
|==================================|
|  You won: %3d spins.             |
|  You lost: %3d spins.            |
|  You started with %4d credits.  |
|  You ended with %4d credits.    |
|==================================|
"""

# Variable Declaration
credit = 100
gameover = False
slot1 = None
slot2 = None
slot3 = None

# Print Out Intro
print(TITLE % credit)
input()
os.system('cls')

# Main Loop
while not gameover:
    print(OPTIONS % credit)
    userInput = input().upper()
    if userInput == 'Q':
        gameover = True
    elif userInput == "H":
        os.system('cls')
        print("Placeholder Hold System")
    elif userInput == "B":
        os.system('cls')
        print("Placeholder Bet System")
    else:
        os.system('cls')
        print("Placeholder Invalid input system")

# Goodbye Message
os.system('cls')
print(GOODBYE % (4, 3, 100, credit))
