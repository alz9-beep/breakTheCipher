import random
import sys

import string


PlainText = []
if len(sys.argv) <= 1:
    PlainText = ["test", "sentence", "of", "plain", "text"] 
    print(sys.argv[0:])
    print(len(sys.argv))
    
else:
    PlainText = sys.argv[1:]



uppercase_letters = string.ascii_uppercase
lowercase_letters = string.ascii_lowercase
punctuation_chars = string.punctuation

cipher_sigma = uppercase_letters + punctuation_chars

plaintext_sigma = lowercase_letters

def randomIndGen(n):
	return random.randint(1, n) - 1

def countingArr(size): #this is created to hold valid swappable character indices
	ret = []
	for i in range(size):
		ret.append(i)	
	return ret

def randomizedPlainText(pt): #pt elements
	random_chars = string.ascii_uppercase + string.punctuation
	index_pool = countingArr(len(random_chars))
	pt_len = len(pt)
	
	for i in range(pt_len):
		pool_depth = len(index_pool)
		randInd = randomIndGen(pool_depth)
		pt[i] = index_pool.pop(randInd)
	return pt

def cipherConvert(arr):
	random_txt = string.ascii_uppercase + string.punctuation
	length = len(random_txt)
	arr_length = len(arr)
	key = dict()
	for i in range(arr_length):
		key[itoa(i)] = random_txt[arr[i]]
	return key 

def itoa(x):
	if x > 25 or x < 0:
		return "nah"
	lowercase = list(string.ascii_lowercase)
	return lowercase[x]

def parseMessageArr(arr_of_str):
	space = " "
	message = space.join(arr_of_str)
	return message

def PtToCt(message, key):
	ret = ""
	message_len = len(message)
	for i in range(message_len):
		if message[i] == " ":
			ret += " "
			continue
		if message[i] in key:
			ret += key[message[i]]
		else:
			print("invalid char", message[i])
	return ret 
			 

	
arr = randomizedPlainText(list(string.ascii_lowercase))
#print("randomized Plain Text:", arr)

cipher_key = cipherConvert(arr)

for key, value in cipher_key.items():
	print("key: ", key, " val: ", value)
#print(PlainText)
print(PlainText)
message = parseMessageArr(PlainText)
print(message)

cipher_text = PtToCt(message, cipher_key)
print(cipher_text)

