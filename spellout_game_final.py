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

    resume_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 20, 160, 40)
    info_text = FONT.render("Press Enter for New Game", True, BLACK)

    running = True
    while running:
        screen.fill(WHITE)

        if saved_state:
            # Draw resume button
            pygame.draw.rect(screen, BLUE, resume_button, border_radius=8)
            resume_text = BUTTON_FONT.render("Resume", True, WHITE)
            text_rect = resume_text.get_rect(center=resume_button.center)
            screen.blit(resume_text, text_rect)

        # Always show new game option
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Clear saved game and proceed to UID screen
                    if os.path.exists("savegame.json"):
                        os.remove("savegame.json")
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

# Function to display the leaderboard
def display_leaderboard():
    player_data = load_player_data()
    sorted_players = sorted(player_data.items(), key=lambda x: x[1]['level'], reverse=True)

    screen.fill(WHITE)

    title_font = pygame.font.Font(None, 40)
    title_surface = title_font.render("Leaderboard", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 30))

    list_font = pygame.font.Font(None, 30)
    y_offset = 100

    if sorted_players:
        for idx, (uid, data) in enumerate(sorted_players[:10]):
            player_info = f"{idx + 1}. {uid} - Level: {data['level']} - Duration: {data['duration']:.2f}s"
            player_surface = list_font.render(player_info, True, BLACK)
            screen.blit(player_surface, (WIDTH // 2 - player_surface.get_width() // 2, y_offset))
            y_offset += 25
    else:
        empty_msg = list_font.render("No data available.", True, (100, 0, 0))
        screen.blit(empty_msg, (WIDTH // 2 - empty_msg.get_width() // 2, y_offset))

    # Back to main menu button
    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 40)
    pygame.draw.rect(screen, BLUE, back_button, border_radius=8)
    back_text = list_font.render("Back to Main", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

    pygame.display.flip()

    # Event loop for back button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

# Function to show the last record of a player
def show_last_record(uid_input):
    player_data = load_player_data()

    screen.fill(WHITE)
    title_font = pygame.font.Font(None, 40)
    info_font = pygame.font.Font(None, 30)

    title_surface = title_font.render("Your Last Record", True, BLACK)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 30))

    if uid_input in player_data:
        info = player_data[uid_input]
        level_text = info_font.render(f"Last Level: {info['level']}", True, BLACK)
        duration_text = info_font.render(f"Duration: {info['duration']:.2f}s", True, BLACK)
        last_played_text = info_font.render(f"Last Played: {info['last_played']}", True, BLACK)

        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 100))
        screen.blit(duration_text, (WIDTH // 2 - duration_text.get_width() // 2, 150))
        screen.blit(last_played_text, (WIDTH // 2 - last_played_text.get_width() // 2, 200))
    else:
        error_msg = info_font.render("No record found for this player.", True, (200, 0, 0))
        screen.blit(error_msg, (WIDTH // 2 - error_msg.get_width() // 2, 150))

    # Back button
    back_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 80, 150, 40)
    pygame.draw.rect(screen, BLUE, back_button, border_radius=8)
    back_text = info_font.render("Back to Main", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return
                
# 🎮 Function to draw game controls
def draw_game_controls(player_name=None, state='start'):
    button_color = (71, 185, 112)      # Green
    border_color = (12, 192, 223)      # Cyan
    quit_button_color = (255, 0, 0)    # Red
    leaderboard_button_color = (100, 150, 255)  # Blue
    last_record_button_color = (255, 223, 100)  # Yellow
    text_color = (0, 0, 0)             # Black

    button_x = WIDTH // 2 - 80
    button_y = HEIGHT // 2 - 100
    button_width = 160
    button_height = 50
    spacing = button_height + 10
    current_y = button_y + spacing

    font = pygame.font.Font(None, 30)
    button_rects = [None, None, None, None]  # [main, quit, leaderboard, last_record]

    # ✳️ STATE-SPECIFIC UI
    if state == 'start':
        text = f"Welcome {player_name}!"
        play_text = "PLAY"

        # Title Text
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, button_y - 30)))

        # PLAY button
        pygame.draw.rect(screen, border_color, (button_x - 4, button_y - 4, button_width + 10, button_height + 10), border_radius=10)
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=8)
        play_surface = font.render(play_text, True, text_color)
        screen.blit(play_surface, play_surface.get_rect(center=(WIDTH // 2, button_y + button_height // 2)))
        button_rects[0] = pygame.Rect(button_x, button_y, button_width, button_height)

        # LEADERBOARD button
        pygame.draw.rect(screen, leaderboard_button_color, (button_x, current_y, button_width, button_height), border_radius=8)
        lb_surface = font.render("LEADERBOARD", True, text_color)
        screen.blit(lb_surface, lb_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects[2] = pygame.Rect(button_x, current_y, button_width, button_height)

    elif state in ('over', 'complete'):
        if state == 'over':
            text = "GAME OVER! WANT TO PLAY AGAIN?"
        else:
            text = "CONGRATULATIONS! YOU COMPLETED 10 LEVELS!"
        play_text = "PLAY AGAIN"

        # Title Text
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, button_y - 30)))

        # PLAY AGAIN button
        pygame.draw.rect(screen, border_color, (button_x - 4, button_y - 4, button_width + 10, button_height + 10), border_radius=10)
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height), border_radius=8)
        play_surface = font.render(play_text, True, text_color)
        screen.blit(play_surface, play_surface.get_rect(center=(WIDTH // 2, button_y + button_height // 2)))
        button_rects[0] = pygame.Rect(button_x, button_y, button_width, button_height)

        # LEADERBOARD
        pygame.draw.rect(screen, leaderboard_button_color, (button_x, current_y, button_width, button_height), border_radius=8)
        lb_surface = font.render("LEADERBOARD", True, text_color)
        screen.blit(lb_surface, lb_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects[2] = pygame.Rect(button_x, current_y, button_width, button_height)

        # LAST RECORD
        current_y += spacing
        pygame.draw.rect(screen, last_record_button_color, (button_x, current_y, button_width, button_height), border_radius=8)
        lr_surface = font.render("LAST RECORD", True, text_color)
        screen.blit(lr_surface, lr_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects[3] = pygame.Rect(button_x, current_y, button_width, button_height)

        # QUIT
        current_y += spacing
        pygame.draw.rect(screen, quit_button_color, (button_x, current_y, button_width, button_height), border_radius=8)
        quit_surface = font.render("QUIT", True, text_color)
        screen.blit(quit_surface, quit_surface.get_rect(center=(WIDTH // 2, current_y + button_height // 2)))
        button_rects[1] = pygame.Rect(button_x, current_y, button_width, button_height)

    elif state == 'in_game':
        # Optional: add a status bar, timer, or score here if needed.
        return None, None, None, None

    return tuple(button_rects)  # main, quit, leaderboard, last_record

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

# Functions to save the game state
def pause_menu(uid_input, level, attempts, guessed_letters, selected_word, selected_difficulty, shuffled_words):
    paused = True
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    resume_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 - 40, 150, 40)
    save_exit_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2 + 10, 150, 40)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Resume
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(pos):
                    paused = False
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
        pygame.draw.rect(screen, BLUE, resume_button)
        pygame.draw.rect(screen, ORANGE, save_exit_button)

        screen.blit(BUTTON_FONT.render("Resume", True, WHITE), (resume_button.x + 20, resume_button.y + 8))
        screen.blit(BUTTON_FONT.render("Save and Exit", True, WHITE), (save_exit_button.x + 10, save_exit_button.y + 8))

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

# Function to get a random word based on difficulty
def get_word(difficulty):
    global shuffled_words

    if not shuffled_words:
        shuffled_words = words_by_difficulty[difficulty][:]
        random.shuffle(shuffled_words)

    return shuffled_words.pop() ## Get a word from the shuffled list

# Function to handle button clicks
def handle_button_click(pos):
    global game_started, game_over, attempts, level, selected_word, guessed_letters
    global selected_difficulty, difficulty_selected, shuffled_words

    button_x = WIDTH // 2 - 80  # Centered button
    button_y = HEIGHT // 2 - 100
    button_width = 160
    button_height = 50

    # Check if the Play or Play Again button is clicked
    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        game_started = True
        game_over = False
        level = 0  # Restart from level 0
        attempts = 4
        guessed_letters.clear()
        difficulty_selected = False  # Reset difficulty selection
        shuffled_words = []  # Clear previously shuffled words
        return

    # Check if a difficulty button is clicked after starting the game
    if game_started and not difficulty_selected:
        difficulty_buttons = draw_difficulty_buttons()
        for difficulty, rect in difficulty_buttons.items():
            if rect.collidepoint(pos):
                selected_difficulty = difficulty
                difficulty_selected = True

                shuffled_words = words_by_difficulty[selected_difficulty][:]
                random.shuffle(shuffled_words)

                if shuffled_words:
                    selected_word = shuffled_words.pop()
                return

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

# 🎮 Main game function
def play_spellout(uid_input, resumed=False):
    global game_started, game_over, level_completed, difficulty_selected, selected_difficulty, selected_word, shuffled_words, guessed_letters, attempts, level

    start_time = time.time()

    # 🆕 Restore from resume if available
    if not resumed:
        level = 0
        guessed_letters = set()
        attempts = 4
        selected_word = ""
        selected_difficulty = ""
        shuffled_words = []
        game_started = False
        difficulty_selected = False

    keys = create_virtual_keyboard()
    running = True
    player_name = uid_input

    while running:
        screen.fill(WHITE)

        # 🎨 Draw UI based on state
        if not game_started:
            main_button_rect, quit_button_rect, leaderboard_button_rect, last_record_button_rect = draw_game_controls(player_name, state='start')
        elif game_started and not difficulty_selected:
            draw_difficulty_buttons()
        elif game_over:
            main_button_rect, quit_button_rect, leaderboard_button_rect, last_record_button_rect = draw_game_controls(player_name, state='over')
        elif level_completed:
            main_button_rect, quit_button_rect, leaderboard_button_rect, last_record_button_rect = draw_game_controls(player_name, state='complete')
        else:
            draw_game_controls(player_name, state='in_game')
            draw_word(selected_word, guessed_letters)
            draw_virtual_keyboard(keys, guessed_letters)
            draw_attempts(attempts)
            draw_levels(level)

        pygame.display.flip()
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not game_started:
                    if main_button_rect.collidepoint(mouse_pos):
                        game_started = True
                    elif leaderboard_button_rect.collidepoint(mouse_pos):
                        display_leaderboard()

                elif not difficulty_selected:
                    handle_button_click(mouse_pos)

                elif game_over or level_completed:
                    if main_button_rect.collidepoint(mouse_pos):
                        game_over = False
                        level_completed = False
                        level = 0
                        difficulty_selected = False
                        guessed_letters.clear()
                        attempts = 4
                        selected_word = get_word(selected_difficulty)
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif leaderboard_button_rect.collidepoint(mouse_pos):
                        display_leaderboard()
                    elif last_record_button_rect.collidepoint(mouse_pos):
                        show_last_record(uid_input)
                    else:
                        handle_button_click(mouse_pos)

                elif not game_over:
                    for letter, rect in keys.items():
                        if rect.collidepoint(mouse_pos) and letter not in guessed_letters:
                            guessed_letters.add(letter)
                            if letter in selected_word['word']:
                                correct_sound.play()
                                if all(l in guessed_letters for l in selected_word['word']):
                                    show_word_flash(screen, selected_word['word'], (0, 255, 0), FONT)
                                    pygame.time.delay(500)
                                    level += 1
                                    guessed_letters.clear()
                                    attempts = 4
                                    selected_word = get_word(selected_difficulty)
                                    if level == 10:
                                        level_completed = True
                                        break
                            else:
                                attempts -= 1
                                wrong_sound.play()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(uid_input, level, attempts, guessed_letters, selected_word, selected_difficulty, shuffled_words)  # 🆕
                else:
                    guess = event.unicode.upper()
                    if guess in keys and guess not in guessed_letters:
                        guessed_letters.add(guess)
                        if guess in selected_word['word']:
                            correct_sound.play()
                        else:
                            attempts -= 1
                            wrong_sound.play()


            # ✅ Win check
            if difficulty_selected and not game_over and all(l in guessed_letters for l in selected_word['word']):
                show_word_flash(screen, selected_word['word'], (0, 255, 0), FONT)
                pygame.time.delay(500)
                if level < 10:
                    level += 1
                    selected_word = get_word(selected_difficulty)
                    guessed_letters.clear()
                    attempts = 4
                else:
                    level_completed = True
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"Player UID: {uid_input}, Duration: {duration}, Level: {level}")
                    update_player_record(uid_input, duration, level)
                    break

            # ❌ Loss check
            if not game_over and attempts == 0:
                show_word_flash(screen, selected_word['word'], (255, 0, 0), FONT)
                pygame.time.delay(500)
                game_over = True
                end_time = time.time()
                duration = end_time - start_time
                print(f"Player UID: {uid_input}, Duration: {duration}, Level: {level}")
                update_player_record(uid_input, duration, level)

    pygame.quit()

# 🚀 Run the game
if __name__ == "__main__":
    welcome_screen()
