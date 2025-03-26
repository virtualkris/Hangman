import pygame  # Import pygame for game graphics
import random  # Import random to select a word

# Initialize Pygame
pygame.init()

# 🎨 Define game window settings
WIDTH, HEIGHT = 600, 400  # Screen dimensions
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)  # Text color
GRAY = (200, 200, 200)  # Color for guessed buttons
FONT = pygame.font.Font(None, 40)  # Font for displaying words
BUTTON_FONT = pygame.font.Font(None, 30)  # Font for letter buttons

# 🎮 Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set screen size
pygame.display.set_caption("Hangman Game")  # Set window title

# 📜 List of words to choose from (Now Uppercase)
words = ["PYTHON", "DEVELOPER", "HANGMAN", "PROGRAMMING", "INTERACTIVE", "CHALLENGE"]

# 🎲 Function to randomly select a word
def get_word():
    return random.choice(words)  # Picks a random word from the list

# 🔡 Function to display the word with guessed letters
def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])  # Shows guessed letters, hides others

# 🔘 Function to create letter buttons
def create_buttons():
    buttons = {}
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Use uppercase letters
    x, y = 50, 300  # Starting position for buttons

    for letter in letters:
        buttons[letter] = pygame.Rect(x, y, 30, 30)  # Create a rectangle for each letter button
        x += 35
        if x > WIDTH - 50:  # Move to next row if out of space
            x = 50
            y += 40
    return buttons

# 🔘 Function to draw buttons
def draw_buttons(buttons, guessed_letters):
    for letter, rect in buttons.items():
        color = GRAY if letter in guessed_letters else WHITE  # Gray out guessed letters
        pygame.draw.rect(screen, color, rect, border_radius=5)  # Draw button
        text_surface = BUTTON_FONT.render(letter, True, BLACK)  # Render letter
        screen.blit(text_surface, (rect.x + 10, rect.y + 5))  # Center text on button

# 🕹 Main game function
def play_hangman():
    word = get_word()  # Select a random word
    guessed_letters = set()  # Store guessed letters
    attempts = 6  # Maximum incorrect guesses allowed
    buttons = create_buttons()  # Generate letter buttons
    running = True  # Control game loop

    while running:
        screen.fill(WHITE)  # Fill the screen with white (reset screen)

        # Display the guessed word on the screen
        displayed_text = display_word(word, guessed_letters)
        text_surface = FONT.render(displayed_text, True, BLACK)  # Render the word
        screen.blit(text_surface, (WIDTH // 2 - 100, 100))  # Position the word in the center

        # Draw the letter buttons
        draw_buttons(buttons, guessed_letters)

        # Display the remaining attempts
        attempt_text = FONT.render(f"Attempts left: {attempts}", True, BLACK)
        screen.blit(attempt_text, (WIDTH // 2 - 100, 50))

        # Refresh screen
        pygame.display.flip()
        
        # Handle events (e.g., quitting the game, button clicks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicks close button
                running = False  # Exit game loop
            
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the player clicks the mouse
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                
                for letter, rect in buttons.items():  # Loop through all letter buttons
                    if rect.collidepoint(mouse_pos) and letter not in guessed_letters:  # Check if button is clicked
                        guessed_letters.add(letter)  # Add letter to guessed letters

                        # If the guess is wrong, reduce attempts
                        if letter not in word:
                            attempts -= 1  

                        # Check if player has guessed all letters correctly
                        if all(letter in guessed_letters for letter in word):
                            print(f"You won! The word was: {word}")
                            running = False  # End game loop

                        # Check if player has run out of attempts
                        elif attempts == 0:
                            print(f"Game over! The word was: {word}")
                            running = False  # End game loop

    pygame.quit()  # Quit pygame after the game ends

# Run the game when script is executed
if __name__ == "__main__":
    play_hangman()
