import random

words = ("python", "java", "swift", "javascript", "go", "kotlin", "php", "rust", "perl", "ruby")
word: str = ...
attempts: int = ...
secret_word: list = ...
win = 0
lose = 0
letters_used = set()


def game():
    global attempts
    global secret_word
    global word
    global win
    global lose
    global letters_used
    while attempts > 0:
        if "".join(secret_word) == word:
            print(f"You guessed the word {word}!")
            break
        print()
        print("".join(secret_word))
        input_letter = input("Input a letter: ")
        if 1 < len(input_letter) or len(input_letter) <= 0:
            print("Please, input a single letter.")
        elif input_letter.isalpha() and input_letter.islower():
            if input_letter in letters_used:
                print("You've already guessed this letter.")
            else:
                if input_letter in word:
                    for i in range(len(word) - 1):
                        if word.find(input_letter, i) != -1:
                            secret_word[word.find(input_letter, i)] = input_letter
                            letters_used.add(input_letter)
                elif input_letter not in word:
                    print("That letter doesn't appear in the word.")
                    attempts -= 1
                    letters_used.add(input_letter)
        else:
            print("Please, enter a lowercase letter from the English alphabet.")
    if attempts > 0:
        print("You survived!")
        win += 1
    else:
        print()
        print("You lost!")
        lose += 1


def menu():
    while True:
        global win
        global lose
        global words
        global word
        global attempts
        global secret_word
        global letters_used
        word = words[random.randint(0, 9)]
        attempts = 8
        secret_word = list("-" * len(word))
        letters_used = set()
        menu_input = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')
        if menu_input == "play":
            game()
        if menu_input == "results":
            print(f"You won: {win} times")
            print(f"You lost: {lose} times")
        if menu_input == "exit":
            quit()


if __name__ == "__main__":
    print("H A N G M A N")
    menu()
