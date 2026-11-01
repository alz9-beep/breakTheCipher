import os
import sys
import string
import random
from collections import Counter


def printDict(dictionary):
    for key, val in dictionary.items():
        print("key:", key, "\tval:", val)


# Count uppercase letter frequencies in the ciphertext.
def getFrequencies(cipherText: str) -> dict:
    return dict(Counter(
        letter for letter in cipherText
        if letter in string.ascii_uppercase
    ))


# Dynamically build groups based on the requested group size. We should recommend a size based on testing !!
def buildGroups(alphabetFreq: list, groupSize: int) -> list:
    groups = []

    for i in range(0, len(alphabetFreq), groupSize):
        groups.append(alphabetFreq[i:i + groupSize])

    return groups


# Combine frequency groups into one list. Double for loop; the first "letter" appends the current char to the returned list
def listConcat(groups: list) -> list:
    return [letter for group in groups for letter in group]


# Randomize letters within each group.
# Do not modify the original groups.
def shuffleGroups(groups: list) -> list:
    shuffledGroups = []

    for group in groups:
        newGroup = group.copy()
        random.shuffle(newGroup)
        shuffledGroups.append(newGroup)

    return shuffledGroups


# Map ciphertext letters to English letters by frequency.
def cipherEngFreqMap(cipherFreq: dict, alphabetFreq: list) -> dict:
    cipherEngMap = {}

    # key=lambda lets us store each letter and its corresponding frequency
    # The negative sign pushes higher frequency letters to the front of the sorted dictionary
    sortedCipherLetters = sorted(cipherFreq, key=lambda letter: (-cipherFreq[letter], letter))
    
    # Since the dictionary and alphabetFreq list are sorted, we line them up with zip() and add entry pairs X->x to cipherEngMap
    for cipherLetter, plainLetter in zip(sortedCipherLetters, alphabetFreq):
        cipherEngMap[cipherLetter] = plainLetter

    return cipherEngMap


# Generate plaintext guess from the original ciphertext.
def freqMap(cipherEngMap: dict, cipherText: str) -> str:
    freqGuess = ""

    for letter in cipherText:
        if letter in string.ascii_uppercase:
            freqGuess += cipherEngMap.get(letter, letter)
        else:
            freqGuess += letter

    return freqGuess


# Swap plaintext letter assignments in the cipher mapping.
def swapLetters(cipherEngMap: dict, oldLetter: str, newLetter: str) -> bool:

    if oldLetter == newLetter:
        print("Both letters are the same. No change made.")
        return False

    oldCipherLetter = None
    newCipherLetter = None
    
    for cipherLetter, plainLetter in cipherEngMap.items():
        if plainLetter == oldLetter:
            oldCipherLetter = cipherLetter

        if plainLetter == newLetter:
            newCipherLetter = cipherLetter

    if oldCipherLetter is None:
        print(oldLetter, "is not in the current mapping.")
        return False
    if newCipherLetter is None:
        cipherEngMap[oldCipherLetter] = newLetter
    # If the swap is with a letter that is already mapped, the plaintext letters get their cipherLetters swapped
    else:
        cipherEngMap[oldCipherLetter] = newLetter
        cipherEngMap[newCipherLetter] = oldLetter

    return True

def printGuesses(history: list):
    for count, guess in enumerate(history):
        print(count + 1, ": ", guess)


def printMapping(cipherEngMap: dict):
    print("\nCurrent cipher-to-plaintext mapping:")

    for cipherLetter in sorted(cipherEngMap):
        print(cipherLetter, "->", cipherEngMap[cipherLetter])

    print()


def printGroups(groups: list):
    print("\nCurrent frequency groups:")

    for i, group in enumerate(groups, start=1):
        print("Group", i, ":", " ".join(group))

    print()


def getGroupSize() -> int:
    while True:
        userInput = input("\nEnter frequency group size (1-26): ").strip()

        try:
            groupSize = int(userInput)

            if 1 <= groupSize <= 26:
                return groupSize

            print("Group size must be between 1 and 26.")

        except ValueError:
            print("Please enter a valid integer.")

def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    CipherText = input("Enter cipher text: ").upper()

    if CipherText.strip() == "":
        print("No encrypted message given!")
        sys.exit()

    CipherFreq = getFrequencies(CipherText)

    if not CipherFreq:
        print("Ciphertext contains no alphabetic characters!")
        sys.exit()

    # English letter frequency order, highest to lowest.
    alphabetFreq = list("etaoinshrdlcumwfgypbvkjxqz")

    # Build groups 
    groupSize = getGroupSize()

    group_bucket = buildGroups(alphabetFreq, groupSize)

    printGroups(group_bucket)

    # Create initial mapping and plaintext guess.
    cipherEngMap = cipherEngFreqMap(CipherFreq, alphabetFreq)

    newGuess = freqMap(cipherEngMap, CipherText)
    history = [newGuess]

    print("\nGuess using frequency analysis:")
    print(newGuess)
    input("\nPress enter to continue\n")

    # Re-Randomize/shuffle groups, change frequency group size or go to letter swapping
    while True:
        choice = input("\nEnter 'r' to try another guess, \n'g' to change group size,"
                       "\n'guesses' to view previous random guesses""\nor anything else to continue to swapping:\n").strip().lower()

        if choice == "g":
            groupSize = getGroupSize()
            group_bucket = buildGroups(alphabetFreq, groupSize)
            printGroups(group_bucket)
            continue
        
        if choice == "guesses":
            printGuesses(history)
            continue

        if choice != "r":
            break

        shuffledGroups = shuffleGroups(group_bucket)
        newAlphabetFreq = listConcat(shuffledGroups)

        cipherEngMap = cipherEngFreqMap(CipherFreq, newAlphabetFreq)

        newGuess = freqMap(cipherEngMap, CipherText)

        history.append(newGuess)
		
        clearTerminal()

        print("\nNew guess using frequency analysis:")
        print(newGuess)


    # Manual letter swapping
    print("\nEntering manual letter swapping mode.")
    print("Enter two lowercase plaintext letters to swap.")
    print("Enter '-1' to finish.")
    print("Enter 'map' to display the current mapping.")

    while True:
        originalLetter = input("\nEnter a symbol to swap, 'map', 'guesses', or -1 to end:\n").strip().lower()

        if originalLetter == "-1":
            break

        if originalLetter == "map":
            printMapping(cipherEngMap)
            input("\npress enter to go back to swap")
            continue
        if originalLetter == "guesses":
            printGuesses(history)
            input("\npress enter to go back to swap")
            continue

        if (len(originalLetter) != 1 or originalLetter not in string.ascii_lowercase):
            print("Please enter a single lowercase letter.")
            continue

        newLetter = input("Enter the new symbol:\n").strip().lower()

        if (len(newLetter) != 1 or newLetter not in string.ascii_lowercase):
            print("Please enter a single lowercase letter.")
            continue

        success = swapLetters(cipherEngMap, originalLetter, newLetter)

        if not success:
            continue

        newGuess = freqMap(cipherEngMap, CipherText)
        clearTerminal()

        print("\nNew Guess:")
        print(newGuess)

    print("\nFinal Guess:")
    print(newGuess)
    print("\nFinal Cipher->Plain Text Mapping:")
    printMapping(cipherEngMap)


if __name__ == "__main__":
    main()

