import sys
import string

#takes a cipher text, finds letter frequency, uses letter distributions and guesses PT

#assumes cipher text is letters, spaces and punctuation. Lowercase is also converted to uppercase
CipherText = input("Enter cipher text: ").upper()

if CipherText.strip() == "":
    print("No encrypted message given!")
    sys.exit()

PlainSigma = string.ascii_lowercase
CipherSigma = string.ascii_uppercase

CipherFreq = dict()

#only A-Z are counted, spaces and punctuation are skipped
for letter in CipherText:
    if letter not in string.ascii_uppercase:
        continue
    if letter not in CipherFreq:
        CipherFreq[letter] = 1
    else:
        CipherFreq[letter] += 1

#to narrow 25! to something more manageable, we will use freq pools
#permutations will only be made with letters from the same pool

#groups follow english letter frequency order from most common to least
group1 = [ "e", "t", "a" ]
group2 = [ "o", "i", "n" ]
group3 = [ "s", "h", "r" ]
group4 = [ "d", "l", "c" ]
group5 = [ "u", "m", "w" ]
group6 = [ "f", "g", "y" ]
group7 = [ "p", "b", "v" ]
group8 = [ "k", "j", "x" ]
group9 = [ "q", "z" ]

