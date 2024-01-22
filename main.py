"""
Programmer: Ryan Mehrian
Date Created: December 12, 2023
Last Modified: January
-----
This program is a game emulating a casino's slot machine. The user is prompted with a dialogue where they have the
opportunity to input a number of starting credits on startup. Once the game starts,
they will be given the choice to bet 1, 2, 5, or 10 credits, with each spin having 3 slots with
6 different possibilities (Cherry, Lemon, Lucky 7, Bar, Diamond, and Jackpot). The user will receive a reward
dependent on what combination they roll and the bet inputted. When a player loses, their lost credits accrue
in the jackpot that will be given back to them if the user rolls a jackpot. The user may also choose
to hold 2 out of 3 slots if they do not get a winning combination or haven't held last spin. When the user
runs out of credits, they are given the opportunity to add more credits. When the user decides to Quit the game,
a box will pop up letting them know of their game-statistics (i.e. Wins, Losses, etc.)
"""
# Imports
import os
import random
import time


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
    # Blank, bordered lines. Different fieldwidths to account for Style.Highlight + Style.Default ANSI keycode
    # characters.
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
    class GameOver:
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
gameOver = False
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

    # creditAdd is called by function outOfCredit, when the user chooses to add more credits.
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

    # The function outOfCredit is a screen that appears when the user inputs a bet that they cannot afford.
    # The function brings up a prompt letting the user know they are short on credits, and provides the
    # player with options to add more credits, choose a cheaper bet, or to quit the game.
    @staticmethod
    def outOfCredit():
        global userInput, credit, gameOver
        os.system('cls || clear')

        # Printing out the screen, prompt, and options.
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

        # Take user input
        userInput = input().upper().strip()

        # Checks for user input, and then redirects to relevant screen. If a valid input isn't detected,
        # Screen.invalidInput is called with the error code "CREDITOPTIONS".
        if userInput.upper() == '+':
            Screen.creditAdd()
        elif userInput.upper() == 'Q':
            gameOver = True
            Screen.quitScreen()
        elif userInput.upper() == "":
            Screen.betOptionsScreen()
        else:
            Screen.invalidInput("CREDITOPTIONS")

    # The function slotScreen deals with the spinning of the slot machine.
    # slotScreen randomizes the slots in each printed frame. The frames slow down, then the slot machine
    # comes to a complete stop. The program then waits for 2 second for suspense, followed by the calling of
    # the function winCalculation to continue the program.
    @staticmethod
    def slotScreen():
        global credit, betAmount, hold1, hold2, hold3, slots_array, oldSlot
        os.system('cls || clear')

        # Subtract the user bet from the user credit account
        credit -= betAmount

        # For Loop, dealing with the 20 frames of slot spinning.
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

            # To stop flickering, slow down speed at which the frame refreshes.
            time.sleep(1 / 3)

            # Timer to make the slot machine slow down to a rolling stop towards the end of the spin.
            if i > 17:
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

    # The function invalidInput is a general purpose function that is used to handle unexpected inputs.
    # It takes an origin as its parameter, which is the error code passed down from where it was called.
    # invalidInput then uses this origin error code to decide how to proceed, outputting different error
    # messages as needed and redirecting the user back to the relevant screen.
    @staticmethod
    def invalidInput(origin):
        os.system('cls || clear')

        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Info.CREDIT_COUNT % credit))
        print(DisplayBlock.BORDER)

        # Checks for origin codes that require a specific/constructive error output, and prints out the relevant
        # error. If the origin code does not require a special message, prints out generic "INVALID INPUT" line.
        if origin == "3HOLD":
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    "You can only hold " + Style.HIGHLIGHT + "MAX 2 SLOTS" + Style.DEFAULT))
        elif origin == "CREDITADD_TOOMUCH":
            print(DisplayBlock.DEFAULT % "Max Credit Carrying Capacity is")
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "10,000" + Style.DEFAULT + " CREDITS"))
            print(DisplayBlock.DEFAULT % "Please enter a lower number.")
        else:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "INVALID INPUT" + Style.DEFAULT))
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                "Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to try again."))
        print(DisplayBlock.BORDER)

        # Input to continue
        input()

        # Check the origin code to decide which function/screen to redirect the user back to.
        if origin == "BET":
            Screen.betOptionsScreen()
        elif origin == "HOLD" or origin == "3HOLD":
            Screen.holdOptionsScreen()
        elif origin == "CREDITADD" or origin == "CREDITADD_TOOMUCH":
            Screen.creditAdd()
        else:
            Screen.outOfCredit()

    # The function holdOptionsScreen prints a screen that displays to the user which slots are held and not held,
    # and provides them with prompts to either toggle a hold or to spin the slot machine.
    # holdOptionsScreen calls upon toggleHold and slotScreen to complete the actions described above.
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

        # Check the hold status of slot #1, and displays info accordingly.
        if hold1:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (1, DisplayBlock.Info.HELD_TRUE)))
        else:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (1, DisplayBlock.Info.HELD_FALSE)))

        # Check the hold status of slot #2, and displays info accordingly.
        if hold2:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (2, DisplayBlock.Info.HELD_TRUE)))
        else:
            print(
                DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.Options.HOLD_OPTION % (2, DisplayBlock.Info.HELD_FALSE)))

        # Check the hold status of slot #3, and displays info accordingly.
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

        # Checks user input. If user inputs a slot #, calls upon toggleHold with the slot# as a parameter. If a blank
        # string is inputted, the program calls upon slotScreen and spins, and sets canHold to false if slots are
        # held. The if statement also calls upon invalidInput with 2 different codes in 2 different cases,
        # one for too many held slots, another for an unrecognized input.
        if not userInput.upper() == '1' and not userInput.upper() == '2' and not userInput.upper() == '3' and not userInput.upper() == "":
            Screen.invalidInput("HOLD")
        elif userInput.upper() == '1':
            toggleHold(1)
        elif userInput.upper() == '2':
            toggleHold(2)
        elif userInput.upper() == '3':
            toggleHold(3)
        else:

            # This if block checks to see if there are too many held slots (more than 2), and reports an invalid input
            # with the specific code "3HOLD" using the function invalidInput(). The if block also checks if the user
            # has actually held any slot or if they have spun with all slots free, which then determines if the user
            # canHold on the next bet/spin.
            if hold1 and hold2 and hold3:
                Screen.invalidInput("3HOLD")
            elif hold1 or hold2 or hold3:
                canHold = False
                Screen.slotScreen()
            else:
                canHold = True
                Screen.slotScreen()

    # betOptionsScreen is a screen that allows the user to either input a bet amount, or to quit the game.
    # The function betOptionsScreen() is also the highest-level function, being called directly by a while loop.
    # All other functions except the titleScreen are all called in chains from betOptionsScreen().
    @staticmethod
    def betOptionsScreen():
        global gameOver, betAmount, userInput, hold1, hold2, hold3, canHold, slots_array
        os.system('cls || clear')

        # Print out the screen and detect input
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
        userInput = input().upper().strip()

        # This if block checks to see if the input is either a 'Q' for quit, or a valid bet option, then
        # directs the user to the relevant screen. The betAmount is set to the inputted amount by the user.
        # If no valid input is recognized, the user function invalidInput is called.
        if userInput.upper() == 'Q':
            gameOver = True
            Screen.quitScreen()
        elif userInput in ['1', '2', '5', '10']:
            betAmount = int(userInput)
        else:
            Screen.invalidInput("BET")

        # This if block checks to see if the user should be allowed to hold next spin. If any slot was held,
        # or they won, they cannot hold next spin.
        if hold1 or hold2 or hold3 or didWin:
            canHold = False
        else:
            canHold = True

        # This if block checks to see if the user can afford the bet they want to input. If they cannot, it redirects
        # them to the outOfCredit() screen. The if block also checks if the user can hold: If they can,
        # they are directed to the hold screen. If they cannot hold, they are directed straight into a spin with
        # their inputted bet amount.
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

    # The function quitScreen is called whenever a user decides to quit the game. The function prints out
    # a screen that provides the user with player-statistics.
    @staticmethod
    def quitScreen():
        os.system('cls || clear')

        # Print out the statistics
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % DisplayBlock.GameOver.GOODBYE)
        print(DisplayBlock.BORDER)
        print(DisplayBlock.DEFAULT % "STATISTICS:")
        print(DisplayBlock.DIVIDER)
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.GameOver.WIN_COUNT % countSpinWin))
        print(DisplayBlock.DEFAULT_HIGHLIGHT % (DisplayBlock.GameOver.LOSE_COUNT % countSpinLoss))
        print(DisplayBlock.BORDER)

        # This if block checks if the user has made a profit or a loss, and outputs a statistic and a message
        # accordingly.
        if credit - originalCredit > 0:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    DisplayBlock.GameOver.CREDIT_CHANGE % ("PROFIT", credit - originalCredit)))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "NICE JOB!" + Style.DEFAULT))
        else:
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (
                    DisplayBlock.GameOver.CREDIT_CHANGE % ("LOSS", -(credit - originalCredit))))
            print(DisplayBlock.DEFAULT_HIGHLIGHT % (Style.HIGHLIGHT + "BETTER LUCK NEXT TIME!" + Style.DEFAULT))

        print(DisplayBlock.BORDER)
        input()
        exit()

# -- Startup Sequence --

# Ask how many Credits user has to start with.
userInput = input(
    "As you walk into the Casino, you wonder how much you can afford.\nHow many credits did you bring with you?\n").strip()

# Check to see if user input is a valid number. If it isn't a number, keep asking the user for new inputs.
while not userInput.lstrip('-').isnumeric():
    os.system('cls || clear')
    userInput = input(
        "That isn't a number! Lets try again, this time just tell me the number of credits you have.\n").strip()

userInput = int(userInput)

# Check to see if the user inputted credit is greater than 10,000, and caps their credits at 10,000 along with a
# notifying message. This is done to avoid breaking the program, which has a finite number of allowed digits.
if userInput > 10000:
    os.system('cls || clear')
    print(
        "Woah there buddy, you can only carry up to 10,000 credits for safety. Don't want to be robbed or something! "
        "I'll let you in with that amount.")
    userInput = 10000
    input("Press " + Style.HIGHLIGHT + "[Enter]" + Style.DEFAULT + " to go to the slot machine.")

# Checks to see if the inputted number is less than 5, and asks the user to input a higher number. This is done
# to help player experience, as the game is un-fun if you start at just 5 credits.
while userInput <= 5:
    os.system('cls || clear')
    userInput = input(
        "That's a sad amount! I'll give you as many credits you want, on the house!\nJust tell me how many you want:\n").strip()

    # This while loop checks to see if the user input is numeric. If it isn't, the loop keeps prompting the user to
    # input a number.
    while not userInput.isnumeric():
        os.system('cls || clear')
        userInput = input(
            "I need a number, not a story. Just give me the number of your dreams,\nand I'll give you that many!\n").strip()

    userInput = int(userInput)

    # Check to see if the user inputted credit is greater than 10,000, and caps their credits at 10,000 along with a
    # notifying message. This is done to avoid breaking the program, which has a finite number of allowed digits.
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

# -- Main Loop --
while not gameOver:
    Screen.betOptionsScreen()

#  -- Program Quit Message --
Screen.quitScreen()
