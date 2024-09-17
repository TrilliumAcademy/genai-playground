#!/usr/bin/env python

import genai.utils
import requests
from rich.console import Console

console = Console()

# The LLM model we wish to use. Try "gpt-3.5-turbo" for faster responses.
LLM_MODEL = "gpt-4o"

# The number of letters in the word to guess.
NUM_LETTERS = 5
# The total number of guesses the AI gets.
MAX_GUESSES = 6

# List of common English words we can use to filter out nonsense guesses.
WORD_LIST_URL = "https://raw.githubusercontent.com/dolph/dictionary/master/ospd.txt"

# System prompt.
SYSTEM_PROMPT = "You are an agent that plays a variant on the game 'Wordle' with the user."

# The initial prompt we send to the AI at the beginning of the game.
INITIAL_PROMPT = f"""We are going to play a variant of the game 'Wordle'. I am thinking of a {NUM_LETTERS}-letter
English word. You have {MAX_GUESSES} guesses to figure out what it is. After each guess, I will tell you
which letters are correct and in the right position, which letters are correct but in the wrong
position, and which letters are not in the word at all. 

You should ONLY return the {NUM_LETTERS}-letter word you are guessing, with no other commentary.

What is your first guess?"""


# Read the word list from WORD_LIST_URL and filter out words that are not NUM_LETTERS long.
def read_word_list():
    with console.status("Downloading word list..."):
        response = requests.get(WORD_LIST_URL, timeout=30)

    wordlist = response.text.splitlines()
    # Filter out words that are not the right length.
    wordlist = [word.lower() for word in wordlist if len(word) == NUM_LETTERS]
    return wordlist


# Get a guess from the AI.
def get_guess(client, messages):
    response = client.chat.completions.create(
        messages=messages,
        model=LLM_MODEL,
    )
    return response.choices[0].message.content


# Process the AI's guess.
def process_guess(word, guess):
    word = word.lower()
    guess = guess.lower()
    if guess == word:
        return ("Correct! You guessed the word.", True)
    else:
        # Figure out which letters are correct, misplaced, and incorrect.
        correct = []
        misplaced = []
        incorrect = []
        for i in range(NUM_LETTERS):
            if guess[i] == word[i]:
                correct.append(guess[i])
            elif guess[i] in word:
                misplaced.append(guess[i])
            else:
                incorrect.append(guess[i])

        # Generate the reply.
        reply = f"I'm sorry, that is not correct. Correct: {correct}, Misplaced: {misplaced}, Incorrect: {incorrect}"
        return (reply, False)


# Main function to play the game.
def play_wordle(client, word):
    # Start out with the initial messages.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INITIAL_PROMPT},
    ]

    # Loop through until we run out of guesses.
    guesses = 0
    while guesses < MAX_GUESSES:
        guess = get_guess(client, messages)
        guesses += 1
        console.print(f":robot: Guess {guesses}/{MAX_GUESSES}: [green]{guess}")

        # Append the AI's guess to the list of messages.
        messages.append(
            {
                "role": "assistant",
                "content": guess,
            }
        )

        # Generate the reply to the AI.
        reply, correct = process_guess(word, guess)
        console.print(f":man: {reply}")
        if correct:
            console.print(f":tada: [green]The AI guessed the correct word in {guesses} guesses!")
            return
        messages.append(
            {
                "role": "user",
                "content": reply,
            }
        )
    console.print(f":sob: [red]The AI did not guess the correct word. The word was '{word}'.")


# Main function called when the program is run.
def main():

    # Get the word list.
    word_list = read_word_list()

    # Initialize the OpenAI client.
    client = genai.utils.setup()

    # Get a word from the user.
    while True:
        word = console.input(f"Enter a {NUM_LETTERS}-letter English word for the AI to guess: ")
        word = word.lower()
        # Check that the word has five letters, and is only letters.
        if len(word) == NUM_LETTERS and word.isalpha() and word in word_list:
            break
        console.print(f"[red]Please enter a {NUM_LETTERS}-letter English word containing only letters.")

    # Play the game.
    play_wordle(client, word)


if __name__ == "__main__":
    main()
