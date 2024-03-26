import sys
import time
import os.path
import random

class color:
   #escape codes taken from https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
   #how to use escape codes to format what's printed - https://realpython.com/lessons/ansi-escape-sequences/
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   GREENER = '\033[42m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   BLINK = '\033[5m'
   END = '\033[0m'

if len(sys.argv) < 3:
    print(f"Missing command line arguments. Please re-run as 'python {sys.argv[0]} words_file_name number_of_guesses'")
    exit(1)
else:
    filename = sys.argv[1]
    num_guesses = sys.argv[2]

    check_file_exists = os.path.isfile(filename)
    
    if check_file_exists:
        with open(filename, "r") as file:
            words = [newword.strip() for newword in file.readlines()]    
            print(f"Loaded {len(words):,} words, picking one at random...")
            word = random.choice(words)
            file.close()
    else:
        print(f"The words file {sys.argv[1]} doesn't exist or cannot be loaded. Check the file name given is correct and try again")
        exit(1)

    if num_guesses.isdigit() and int(num_guesses) > 0:
        max_guesses = int(num_guesses)
    else:
        print("The number of guesses must be numerical and greater than zero")
        exit(1)
    
    guessed_word = ["*" for _ in word]
    guesses = 0
    guessed = []

    #If optional debug argument is passed, prints the word for testing
    if len(sys.argv) == 4 and sys.argv[3] == "debug":
        print(color.PURPLE + word + color.END)

    start_time = time.time()

    while guesses < max_guesses and "*" in guessed_word:
        print("\n",color.YELLOW, "".join(guessed_word), color.END,"\n")
        print("You have ", color.BOLD, color.GREEN, max_guesses - guesses, color.END, " guesses remaining", sep='')
        

        if len(guessed) > 0:
            guessed.sort()
            print("Your previous guesses are: ", " ".join(guessed))
            print("You have correctly guessed ", color.BLUE, len(word) - guessed_word.count("*"), \
                  color.END, " letters out of ", color.BLUE, len(word), color.END, " so far", sep='')
        
        try:
            guess = input("Enter a letter> ").lower()
        except (EOFError, KeyboardInterrupt):
            print("Thank you for playing. Goodbye")
            exit(1)

        if not guess.isalpha() or len(guess) != 1:
            print(color.RED, "Invalid input - please enter only a single alphabetic character (A to Z)", color.END, sep='')
            continue
        
        if guess in guessed:
            print(color.RED, "You've already tried the letter '", guess, "' before. Please try a new letter", color.END, sep='')
        else:
            guessed.append(guess)

            if guess in word:
                for index, letter in enumerate(word):
                    if letter == guess:
                        guessed_word[index] = guess
            else:
                guesses += 1

    if "*" in guessed_word:
        print(color.RED, "\nHard Luck. The word you were looking for was ", color.UNDERLINE, word, color.END, \
              color.RED, ". What a waste of %.2f" % (time.time() - start_time), " seconds", color.END, "\n", sep='')
    else:
        print(color.GREEN, "\nWell Done. You correctly guessed ", color.UNDERLINE, color.BOLD, word, color.END, \
              color.GREEN, " in %.2f" % (time.time() - start_time), " seconds", color.END, "\n", sep='')
