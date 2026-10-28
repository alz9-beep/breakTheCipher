import sys
import string

#takes a cipher text, finds letter frequency, uses letter distributions and guesses PT

if len(sys.argv) <= 1:
    print("No encrypted message given! Enter via command line.")
    return

CipherText = sys.argv[1:]

PlainSigma = string.ascii_lowercase
CipherSigma = string.ascii_uppercase + string.punctuation


CipherFreq = dict()

for letter in CipherText:
    if letter == " ":
        continue
    if letter not in CipherFreq:
        CipherFreq[letter] = 1
    else:
        CipherFreq[letter] += 1

#to narrow 25! to something more manageable, we will use freq pools
#permutations will only be made with letters from the same pool

group1 = [ "e", "t", "a"
