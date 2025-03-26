import random

# List of words
words = ["python", "developer", "hangman", "programming", "interactive", "challenge"]

# Function to choose a random word
def get_word():
    return random.choice(words)  # Ensures a valid word is always chosen

# Function to display the word with guessed letters
def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

# Main function
def play_hangman():
    while True:  # Loop to allow replaying the game
        word = get_word()
        guessed_letters = set()
        attempts = 6  # Number of wrong guesses allowed

        print("\nWelcome to Hangman! Try to guess the word.")

        while attempts > 0:
            print("\n" + display_word(word, guessed_letters))
            print(f"Attempts left: {attempts}")
            guess = input("Guess a letter: ").lower()

            if len(guess) != 1 or not guess.isalpha():
                print("Invalid input. Please enter a single letter.")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter.")
                continue

            guessed_letters.add(guess)

            if guess in word:
                print("Correct!")
                if all(letter in guessed_letters for letter in word):
                    print(f"You won! The word was: {word}")
                    break
            else:
                attempts -= 1  # Deduct attempts on wrong guess
                print("Wrong guess!")

        if attempts == 0:
            print(f"Game over! The word was: {word}")

        # Ask if the player wants to play again
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye!")
            break  # Exit the loop and end the game

# Run the game
if __name__ == "__main__":
    play_hangman()
