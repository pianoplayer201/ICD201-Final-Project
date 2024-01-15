"""
Programmer: Ryan Mehrian
Date Created: December 12, 2023
Last Modified: January
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
import time
import math


# --- Constant Declaration ---

# Style class to store all ANSI Colour Codes used in the program.
class Style:
    # Styling text for SLOTS
    DIAMOND = '\033[1;30;44m'
    SEVEN_NUM = '\033[1;30;41m'
    SEVEN = '\033[0;34;41m'
    FRUIT = '\033[0;30;107m'
    BAR = '\033[1;37;40m'
    JACKPOT = '\033[1;30;43m'

    # Styling text in PROMPTS and UI
    DEFAULT = '\033[0m'
    HIGHLIGHT = '\033[92m'

    # NOTE TO SELF: ^ 9 Character Offset for HIGHLIGHT + DEFAULT


# An array that stores every possible option in the slot machine per slot.
SLOT_OPTIONS = [Style.FRUIT + "   CH🍒RRY  " + Style.DEFAULT, Style.FRUIT + "   LEM🍋N   " + Style.DEFAULT, Style.SEVEN
                + "   SE" + Style.SEVEN_NUM + '7' + Style.SEVEN + "EN    " + Style.DEFAULT, Style.BAR + "    BAR!    " +
                Style.DEFAULT, Style.DIAMOND + "  DIA💎OND  " + Style.DEFAULT,
                Style.JACKPOT + "   JACKPOT  " + Style.DEFAULT]


# DisplayBlock Class to store every possible printed line as a string, used later as modules to print a screen.
class DisplayBlock:
    # Blank, bordered lines. Different fieldwidths to account for Style.Highlight + Style.Default ANSI keycode characters.
    DEFAULT = "| %-36s |"
    DEFAULT_HIGHLIGHT = "| %-45s |"

    # Different Borders, to better user experience and UI readability.
    DIVIDER = "|--------------------------------------|"
    BORDER = "|======================================|"

    # String to print out the SLOTS of the slot machine. Accepts 3 strings, drawn randomly from SLOT_OPTIONS
    SLOTS = """|-----\\/-----------\\/-----------\\/-----|\n|%s|%s|%s|\n|-----/\\-----------/\\-----------/\\-----|"""

    # Prompts UNIQUE to startup sequence.
    class Title:
        TITLE_INTRO = "Welcome to the Slot Machine"
        TITLE_PROMPT = "Press " + Style.HIGHLIGHT + "ENTER" + Style.DEFAULT + " to start the game!"

    # Text that provides user with information based on changing variables while the program runs.
    class Info:
        CREDIT_COUNT = "You have " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " credits."
        BET_AMOUNT = "Bet amount: " + Style.HIGHLIGHT + "%d CREDITS" + Style.DEFAULT
        JACKPOT = Style.HIGHLIGHT + "JACKPOT: %d CREDITS" + Style.DEFAULT
        HELD_TRUE = "HELD"
        HELD_FALSE = "NOT HELD"

    # Prompts given to the user while the program is running.
    class Options:
        BET_PROMPT = "Please input # of credits to bet:"
        BET_OPTIONS = Style.HIGHLIGHT + "        [1]  [2]  [5]  [10]" + Style.DEFAULT
        HOLD_PROMPT = "Input Slot # to toggle hold:"
        HOLD_OPTION = Style.HIGHLIGHT + "[%d]" + Style.DEFAULT + " ----- %s"
        QUIT = "Press " + Style.HIGHLIGHT + "[Q]" + Style.DEFAULT + " to quit."

    # All the strings that will show on the QUIT SCREEN, such as player statistics.
    class GAMEOVER:
        GOODBYE = "Game Over, Thanks for Playing!"
        WIN_COUNT = "You won " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " spins."
        LOSE_COUNT = "You lost " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " spins."
        CREDIT_FINISH = "You left with: " + Style.HIGHLIGHT + "%d" + Style.DEFAULT + " credits"
        CREDIT_CHANGE = "TOTAL %s: " + Style.HIGHLIGHT + "%d" + " credits." + Style.DEFAULT


# --- Variable Declaration ---
winAmount = -1
didWin = False
jackpot = 0
credit = 100
oldSlot = ""
betAmount = -1
gameover = False
slots_array = random.choices(SLOT_OPTIONS, k=3)
userInput = ""
canHold = True
hold1 = False
hold2 = False
hold3 = False
winMessage = ""
winOutput = ""
countSpinWin = 0
countSpinLoss = 0
originalCredit = 0
totalWinAmount = 0


# --- Define Methods and Functions for printing different screens, hold toggle, and bet-reward calculations ---


# toggleHold Function that toggles hold status for the selected slot #, slot # is taken as a parameter when called.
# toggleHold is purely backend, and does not print out any result for the user.
def toggleHold(slot):
    global hold1, hold2, hold3, canHold

    # If block to check the selected slot # to toggle that slot's hold status.
    if slot == 1:
        hold1 = not hold1
    elif slot == 2:
        hold2 = not hold2
    else:
        hold3 = not hold3

    Screen.holdOptionsScreen()


# winCalculation is a function that calculates the result of the slots rolled by making comparisons between them, and
# then calling upon Screen.winScreen with an OUTCOME CODE as a parameter.
# winCalculation is called at the end of Screen. slotScreen, is purely backend, and does not print out any result for the user.
def winCalculation():
    global slots_array, credit, jackpot, didWin, winAmount

    didWin = True

    # If BLOCK that makes comparisons to identify if the player has a winning combination, recording their winAmount,
    # and then calling upon Screen.winScreen with the win-type as a parameter. If no win is detected, the if BlOCK
    # sets didWin to false and adds betAmount to the jackpot pool.
    if slots_array[0] == SLOT_OPTIONS[0] and slots_array[1] != SLOT_OPTIONS[0]:
        winAmount = betAmount
        Screen.winScreen("CHERRY1")
    elif slots_array[0] == SLOT_OPTIONS[0] and slots_array[1] == SLOT_OPTIONS[0] and slots_array[2] != SLOT_OPTIONS[0]:
        winAmount = betAmount * 2
        Screen.winScreen("CHERRY2")
    elif slots_array[0] == SLOT_OPTIONS[0] and slots_array[1] == SLOT_OPTIONS[0] and slots_array[2] == SLOT_OPTIONS[0]:
        winAmount = betAmount * 3
        Screen.winScreen("CHERRY3")
    elif slots_array[0] == SLOT_OPTIONS[1] and slots_array[1] == SLOT_OPTIONS[1] and slots_array[2] == SLOT_OPTIONS[1]:
        winAmount = betAmount * 5
        Screen.winScreen("LEMON3")
    elif slots_array[0] == SLOT_OPTIONS[2] and slots_array[1] == SLOT_OPTIONS[2] and slots_array[2] == SLOT_OPTIONS[2]:
        winAmount = betAmount * 7
        Screen.winScreen("SEVEN3")
    elif slots_array[0] == SLOT_OPTIONS[3] and slots_array[1] == SLOT_OPTIONS[3] and slots_array[2] == SLOT_OPTIONS[3]:
        winAmount = betAmount * 10
        Screen.winScreen("BAR3")
    elif slots_array[0] == SLOT_OPTIONS[4] and slots_array[1] == SLOT_OPTIONS[4] and slots_array[2] == SLOT_OPTIONS[4]:
        winAmount = betAmount * 20
        Screen.winScreen("DIAMOND3")
    elif slots_array[0] == SLOT_OPTIONS[5] and slots_array[1] == SLOT_OPTIONS[5] and slots_array[2] == SLOT_OPTIONS[5]:
        winAmount = jackpot
        # Remember to set jackpot to 0 inside winScreen
        Screen.winScreen("JACKPOT")
    else:
        winAmount = 0
        didWin = False
        jackpot += betAmount
        Screen.winScreen("LOSE")


# The Screen class contains various functions that use the DisplayBlock class to print out screens in a modular manner.
# The functions inside the Screen class also handle input detection.
class Screen:

    # Prints out Title screen.
    @staticmethod
    def titleScreen():
        os.system('cls || clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Title.TITLE_INTRO)
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Title.TITLE_PROMPT)
        print(DisplayBlock.BORDER)
        input()

    # winScreenFlicker creates a flashing effect for when the user wins. The screen lets the user know they've won,
    # and has a different message for a jackpot win (detected via a parameter of the function)
    @staticmethod
    def winScreenFlicker(message):
        os.system('cls||clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % "")
        print(DisplayBlock.DEFAULT_HIGHLIGHT % ("             " + Style.HIGHLIGHT + message + Style.DEFAULT))
        print(DisplayBlock.DEFAULT % "")
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.BET_AMOUNT % betAmount))
        print(DisplayBlock.BORDER)

    # This function is called by winCalculation. Taking the outcome from winCalculation, this function constructs
    # and prints a winning/losing screen for the user. If the user has won, the function also calls upon
    # Screen.winScreenFlicker, to create a flashing winning effect to congratulate the user. Ends by
    # calling betScreenOptions to get the user to play again.
    @staticmethod
    def winScreen(outcome):
        global winMessage, betAmount, winOutput, winAmount, credit, jackpot, didWin, countSpinWin, countSpinLoss
        credit += winAmount

        # Set win message
        if outcome == "JACKPOT":
            winMessage = "JACKPOT!!"
            jackpot = 0
            countSpinWin += 1
        elif didWin:
            winMessage = "WINNER!!"
            countSpinWin += 1
        else:
            winMessage = "Better luck next time!"
            countSpinLoss += 1

        # Flash winMessage if you win
        if didWin:
            for i in range(4):
                if winOutput == "":
                    winOutput = winMessage
                else:
                    winOutput = ""
                time.sleep(1)
                Screen.winScreenFlicker(winOutput)
        else:
            Screen.winScreenFlicker(winOutput)

        # After screenFlicker is finished, prints out a final winning/losing message that lets the user know how much
        # they won, or wishes them good luck if they lost.

        os.system('cls || clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % "")

        # Check to see if win or loss.
        if didWin:

            # Edge-case scenario where jackpot is greater than 100000
            if winAmount > 100000:
                print(DisplayBlock.DEFAULT % ("You won:"))
                print(DisplayBlock.DEFAULT_HIGHLIGHT % ((Style.HIGHLIGHT + " %2d CREDITS" + Style.DEFAULT) % winAmount))
            else:
                print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                        ("You won:" + Style.HIGHLIGHT + " %2d CREDITS" + Style.DEFAULT) % winAmount))
        else:
            print(DisplayBlock.DEFAULT % winMessage)

        print(DisplayBlock.DEFAULT % "")
        print(DisplayBlock.DIVIDER)
        print(
            DisplayBlock.DEFAULT_HIGHLIGHT % ("Press" + Style.HIGHLIGHT + " [Enter] " + Style.DEFAULT + "to continue."))
        print(DisplayBlock.BORDER)
        input()
        Screen.betOptionsScreen()

    # creditAdd is called by outOfCredits, when the user chooses to add more credits when they don't have enough.
    # creditAdd adds the # of inputted credits to the total credit amount, and also the originalCredit amount
    # in order to not skew the QUIT SCREEN's profit/loss calculations.
    @staticmethod
    def creditAdd():
        global credit, userInput, originalCredit
        os.system('cls || clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % "Please enter # of credits to add.")
        print(DisplayBlock.BORDER)
        userInput = input().strip()

        # Checks to see userInput is valid.
        if userInput.isnumeric():
            userInput = int(userInput)

            # Checks to ensure that the credit amount after the addition won't exceed 10,000.
            # If it does exceed 10,000, calls upon Screen.invalidInput with its own invalid-input code.
            if (credit + userInput) > 10000:
                Screen.invalidInput("CREDITADD_TOOMUCH")
            else:
                credit += userInput
                originalCredit += userInput
        else:
            Screen.invalidInput("CREDITADD")

    @staticmethod
    def outOfCredit():
        global userInput, credit, gameover
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "Not enough Credits!" + Style.DEFAULT))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                "Press " + Style.HIGHLIGHT + "[+]" + Style.DEFAULT + " to add more credits."))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " (by itself)"))
        print(DisplayBlock.DEFAULT % "to try a cheaper bet.")
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % DisplayBlock.Options.QUIT)
        print(DisplayBlock.BORDER)

        userInput = input().upper().strip()
        if userInput.upper() == '+':
            Screen.creditAdd()
        elif userInput.upper() == 'Q':
            gameover = True
            Screen.quitScreen()
        elif userInput.upper() == "":
            Screen.betOptionsScreen()
        else:
            Screen.invalidInput("CREDITOPTIONS")

    @staticmethod
    def slotScreen():
        global credit, betAmount, hold1, hold2, hold3, slots_array, oldSlot
        os.system('cls || clear')
        credit -= betAmount
        for i in range(20):

            # Check for Holds, and ensure that every new animation is a new slot type (No repeat Cherries)
            if not hold1:
                oldSlot = slots_array[0]
                while oldSlot == slots_array[0]:
                    slots_array[0] = random.choice(SLOT_OPTIONS)
            if not hold2:
                oldSlot = slots_array[1]
                while oldSlot == slots_array[1]:
                    slots_array[1] = random.choice(SLOT_OPTIONS)
            if not hold3:
                oldSlot = slots_array[2]
                while oldSlot == slots_array[2]:
                    slots_array[2] = random.choice(SLOT_OPTIONS)

            # To stop flickering, slow down speed
            time.sleep(1 / 3)

            if i > 17:
                # Timer to make the slot machine slow down to a rolling stop.
                time.sleep(((i - 10) ** 0.6) / 3)

            os.system('cls || clear')

            print(DisplayBlock.BORDER)
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
            print(DisplayBlock.BORDER)
            print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
            print(DisplayBlock.BORDER)
            print(DisplayBlock.DEFAULT % "")
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "           SPINNING..." + Style.DEFAULT))
            print(DisplayBlock.DEFAULT % "")
            print(DisplayBlock.DIVIDER)
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.BET_AMOUNT % betAmount))
            print(DisplayBlock.BORDER)

        time.sleep(2)
        winCalculation()

    @staticmethod
    def invalidInput(origin):
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.BORDER)

        # Make Error message more precise for too many holds
        if origin == "3HOLD":
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    "You can only hold " + Style.HIGHLIGHT + "MAX 2 SLOTS" + Style.DEFAULT))
        elif origin == "CREDITADD_TOOMUCH":
            print(DisplayBlock.DEFAULT % ("Max Credit Carrying Capacity is"))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "10,000" + Style.DEFAULT + " CREDITS"))
            print(DisplayBlock.DEFAULT % "Please enter a lower number.")
        else:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "INVALID INPUT" + Style.DEFAULT))

        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to try again."))
        print(DisplayBlock.BORDER)
        input()

        if origin == "BET":
            Screen.betOptionsScreen()
        elif origin == "HOLD" or origin == "3HOLD":
            Screen.holdOptionsScreen()
        elif origin == "CREDITOPTIONS":
            Screen.outOfCredit()
        elif origin == "CREDITADD" or origin == "CREDITADD_TOOMUCH":
            Screen.creditAdd()

    @staticmethod
    def holdOptionsScreen():
        global betAmount, userInput, hold1, hold2, hold3, canHold, slots_array
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.SLOTS % (slots_array[0], slots_array[1], slots_array[2]))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.Options.HOLD_PROMPT)
        print(DisplayBlock.DIVIDER)
        if hold1:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (1, DisplayBlock.Info.HELD_TRUE)))
        else:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (1, DisplayBlock.Info.HELD_FALSE)))
        if hold2:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (2, DisplayBlock.Info.HELD_TRUE)))
        else:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (2, DisplayBlock.Info.HELD_FALSE)))
        if hold3:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (3, DisplayBlock.Info.HELD_TRUE)))
        else:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (3, DisplayBlock.Info.HELD_FALSE)))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.BET_AMOUNT % betAmount))
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to confirm and spin!"))
        print(DisplayBlock.BORDER)

        userInput = input().upper().strip()
        if not userInput.upper() == '1' and not userInput.upper() == '2' and not userInput.upper() == '3' and not userInput.upper() == "":
            Screen.invalidInput("HOLD")
        elif userInput.upper() == '1':
            toggleHold(1)
        elif userInput.upper() == '2':
            toggleHold(2)
        elif userInput.upper() == '3':
            toggleHold(3)
        else:
            if hold1 and hold2 and hold3:
                Screen.invalidInput("3HOLD")
            elif hold1 or hold2 or hold3:
                canHold = False
                Screen.slotScreen()
            else:
                canHold = True
                Screen.slotScreen()

    @staticmethod
    def betOptionsScreen():
        global gameover, betAmount, userInput, hold1, hold2, hold3, canHold, slots_array
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.JACKPOT % jackpot))
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
        userInput = input().upper().strip()
        if userInput.upper() == 'Q':
            gameover = True
            Screen.quitScreen()
        elif userInput in ['1', '2', '5', '10']:
            betAmount = int(userInput)
        else:
            Screen.invalidInput("BET")

        if hold1 or hold2 or hold3 or didWin:
            canHold = False
        else:
            canHold = True

        if credit <= 0 or credit < betAmount:
            Screen.outOfCredit()
        elif canHold:
            hold1 = False
            hold2 = False
            hold3 = False
            Screen.holdOptionsScreen()
        else:
            hold1 = False
            hold2 = False
            hold3 = False
            Screen.slotScreen()

    @staticmethod
    def quitScreen():
        os.system('cls || clear')
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.GAMEOVER.GOODBYE)
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % "STATISTICS:")
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.GAMEOVER.WIN_COUNT % countSpinWin))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.GAMEOVER.LOSE_COUNT % countSpinLoss))
        print(DisplayBlock.BORDER)
        if credit - originalCredit > 0:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    DisplayBlock.GAMEOVER.CREDIT_CHANGE % ("PROFIT", credit - originalCredit)))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "NICE JOB!" + Style.DEFAULT))
        else:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    DisplayBlock.GAMEOVER.CREDIT_CHANGE % ("LOSS", -(credit - originalCredit))))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "BETTER LUCK NEXT TIME!" + Style.DEFAULT))
        print(DisplayBlock.BORDER)
        input()
        exit()


# Ask how many Credits you have today?
userInput = input(
    "As you walk into the Casino, you wonder how much you can afford.\nHow many credits did you bring with you?\n").strip()

while not userInput.lstrip('-').isnumeric():
    os.system('cls || clear')
    userInput = input(
        "That isn't a number! Lets try again, this time just tell me the number of credits you have.\n").strip()

userInput = int(userInput)
if userInput > 10000:
    os.system('cls || clear')
    print(
        "Woah there buddy, you can only carry up to 10,000 credits for safety. Don't want to be robbed or something! I'll let you in with that amount.")
    userInput = 10000
    input("Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to go to the slot machine.")

while userInput <= 5:
    os.system('cls || clear')
    userInput = input(
        "That's a sad amount! I'll give you as many credits you want, on the house!\nJust tell me how many you want:\n").strip()
    while not userInput.isnumeric():
        os.system('cls || clear')
        userInput = input(
            "I need a number, not a story. Just give me the number of your dreams,\nand I'll give you that many!\n").strip()
    userInput = int(userInput)
    if userInput > 10000:
        os.system('cls || clear')
        print(
            "Woah there buddy, don't put me out of business! Since you're being annoying, Ill just give you " + Style.HIGHLIGHT + "100 Credits" + Style.DEFAULT)
        userInput = 100
        input("Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to go to the slot machine.")
credit = userInput
originalCredit = credit

# Print Out Intro
Screen.titleScreen()

# Main Loop
while not gameover:
    Screen.betOptionsScreen()

# Goodbye Message
Screen.quitScreen()
