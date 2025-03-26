import pygame  # Import pygame for UI
import random  # Import random for word selection

# Initialize Pygame
pygame.init()

# 🎨 Define screen settings
WIDTH, HEIGHT = 600, 450  # Adjusted height for better keyboard spacing
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)  # Text color
BLUE = (65, 120, 189)  # Default key color (#4178bd)
GRAY = (217, 217, 217)  # Guessed key color (#d9d9d9)
RED = (222, 52, 52)  
ORANGE = (251, 179, 22)
RECT_COLOR = (12, 192, 223)  # Rectangle color for letters (#0cc0df)

# Fonts
FONT = pygame.font.Font(None, 40)  # Font for word display
BUTTON_FONT = pygame.font.Font(None, 30)  # Font for virtual keyboard
LETTER_FONT = pygame.font.Font(None, 50)  # Font for letter display

# 🖥️ Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# 📜 List of words (Uppercase)
words = ["PYTHON", "DEVELOPER", "HANGMAN", "PROGRAMMING", "INTERACTIVE", "CHALLENGE"]

# 🎲 Function to get a random word
def get_word():
    return random.choice(words)

# 🔡 Function to draw word with rectangles instead of underscores
def draw_word(word, guessed_letters):
    x_start = WIDTH // 2 - (len(word) * 45) // 2  # Centering logic
    y_start = 150  
    cell_size = 40  

    for i, letter in enumerate(word):
        rect_x = x_start + i * (cell_size + 5)  # Space between letters
        pygame.draw.rect(screen, RECT_COLOR, (rect_x, y_start, cell_size, cell_size), border_radius=5)

        if letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, BLACK)
            screen.blit(text_surface, (rect_x + 10, y_start + 5))

# ⌨️ Function to create a **QWERTY-based virtual keyboard**
def create_virtual_keyboard():
    keys = {}
    layout = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ]  # QWERTY keyboard rows

    x_start = 80  # Start position for first row
    y_start = 300  # Start position for the keyboard
    key_width, key_height = 40, 40  # Key dimensions
    spacing = 10  # Space between keys

    for row in layout:
        x = x_start
        for letter in row:
            keys[letter] = pygame.Rect(x, y_start, key_width, key_height)  # Create button rectangles
            x += key_width + spacing  # Move right for next key
        y_start += key_height + spacing  # Move down for next row
        x_start += 20  # Indent next row like a real keyboard

    return keys

# ⌨️ Function to draw the virtual keyboard
def draw_virtual_keyboard(keys, guessed_letters):
    for letter, rect in keys.items():
        color = GRAY if letter in guessed_letters else BLUE  # Change color when guessed
        pygame.draw.rect(screen, color, rect, border_radius=5)  # Draw key
        text_surface = BUTTON_FONT.render(letter, True, WHITE)  # Render letter (always white)
        screen.blit(text_surface, (rect.x + 10, rect.y + 5))  # Position text at center

# Function to draw attempt indicators
def draw_attempts(attempts):
    x_start = WIDTH // 2 - 90  # 📌 Shift to the left for better centering
    y_start = 30  # 📌 Slightly higher for balance
    width, height = 40, 50  # 📏 Updated rectangle size

    spacing = width + 15  # 📏 Adjusted spacing between rectangles

    # 🎨 Define X mark font
    X_FONT = pygame.font.Font(None, 45)  # Slightly larger X

    # 🔄 Loop through 4 attempt slots
    for i in range(4):
        pygame.draw.rect(screen, RED, 
                         (x_start + (i * spacing), y_start, width, height), 
                         border_radius=5)  # 🟥 Keep all rectangles red

    # ❌ Display X marks over the rectangles for every wrong attempt
    wrong_attempts = 4 - attempts  # 🔢 How many mistakes were made?

    for i in range(wrong_attempts):  
        x_pos = x_start + (i * spacing) + 7  # 📌 Adjust X position for centering
        y_pos = y_start + 10  # 📌 Center X within the rectangle
        text_surface = X_FONT.render("X", True, ORANGE)  # 🎨 X in #fbb316
        screen.blit(text_surface, (x_pos, y_pos))  # 🖥️ Display X mark

# 🎮 Main game function
def play_hangman():
    word = get_word()  # Pick a random word
    guessed_letters = set()  # Store guessed letters
    attempts = 4  # Maximum incorrect guesses
    keys = create_virtual_keyboard()  # Generate virtual keyboard
    running = True  # Control game loop

    while running:
        screen.fill(WHITE)  # Reset screen

        # 🔤 Display word as rectangles
        draw_word(word, guessed_letters)

        # 🔘 Draw the virtual keyboard
        draw_virtual_keyboard(keys, guessed_letters)

        # 🔢 Draw attempt indicators
        draw_attempts(attempts)

        # 🔄 Update screen
        pygame.display.flip()

        # 🎭 Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game
                running = False  
            
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse clicks
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                for letter, rect in keys.items():  # Check all keys
                    if rect.collidepoint(mouse_pos):  # If clicked
                        if letter not in guessed_letters:
                            guessed_letters.add(letter)  # Mark as guessed
                            if letter not in word:
                                attempts -= 1  # Wrong guess

            elif event.type == pygame.KEYDOWN:  # Detect physical keyboard input
                guess = event.unicode.upper()  # Convert to uppercase
                if guess in keys and guess not in guessed_letters:  # Valid letter
                    guessed_letters.add(guess)  # Mark as guessed
                    if guess not in word:
                        attempts -= 1  # Wrong guess

            # 🏆 Check win condition
            if all(letter in guessed_letters for letter in word):
                print(f"You won! The word was: {word}")
                running = False  

            # ☠️ Check loss condition
            if attempts == 0:
                print(f"Game over! The word was: {word}")
                running = False  

    pygame.quit()  # Quit Pygame after game ends

# 🚀 Run the game
if __name__ == "__main__":
    play_hangman()
