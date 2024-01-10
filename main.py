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
class Style:
    # All styles use ANSI COLORS CODES
    DIAMOND = '\033[1;30;44m'
    SEVEN_NUM = '\033[1;30;41m'
    SEVEN = '\033[0;34;41m'
    FRUIT = '\033[0;30;107m'
    BAR = '\033[1;37;40m'
    JACKPOT = '\033[1;30;43m'
    # 9 Character Offset for HIGHLIGHT + DEFAULT
    DEFAULT = '\033[0m'
    HIGHLIGHT = '\033[92m'


SLOT_OPTIONS = [Style.FRUIT + "   CH🍒RRY  " + Style.DEFAULT, Style.FRUIT + "   LEM🍋N   " + Style.DEFAULT, Style.SEVEN
                + "   SE" + Style.SEVEN_NUM + '7' + Style.SEVEN + "EN    " + Style.DEFAULT, Style.BAR + "    BAR!    " +
                Style.DEFAULT, Style.DIAMOND + "  DIA💎OND  " + Style.DEFAULT,
                Style.JACKPOT + "   JACKPOT  " + Style.DEFAULT]


# ^ Each entry has a field-with of 9.

class DisplayBlock:
    DEFAULT = "| %-36s |"
    DIVIDER = "|--------------------------------------|"
    DEFAULT_HIGHLIGHT = "| %-45s |"
    BORDER = "|======================================|"
    SLOTS = """|-----\\/-----------\\/-----------\\/-----|\n|%s|%s|%s|\n|-----/\\-----------/\\-----------/\\-----|"""

    class Title:
        TITLE_INTRO = "Welcome to the Slot Machine"
        TITLE_PROMPT = "Press " + Style.HIGHLIGHT + "ENTER" + Style.DEFAULT + " to start the game!"

    class Info:
        CREDIT_COUNT = "You have " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " credits."

    class Options:
        BET_PROMPT = "Please input # of credits to bet:"
        BET_OPTIONS = Style.HIGHLIGHT + "        [1]  [2]  [5]  [10]" + Style.DEFAULT
        QUIT = "Press " + Style.HIGHLIGHT + "[Q]" + Style.DEFAULT + " to quit."

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
slots_array = random.choices(SLOT_OPTIONS, k=3)
bet_amount = -1
userInput = ""
canHold = True
hold1 = False
hold2 = False
hold3 = False
minimumAge = 18


# Define Methods and Functions for printing different screens, hold toggle, and bet-reward calculations
def toggleHold(slot):
    global hold1, hold2, hold3
    if slot == 1:
        if hold1:
            hold1 = False
        else:
            hold1 = True
    elif slot == 2:
        if hold2:
            hold2 = False
        else:
            hold2 = True
    elif slot == 3:
        if hold3:
            hold3 = False
        else:
            hold3 = True
class Screen:
    @staticmethod
    def titleScreen():
        os.system('cls || clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Title.TITLE_INTRO)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Title.TITLE_PROMPT)
        print(DisplayBlock.BORDER)
        input()

    @staticmethod
    def outOfCredit():
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "Not enough Credits!" + Style.DEFAULT))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    "Press " + Style.HIGHLIGHT + "[+]" + Style.DEFAULT + "to add more credits."))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "        OR" + Style.DEFAULT))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "INVALID INPUT" + Style.DEFAULT))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to try another bet."))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.QUIT))
        print(DisplayBlock.BORDER)
        input()

    @staticmethod
    def slotScreen():
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))

    def holdScreen():
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Info.CREDIT_COUNT)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Options.BET_PROMPT)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.BET_OPTIONS)
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.QUIT)
        print(DisplayBlock.BORDER)



    @staticmethod
    def invalidInput(origin):
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "INVALID INPUT" + Style.DEFAULT))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to try again."))
        print(DisplayBlock.BORDER)
        input()

        if origin == "BET":
            Screen.betOptionsScreen()
        elif origin == "HOLD":
            Screen.holdOptionsScreen()

    @staticmethod
    def holdOptionsScreen():
        global bet_amount, userInput, hold1, hold2, hold3, canHold
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Options.BET_PROMPT)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.BET_OPTIONS)
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.QUIT)
        print(DisplayBlock.BORDER)

    def betOptionsScreen():
        global gameover, bet_amount, userInput, hold1, hold2, hold3, canHold
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Options.BET_PROMPT)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.BET_OPTIONS)
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.QUIT)
        print(DisplayBlock.BORDER)

        # Check Input
        userInput = input().upper()
        if userInput == 'Q':
            gameover = True
        elif userInput == '1':
            bet_amount = 1
            Screen.holdScreen()
        elif userInput == '2':
            bet_amount = 2
            Screen.holdScreen()
        elif userInput == '5':
            bet_amount = 5
            Screen.holdScreen()
        elif userInput == '10':
            bet_amount = 10
            Screen.holdScreen()
        else:
            Screen.invalidInput("BET")

        if credit <= 0 or credit < bet_amount:
            Screen.outOfCredit()

        if canHold:
            Screen.holdOptionsScreen()
        else:
            hold1 = False
            hold2 = False
            hold3 = False
            Screen.slotScreen()


# Ask how many Credits you have today?
userInput = input("As you walk into the Casino, you wonder how much you can afford.\nHow many credits did you bring with you?\n")

while not userInput.lstrip('-').isnumeric():
    os.system('cls || clear')
    print("That isn't a number! Lets try again, this time just tell me the number of credits you have.")
    userInput = input("As you walk into the Casino, you wonder how much you can afford. \nHow many credits did you bring with you?\n")

userInput = int(userInput)
if userInput > 999999999999999999:
    os.system('cls || clear')
    print(
        "Woah there buddy, don't spend all your credits right now! I'll let in " + Style.HIGHLIGHT + "999999999999999999 Credits" + Style.DEFAULT)
    userInput = 100
    input("Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to go to the slot machine.")

while userInput <= 5:
    os.system('cls || clear')
    userInput = input("That's a sad amount! I'll give you as many credits you want, on the house!\nJust tell me how many you want:\n")
    while not userInput.isnumeric():
        os.system('cls || clear')
        userInput = input("I need a number, not a story. Just give me the number of your dreams,\nand I'll give you that many!\n")
    userInput = int(userInput)
    if userInput > 999999999999999999:
        os.system('cls || clear')
        print("Woah there buddy, don't put me out of business! Since you're being annoying, Ill just give you " + Style.HIGHLIGHT + "100 Credits" + Style.DEFAULT)
        userInput = 100
        input("Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to go to the slot machine.")
credit = userInput


# Print Out Intro
Screen.titleScreen()

# Main Loop
while not gameover:
    Screen.betOptionsScreen()

# Goodbye Message
os.system('cls || clear')
print(DisplayBlock.GOODBYE % (4, 3, 100, credit))
