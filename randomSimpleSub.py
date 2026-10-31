import sys
import string
import random


def printDict(dictionary):
    for key,val in dictionary.items():
        print("key: ", key, "\tval: ", val ,"\n")

#takes a cipher text, finds letter frequency, uses letter distributions and guesses PT

def freqDictToList(freqDict) -> list:
    frequencies = []
    for value in freqDict.values():
        frequencies.append(value)
    return sorted(frequencies)


#to narrow 25! to something more manageable, we will use freq pools
#permutations will only be made with letters from the same pool

def counter(num):
    ret = []
    for i in range(num):
        ret.append(i)
    return ret

#groups follow english letter frequency order from most common to least

def shuffle(group):
    mini_list = group.copy() 
    shuffled = []

    while len(mini_list) > 0:
        test = random.randint(0, len(mini_list) - 1)
        shuffled.append(mini_list.pop(test))

    return shuffled


def listConcat(groups):
   ret = []
   for i in range(0, len(groups)):
       ret += groups[i]
   return ret

def flipped(list) -> list:
    revList = []
    for item in reversed(list):
        revList.append(item)
    return revList

#first version sorts the frequencies creates the cipher/englishFrequency map

def cipherEngFreqMap(cipherMap: dict, frequencies: list, alphaList: list) -> dict:
    cipherEngMap = dict()

    #frequencies are sorted, frequencies[len - 1] checks the current highest frequency
    #since we are popping the alphabetFreq, we will keep a reversed order
    revAlphabetFreq = flipped(alphaList)
    while True:
        for key, val in cipherMap.items():
            freq_length = len(frequencies)
            alpha_length = len(revAlphabetFreq)
            if freq_length <= 0 or alpha_length <= 0:
                break
        
            if val == frequencies[freq_length - 1]:
                cipherEngMap[key] = revAlphabetFreq.pop()
                frequencies.pop()
        if freq_length <= 0 or alpha_length <= 0:
            break
    return cipherEngMap

def freqMap(cipherEngFreqDict, cText):
    freqGuess = ""
    for letter in cText:
        if letter not in CipherSigma:
            freqGuess += letter
            continue
        if letter in cipherEngFreqDict:
            freqGuess += cipherEngFreqDict[letter]
            continue
        print( letter + " not found in cipher frequency dictionary\n")
        return
    return freqGuess

def swapLetter(originalLetter, newLetter, cText):
    
    newCText = ""
    for letter in cText:
        if letter == originalLetter:
            newCText += newLetter
        else:
            newCText += letter
    return newCText
#only A-Z are counted, spaces and punctuation are skipped
def getFrequencies(cipherText: str):
    CipherFreq = dict()
    for letter in CipherText:
        if letter not in string.ascii_uppercase:
            continue
        if letter not in CipherFreq:
            CipherFreq[letter] = 1
        else:
            CipherFreq[letter] += 1
    return CipherFreq



#assumes cipher text is letters, spaces and punctuation. Lowercase is also converted to uppercase
CipherText = input("Enter cipher text: ").upper()

if CipherText.strip() == "":
    print("No encrypted message given!")
    sys.exit()

PlainSigma = string.ascii_lowercase
CipherSigma = string.ascii_uppercase


CipherFreq = getFrequencies(CipherText)
#print("cipher freq:\n")
#printDict(CipherFreq)


frequencyList = freqDictToList(CipherFreq)

group1 = [ "e", "t", "a" ]
group2 = [ "o", "i", "n" ]
group3 = [ "s", "h", "r" ]
group4 = [ "d", "l", "c" ]
group5 = [ "u", "m", "w" ]
group6 = [ "f", "g", "y" ]
group7 = [ "p", "b", "v" ]
group8 = [ "k", "j", "x" ]
group9 = [ "q", "z" ]


group_bucket = [group1, group2, group3, group4, group5, group6, group7, group8, group9] 
def printGroups(groupBucket):
    i = 0
    for group in groupBucket:
        print("group ", i)
        for letter in group:
            print(letter + " ")
        print("\n")
        i += 1
#printGroups(group_bucket)
alphabetFreq = listConcat(group_bucket) 


cipherEngMap = cipherEngFreqMap(CipherFreq, frequencyList, alphabetFreq)
#print("cipher eng map:\n")
#printDict(cipherEngMap)


#need a shuffle function for the group arrs, will start assuming the default frequencies are correct
guessedPlainText = freqMap(cipherEngMap, CipherText)

print("Guess using frequency analysis:\n", guessedPlainText, "\n", )

while True:
    choice = input("Enter 'r' to try another guess, anything else to continue to letter swap\n\n\n")
    if choice != 'r':
        break
    group_bucket_copy = group_bucket.copy()
    for i in range(len(group_bucket_copy)):
        shuffled_group = shuffle(group_bucket_copy[i])
        group_bucket_copy[i] = shuffled_group
    #printGroups(group_bucket_copy)
    newList = listConcat(group_bucket_copy)
    CipherFreq = getFrequencies(CipherText)
    frequencyList = freqDictToList(CipherFreq)
    #print("cipherfreq: ", printDict(CipherFreq), "\nFrequency List: ", frequencyList)
    cipherEngMap = cipherEngFreqMap(CipherFreq, frequencyList, newList)
    #printDict(cipherEngMap)
    newGuess = freqMap(cipherEngMap, CipherText)
    
    print("\n\n\nNew guess using frequency analysis:\n", newGuess, "\n")



while True:
    
    originalLetter = input("Enter a symbol to swap, -1 to end:\n")
    if originalLetter == "-1":
        break
    else:
        print("entered:" + originalLetter)
    if originalLetter not in PlainSigma:
        print("symbol not lowercase:", originalLetter)
        continue

    newLetter = input("Enter the new symbol:\n")
    
    if newLetter in CipherText:
        choice = input("Warning: since ", newLetter, " is already in the cipher text, swapping this letter will increase the amount of ", newLetter, "'s! press y to continue\n")
        if choice != "y":
            break 
    newGuess = swapLetter(originalLetter, newLetter, newGuess)
    print("New Guess: \n", newGuess, "\n")

print("Final Guess: \n", newGuess, "\n")

#NOTES:
#the current program only swaps with the preset most frequency english letters, needs the following addressed:

#1. Add a function to mix AlphabetFreq by manipulating the group lists before adding them

#2. When the previous function is done, we have to present the user with candidates to begin the swapping process from, with an option to further randomize
#this can start as a single randomize option

#3. When swapping letters after the first mapping, we need to distinguish letters from each other
#for example, if the user swaps all the b's in the previous guess with a's, but a's already existed in the previous guess,
#the pool of a's will grow, merging what should be distinguished letter groups  (m, n -> o instead of m->o, n->p)
