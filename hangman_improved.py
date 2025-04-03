import pygame  # Import pygame for UI
import random  # Import random for word selection
import sys

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

# 🎨 Difficulty Button Colors
EASY_COLOR = (71, 185, 112)  # Green (#47b970)
NORMAL_COLOR = (12, 192, 223)  # Cyan (#0cc0df)
MEDIUM_COLOR = (251, 179, 22)  # Orange (#fbb316)
HARD_COLOR = (222, 52, 52)  # Red (#de3434)

# Fonts
FONT = pygame.font.Font(None, 40)  # Font for word display
BUTTON_FONT = pygame.font.Font(None, 30)  # Font for virtual keyboard
LETTER_FONT = pygame.font.Font(None, 50)  # Font for letter display

# 🖥️ Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# 📜 Word Lists by Difficulty
words_by_difficulty = {
    "Easy": ["DESIGN", "COLOR", "SHAPE", "LOGO", "IMAGE", "PIXEL", "LAYER", "BRUSH", "TEXTURE", "VECTOR"],
    "Normal": ["NETWORK", "CODING", "DATABASE", "SECURITY", "ALGORITHM", "HARDWARE", "SOFTWARE", "ANALYSIS", "SERVERS", "VIRTUAL"],
    "Medium": ["MOTION", "RENDER", "LIGHTING", "GRAPHICS", "FRAMERATE", "MODEL", "ANIMATION", "KEYFRAME", "RIGGING", "TEXTURING"],
    "Hard": ["JAVASCRIPT", "PYTHON", "PROGRAMMER", "DEBUGGING", "FRAMEWORK", "BACKEND", "FRONTEND", "ALGORITHMS", "COMPILER", "RECURSION"]
}

# Game variables
game_started = False # Game state
game_over = False # Game over state
level_completed = False # Level completion state
difficulty_selected = False # Difficulty state
level = 0 # Current level
attempts = 4 # Number of attempts
guessed_letters = set() # Set to store guessed letters
selected_word = "" # Word to guess
selected_difficulty = "" # Selected difficulty

# Load Sounds
correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong-2.mp3")
warning_sound = pygame.mixer.Sound("warning.mp3")

# 🎮 Draw Play and Play Again buttons
def draw_game_controls():
    global game_started, game_over, level_completed

    button_color = (71, 185, 112)  # #47b970
    border_color = (12, 192, 223)  # #0cc0df
    quit_button_color = (255, 0, 0)  # Red color for quit button (no border)
    text_color = (0, 0, 0)  # Black

    button_x = WIDTH // 2 - 80
    button_y = HEIGHT // 2 - 100  # Adjust the starting Y for the first button
    button_width = 160
    button_height = 50

    # Initialize quit_button_y in case of game over or completion of 10 levels
    quit_button_y = None

    # Determine the text and display indicator
    if not game_started:
        text = "CLICK TO START GAME"
    elif game_over:
        text = "GAME OVER! WANT TO PLAY AGAIN?"
        quit_button_y = button_y + button_height + 10  # Position the quit button below the play again button
    elif level_completed:  # If game completed 10 levels, show the congratulatory message
        text = "CONGRATULATIONS! YOU COMPLETED 10 LEVELS!"
        quit_button_y = button_y + button_height + 10  # Position the quit button below the play again button
    else:
        return None, None  # No button needed mid-game
    
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

    # 🟥 Draw the QUIT button (Red button, no border)
    quit_button_rect = None
    if quit_button_y is not None:  # Ensure quit_button_y is not None before drawing
        pygame.draw.rect(screen, quit_button_color, (button_x, quit_button_y, button_width, button_height), border_radius=8)
        
        # 📝 Draw "QUIT" button text
        quit_button_text = "QUIT"
        quit_button_surface = font.render(quit_button_text, True, text_color)
        quit_button_text_rect = quit_button_surface.get_rect(center=(WIDTH // 2, quit_button_y + button_height // 2))
        screen.blit(quit_button_surface, quit_button_text_rect)

        # Create quit button rectangle for collision detection
        quit_button_rect = pygame.Rect(button_x, quit_button_y, button_width, button_height)

    # ✅ Return both button rectangles
    return pygame.Rect(button_x, button_y, button_width, button_height), quit_button_rect

# 🎮 Draw Difficulty Buttons (Stacked)
def draw_difficulty_buttons():
    global difficulty_selected

    y_start = HEIGHT // 2 - 60 # Centered vertically
    button_width = 180 # Width of the buttons
    button_height = 40 # Height of the buttons
    spacing = 5

    difficulties = ["Easy", "Normal", "Medium", "Hard"]
    colors = [EASY_COLOR, NORMAL_COLOR, MEDIUM_COLOR, HARD_COLOR]
    button_rects = {}

    title_font = pygame.font.Font(None, 35)
    title_text = title_font.render("CHOOSE DIFFICULTY", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - 100, y_start - 50))

    for i, difficulty in enumerate(difficulties):
        button_x = WIDTH // 2 - button_width // 2  # Centered horizontally
        button_y = y_start + (i * (button_height + spacing)) # Centered vertically
        pygame.draw.rect(screen, colors[i], (button_x, button_y, button_width, button_height), border_radius=8)

        text_surface = BUTTON_FONT.render(difficulty, True, BLACK)
        text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text_surface, text_rect)

        button_rects[difficulty] = pygame.Rect(button_x, button_y, button_width, button_height)

    return button_rects

# Function to get a random word based on difficulty
def get_word(difficulty):
    return random.choice(words_by_difficulty[difficulty])

# Function to handle Play, Play Again, and Difficulty buttons
def handle_button_click(pos):
    global game_started, game_over, attempts, level, selected_word, guessed_letters
    global selected_difficulty, difficulty_selected

    button_x = WIDTH // 2 - 80  # Centered button
    button_y = HEIGHT // 2 + -100 # Centered button
    button_width = 160
    button_height = 50

    # Check if the Play or Play Again button is clicked
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        game_started = True
        game_over = False
        attempts = 4
        level = 1 if level >= 10 else level + 1  # Reset after 10 levels
        guessed_letters.clear()
        difficulty_selected = False  # Reset difficulty selection on a new game
        return  # Exit to avoid checking difficulty buttons immediately

    # Check if a difficulty button is clicked after starting the game
    if game_started and not difficulty_selected:
        difficulty_buttons = draw_difficulty_buttons()
        for difficulty, rect in difficulty_buttons.items():
            if rect.collidepoint(pos):
                selected_difficulty = difficulty
                selected_word = get_word(difficulty)  # Get word based on difficulty
                difficulty_selected = True
                return

# 🔡 Function to draw word with rectangles instead of underscores
def draw_word(selected_word, guessed_letters):
    if not game_started or game_over or not difficulty_selected:
        return  # Only draw if game is active and difficulty is selected 

    x_start = WIDTH // 2 - (len(selected_word) * 45) // 2  # Centering logic
    y_start = 150  
    cell_size = 40  

    for i, letter in enumerate(selected_word): 
        rect_x = x_start + i * (cell_size + 5)  # Space between letters
        pygame.draw.rect(screen, RECT_COLOR, (rect_x, y_start, cell_size, cell_size), border_radius=5)

        if letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, WHITE)
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, y_start + cell_size // 2))
            screen.blit(text_surface, text_rect)

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
        text_surface = BUTTON_FONT.render(letter, True, BLACK)  # Render letter (always white)
        screen.blit(text_surface, (rect.x + 10, rect.y + 5))  # Position text at center

# Function to draw attempt indicators
def draw_attempts(attempts):
    global warning_sound # Load warning sound

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

def show_word_flash(screen, word, color, font):
    screen.fill((255, 255, 255))  # White background
    text_surface = font.render(word.upper(), True, color)  # Render word in uppercase
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centered position
    screen.blit(text_surface, text_rect)  # Draw text on the screen
    pygame.display.update()
    pygame.time.delay(1500)  # Pause for 1.5 seconds


# 🎮 Main game function
def play_hangman():
    global game_started, game_over, level_completed, difficulty_selected, selected_difficulty, selected_word
    
    level = 0  # Start at level 1
    guessed_letters = set()  # Store guessed letters
    attempts = 4  # Maximum incorrect guesses
    keys = create_virtual_keyboard()  # Generate virtual keyboard
    running = True  # Control game loop

    while running:
        screen.fill(WHITE)  # Reset screen

        # Draw appropriate UI based on the game state
        if not game_started:
            draw_game_controls()  # Draw Play button
        elif game_started and not difficulty_selected:
            draw_difficulty_buttons()  # Draw difficulty selection buttons
        elif game_over:
            main_button_rect, quit_button_rect = draw_game_controls()  # Draw Play Again and Quit buttons
        elif level_completed:  # If level 10 is completed, show the congratulations message
            main_button_rect, quit_button_rect = draw_game_controls()  # Draw congratulations and quit button
        else:
            draw_game_controls()  # Draw game controls
            draw_word(selected_word, guessed_letters)  # Display word
            draw_virtual_keyboard(keys, guessed_letters)  # Draw virtual keyboard
            draw_attempts(attempts)  # Show remaining attempts
            draw_levels(level)  # Show level progress

        pygame.display.flip()
        pygame.time.delay(100)  # Smooth animation delay

        # 🎭 Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Quit game
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not game_started:  # Game hasn't started, handle Play or Difficulty selection
                    handle_button_click(mouse_pos)  # Start game or handle difficulty selection
                
                elif game_over:  # If game is over, handle Play Again button and Quit button
                    main_button_rect, quit_button_rect = draw_game_controls()  # Draw buttons
                    if main_button_rect.collidepoint(mouse_pos):  # Play Again button clicked
                        game_over = False
                        level = 0  # Reset level when restarting the game
                        difficulty_selected = False  # Reset difficulty
                        guessed_letters.clear()
                        attempts = 4
                        selected_word = get_word(selected_difficulty)  # New word after Play Again
                    elif quit_button_rect.collidepoint(mouse_pos):  # Quit button clicked
                        pygame.quit()
                        sys.exit()
                    else:
                        handle_button_click(mouse_pos)  # Difficulty button clicked

                elif level_completed:  # If the player completed level 10, handle button click
                    main_button_rect, quit_button_rect = draw_game_controls()  # Draw buttons
                    if main_button_rect.collidepoint(mouse_pos):  # Play Again button clicked
                        level_completed = False  # Reset level completion
                        level = 0  # Reset level when restarting the game
                        guessed_letters.clear()
                        attempts = 4
                        selected_word = get_word(selected_difficulty)  # New word after Play Again
                    elif quit_button_rect.collidepoint(mouse_pos):  # Quit button clicked
                        pygame.quit()
                        sys.exit()
                    else:
                        handle_button_click(mouse_pos)  # Difficulty button clicked

                elif not game_over:  # Handle in-game clicks
                    for letter, rect in keys.items():
                        if rect.collidepoint(mouse_pos):
                            if letter not in guessed_letters:
                                guessed_letters.add(letter)
                                if letter in selected_word:
                                    correct_sound.play()

                                    if all(l in guessed_letters for l in selected_word):
                                        show_word_flash(screen, selected_word, (0, 255, 0), FONT)  # Show word flash in green
                                        pygame.time.delay(500)  # Small delay before switching
                                        level += 1  # Move to the next level only after winning
                                        guessed_letters.clear()  # Reset guessed letters
                                        attempts = 4  # Reset attempts
                                        selected_word = get_word(selected_difficulty)
                                        
                                        # Check if level has reached 10 to trigger game over
                                        if level == 10:
                                            level_completed = True  # Game over after Level 10
                                            break
                                else:
                                    attempts -= 1
                                    wrong_sound.play()

                # Handle difficulty buttons after game over or before the game starts
                handle_button_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                guess = event.unicode.upper()
                if guess in keys and guess not in guessed_letters:
                    guessed_letters.add(guess)
                    if guess in selected_word:
                        correct_sound.play()
                    else:
                        attempts -= 1
                        wrong_sound.play()

            # 🏆 Check win condition
            if difficulty_selected and not game_over and all(letter in guessed_letters for letter in selected_word):
                show_word_flash(screen, selected_word, (0, 255, 0), FONT)
                pygame.time.delay(500)
                if level < 10:
                    level += 1  
                    selected_word = get_word(selected_difficulty)  # Get new word
                    guessed_letters.clear()  
                    attempts = 4  
                else:
                    level_completed = True
                    break
            
            # Check loss condition
            if not game_over and attempts == 0:
                show_word_flash(screen, selected_word, (255, 0, 0), FONT)
                pygame.time.delay(500)
                game_over = True

    pygame.quit()

# 🚀 Run the game
if __name__ == "__main__":
    play_hangman()
