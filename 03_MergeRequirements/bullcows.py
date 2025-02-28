from random import choice
from copy import copy
import argparse


def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        print(prompt)
        res = input()
        if not valid or res in valid:
            return res
        

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    target = choice(words)
    #print(target) #uncomment if you want to see the word to be guessed

    letter_count = {}
    for letter in target:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1

    attempts = 0
    while True:
        attempts += 1
        guess = ask("Input word", words)
        if guess == target:
            return attempts
        else:
            bulls = 0
            cows = 0
            letter_count_cpy = copy(letter_count)
            for i in range(len(target)):
                if guess[i] == target[i]:
                    bulls += 1
                    letter_count_cpy[guess[i]] -= 1
                elif guess[i] in letter_count_cpy and letter_count_cpy[guess[i]] > 0:
                    cows += 1
                    letter_count_cpy[guess[i]] -= 1
            inform("Bulls: {}, Cows: {}", bulls, cows)


parser = argparse.ArgumentParser()
parser.add_argument("wordfile", type=str, help="name of the file with valid words")
parser.add_argument("length", type=int, help="length of the word", default=5, nargs='?')
args = parser.parse_args()

words = []
file = open(args.wordfile, "r")
word = file.readline()
while word:
    word = word[:-1]
    if len(word) == args.length:
        words.append(word)
    word = file.readline()
file.close()

if len(words) == 0:
    print("There are no words with that length in your file")
    exit()

attempts = gameplay(ask, inform, words)
print(f"You won! It took you {attempts} attempts.")
