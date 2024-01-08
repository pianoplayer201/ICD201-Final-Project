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
import tkinter


# Constant Declaration
class Style:
    # All styles use ANSI COLORS CODES
    DIAMOND = '\033[1;30;44m'
    SEVEN_NUM = '\033[1;30;41m'
    SEVEN = '\033[0;34;41m'
    FRUIT = '\033[0;30;107m'
    BAR = '\033[1;37;40m'
    #9 Character Offset for HIGHLIGHT + DEFAULT
    DEFAULT = '\033[0m'
    HIGHLIGHT = '\033[92m'


SLOT_OPTIONS = [Style.FRUIT + "   CH🍒RRY  " + Style.DEFAULT, Style.FRUIT + "   LEM🍋N   " + Style.DEFAULT, Style.SEVEN
                + "   SE" + Style.SEVEN_NUM + '7' + Style.SEVEN + "EN    " + Style.DEFAULT, Style.BAR + "    BAR!    " +
                Style.DEFAULT, Style.DIAMOND + "  DIA💎OND  " + Style.DEFAULT, " JACKPOT "]


# ^ Each entry has a field-with of 9.

class DisplayBlock:
    DEFAULT = "| %-32s |"
    DIVIDER = "|----------------------------------|"
    DEFAULT_HIGHLIGHT = "| %-41s |"
    BORDER = "|==================================|"

    class Title:
        TITLE_INTRO = "Welcome to the Slot Machine"
        TITLE_PROMPT = "Press " + Style.HIGHLIGHT + "ENTER" + Style.DEFAULT + " to start the game!"

    class Info:
        CREDIT_COUNT = "You have " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " credits."

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


# Define Methods for printing different screens.
class Screen:
    @staticmethod
    def titleScreen():
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Title.TITLE_INTRO)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Title.TITLE_PROMPT)
        print(DisplayBlock.BORDER)


# Print Out Intro

Screen.titleScreen()
input()
os.system('cls')

# Main Loop
while not gameover:
    print(DisplayBlock.OPTIONS % credit)
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
print(DisplayBlock.GOODBYE % (4, 3, 100, credit))
