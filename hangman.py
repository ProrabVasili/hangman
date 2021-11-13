# Problem Set 2, hangman.py
# Name: Pazyuka Oleg
# Collaborators: -
# Time spent: 4h 55m

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"
salc = string.ascii_lowercase
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set([i for i in secret_word]).issubset(set(letters_guessed))




def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    letters = [i if i in letters_guessed else '_ ' for i in secret_word]
    return ''.join(letters)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    another_letters = [i for i in salc if i not in letters_guessed]
    return ''.join(another_letters)
def minus_guess(inp):
    global guesses_remaining
    if inp not in secret_word:
        if inp in 'aoiue':
            guesses_remaining-=2
        else:
            guesses_remaining-=1
def correct_input(inp):
    global prod, minus_gr
    prod, minus_gr = True, True
    ggw = get_guessed_word(secret_word, letters_guessed)
    if inp not in salc or inp in letters_guessed:
        global warnings_remaining
        warnings_remaining -= 1
        prod = False
        if inp in letters_guessed:
            pred = 'You\'ve already guessed that letter'
        else:
            pred = 'That is not a valid letter'
        if warnings_remaining<0:
            global guesses_remaining
            guesses_remaining  -= 1
            minus_gr = False
            print(f'Oops! {pred}. You have no warnings left:\nSo you lose one guess: {ggw}')
            warnings_remaining = 3
        else:
            print(f'Oops! {pred}. You have {warnings_remaining} warnings left: {ggw}')
        
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.\nYou have {warnings_remaining} warnings left.')
    while True:
        global guesses_remaining, letters_guessed
        if guesses_remaining == 0 or is_word_guessed(secret_word, letters_guessed):
            break
        print(f'-------------\nYou have {guesses_remaining} guesses left.\nAvailable letters: {get_available_letters(letters_guessed)}')
        inp = input('Please guess a letter: ').lower()
        correct_input(inp)
        if prod == True:
            letters_guessed += [inp]
            minus_guess(inp)
            if inp not in secret_word:
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
    if is_word_guessed(secret_word, letters_guessed) == True:
        print(f'------------\nCongratulations, you won! Your total score for this game is: {guesses_remaining*len(set(secret_word))}')
    else:
        print(f'-----------\nSorry, you ran out of guesses. The word was {secret_word}')


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    mwl,owl = [i for i in my_word.replace(' ','')],[i for i in other_word]
    if len(mwl)==len(owl):
        return all([mwl[i]==owl[i] if letters_guessed.count(mwl[i])==1 else False for i in range(len(mwl)) if mwl[i]!='_' ])
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    words = [i for i in wordlist if match_with_gaps(my_word, i)]
    return ' '.join(words) if len(words)>0 else 'No matches found'


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.\nYou have {warnings_remaining} warnings left.\nYou have a hint that you can use after the first guessed letter if you enter "*"')
    while True:
        global letters_guessed, guesses_remaining
        if guesses_remaining == 0 and '*' not in letters_guessed or is_word_guessed(secret_word, letters_guessed):
            break
        elif '*' in letters_guessed and guesses_remaining<=0:
            guesses_remaining = 0
        print(f'-------------\nYou have {guesses_remaining} guesses left.\nAvailable letters: {get_available_letters(letters_guessed)}')
        inp = input('Please guess a letter: ').lower()
        if inp == '*':
            ggw = get_guessed_word(secret_word, letters_guessed)
            if len([i for i in letters_guessed if i in secret_word])==0:
                print('Hint is not yet available!')
            elif "*" in letters_guessed:
                print(f'Oops! You have already used hint')
            else:
                letters_guessed+=['*']
                print(f'Possible word matches are: {show_possible_matches(ggw)}')
        else:
            correct_input(inp)
            if prod == True:
                letters_guessed += [inp]
                minus_guess(inp)
                if inp not in secret_word:
                    print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
                else:
                    print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')
    if "*" not in letters_guessed:
        print(f'-----------\nSorry, you ran out of guesses. The word was {secret_word}')
    else:
        print(f'------------\nCongratulations, you won! Your total score for this game is: {guesses_remaining*len(set(secret_word))}')

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    letters_guessed = []
    guesses_remaining  = 6
    warnings_remaining = 3
    secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    hangman_with_hints(secret_word)
