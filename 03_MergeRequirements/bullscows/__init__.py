import os
import sys
import urllib.request
import random as r

import textdistance as td


__all__ = ["bullscows", "gameplay"]


def bullscows(guess, secret):
    bulls = td.hamming.similarity(guess, secret)
    cows = td.bag.similarity(guess, secret) - bulls
    return bulls, cows


def gameplay(ask_f, inform_f, words):
    secret = r.choice(words)

    attempts = 0
    correct_guess = False
    while not correct_guess:
        guess = ask_f("Введите слово: ", words)
        attempts += 1

        b, c = bullscows(guess, secret)
        inform_f("Быки: {}, Коровы: {}", b, c)

        if guess == secret:
            correct_guess = True

    return attempts


def ask(prompt, valid):
    while True:
        print(prompt, end="")
        guess = input()

        if (valid is not None) and (guess not in valid):
            continue
        return guess


def inform(format_string, bulls, cows):
    print(format_string.format(bulls, cows))


def main():
    filename = sys.argv[1]
    if os.path.isfile(filename):
        with open(filename) as file:
            lines = [line.rstrip() for line in file]
    else:
        with urllib.request.urlopen(filename) as response:
            html_response = response.read()
            lines = html_response.decode('utf8').split()

    if len(sys.argv) > 2:
        length = int(sys.argv[2])
        lines = list(filter(lambda x: len(x) == length, lines))

    print(f"Количество попыток: {gameplay(ask, inform, lines)}")
