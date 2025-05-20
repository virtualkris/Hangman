import pygame  # Import pygame for UI
import random  # Import random for word selection
import sys
import json  # Import json for data handling
import os  # Import os for file handling
import time  # Import time for delays
from datetime import datetime  # Import datetime for timestamping
from PIL import Image, ImageSequence  # Import Image for GIF handling
import math  # Import math for animations

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

# Tier-based color schemes
TIER_COLORS = {
    "Easy": {
        "tier_text": (65, 120, 189),      # #4178bd - Base color
        "clue_text": (255, 255, 255),     # Lighter blue for better readability
        "word_box": (168, 200, 230),      # Very light blue for word boxes
        "keyboard": (65, 120, 189),       # #4178bd - Base color for keyboard
        "keyboard_guessed": (200, 220, 240)  # Light blue for guessed keys
    },
    "Normal": {
        "tier_text": (12, 73, 116),       # #0c4974 - Base color
        "clue_text": (255, 255, 255),      # Lighter navy for better readability
        "word_box": (142, 177, 200),      # Light navy for word boxes
        "keyboard": (12, 73, 116),        # #0c4974 - Base color for keyboard
        "keyboard_guessed": (200, 215, 230)  # Light navy for guessed keys
    },
    "Hard": {
        "tier_text": (255, 145, 77),      # #ff914d - Base color
        "clue_text": (255, 165, 107),     # Lighter orange for better readability
        "word_box": (255, 200, 167),      # Light orange for word boxes
        "keyboard": (255, 145, 77),       # #ff914d - Base color for keyboard
        "keyboard_guessed": (255, 230, 215)  # Light orange for guessed keys
    }
}

# Load pre-game background
pre_game_bg = pygame.image.load('assets/images/pre_game.png')
pre_game_bg = pygame.transform.scale(pre_game_bg, (WIDTH, HEIGHT))

# Load post-game background
post_game_bg = pygame.image.load('assets/images/post_game.png')
post_game_bg = pygame.transform.scale(post_game_bg, (WIDTH, HEIGHT))

# Load tier backgrounds
easy_tier_bg = pygame.image.load('assets/images/easy_tier.png')
easy_tier_bg = pygame.transform.scale(easy_tier_bg, (WIDTH, HEIGHT))

normal_tier_bg = pygame.image.load('assets/images/normal_tier.png')
normal_tier_bg = pygame.transform.scale(normal_tier_bg, (WIDTH, HEIGHT))

hard_tier_bg = pygame.image.load('assets/images/hard_tier.png')
hard_tier_bg = pygame.transform.scale(hard_tier_bg, (WIDTH, HEIGHT))

# Load records background
records_bg = pygame.image.load('assets/images/records.png')
records_bg = pygame.transform.scale(records_bg, (WIDTH, HEIGHT))

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

# 📜 Word Lists by Tier with Clues
words_by_tier = {
    "Easy": [  # Levels 1-5
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
    "Normal": [  # Levels 6-10
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
    "Hard": [  # Levels 11-15
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

# 🏷️ Category Names per Tier
category_by_tier = {
    "Easy": "Animal Kingdom",
    "Normal": "Song Titles",
    "Hard": "World & History"
}

# Time limits for each tier (in seconds)
time_limits = {
    "Easy": 15,    # 15 seconds per word
    "Normal": 30,  # 30 seconds per word
    "Hard": 60     # 60 seconds per word
}

# Background colors for each tier (from light to dark)
tier_colors = {
    "Easy": [
        (236, 250, 220),  # Level 1: #ecfadc
        (221, 242, 209),  # Level 2: #ddf2d1
        (205, 235, 197),  # Level 3: #cdebc5
        (190, 227, 186),  # Level 4: #bee3ba
        (174, 220, 174)   # Level 5: #aedcae
    ],
    "Normal": [
        (245, 241, 251),  # Level 6: #f5f1fb
        (234, 226, 247),  # Level 7: #eae2f7
        (224, 212, 243),  # Level 8: #e0d4f3
        (213, 197, 239),  # Level 9: #d5c5ef
        (203, 183, 235)   # Level 10: #cbb7eb
    ],
    "Hard": [
        (245, 241, 251),  # Level 11: #f5f1fb
        (234, 226, 247),  # Level 12: #eae2f7
        (224, 212, 243),  # Level 13: #e0d4f3
        (213, 197, 239),  # Level 14: #d5c5ef
        (203, 183, 235)   # Level 15: #cbb7eb
    ]
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
shuffled_words = {}  # List of non-repeating words per game
game_mode = "classic"  # Game mode (classic or timed)
word_timer = 0  # Timer for timed mode
word_start_time = 0  # Start time for current word
is_paused = False  # Track pause state
pause_start_time = 0  # Track when pause started
total_pause_time = 0  # Track total time spent paused

# Separate leaderboards for classic and timed modes
CLASSIC_LEADERBOARD_FILE = "data/classic_leaderboard.json"
TIMED_LEADERBOARD_FILE = "data/timed_leaderboard.json"

# Load Sounds
correct_sound = pygame.mixer.Sound("assets/sounds/correct.mp3")
wrong_sound = pygame.mixer.Sound("assets/sounds/wrong-2.mp3")
warning_sound = pygame.mixer.Sound("assets/sounds/warning.mp3")

# Add after the other sound loading
game_over_sound = pygame.mixer.Sound("assets/sounds/negative_beeps-6008.mp3")

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
def update_player_record(uid, duration, level, game_mode):
    # Only update records for the current game mode
    leaderboard_file = TIMED_LEADERBOARD_FILE if game_mode == "timed" else CLASSIC_LEADERBOARD_FILE
    
    try:
        # Load existing data for the current mode only
        data = {}
        if os.path.exists(leaderboard_file):
            with open(leaderboard_file, 'r') as f:
                data = json.load(f)

        # Calculate stars based on game mode and new requirements
        if game_mode == "timed":
            # For timed mode, count correctly guessed words
            correct_words = level  # level represents correctly guessed words
            stars = 0
            if correct_words >= 15:
                stars = 3
            elif correct_words >= 10:
                stars = 2
            elif correct_words >= 5:
                stars = 1
        else:
            # Classic mode - stars based on levels completed
            stars = 0
            if level >= 15:
                stars = 3
            elif level >= 10:
                stars = 2
            elif level >= 5:
                stars = 1

        # Create new record
        new_record = {
            "level": level,
            "duration": round(duration, 2),
            "stars": stars,
            "last_played": datetime.now().isoformat()
        }

        # Initialize player data if not exists
        if uid not in data:
            data[uid] = {"last_record": {}, "best_record": {}}

        # Update last_record
        data[uid]["last_record"] = new_record.copy()

        # Update best_record only if it's a better performance
        current_best = data[uid].get("best_record", {})
        if (not current_best or
            level > current_best.get("level", 0) or
            (level == current_best.get("level", 0) and
             duration < current_best.get("duration", float('inf')))):
            data[uid]["best_record"] = new_record.copy()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True)
        
        # Save the data
        with open(leaderboard_file, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"[DEBUG] Successfully updated {game_mode} leaderboard for player {uid}")
        
    except Exception as e:
        print(f"[ERROR] Failed to update player record: {str(e)}")
        # Optionally, create the directory if it doesn't exist
        os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True)

# Load and resize GIFs
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
uid_frames = load_and_resize_gif('assets/images/welcome2.gif')
resume_frames = load_and_resize_gif('assets/images/resume_screen.gif')  # Add new GIF

# Function to show the game manual
def show_game_manual():
    manual_running = True
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 30)
    text_font = pygame.font.Font(None, 20)

    title = title_font.render("Game Manual", True, BLACK)

    # Load icons
    icon_paths = [
        "objective.png", "keyboard.png", "lives.png", "goal.png",
        "gamepad.png", "wrong.png", "trophy.png", "pause.png", "back.png"
    ]
    icon_images = [pygame.image.load(f"assets/icons/{img}").convert_alpha() for img in icon_paths]

    # Instructions (text without emojis now)
    instructions = [
        "Objective: Guess the hidden word one letter at a time.",
        "Click letters or use your keyboard to guess.",
        "You get 4 attempts per word.",
        "Complete 10 levels to finish the game.",
        "Click 'Random' for a surprise name.",
        "Wrong guesses reduce your attempts.",
        "Leaderboard tracks your level & time.",
        "Press ESC during the game to pause/resume.",
        "Press ESC now to return to the previous screen."
    ]

    while manual_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                manual_running = False

        # Draw background first
        screen.blit(records_bg, (0, 0))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # Adjust alpha for desired transparency
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

        # Create manual surface
        manual_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100))
        manual_surface.fill((255, 255, 255))
        pygame.draw.rect(manual_surface, BLACK, manual_surface.get_rect(), 3)

        manual_surface.blit(title, (manual_surface.get_width() // 2 - title.get_width() // 2, 20))

        # Draw each instruction with its corresponding icon
        for i, (icon, line) in enumerate(zip(icon_images, instructions)):
            y_pos = 60 + i * 30
            icon = pygame.transform.scale(icon, (24, 24))
            manual_surface.blit(icon, (25, y_pos))
            text = text_font.render(line, True, (0, 0, 0))
            manual_surface.blit(text, (60, y_pos))

        screen.blit(manual_surface, (50, 50))
        pygame.display.flip()
        clock.tick(30)

# Define the welcome screen function
def welcome_screen():
    running = True
    clock = pygame.time.Clock()
    frame_index = 0
    total_frames = len(welcome_frames)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game when 'Enter' is pressed
                    running = False  # Exit the welcome screen

        # Clear the screen
        screen.fill(WHITE)

        # Display the welcome GIF frame
        screen.blit(welcome_frames[frame_index], (0, 0))

        pygame.display.flip()

        frame_index = (frame_index + 1) % total_frames
        clock.tick(15)

    # 🆕 Resume screen logic after exiting welcome screen
    resume_prompt_screen()  # NEW: Show Resume or New Game option after welcome

# Function to show the UID screen
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
    random_button_color = (50, 150, 205)  # Base color for random button

    # ❓ Help/manual button in lower right
    help_button = pygame.Rect(WIDTH - 50, HEIGHT - 50, 35, 35)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color = color_active
                elif help_button.collidepoint(event.pos):
                    show_game_manual()
                elif random_button.collidepoint(event.pos):
                    uid_input = generate_random_name()
                else:
                    input_active = False
                    color = color_inactive
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and uid_input.strip() != "":
                        print(f"Player UID: {uid_input}")
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        uid_input = uid_input[:-1]
                    else:
                        uid_input += event.unicode

        screen.fill((255, 255, 255))
        screen.blit(uid_frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % total_frames

        # Draw label above input box
        label_font = pygame.font.Font(None, 25)
        label_surface = label_font.render("Enter player name", True, BLACK)
        label_rect = label_surface.get_rect(center=(WIDTH // 2, input_box.y - 20))
        screen.blit(label_surface, label_rect)

        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(uid_input, True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

        # Draw "or" below input box
        or_surface = label_font.render("or", True, BLACK)
        or_rect = or_surface.get_rect(center=(WIDTH // 2, input_box.y + 60))
        screen.blit(or_surface, or_rect)

        # Draw random name button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        current_random_color = get_hover_color(random_button_color) if random_button.collidepoint(mouse_pos) else random_button_color
        pygame.draw.rect(screen, current_random_color, random_button, border_radius=8)
        button_text = button_font.render("Random", True, WHITE)
        text_rect = button_text.get_rect(center=(
            random_button.x + random_button.width // 2,
            random_button.y + random_button.height // 2
        ))
        screen.blit(button_text, text_rect)

        # Draw "?" help/manual button
        pygame.draw.circle(screen, (200, 200, 200), help_button.center, 18)
        help_font = pygame.font.Font(None, 28)
        help_text = help_font.render("?", True, BLACK)
        screen.blit(help_text, help_text.get_rect(center=help_button.center))

        pygame.display.flip()
        clock.tick(15)

    # Move to the game after UID is submitted
    play_spellout(uid_input)

# Function to resume the game
def resume_prompt_screen():
    global game_started, difficulty_selected, selected_difficulty, level, guessed_letters, selected_word, attempts, shuffled_words

    print("[DEBUG] Checking for saved game state...")
    # Load saved state if available
    saved_state = None
    if os.path.exists("data/savegame.json"):
        print("Save file exists.")
        with open("data/savegame.json", "r") as f:
            try:
                saved_state = json.load(f)
                print("Save file loaded:", saved_state)
                required_keys = ["selected_difficulty", "level", "guessed_letters", "selected_word", "attempts", "shuffled_words", "uid"]
                if not all(key in saved_state for key in required_keys):
                    print("Save file missing required keys.")
                    saved_state = None
                else:
                    print("Save file has all required keys.")
            except json.JSONDecodeError as e:
                print("Error decoding save file:", e)
                saved_state = None

    # Button dimensions and positioning
    button_width = 160
    button_height = 40
    button_spacing = 10

    # Position resume button near bottom of screen
    resume_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - button_height - 100, button_width, button_height)
    
    running = True
    clock = pygame.time.Clock()
    frame_index = 0
    total_frames = len(resume_frames)

    while running:
        screen.fill(WHITE)

        # Display the resume screen GIF frame
        screen.blit(resume_frames[frame_index], (0, 0))
        frame_index = (frame_index + 1) % total_frames

        if saved_state:
            # Draw resume button with consistent styling
            pygame.draw.rect(screen, BLUE, resume_button, border_radius=8)
            resume_text = BUTTON_FONT.render("Resume Game", True, WHITE)
            text_rect = resume_text.get_rect(center=resume_button.center)
            screen.blit(resume_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    # Clear saved game and proceed to UID screen
                    if os.path.exists("data/savegame.json"):
                        os.remove("data/savegame.json")
                    uid_screen()
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN and saved_state:
                if resume_button.collidepoint(pygame.mouse.get_pos()):
                    # Restore game variables
                    game_started = True
                    difficulty_selected = True
                    selected_difficulty = saved_state["selected_difficulty"]
                    level = saved_state["level"]
                    guessed_letters = set(saved_state["guessed_letters"])
                    selected_word = saved_state["selected_word"]
                    attempts = saved_state["attempts"]
                    shuffled_words = saved_state["shuffled_words"]
                    uid_input = saved_state["uid"]
                    play_spellout(uid_input, resumed=True)
                    return

        clock.tick(15)  # Control animation speed

# Function to display the leaderboard
def display_leaderboard(uid_input):
    # Load both leaderboards
    classic_data = {}
    timed_data = {}
    
    if os.path.exists(CLASSIC_LEADERBOARD_FILE):
        with open(CLASSIC_LEADERBOARD_FILE, 'r') as f:
            classic_data = json.load(f)
            
    if os.path.exists(TIMED_LEADERBOARD_FILE):
        with open(TIMED_LEADERBOARD_FILE, 'r') as f:
            timed_data = json.load(f)

    # Create leaderboard surface
    board_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100))
    board_surface.fill((240, 240, 240))
    pygame.draw.rect(board_surface, BLACK, board_surface.get_rect(), 3)

    # Load icons
    trophy_icon = pygame.image.load("assets/icons/trophy.png")
    trophy_icon = pygame.transform.scale(trophy_icon, (30, 30))
    
    gold_icon = pygame.image.load("assets/icons/gold_cup.png")
    silver_icon = pygame.image.load("assets/icons/silver_cup.png")
    bronze_icon = pygame.image.load("assets/icons/bronze_cup.png")
    badge_icon = pygame.image.load("assets/icons/badge.png")
    star_icon = pygame.image.load("assets/icons/star.png")
    star_icon = pygame.transform.scale(star_icon, (15, 15))

    x_icon = pygame.image.load("assets/icons/x_icon.png")
    x_icon = pygame.transform.scale(x_icon, (25, 25))
    x_button = pygame.Rect(WIDTH - 50, 20, 25, 25)

    # Title
    title_font = pygame.font.Font(None, 36)
    list_font = pygame.font.Font(None, 20)
    mode_font = pygame.font.Font(None, 28)

    # Mode selection buttons - positioned relative to board_surface
    classic_button = pygame.Rect(board_surface.get_width() // 4 - 50, 20, 100, 30)
    timed_button = pygame.Rect(board_surface.get_width() * 3 // 4 - 50, 20, 100, 30)
    
    current_mode = "classic"  # Default mode to show
    
    while True:
        # Draw background first
        screen.blit(records_bg, (0, 0))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # Adjust alpha for desired transparency
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

        board_surface.fill((240, 240, 240))
        pygame.draw.rect(board_surface, BLACK, board_surface.get_rect(), 3)

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        board_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)  # Adjust for board position

        # Draw mode buttons with hover effects
        for button, text, mode in [(classic_button, "Classic", "classic"), 
                                 (timed_button, "Timed", "timed")]:
            base_color = BLUE if mode == current_mode else GRAY
            color = get_hover_color(base_color) if button.collidepoint(board_pos) else base_color
            pygame.draw.rect(board_surface, color, button, border_radius=5)
            text_surface = mode_font.render(text, True, WHITE if mode == current_mode else BLACK)
            text_rect = text_surface.get_rect(center=button.center)
            board_surface.blit(text_surface, text_rect)

        # Get current leaderboard data
        current_data = classic_data if current_mode == "classic" else timed_data
        
        # Extract and sort players
        valid_players = [
            (uid, data["best_record"])
            for uid, data in current_data.items()
            if "best_record" in data
        ]
        
        sorted_players = sorted(
            valid_players,
            key=lambda x: (-x[1]["level"], x[1]["duration"])
        )

        # Find current player's rank
        player_rank = None
        for i, (uid, _) in enumerate(sorted_players):
            if uid == uid_input:
                player_rank = i + 1
                break

        y_offset = 70
        if sorted_players:
            for idx, (uid, record) in enumerate(sorted_players[:10]):
                if idx == 0:
                    icon = gold_icon
                elif idx == 1:
                    icon = silver_icon
                elif idx == 2:
                    icon = bronze_icon
                else:
                    icon = badge_icon

                icon = pygame.transform.scale(icon, (20, 20))

                level = record["level"]
                duration = record["duration"]
                stars = record["stars"]
                
                # Draw rank icon
                board_surface.blit(icon, (30, y_offset))
                
                # Draw player info
                text_color = (0, 100, 200) if uid == uid_input else BLACK
                player_info = f"{uid} - Level: {level} - {duration:.2f}s"
                player_surface = list_font.render(player_info, True, text_color)
                board_surface.blit(player_surface, (65, y_offset))
                
                # Draw stars - moved further right
                star_x = board_surface.get_width() - (stars * 20) - 30  # Adjusted position
                for _ in range(stars):
                    board_surface.blit(star_icon, (star_x, y_offset))
                    star_x += 20
                
                y_offset += 25

            # Show current player's rank if not in top 10
            if player_rank and player_rank > 10:
                y_offset += 10
                pygame.draw.line(board_surface, GRAY, (25, y_offset), 
                               (board_surface.get_width() - 25, y_offset), 1)
                y_offset += 10

                record = current_data[uid_input]["best_record"]
                level = record["level"]
                duration = record["duration"]
                stars = record["stars"]
                player_info = f"{player_rank}. {uid_input} - Level: {level} - {duration:.2f}s"
                player_surface = list_font.render(player_info, True, (0, 100, 200))
                board_surface.blit(player_surface, (30, y_offset))
                
                # Draw stars for current player - moved further right
                star_x = board_surface.get_width() - (stars * 20) - 30  # Adjusted position
                for _ in range(stars):
                    board_surface.blit(star_icon, (star_x, y_offset))
                    star_x += 20

        else:
            empty_msg = list_font.render("No data available.", True, (100, 0, 0))
            board_surface.blit(empty_msg, (board_surface.get_width() // 2 - empty_msg.get_width() // 2, y_offset))

        # Draw everything
        screen.blit(board_surface, (50, 50))
        screen.blit(x_icon, x_button.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                board_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)  # Adjust for board position
                
                if x_button.collidepoint(mouse_pos):
                    return
                elif classic_button.collidepoint(board_pos):
                    current_mode = "classic"
                elif timed_button.collidepoint(board_pos):
                    current_mode = "timed"

# Function to show the last record of a player
def show_last_record(uid_input):
    # Load both leaderboards
    classic_data = {}
    timed_data = {}
    
    if os.path.exists(CLASSIC_LEADERBOARD_FILE):
        with open(CLASSIC_LEADERBOARD_FILE, 'r') as f:
            classic_data = json.load(f)
            
    if os.path.exists(TIMED_LEADERBOARD_FILE):
        with open(TIMED_LEADERBOARD_FILE, 'r') as f:
            timed_data = json.load(f)

    # Load icons
    x_icon = pygame.image.load("assets/icons/x_icon.png")
    x_icon = pygame.transform.scale(x_icon, (25, 25))
    x_button = pygame.Rect(WIDTH - 50, 20, 25, 25)

    star_icon = pygame.image.load("assets/icons/star.png")
    star_icon = pygame.transform.scale(star_icon, (30, 30))

    # Draw border box surface
    manual_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100))
    manual_surface.fill((240, 240, 240))
    pygame.draw.rect(manual_surface, BLACK, manual_surface.get_rect(), 3)

    title_font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 26)
    mode_font = pygame.font.Font(None, 28)

    # Mode selection buttons
    classic_button = pygame.Rect(manual_surface.get_width() // 4 - 50, 20, 100, 30)
    timed_button = pygame.Rect(manual_surface.get_width() * 3 // 4 - 50, 20, 100, 30)
    
    current_mode = "classic"  # Default mode to show
    
    while True:
        # Draw background first
        screen.blit(records_bg, (0, 0))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)  # Adjust alpha for desired transparency
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

        manual_surface.fill((240, 240, 240))
        pygame.draw.rect(manual_surface, BLACK, manual_surface.get_rect(), 3)

        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        board_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)  # Adjust for board position

        # Draw mode buttons with hover effects
        for button, text, mode in [(classic_button, "Classic", "classic"), 
                                 (timed_button, "Timed", "timed")]:
            base_color = BLUE if mode == current_mode else GRAY
            color = get_hover_color(base_color) if button.collidepoint(board_pos) else base_color
            pygame.draw.rect(manual_surface, color, button, border_radius=5)
            text_surface = mode_font.render(text, True, WHITE if mode == current_mode else BLACK)
            text_rect = text_surface.get_rect(center=button.center)
            manual_surface.blit(text_surface, text_rect)

        # Get current data
        current_data = classic_data if current_mode == "classic" else timed_data

        if uid_input in current_data and "last_record" in current_data[uid_input]:
            record = current_data[uid_input]["last_record"]
            level = record.get('level', 0)
            duration = record.get('duration', 0)
            stars = record.get('stars', 0)
            last_played = record.get('last_played', "Unknown")

            # Center stars at top line
            stars_width = stars * 30 - 6
            star_x = (manual_surface.get_width() - stars_width) // 2
            star_y = 60

            for i in range(stars):
                manual_surface.blit(star_icon, (star_x + i * 30, star_y))
            
            y_offset = 100
            spacing = 30

            # Change text based on game mode
            if current_mode == "classic":
                level_text = info_font.render(f"Levels Completed: {level}", True, BLACK)
            else:  # timed mode
                level_text = info_font.render(f"Words Completed: {level}", True, BLACK)
            manual_surface.blit(level_text, (50, y_offset))

            duration_text = info_font.render(f"Duration: {duration:.2f}s", True, BLACK)
            manual_surface.blit(duration_text, (50, y_offset + spacing))

            last_played_text = info_font.render(f"Last Played: {last_played}", True, BLACK)
            manual_surface.blit(last_played_text, (50, y_offset + spacing * 2))

        else:
            error_msg = info_font.render("No record found for this player.", True, (200, 0, 0))
            manual_surface.blit(error_msg, (manual_surface.get_width() // 2 - error_msg.get_width() // 2, 120))

        # Blit manual_surface to main screen
        screen.blit(manual_surface, (50, 50))

        # Draw X (back) icon on the main screen
        screen.blit(x_icon, x_button.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                board_pos = (mouse_pos[0] - 50, mouse_pos[1] - 50)  # Adjust for board position
                
                if x_button.collidepoint(mouse_pos):
                    return
                elif classic_button.collidepoint(board_pos):
                    current_mode = "classic"
                elif timed_button.collidepoint(board_pos):
                    current_mode = "timed"

# Function to get hover color
def get_hover_color(base_color):
    """Lighten a color when hovering."""
    return tuple(min(c + 30, 255) for c in base_color)

# 🎮 Function to draw game controls
def draw_game_controls(player_name=None, state='start'):
    button_color = (71, 185, 112)      # Green
    quit_button_color = (222, 52, 52)  # Red (#de3434)
    leaderboard_button_color = (100, 150, 255)  # Blue
    last_record_button_color = (255, 223, 100)  # Yellow
    
    # Separate text colors for different screens
    pre_game_text_color = BLACK
    post_game_text_color = (12, 73, 116)
    text_button_color = WHITE  # Button text color remains white for both screens

    # Common button dimensions
    button_width = 160
    button_height = 50
    
    # Use consistent spacing for all screens
    spacing = 10
    
    # Separate vertical offsets for different screens
    pre_game_offset = 0  # Offset for welcome screen
    post_game_offset = -35  # Offset for game over/complete screen
    
    # Calculate total height of elements based on state
    if state == 'start':
        total_height = 30 + button_height + spacing + button_height  # Title + 2 buttons + spacing
        vertical_offset = pre_game_offset
        text_color = pre_game_text_color
    else:
        total_height = 30 + button_height + spacing * 3 + button_height  # Title + 4 buttons + spacings
        vertical_offset = post_game_offset
        text_color = post_game_text_color
    
    # Start position for first element
    start_y = (HEIGHT - total_height) // 2 + vertical_offset  # Adjust vertical_offset to move everything up/down
    
    button_x = WIDTH // 2 - button_width // 2
    current_y = start_y + 30  # Adjust this value (30) to change space between title and first button

    font = pygame.font.Font(None, 35)
    button_font = pygame.font.Font(None, 25)
    button_rects = {"classic": None, "timed": None, "quit": None, "leaderboard": None, "last_record": None}

    # Get mouse position for hover effects
    mouse_pos = pygame.mouse.get_pos()

    # Draw appropriate background based on state
    if state == 'start':
        screen.blit(pre_game_bg, (0, 0))
    elif state in ('over', 'complete'):
        screen.blit(post_game_bg, (0, 0))

    # ✳️ STATE-SPECIFIC UI
    if state == 'start':
        text = f"Welcome {player_name}!"
        
        # Title Text - Position controlled by start_y
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, start_y)))

        # CLASSIC MODE button - Position controlled by current_y
        classic_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        classic_color = get_hover_color(button_color) if classic_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, classic_color, classic_rect, border_radius=8)
        classic_surface = button_font.render("CLASSIC MODE", True, text_button_color)
        screen.blit(classic_surface, classic_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["classic"] = classic_rect

        # TIMED MODE button - Position controlled by current_y + spacing
        current_y += button_height + spacing
        timed_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        timed_color = get_hover_color(leaderboard_button_color) if timed_rect.collidepoint(mouse_pos) else leaderboard_button_color
        pygame.draw.rect(screen, timed_color, timed_rect, border_radius=8)
        timed_surface = button_font.render("TIMED MODE", True, text_button_color)
        screen.blit(timed_surface, timed_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["timed"] = timed_rect

    elif state in ('over', 'complete'):
        if state == 'over':
            text = "GAME OVER! Want to try again?"
        else:
            text = "CONGRATULATIONS! You completed all Levels!"
        play_text = "PLAY AGAIN"

        # Title Text - Position controlled by start_y
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, start_y)))

        # PLAY AGAIN button - Position controlled by current_y
        play_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        play_color = get_hover_color(button_color) if play_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, play_color, play_rect, border_radius=8)
        play_surface = button_font.render(play_text, True, text_button_color)
        screen.blit(play_surface, play_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["classic"] = play_rect

        # LEADERBOARD - Position controlled by current_y + spacing
        current_y += button_height + spacing
        lb_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        lb_color = get_hover_color(leaderboard_button_color) if lb_rect.collidepoint(mouse_pos) else leaderboard_button_color
        pygame.draw.rect(screen, lb_color, lb_rect, border_radius=8)
        lb_surface = button_font.render("LEADERBOARD", True, text_button_color)
        screen.blit(lb_surface, lb_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["leaderboard"] = lb_rect

        # LAST RECORD - Position controlled by current_y + spacing
        current_y += button_height + spacing
        lr_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        lr_color = get_hover_color(last_record_button_color) if lr_rect.collidepoint(mouse_pos) else last_record_button_color
        pygame.draw.rect(screen, lr_color, lr_rect, border_radius=8)
        lr_surface = button_font.render("LAST RECORD", True, text_button_color)
        screen.blit(lr_surface, lr_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["last_record"] = lr_rect

        # QUIT - Position controlled by current_y + spacing
        current_y += button_height + spacing
        quit_rect = pygame.Rect(button_x, current_y, button_width, button_height)
        quit_color = get_hover_color(quit_button_color) if quit_rect.collidepoint(mouse_pos) else quit_button_color
        pygame.draw.rect(screen, quit_color, quit_rect, border_radius=8)
        quit_surface = button_font.render("QUIT", True, text_button_color)
        screen.blit(quit_surface, quit_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects["quit"] = quit_rect

    return button_rects

# Functions to save the game state
def pause_menu(uid_input, level, attempts, guessed_letters, selected_word, selected_difficulty, shuffled_words):
    global is_paused, pause_start_time, total_pause_time
    
    paused = True
    is_paused = True
    pause_start_time = time.time()
    
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    # Button dimensions and positioning
    button_width = 160
    button_height = 40
    button_spacing = 10
    total_height = (button_height * 3) + (button_spacing * 2)  # 3 buttons with spacing
    start_y = (HEIGHT - total_height) // 2

    # Create buttons with consistent styling
    resume_button = pygame.Rect(WIDTH//2 - button_width//2, start_y, button_width, button_height)
    save_button = pygame.Rect(WIDTH//2 - button_width//2, start_y + button_height + button_spacing, button_width, button_height)
    save_exit_button = pygame.Rect(WIDTH//2 - button_width//2, start_y + (button_height + button_spacing) * 2, button_width, button_height)

    # Title font
    title_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 30)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Resume
                    is_paused = False
                    total_pause_time += time.time() - pause_start_time
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(pos):
                    paused = False
                    is_paused = False
                    total_pause_time += time.time() - pause_start_time
                elif save_button.collidepoint(pos):
                    save_game_state(
                        uid_input,
                        level,
                        attempts,
                        guessed_letters,
                        selected_word,
                        selected_difficulty,
                        shuffled_words
                    )
                elif save_exit_button.collidepoint(pos):
                    save_game_state(
                        uid_input,
                        level,
                        attempts,
                        guessed_letters,
                        selected_word,
                        selected_difficulty,
                        shuffled_words
                    )
                    pygame.quit()
                    sys.exit()

        screen.blit(overlay, (0, 0))

        # Draw title
        title_text = title_font.render("GAME PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, start_y - 50))
        screen.blit(title_text, title_rect)

        # Draw buttons with consistent styling
        for button, text, color in [
            (resume_button, "Resume", BLUE),
            (save_button, "Save", NORMAL_COLOR),
            (save_exit_button, "Save and Exit", ORANGE)
        ]:
            # Draw button with rounded corners
            pygame.draw.rect(screen, color, button, border_radius=8)
            
            # Draw button text
            text_surface = button_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        pygame.time.delay(100)

def save_game_state(uid_input, level, attempts, guessed_letters, selected_word, selected_difficulty, shuffled_words):
    save_data = {
        'uid': uid_input,
        'level': level,
        'attempts': attempts,
        'guessed_letters': list(guessed_letters),
        'selected_word': selected_word,
        'selected_difficulty': selected_difficulty,
        'shuffled_words': shuffled_words
    }

    with open("data/savegame.json", "w") as f:
        json.dump(save_data, f)
    
    print("[💾] Game state saved.")

# Function to get current tier based on level
def get_current_tier(level):
    if level <= 5:
        return "Easy"
    elif level <= 10:
        return "Normal"
    else:
        return "Hard"

# Function to get background color based on level
def get_background_color(level):
    current_tier = get_current_tier(level)
    if current_tier == "Easy":
        return easy_tier_bg
    elif current_tier == "Normal":
        return normal_tier_bg
    else:  # Hard tier
        return hard_tier_bg

# Function to show tier completion screen
def show_tier_completion(screen, tier, stars):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Load star icon
    star_icon = pygame.image.load("assets/icons/star.png")
    star_icon = pygame.transform.scale(star_icon, (50, 50))

    # Display congratulations text
    font = pygame.font.Font(None, 48)
    text = font.render(f"{tier} Tier Complete!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Display stars
    star_x = WIDTH // 2 - (stars * 30)
    for i in range(stars):
        screen.blit(star_icon, (star_x + i * 60, HEIGHT // 2 + 20))

    # Display "Press any key to continue"
    continue_font = pygame.font.Font(None, 24)
    continue_text = continue_font.render("Press any key to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

# Function to get a word based on current level
def get_word_for_level(level):
    """Get a word appropriate for the current level.
    Maintains separate shuffled lists for each tier."""
    global shuffled_words
    
    # Initialize shuffled_words as a dictionary if it doesn't exist
    if not isinstance(shuffled_words, dict):
        shuffled_words = {
            "Easy": [],
            "Normal": [],
            "Hard": []
        }
    
    current_tier = get_current_tier(level)
    
    # If the current tier's list is empty, refill it
    if not shuffled_words[current_tier]:
        shuffled_words[current_tier] = words_by_tier[current_tier][:]
        random.shuffle(shuffled_words[current_tier])
    
    return shuffled_words[current_tier].pop()

# 🔵 Function to draw level indicators (updated for 15 levels)
def draw_levels(level):
    if not game_started or game_over:
        return  # Draw levels only if the game is active
    
    x_start = 20  
    y_start = 20  
    radius = 8  
    spacing = 5  

    for i in range(15):  # 15 levels total
        row = i % 5
        col = i // 5
        current_level = i + 1  # Convert to 1-based level number
        
        # Determine base color based on tier
        if current_level <= 5:  # Easy tier (levels 1-5)
            base_color = EASY_COLOR
        elif current_level <= 10:  # Normal tier (levels 6-10)
            base_color = NORMAL_COLOR
        else:  # Hard tier (levels 11-15)
            base_color = HARD_COLOR
            
        # Level is completed if current game level is higher than this indicator
        # For level 1, the indicator should not be highlighted initially
        is_completed = current_level < level
        # Current level indicator should be orange
        is_current = current_level == level
        
        if is_completed:
            color = base_color  # Show completed levels in their tier color
        elif is_current:
            color = ORANGE  # Current level in orange
        else:
            color = GRAY  # Upcoming levels in gray
        
        x_pos = x_start + col * (radius * 2 + spacing)  
        y_pos = y_start + row * (radius * 2 + spacing)  

        pygame.draw.circle(screen, color, (x_pos, y_pos), radius)
        pygame.draw.circle(screen, BLACK, (x_pos, y_pos), radius, 2)

# 🔡 Function to draw word with rectangles and display category
def draw_word(selected_word, guessed_letters):
    if not game_started or game_over:
        return  # Only draw if game is active

    # Get current tier colors
    current_tier = get_current_tier(level)
    colors = TIER_COLORS[current_tier]

    # 🏷️ Display Tier and Category Name
    category_name = category_by_tier.get(current_tier, "Unknown Category")
    tier_text = f"Tier: {current_tier}"
    category_text = f"Category: {category_name}"
    
    # Render tier text
    tier_surface = CATEGORY_FONT.render(tier_text, True, colors["tier_text"])
    tier_rect = tier_surface.get_rect(center=(WIDTH // 2, 110))
    screen.blit(tier_surface, tier_rect)
    
    # Render category text
    category_surface = CATEGORY_FONT.render(category_text, True, colors["tier_text"])
    category_rect = category_surface.get_rect(center=(WIDTH // 2, 130))
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
        pygame.draw.rect(screen, colors["word_box"], (rect_x, y_start, cell_size, cell_size), border_radius=5)

        if letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, colors["tier_text"])
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, y_start + cell_size // 2))
            screen.blit(text_surface, text_rect)

    clue_surface = CLUE_FONT.render(f"Clue: {clue}", True, colors["clue_text"])
    clue_rect = clue_surface.get_rect(center=(WIDTH // 2, y_start + cell_size + 40))
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
    """Draw the virtual keyboard with proper letter highlighting"""
    if not game_started or game_over:
        return # Draw the keyboard only if the game is active
    
    # Get current tier colors
    current_tier = get_current_tier(level)
    colors = TIER_COLORS[current_tier]
    
    # Create a surface for the keyboard
    keyboard_surface = pygame.Surface((WIDTH, 150))
    keyboard_surface.set_colorkey((0, 0, 0))  # Make black transparent
    
    # Draw each key on the keyboard surface
    for letter, rect in keys.items():
        # Create a new rect relative to the keyboard surface
        key_rect = pygame.Rect(rect.x, rect.y - 300, rect.width, rect.height)
        
        # Determine key color based on whether it's been guessed
        if letter in guessed_letters:
            color = colors["keyboard_guessed"]
        else:
            color = colors["keyboard"]
            
        # Draw the key
        pygame.draw.rect(keyboard_surface, color, key_rect, border_radius=5)
        
        # Draw the letter
        text_surface = BUTTON_FONT.render(letter, True, WHITE)
        text_rect = text_surface.get_rect(center=key_rect.center)
        keyboard_surface.blit(text_surface, text_rect)
    
    # Blit the keyboard surface onto the main screen
    screen.blit(keyboard_surface, (0, 300))

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

# 🔤 Function to show the word flash
def show_word_flash(screen, word, color, font):
    screen.fill((255, 255, 255))  # White background
    text_surface = font.render(word.upper(), True, color)  # Render word in uppercase
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))  # Centered position
    screen.blit(text_surface, text_rect)  # Draw text on the screen
    pygame.display.update()
    pygame.time.delay(1500)  # Pause for 1.5 seconds

# Function to draw timer
def draw_timer():
    global total_pause_time
    
    current_tier = get_current_tier(level)
    if game_mode != "timed":
        return False
        
    time_limit = time_limits[current_tier]
    
    # Calculate elapsed time accounting for pauses
    if is_paused:
        elapsed_time = pause_start_time - word_start_time - total_pause_time
    else:
        elapsed_time = time.time() - word_start_time - total_pause_time
    
    remaining_time = max(0, time_limit - elapsed_time)
    
    # Draw timer bar - centered below clue and above keyboard
    bar_width = 200  # Wider bar for better visibility
    bar_height = 8   # Thinner bar
    bar_x = (WIDTH - bar_width) // 2  # Center horizontally
    bar_y = 250  # Position below clue and above keyboard
    
    # Background bar (gray)
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    
    # Time remaining bar (color based on time left)
    remaining_ratio = remaining_time / time_limit
    remaining_width = int(bar_width * remaining_ratio)
    
    if remaining_ratio > 0.6:
        color = EASY_COLOR  # Green
    elif remaining_ratio > 0.3:
        color = ORANGE  # Orange
    else:
        color = RED  # Red
        
    pygame.draw.rect(screen, color, (bar_x, bar_y, remaining_width, bar_height))
    
    # Check if time is up
    if remaining_time <= 0 and not game_over and not is_paused:
        show_word_flash(screen, selected_word['word'], RED, FONT)
        return True
    return False

# Function to handle word completion and level progression
def handle_word_completion(screen, current_level, game_mode, total_time_bonus):
    """Handle level progression and tier completion.
    Called BEFORE level increment, so:
    - Level 5 completion = moving to level 6 (Easy tier complete)
    - Level 10 completion = moving to level 11 (Normal tier complete)
    - Level 15 = game complete (Hard tier complete)
    """
    if current_level == 5:  # Completing level 5, moving to level 6
        show_tier_completion(screen, "Easy", 1)
        if game_mode == "timed":
            return 15  # Add 15 seconds bonus
    elif current_level == 10:  # Completing level 10, moving to level 11
        show_tier_completion(screen, "Normal", 2)
        if game_mode == "timed":
            return 30  # Add 30 seconds bonus
    elif current_level == 15:  # Completing level 15, game complete
        show_tier_completion(screen, "Hard", 3)
    return 0  # No time bonus

# Add these new functions after the get_hover_color function

def animate_word_panel(screen, word, guessed_letters, animation_type, progress):
    """Animate the word panel based on the animation type and progress (0.0 to 1.0)"""
    # Get current tier colors
    current_tier = get_current_tier(level)
    colors = TIER_COLORS[current_tier]

    # Base positions and sizes
    x_start = WIDTH // 2 - (len(word.replace(" ", "")) * 45) // 2
    y_start = 150
    cell_size = 40

    if animation_type == "shake":
        # Shake animation for wrong guesses
        shake_amount = 15 * (1 - progress)  # Increased shake amount
        x_offset = math.sin(progress * 25) * shake_amount  # Faster oscillation
        x_start += x_offset
    elif animation_type == "pop":
        # Pop animation for correct guesses
        scale = 1 + 0.15 * math.sin(progress * math.pi)  # Subtler pop effect
        cell_size = int(40 * scale)
        x_start = WIDTH // 2 - (len(word.replace(" ", "")) * (cell_size + 5)) // 2
        y_start = 150 - (cell_size - 40) // 2  # Adjust y position to keep center

    # Draw the word's letters
    for i, letter in enumerate(word):
        if letter == " ":
            x_start += cell_size + 5
            continue

        rect_x = x_start + i * (cell_size + 5)
        pygame.draw.rect(screen, colors["word_box"], (rect_x, y_start, cell_size, cell_size), border_radius=5)

        if letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, colors["tier_text"])
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, y_start + cell_size // 2))
            screen.blit(text_surface, text_rect)

def animate_word_panel_sequence(screen, word, guessed_letters, animation_type):
    """Run the animation sequence for the word panel"""
    clock = pygame.time.Clock()
    start_time = time.time()
    duration = 0.4  # Slightly faster animation

    # Store the current state of the screen
    screen_copy = screen.copy()

    while True:
        current_time = time.time()
        progress = (current_time - start_time) / duration

        if progress >= 1.0:
            break

        # Restore the screen state
        screen.blit(screen_copy, (0, 0))

        # Draw the animated word panel
        animate_word_panel(screen, word, guessed_letters, animation_type, progress)
        
        pygame.display.flip()
        clock.tick(60)

def reveal_word_animation(screen, word, guessed_letters, progress):
    """Animate the reveal of the correct word"""
    # Get current tier colors
    current_tier = get_current_tier(level)
    colors = TIER_COLORS[current_tier]

    # Base positions and sizes
    x_start = WIDTH // 2 - (len(word.replace(" ", "")) * 45) // 2
    y_start = 150
    cell_size = 40

    # Calculate how many letters to reveal based on progress
    total_letters = len(word.replace(" ", ""))
    # Adjust progress to ensure last letter is revealed
    adjusted_progress = min(1.0, progress * 1.1)  # Multiply by 1.1 to ensure full reveal
    letters_to_reveal = int(total_letters * adjusted_progress)
    
    # Draw the word's letters
    for i, letter in enumerate(word):
        if letter == " ":
            x_start += cell_size + 5
            continue

        rect_x = x_start + i * (cell_size + 5)
        pygame.draw.rect(screen, colors["word_box"], (rect_x, y_start, cell_size, cell_size), border_radius=5)

        # Reveal letters based on progress
        if i < letters_to_reveal or letter in guessed_letters:
            text_surface = LETTER_FONT.render(letter, True, colors["tier_text"])
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, y_start + cell_size // 2))
            screen.blit(text_surface, text_rect)

def reveal_word_sequence(screen, word, guessed_letters):
    """Run the word reveal animation sequence"""
    clock = pygame.time.Clock()
    start_time = time.time()
    duration = 1.0  # 1 second reveal animation

    # Store the current state of the screen
    screen_copy = screen.copy()

    while True:
        current_time = time.time()
        progress = (current_time - start_time) / duration

        if progress >= 1.0:
            break

        # Restore the screen state
        screen.blit(screen_copy, (0, 0))

        # Draw the word reveal animation
        reveal_word_animation(screen, word, guessed_letters, progress)
        
        pygame.display.flip()
        clock.tick(60)

# Modify the play_spellout function to use the new animation behavior
def play_spellout(uid_input, resumed=False):
    global game_started, game_over, level_completed, difficulty_selected
    global selected_word, shuffled_words, guessed_letters, attempts, level, game_mode, word_start_time

    start_time = time.time()
    total_time_bonus = 0  # Track accumulated time bonuses

    if not resumed:
        level = 1  # Start at level 1
        guessed_letters = set()
        attempts = 4
        selected_word = None
        game_started = False  # Changed to False to show mode selection first
        difficulty_selected = True  # No manual difficulty selection needed
        game_mode = None  # No default mode, player must choose
        # Initialize shuffled_words as a dictionary
        shuffled_words = {
            "Easy": [],
            "Normal": [],
            "Hard": []
        }

    # Track correctly guessed words for timed mode
    correct_words = 0

    keys = create_virtual_keyboard()
    running = True
    player_name = uid_input

    while running:
        # Only use level-based background during active gameplay
        if game_started and not (game_over or level_completed):
            current_bg = get_background_color(level)
            screen.blit(current_bg, (0, 0))
        else:
            screen.fill(WHITE)

        if not game_started:
            # Draw game mode selection screen
            button_rects = draw_game_controls(player_name, state='start')
        elif game_over:
            button_rects = draw_game_controls(player_name, state='over')
        elif level_completed:
            button_rects = draw_game_controls(player_name, state='complete')
        else:
            button_rects = draw_game_controls(player_name, state='in_game')
            draw_word(selected_word, guessed_letters)
            draw_virtual_keyboard(keys, guessed_letters)
            draw_attempts(attempts)
            draw_levels(level)
            
            if game_mode == "timed":
                if draw_timer():  # If time is up
                    # Play game over sound
                    game_over_sound.play()
                    
                    # Reveal the correct word with animation
                    reveal_word_sequence(screen, selected_word['word'], guessed_letters)
                    
                    pygame.time.delay(1000)
                    
                    # Check for tier completion before incrementing level
                    time_bonus = handle_word_completion(screen, level, game_mode, total_time_bonus)
                    total_time_bonus += time_bonus
                    
                    level += 1
                    guessed_letters.clear()
                    attempts = 4
                    
                    # Handle level 15 completion
                    if level > 15:  # After completing level 15
                        end_time = time.time()
                        duration = end_time - start_time
                        level_completed = True
                        update_player_record(uid_input, duration, correct_words, game_mode)
                        show_last_record(uid_input)
                    else:  # Levels 1-15
                        selected_word = get_word_for_level(level)
                        word_start_time = time.time()

        pygame.display.flip()
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not game_started:
                    if button_rects["classic"].collidepoint(mouse_pos):
                        game_started = True
                        game_mode = "classic"
                        selected_word = get_word_for_level(level)
                        word_start_time = time.time()
                        start_time = time.time()
                    elif button_rects["timed"].collidepoint(mouse_pos):
                        game_started = True
                        game_mode = "timed"
                        selected_word = get_word_for_level(level)
                        word_start_time = time.time()
                        start_time = time.time()

                elif game_over or level_completed:
                    if button_rects["classic"].collidepoint(mouse_pos):
                        game_over = False
                        level_completed = False
                        level = 1
                        guessed_letters.clear()
                        attempts = 4
                        correct_words = 0
                        total_time_bonus = 0
                        selected_word = get_word_for_level(level)
                        word_start_time = time.time()
                        start_time = time.time()
                    elif button_rects["quit"].collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif button_rects["leaderboard"].collidepoint(mouse_pos):
                        display_leaderboard(uid_input)
                    elif button_rects["last_record"].collidepoint(mouse_pos):
                        show_last_record(uid_input)

                elif not game_over:
                    for letter, rect in keys.items():
                        if rect.collidepoint(mouse_pos) and letter not in guessed_letters:
                            guessed_letters.add(letter)
                            
                            # Update the display immediately to show the key change
                            if game_started and not (game_over or level_completed):
                                current_bg = get_background_color(level)
                                screen.blit(current_bg, (0, 0))
                                draw_word(selected_word, guessed_letters)
                                draw_virtual_keyboard(keys, guessed_letters)
                                draw_attempts(attempts)
                                draw_levels(level)
                                pygame.display.flip()
                            
                            # Process the guess
                            if letter in selected_word['word']:
                                correct_sound.play()
                                if all(l in guessed_letters for l in selected_word['word']):
                                    # Store current state for animation
                                    current_guessed_letters = guessed_letters.copy()
                                    
                                    # Update display one more time before animation
                                    current_bg = get_background_color(level)
                                    screen.blit(current_bg, (0, 0))
                                    draw_word(selected_word, current_guessed_letters)
                                    draw_virtual_keyboard(keys, current_guessed_letters)
                                    draw_attempts(attempts)
                                    draw_levels(level)
                                    pygame.display.flip()
                                    
                                    # Play animation with current state
                                    animate_word_panel_sequence(screen, selected_word['word'], current_guessed_letters, "pop")
                                    pygame.time.delay(500)
                                    
                                    # Now update game state
                                    time_bonus = handle_word_completion(screen, level, game_mode, total_time_bonus)
                                    total_time_bonus += time_bonus
                                    
                                    level += 1
                                    if game_mode == "timed":
                                        correct_words += 1
                                    guessed_letters.clear()
                                    attempts = 4
                                    
                                    # Handle level completion
                                    if level > 15:  # After completing level 15
                                        end_time = time.time()
                                        duration = end_time - start_time
                                        level_completed = True
                                        update_player_record(uid_input, duration, correct_words if game_mode == "timed" else level - 1, game_mode)
                                        show_last_record(uid_input)
                                    else:  # Levels 1-15
                                        selected_word = get_word_for_level(level)
                                        word_start_time = time.time()
                            else:
                                attempts -= 1
                                wrong_sound.play()
                                
                                # Store current state for animation
                                current_guessed_letters = guessed_letters.copy()
                                
                                # Update display one more time before animation
                                current_bg = get_background_color(level)
                                screen.blit(current_bg, (0, 0))
                                draw_word(selected_word, current_guessed_letters)
                                draw_virtual_keyboard(keys, current_guessed_letters)
                                draw_attempts(attempts)
                                draw_levels(level)
                                pygame.display.flip()
                                
                                # Play animation with current state
                                animate_word_panel_sequence(screen, selected_word['word'], current_guessed_letters, "shake")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(uid_input, level, attempts, guessed_letters, selected_word, get_current_tier(level), shuffled_words)
                else:
                    guess = event.unicode.upper()
                    if guess in keys and guess not in guessed_letters:
                        guessed_letters.add(guess)
                        
                        # Update the display immediately to show the key change
                        if game_started and not (game_over or level_completed):
                            current_bg = get_background_color(level)
                            screen.blit(current_bg, (0, 0))
                            draw_word(selected_word, guessed_letters)
                            draw_virtual_keyboard(keys, guessed_letters)
                            draw_attempts(attempts)
                            draw_levels(level)
                            pygame.display.flip()
                        
                        # Process the guess
                        if guess in selected_word['word']:
                            correct_sound.play()
                            if all(l in guessed_letters for l in selected_word['word']):
                                # Store current state for animation
                                current_guessed_letters = guessed_letters.copy()
                                
                                # Update display one more time before animation
                                current_bg = get_background_color(level)
                                screen.blit(current_bg, (0, 0))
                                draw_word(selected_word, current_guessed_letters)
                                draw_virtual_keyboard(keys, current_guessed_letters)
                                draw_attempts(attempts)
                                draw_levels(level)
                                pygame.display.flip()
                                
                                # Play animation with current state
                                animate_word_panel_sequence(screen, selected_word['word'], current_guessed_letters, "pop")
                                pygame.time.delay(500)
                                
                                # Now update game state
                                time_bonus = handle_word_completion(screen, level, game_mode, total_time_bonus)
                                total_time_bonus += time_bonus
                                
                                level += 1
                                if game_mode == "timed":
                                    correct_words += 1
                                guessed_letters.clear()
                                attempts = 4
                                
                                # Handle level completion
                                if level > 15:  # After completing level 15
                                    end_time = time.time()
                                    duration = end_time - start_time
                                    level_completed = True
                                    update_player_record(uid_input, duration, correct_words if game_mode == "timed" else level - 1, game_mode)
                                    show_last_record(uid_input)
                                else:  # Levels 1-15
                                    selected_word = get_word_for_level(level)
                                    word_start_time = time.time()
                        else:
                            attempts -= 1
                            wrong_sound.play()
                            
                            # Store current state for animation
                            current_guessed_letters = guessed_letters.copy()
                            
                            # Update display one more time before animation
                            current_bg = get_background_color(level)
                            screen.blit(current_bg, (0, 0))
                            draw_word(selected_word, current_guessed_letters)
                            draw_virtual_keyboard(keys, current_guessed_letters)
                            draw_attempts(attempts)
                            draw_levels(level)
                            pygame.display.flip()
                            
                            # Play animation with current state
                            animate_word_panel_sequence(screen, selected_word['word'], current_guessed_letters, "shake")

        # ❌ LOSS CHECK (outside event loop)
        if not game_over and attempts == 0:
            # Store current state for animation
            current_guessed_letters = guessed_letters.copy()
            
            # Update display one last time before game over
            current_bg = get_background_color(level)
            screen.blit(current_bg, (0, 0))
            draw_word(selected_word, current_guessed_letters)
            draw_virtual_keyboard(keys, current_guessed_letters)
            draw_attempts(attempts)
            draw_levels(level)
            pygame.display.flip()
            
            # Play game over sound
            game_over_sound.play()
            
            # Shake animation with current state
            animate_word_panel_sequence(screen, selected_word['word'], current_guessed_letters, "shake")
            
            # Reveal the correct word with animation
            reveal_word_sequence(screen, selected_word['word'], current_guessed_letters)
            
            pygame.time.delay(500)
            game_over = True
            end_time = time.time()
            duration = end_time - start_time
            update_player_record(uid_input, duration, correct_words if game_mode == "timed" else level, game_mode)
            show_last_record(uid_input)

    pygame.quit()

# 🚀 Run the game
if __name__ == "__main__":
    welcome_screen()
