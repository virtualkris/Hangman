# 🎮 Main game function
def play_hangman():
    global game_started, game_over, difficulty_selected, selected_difficulty, selected_word
    
    level = 1  # Start at level 1
    guessed_letters = set()  # Store guessed letters
    attempts = 4  # Maximum incorrect guesses
    keys = create_virtual_keyboard()  # Generate virtual keyboard
    running = True  # Control game loop

    while running:
        screen.fill(WHITE)  # Reset screen

        if not game_started:
            draw_game_controls()
        elif game_started and not difficulty_selected:
            draw_difficulty_buttons()
        else:
            draw_game_controls()  # Draw Play Again button if needed
            draw_word(selected_word, guessed_letters)  # Display word as rectangles
            draw_virtual_keyboard(keys, guessed_letters)  # Draw the virtual keyboard
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

                if not game_started:
                    handle_button_click(mouse_pos)  # Start game or handle difficulty selection
                elif game_over and draw_game_controls().collidepoint(mouse_pos):  
                    # Reset game on "Play Again" click
                    game_over = False
                    level = 1
                    difficulty_selected = False  # Reset difficulty
                    guessed_letters.clear()
                    attempts = 4
                elif not game_over:  # Handle in-game clicks
                    for letter, rect in keys.items():
                        if rect.collidepoint(mouse_pos):
                            if letter not in guessed_letters:
                                guessed_letters.add(letter)
                                if letter in selected_word:
                                    correct_sound.play()

                                    if all(l in guessed_letters for l in selected_word):
                                        pygame.time.delay(500) ## Small delay before switching
                                        level += 1  # Move to the next level
                                        guessed_letters.clear()  # Reset guessed letters
                                        attempts = 4  # Reset attempts
                                        selected_word = get_word(selected_difficulty)
                                else:
                                    attempts -= 1
                                    wrong_sound.play()

                handle_button_click(event.pos)  # Handle difficulty buttons

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
                if level < 10:
                    level += 1
                    selected_word = random.choice(words_by_difficulty[selected_difficulty])
                    guessed_letters.clear()
                    attempts = 4
                else:
                    game_over = True  # 🚨 Game over after Level 10! 

            # ☠️ Check loss condition
            if not game_over and attempts == 0:
                game_over = True

    pygame.quit()
