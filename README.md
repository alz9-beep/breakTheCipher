breakCipher.py:
    Enter cipher text
    Pick a Group Size*
    Get a Guess
    Swap out Characters to Reveal Message
    Print Final Message and Cipher Map

    Enter cipher text:
        Preferred cipher text is one that is encrypted using random simple subsitution
    Pick a Group Size*:
        Groups are our way of shuffling letters within reason. The larger the group size, the more variability and vice versa
        i.e. a group size of 13 has the alphabet split down the middle (frequency wise)
    Get a Guess:
        Starting from the standard frequency order "eta..." we map the cipher text letters to their frequency matching counterparts
        Users can get a new guess, which shuffles letters within their groups and then re-maps the cipher text letters
    Swap out Character to Reveal Message:
        After leaving the randomizing section, users can swap out individual letters with their own guesses to finish the decryption
        Users can enter the work "guesses" to see the previous guesses based on frequency analysis in one table
    Print Final Message and Cipher Map
        Entering -1 in this stage ends the swapping process and prints the final (hopefully plaintext) message to the screen
        The Cipher->Plain text mapping is also printed

makeCipher.py:
    used to randomize a plaintext [a-z+" "]* into [A-Z" "]*

    python3 makeCipher.py -> randomizes sample pt
    python3 makeCipher.py a b c -> randomizes input strings a b c

---

# Assumptions

- The message is encrypted with a simple substitution cipher (each letter always swaps to the same letter).
- The message is in English and typed on one line.
- Only letters A-Z get decrypted. Spaces and punctuation stay the same.
- Lowercase input is turned into uppercase.

# How It Works

1. Count how often each letter shows up in the message.
2. Match the most common letters to the most common English letters (e, t, a, o, ...).
3. Press `r` to shuffle letters within their group for a new guess. Bigger groups = more random.
4. Swap letters by hand until the message makes sense.
5. Enter `-1` to print the final message and letter mapping.