from random import choice
from copy import copy


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
