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
RED = (222, 52, 52)  # Attempt indicator color (#de3434)
ORANGE = (251, 179, 22)  # X mark and active level color (#fbb316)
RECT_COLOR = (12, 192, 223)  # Rectangle color for letters (#0cc0df)

# Fonts
FONT = pygame.font.Font(None, 40)  # Font for word display
BUTTON_FONT = pygame.font.Font(None, 30)  # Font for virtual keyboard
LETTER_FONT = pygame.font.Font(None, 50)  # Font for letter display

# 🖥️ Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# 📜 List of words (Uppercase)
words = ["PYTHON", "DEVELOPER", "HANGMAN", "PROGRAMMING", "INTERACTIVE", "CHALLENGE", "SOFTWARE",
         "COMPUTER", "ALGORITHM", "DEBUGGING"]  # Expanded for 10 levels

# Game variables
game_started = False
game_over = False
level = 1
attempts = 4
guessed_letters = set()
selected_word = ""

# 🎮 Draw Play and Play Again buttons
def draw_game_controls():
    global game_started, game_over

    button_color = (71, 185, 112)  # #47b970
    border_color = (12, 192, 223)  # #0cc0df
    text_color = (0, 0, 0)  # Black

    button_x = WIDTH // 2 - 80
    button_y = HEIGHT // 2 + 100
    button_width = 160
    button_height = 50

    ## Determine the text and display indicator
    if not game_started:
        text = "CLICK TO START GAME"
    elif game_over:
        text = "WANT TO PLAY AGAIN?"
    else:
        return  # No button needed mid-game
    
    # 📝 Draw text indicator above the button
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, button_y - 30))  # Centered above button
    screen.blit(text_surface, text_rect)

    # 🟩 Draw the outer border (Thicker border effect)
    pygame.draw.rect(screen, border_color, (button_x - 4, button_y - 4, button_width + 10, button_height + 10), border_radius=10)
    
    # 🟩 Draw the main button (Inner rectangle)
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=8)

    # 📝 Draw button text
    button_text = "PLAY" if not game_started else "PLAY AGAIN"
    button_surface = font.render(button_text, True, text_color)
    button_text_rect = button_surface.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    screen.blit(button_surface, button_text_rect)

# 🖱 Handle Play and Play Again button clicks
def handle_button_click(pos):
    global game_started, game_over, attempts, level, selected_word, guessed_letters

    button_x = WIDTH // 2 - 80
    button_y = HEIGHT // 2 + 100
    button_width = 160
    button_height = 50

    # Check if the mouse click is within the button area
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        game_started = True
        game_over = False
        attempts = 4
        level = 1 if level >= 10 else level + 1  # Reset after 10 levels
        guessed_letters.clear()
        selected_word = random.choice(words)  # Select a new word when restarting

# 🎲 Function to get a random word
def get_word():
    return random.choice(words)

# 🔡 Function to draw word with rectangles instead of underscores
def draw_word(word, guessed_letters):
    if not game_started or game_over:
        return  # Only draw if game is active
    
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
    spacing = 5  # Space between keys

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
    if not game_started or game_over:
        return # Draw the keyboard only if the game is active
    
    for letter, rect in keys.items():
        color = GRAY if letter in guessed_letters else BLUE  # Change color when guessed
        pygame.draw.rect(screen, color, rect, border_radius=5)  # Draw key
        text_surface = BUTTON_FONT.render(letter, True, WHITE)  # Render letter (always white)
        screen.blit(text_surface, (rect.x + 10, rect.y + 5))  # Position text at center

# Function to draw attempt indicators
def draw_attempts(attempts):
    if not game_started or game_over:
        return # Draw attempts only if the game is active
    
    # 📏 Define rectangle positions and sizes
    x_start = WIDTH // 2 - 90  # 📌 Shift to the left for better centering
    y_start = 30  # 📌 Slightly higher for balance
    width, height = 40, 50  # 📏 Updated rectangle size
    spacing = width + 5  # 📏 Adjusted spacing between rectangles

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

# 🔵 Function to draw level indicators
def draw_levels(level):
    if not game_started or game_over:
        return  # Draw levels only if the game is active
    
    x_start = 20  
    y_start = 20  
    radius = 8  
    spacing = 5  

    for i in range(10):  
        row = i % 5  
        col = i // 5  
        color = ORANGE if i < level else GRAY  
        
        x_pos = x_start + col * (radius * 2 + spacing)  
        y_pos = y_start + row * (radius * 2 + spacing)  

        pygame.draw.circle(screen, color, (x_pos, y_pos), radius)
        pygame.draw.circle(screen, BLACK, (x_pos, y_pos), radius, 2)

# 🎮 Main game function
def play_hangman():
    global game_started, game_over
    level = 1  # Start at level 1
    word = get_word()  # Pick a random word
    guessed_letters = set()  # Store guessed letters
    attempts = 4  # Maximum incorrect guesses
    keys = create_virtual_keyboard()  # Generate virtual keyboard
    running = True  # Control game loop

    while running:
        screen.fill(WHITE)  # Reset screen

        # 🔘 Draw game controls (buttons)
        draw_game_controls()

        # 🔤 Display word as rectangles
        draw_word(word, guessed_letters)

        # 🔘 Draw the virtual keyboard
        draw_virtual_keyboard(keys, guessed_letters)

        # 🔢 Draw attempt indicators
        draw_attempts(attempts)
        draw_levels(level)  # Draw level indicators

        # 🔄 Update screen
        pygame.display.flip()

        # 🎭 Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit game
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse clicks
                handle_button_click(event.pos)  # Handle button clicks  
            
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
                if level < 10:
                    level += 1  
                    word = get_word()  
                    guessed_letters.clear()  
                    attempts = 4  
                else:
                    game_over = True  # 🚨 Game over after Level 10! 

            # ☠️ Check loss condition
            if attempts == 0:
                game_over = True  # 🚨 Game over when attempts run out!


    pygame.quit()  # Quit Pygame after game ends

# 🚀 Run the game
if __name__ == "__main__":
    play_hangman()
