import pygame  # Import pygame for UI
import random  # Import random for word selection
import sys
import json  # Import json for data handling
import os  # Import os for file handling
import time  # Import time for delays
from datetime import datetime  # Import datetime for timestamping
from PIL import Image, ImageSequence  # Import Image for GIF handling

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
CATEGORY_FONT = pygame.font.SysFont(None, 28)  # Smaller size than LETTER_FONT
CLUE_FONT = pygame.font.SysFont(None, 15)  # Smaller font size for the clue

# Constants
max_width, max_height = WIDTH, HEIGHT
PLAYER_DATA_FILE = "data/player.json"  # File to store player data

# 🖥️ Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spellout Game")

# 📜 Word Lists by Difficulty with Clues
words_by_difficulty = {
    "Easy": [
        {"word": "HUMAN", "clue": "A bipedal primate species, known for its intelligence and ability to create complex tools."},
        {"word": "EAGLE", "clue": "A large bird of prey, known for its keen eyesight and powerful flight."},
        {"word": "PANTHER", "clue": "A big cat found in the Americas, known for its stealthy hunting skills."},
        {"word": "CROCODILE", "clue": "A large reptile that lives in rivers and is known for its sharp teeth and strong jaws."},
        {"word": "TORTOISE", "clue": "A slow-moving land reptile with a hard shell that protects its body."},
        {"word": "SPIDER", "clue": "An arachnid with eight legs, known for spinning webs."},
        {"word": "FROG", "clue": "An amphibian known for its jumping ability and croaking sound."},
        {"word": "CAT", "clue": "A small domesticated carnivorous mammal with retractable claws."},
        {"word": "BUTTERFLY", "clue": "A colorful insect with delicate wings that goes through metamorphosis."},
        {"word": "HUSKY", "clue": "A strong, thick-coated dog breed known for pulling sleds in snowy regions."}
    ],
    
    "Normal": [
        {"word": "BLUE", "clue": "From the album *Blue* by Yung Kai"},
        {"word": "ENCHANTED", "clue": "From the album *Speak Now* by Taylor Swift"},
        {"word": "TREASURE", "clue": "From the album *Unorthodox Jukebox* by Bruno Mars"},
        {"word": "PHOTOGRAPH", "clue": "From the album *x (Multiply)* by Ed Sheeran"},
        {"word": "JUDAS", "clue": "From the album *Born This Way* by Lady Gaga"},
        {"word": "ROAR", "clue": "From the album *Prism* by Katy Perry"},
        {"word": "GRENADE", "clue": "From the album *Doo-Wops & Hooligans* by Bruno Mars"},
        {"word": "CHANDELIER", "clue": "From the album *1000 Forms of Fear* by Sia"},
        {"word": "HELLO", "clue": "From the album *25* by Adele"},
        {"word": "PERFECT", "clue": "From the album *÷ (Divide)* by Ed Sheeran"},
    ],

    "Medium": [
        {"word": "EIFFEL", "clue": "Paris icon"},
        {"word": "PYRAMID", "clue": "Egypt tomb"},
        {"word": "COLOSSEUM", "clue": "Rome arena"},
        {"word": "ACROPOLIS", "clue": "Greek hilltop"},
        {"word": "SYDNEY", "clue": "Opera house"},
        {"word": "STONEHENGE", "clue": "Ancient rocks"},
        {"word": "PETRA", "clue": "Jordan ruins"},
        {"word": "SPHINX", "clue": "Egypt guardian"},
        {"word": "ANGKOR", "clue": "Cambodia temple"},
        {"word": "ALHAMBRA", "clue": "Spanish palace"},
    ],
    
    "Hard": [
        {"word": "RENAISSANCE", "clue": "Rebirth"},
        {"word": "REVOLUTION", "clue": "Uprising"},
        {"word": "IMPERIALISM", "clue": "Colonial"},
        {"word": "GENOCIDE", "clue": "Massacre"},
        {"word": "CRUSADE", "clue": "Holy"},
        {"word": "FASCISM", "clue": "Dictator"},
        {"word": "ARMISTICE", "clue": "Truce"},
        {"word": "TREATY", "clue": "Agreement"},
        {"word": "FEUDALISM", "clue": "Hierarchy"},
        {"word": "ENLIGHTENMENT", "clue": "Reason"},
    ]
}

# 🏷️ Category Names per Difficulty
category_by_difficulty = {
    "Easy": "Animal Kingdom",
    "Normal": "Song Titles",
    "Medium": "World Landmarks",
    "Hard": "History"
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
shuffled_words = []  # List of non-repeating words per game

# Load Sounds
correct_sound = pygame.mixer.Sound("assets/sounds/correct.mp3")
wrong_sound = pygame.mixer.Sound("assets/sounds/wrong-2.mp3")
warning_sound = pygame.mixer.Sound("assets/sounds/warning.mp3")

# Random name generator
def generate_random_name():
    adjectives = ["Brave", "Clever", "Happy", "Zany", "Jolly", "Lucky"]
    animals = ["Tiger", "Eagle", "Penguin", "Fox", "Panda", "Otter"]
    return f"{random.choice(adjectives)}{random.choice(animals)}"

# Load all player data
def load_player_data():
    if os.path.exists(PLAYER_DATA_FILE):
        with open(PLAYER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save all player data
def save_player_data(data):
    os.makedirs(os.path.dirname(PLAYER_DATA_FILE), exist_ok=True)
    print(f"[DEBUG] Saving data to {PLAYER_DATA_FILE}")
    with open(PLAYER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Update a specific player's record
def update_player_record(uid, duration, level):
    data = load_player_data()
    prev = data.get(uid, {})
    
    # Save only if it's a new high level or faster at same level
    if ("level" not in prev or level > prev["level"]) or \
       (level == prev.get("level", 0) and duration < prev.get("duration", float('inf'))):
        data[uid] = {
            "level": level,
            "duration": round(duration, 2),
            "last_played": datetime.now().isoformat()
        }
        save_player_data(data)

def load_and_resize_gif(gif_path):
    image = Image.open(gif_path)
    gif_width, gif_height = image.size

    # Maintain aspect ratio
    aspect_ratio = gif_width / gif_height
    new_width = max_width
    new_height = int(new_width / aspect_ratio)

    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)

    # Resize all frames
    frames = [
        pygame.image.fromstring(
            frame.resize((new_width, new_height)).tobytes(), 
            (new_width, new_height), 
            frame.mode
        )
        for frame in ImageSequence.Iterator(image)
    ]
    return frames

# Load both GIFs
welcome_frames = load_and_resize_gif('assets/images/welcome.gif')
uid_frames = load_and_resize_gif('assets/images/welcome2.gif')  # Replace with actual path

# Define the welcome screen function
def welcome_screen():
    running = True
    clock = pygame.time.Clock()
    frame_index = 0
    total_frames = len(welcome_frames)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game when 'Enter' is pressed
                    running = False  # Exit the welcome screen

        # Clear the screen
        screen.fill((255, 255, 255))

        # Display the GIF (it will animate automatically)
        screen.blit(welcome_frames[frame_index], (0, 0))

        # Update the display
        pygame.display.flip()

        # Increment the frame index for animation
        frame_index = (frame_index + 1) % total_frames

        # Control frame rate (FPS)
        clock.tick(15)  # Set FPS for smooth animation

    # After the welcome screen, get the player UID from the UID screen
    uid_input = uid_screen()  # This will collect the player's UID

    # Once the UID is collected, proceed to the game
    play_spellout(uid_input)  # Start the game with the UID input

# Define the UID screen function
def uid_screen():
    running = True
    clock = pygame.time.Clock()
    frame_index = 0
    total_frames = len(uid_frames)

    uid_input = ""
    input_active = False
    font = pygame.font.Font(None, 40)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    # Random name button
    button_font = pygame.font.Font(None, 32)
    random_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 85, 150, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color = color_active
                elif random_button.collidepoint(event.pos):
                    uid_input = generate_random_name()
                else:
                    input_active = False
                    color = color_inactive
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and uid_input.strip() != "":  # When ENTER is pressed
                        print(f"Player UID: {uid_input}")  # Print or store UID
                        # Initialize player data with default level 0 and duration 0
                        update_player_record(uid_input, duration=0, level=0)  
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        uid_input = uid_input[:-1]
                    else:
                        uid_input += event.unicode

        # 🔄 Background animation
        screen.fill((255, 255, 255))
        screen.blit(uid_frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % total_frames

        # 🖊️ Draw label above input box
        label_font = pygame.font.Font(None, 25)
        label_surface = label_font.render("Enter player name", True, GRAY)
        label_rect = label_surface.get_rect(center=(WIDTH // 2, input_box.y - 20))
        screen.blit(label_surface, label_rect)

        # ✏️ Draw input box
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(uid_input, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # ⬇️ Draw "or" below input box
        or_surface = label_font.render("or", True, GRAY)
        or_rect = or_surface.get_rect(center=(WIDTH // 2, input_box.y + 60))
        screen.blit(or_surface, or_rect)

        # 🎲 Draw random name button
        pygame.draw.rect(screen, (100, 200, 255), random_button, border_radius=8)
        button_text = button_font.render("Random", True, (0, 0, 0))
        text_rect = button_text.get_rect(center=(
            random_button.x + random_button.width // 2,
            random_button.y + random_button.height // 2
        ))
        screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(15)

    # Move to the game after UID is submitted
    play_spellout(uid_input)

# Function to get rankings
def get_rankings():
    data = load_player_data()
    # Sort by level DESC, then duration ASC
    return sorted(data.items(), key=lambda x: (-x[1]['level'], x[1]['duration']))

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
    global shuffled_words

    if not shuffled_words:
        shuffled_words = words_by_difficulty[difficulty][:]
        random.shuffle(shuffled_words)

    return shuffled_words.pop() ## Get a word from the shuffled list

# Function to handle Play, Play Again, and Difficulty buttons
def handle_button_click(pos):
    global game_started, game_over, attempts, level, selected_word, guessed_letters
    global selected_difficulty, difficulty_selected, shuffled_words

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
        shuffled_words = []  # Clear shuffled words when restarting the game
        return  # Exit to avoid checking difficulty buttons immediately

    # Check if a difficulty button is clicked after starting the game
    if game_started and not difficulty_selected:
        difficulty_buttons = draw_difficulty_buttons()
        for difficulty, rect in difficulty_buttons.items():
            if rect.collidepoint(pos):
                selected_difficulty = difficulty
                difficulty_selected = True

                # Shuffle words once and store them
                shuffled_words = words_by_difficulty[selected_difficulty][:]
                random.shuffle(shuffled_words)

                # 🎯 Select first word
                if shuffled_words:
                    selected_word = shuffled_words.pop()
                return  # Exit to avoid checking Play button again

# 🔡 Function to draw word with rectangles and display category
def draw_word(selected_word, guessed_letters):
    if not game_started or game_over or not difficulty_selected:
        return  # Only draw if game is active and difficulty is selected

    # 🏷️ Display Category Name (based on difficulty)
    category_name = category_by_difficulty.get(selected_difficulty, "Unknown Category")
    category_surface = CATEGORY_FONT.render(f"Category: {category_name}", True, (80, 80, 80))
    category_rect = category_surface.get_rect(center=(WIDTH // 2, 130))  # Positioned above word panel
    screen.blit(category_surface, category_rect)

    # 🧩 Draw Word Panel
    word = selected_word['word']  # Extract the word from selected_word
    clue = selected_word['clue']  # Extract the clue from selected_word
    x_start = WIDTH // 2 - (len(word.replace(" ", "")) * 45) // 2  # Adjust for spaces
    y_start = 150
    cell_size = 40

    # Draw the word's letters
    for i, letter in enumerate(word):
        # Adjust position for spaces (no rectangle drawn for spaces)
        if letter == " ":
            x_start += cell_size + 5  # Skip space area
            continue

        rect_x = x_start + i * (cell_size + 5)  # Normal letter positions
        pygame.draw.rect(screen, RECT_COLOR, (rect_x, y_start, cell_size, cell_size), border_radius=5)

        if letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, WHITE)
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, y_start + cell_size // 2))
            screen.blit(text_surface, text_rect)

    clue_surface = CLUE_FONT.render(f"Clue: {clue}", True, (100, 100, 100))  # Render clue in a smaller font
    clue_rect = clue_surface.get_rect(center=(WIDTH // 2, y_start + cell_size + 40))  # Positioned below the word panel
    screen.blit(clue_surface, clue_rect)

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

# 🔤 Function to show the word flash
def show_word_flash(screen, word, color, font):
    screen.fill((255, 255, 255))  # White background
    text_surface = font.render(word.upper(), True, color)  # Render word in uppercase
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centered position
    screen.blit(text_surface, text_rect)  # Draw text on the screen
    pygame.display.update()
    pygame.time.delay(1500)  # Pause for 1.5 seconds

# Sorting function for rankings
def get_rankings():
    data = load_player_data()
    # Sort by level DESC, then duration ASC
    return sorted(data.items(), key=lambda x: (-x[1]['level'], x[1]['duration']))

# 🎮 Main game function
def play_spellout(uid_input):
    global game_started, game_over, level_completed, difficulty_selected, selected_difficulty, selected_word, shuffled_words
    
    start_time = time.time()  # Start time for duration calculation
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
                                if letter in selected_word['word']: ## Check if letter is in the word
                                    correct_sound.play()

                                    if all(l in guessed_letters for l in selected_word['word']):
                                        show_word_flash(screen, selected_word['word'], (0, 255, 0), FONT)  # Show word flash in green
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
                    if guess in selected_word['word']:  # Check against the word part of selected_word
                        correct_sound.play()
                    else:
                        attempts -= 1
                        wrong_sound.play()

            # 🏆 Check win condition
            if difficulty_selected and not game_over and all(letter in guessed_letters for letter in selected_word['word']):
                show_word_flash(screen, selected_word['word'], (0, 255, 0), FONT)
                pygame.time.delay(500)
                if level < 10:
                    level += 1  
                    selected_word = get_word(selected_difficulty)  # Get new word
                    guessed_letters.clear()  
                    attempts = 4  
                else:
                    level_completed = True
                    end_time = time.time()  # End time for duration calculation
                    duration = end_time - start_time  # Calculate duration

                    # Debugging logs before saving
                    print(f"Player UID: {uid_input}, Duration: {duration}, Level: {level}")
                    update_player_record(uid_input, duration, level)  # Update player record
                    break
            
            # Check loss condition
            if not game_over and attempts == 0:
                show_word_flash(screen, selected_word['word'], (255, 0, 0), FONT)
                pygame.time.delay(500)
                game_over = True
                end_time = time.time()  # End time for duration calculation
                duration = end_time - start_time  # Calculate duration

                # Debugging logs before saving
                print(f"Player UID: {uid_input}, Duration: {duration}, Level: {level}")
                update_player_record(uid_input, duration, level)  # Update player record

    pygame.quit()

# 🚀 Run the game
if __name__ == "__main__":
    welcome_screen()
