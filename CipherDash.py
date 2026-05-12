import sys, os
import pygame
import random, itertools

pygame.init()
pygame.font.init()
pygame.mixer.init()

################################################################
################################################################

# Display
WIDTH, HEIGHT = 900, 700
FPS = 48
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(pygame.image.load(os.path.join("Assets", "game_icon.png")))
pygame.display.set_caption("Cipher Dash")


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN_CYAN = (69, 127, 119)


# Fonts
MENU_FONT = pygame.font.SysFont("comicsans ms", 34)
TITLE_FONT = pygame.font.SysFont("comicsans ms", 24)
POP_FONT = pygame.font.SysFont("Tahoma", 40)
DIGITS_FONT = pygame.font.SysFont("segoeui", 36)
TEXT_FONT = pygame.font.SysFont("arial", 19)
SIGNATURE_FONT = pygame.font.SysFont("lucida sans", 10)

# Sounds
SELECT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "clicking_sound_effect.wav"))

################################################################
################################################################

# Game Instances
class Button:
    def __init__(self, text, w, h, pos, elev):
        # Core attributes
        self.pressed = False
        self.clicked = False
        self.elevation = elev
        self.dynamic_elevation = self.elevation
        self.original_y = pos[1]

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (w, h))
        self.top_color = GREEN_CYAN

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (w-2, self.elevation))
        self.bottom_color = (53, 75, 94)

        # Text
        self.text_surf = MENU_FONT.render(text, 1, WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # Elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(WIN, self.bottom_color, self.bottom_rect, border_radius=16)
        pygame.draw.rect(WIN, self.top_color, self.top_rect, border_radius=16)
        WIN.blit(self.text_surf, self.text_rect)
        self.check_click()
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.top_rect.collidepoint(mouse_pos)):
            self.top_color = (215, 75, 75)
            if (pygame.mouse.get_pressed()[0]):
                self.pressed = True
                self.dynamic_elevation = 0
            elif (self.pressed):
                SELECT_SOUND.play()
                pygame.time.wait(164)
                self.pressed = False
                self.clicked = True
                self.dynamic_elevation = self.elevation
        else:
            self.pressed = False
            self.clicked = False
            self.top_color = GREEN_CYAN
            self.dynamic_elevation = self.elevation


button1 = Button("New Game", 300, 100, (WIDTH//2-150, 100), 10)
button2 = Button("Instructions", 300, 100, (WIDTH//2-150, 260), 10)
button3 = Button("About Me", 300, 100, (WIDTH//2-150, 380), 10)
button4 = Button("Exit", 300, 100, (WIDTH//2-150, 500), 10)
button5 = Button("<—", 90, 40, (20, 20), 5)
button6 = Button("Yes", 100, 50, (246, 420), 5)
button7 = Button("No", 100, 50, (566, 420), 5)
button8 = Button("Reset", 140, 45, (WIDTH-160, 20), 7)
button9 = Button("Ok", 100, 50, (400, 420), 7)


possible_numbers, previous_feedback = [], None
L, texts, text_boxes = 0, [], []
attempts, scale_factor, computer_number = 1, 1.00, 0
user_guess, user_feedback, done = "", "", True
computer_won, player_won, fb_error = False, False, False

################################################################
################################################################


def generate_possible_numbers():
    foo = []
    for perm in itertools.permutations('0123456789', 4):
        number = "".join(perm)
        if number[0] != '0' and len(set(number)) == 4:
            foo.append(number)
    return foo

def get_feedback(secret, guess):
    plus, minus = 0, 0
    for i in range(4):
        if guess[i] == secret[i]:
            plus += 1
        elif guess[i] in secret:
            minus += 1
    return plus, minus

def computer_guess_number():

    if previous_feedback is None:
        guess = random.choice(possible_numbers)  # Initial random guess
    else:
        guess = make_smart_guess(possible_numbers, previous_feedback)

    return guess

def make_smart_guess(possible_numbers, previous_feedback):
    best_guess = None
    best_score = -1  # Initialize to a lower value

    for number in possible_numbers:
        # Calculate the number of remaining possibilities consistent with the feedback
        consistent_count = sum(1 for other in possible_numbers if get_feedback(other, number) == previous_feedback)

        # Update the best_guess if the current number is more consistent
        if consistent_count > best_score:
            best_guess = number
            best_score = consistent_count

    if best_guess is not None:
        return best_guess
    else:
        return random.choice(possible_numbers)

def updated_possible_numbers(possible_numbers, guess, plus, minus):
    updated_possible_numbers = []
    for number in possible_numbers:
        if get_feedback(number, guess) == (plus, minus):
            updated_possible_numbers.append(number)
    return updated_possible_numbers


################################################################
################################################################


def draw_menu():
    button1.draw()
    button2.draw()
    button3.draw()
    button4.draw()

def draw_text_box():
    outer_square = pygame.Rect(30, 80, WIDTH - 60, HEIGHT - 115)
    pygame.draw.rect(WIN, GREEN_CYAN, outer_square, 8, border_radius=24)

def handle_game():

    border = pygame.Rect(WIDTH // 2 - 7, 70, 14, HEIGHT - 110)
    left_border = pygame.Rect(WIDTH // 4 - 3, 150, 6, HEIGHT - 200)
    right_border = pygame.Rect(3 * WIDTH // 4 + 10, 150, 6, HEIGHT - 200)
    pygame.draw.rect(WIN, (85, 127, 129), border, border_radius=6) 
    pygame.draw.rect(WIN, GREEN_CYAN, left_border, border_radius=4)
    pygame.draw.rect(WIN, GREEN_CYAN, right_border, border_radius=4)

    # Titles of the running game
    text11 = TITLE_FONT.render("Your Guess", 1, BLACK)
    text12 = TITLE_FONT.render("Feedback", 1, BLACK)
    text21 = TITLE_FONT.render("CPU's Guess", 1, BLACK)
    text22 = TITLE_FONT.render("Feedback", 1, BLACK)

    if (L == 0):
        text11 = TITLE_FONT.render("Your Guess", 1, RED)
    elif (L == 1):
        text22 = TITLE_FONT.render("Feedback", 1, RED)
        

    WIN.blit(text11, (text11.get_width()//2 - 7, 110))
    WIN.blit(text12, (WIDTH//4 + text12.get_width()//2, 110))
    WIN.blit(text21, (WIDTH//2 + text21.get_width()//2 - 14, 110))
    WIN.blit(text22, (3*WIDTH//4 + text22.get_width()//2 + 14, 110))

    # Handling guesses and feedbacks
    t = 0
    for i in text_boxes:
        if (t % 2 == 0):
            pygame.draw.rect(WIN, GREEN_CYAN, i, 3, border_top_left_radius=20, border_bottom_left_radius=20)
        else:
            pygame.draw.rect(WIN, GREEN_CYAN, i, 3, border_top_right_radius=20, border_bottom_right_radius=20)
        t += 1
    
    for j in range(len(texts)):
        if (j % 2 == 0):
            WIN.blit(texts[j], (text_boxes[j].x + 40, text_boxes[j].y - 7))
        else:
            WIN.blit(texts[j], (text_boxes[j].x + 25, text_boxes[j].y - 8))

    if not player_won and not computer_won and not fb_error:
        cursor_x, cursor_y = 0, text_boxes[-1].y - 12
        if (L == 0):
            cursor_x = text_boxes[(attempts - 1)*4].x + 45 + DIGITS_FONT.size(user_guess)[0]
        else:
            cursor_x = text_boxes[-1].x + 30 + DIGITS_FONT.size(user_feedback)[0]
        cursor_surf = DIGITS_FONT.render("_", 1, RED)
        WIN.blit(cursor_surf, (cursor_x, cursor_y))

def resetting():
    global texts, text_boxes, possible_numbers, previous_feedback, L, user_guess, user_feedback, computer_number, done, computer_won, player_won, fb_error
    texts, text_boxes, possible_numbers = [], [], generate_possible_numbers()
    previous_feedback, L = None, 0
    user_guess, user_feedback, done = "", "", True
    computer_number = random.choice(possible_numbers)
    computer_won, player_won, fb_error = False, False, False
    button9.clicked, button8.clicked = False, False

def handle_quit():
    confirmation_top = pygame.Rect(203, 197, 506, 306)
    confirmation_window = pygame.Rect(206, 200, 500, 300)
    pygame.draw.rect(WIN, GREEN_CYAN, confirmation_top, 3, border_radius=24)
    pygame.draw.rect(WIN, (220, 220, 220), confirmation_window, border_radius=24)
    confirmation_surf = POP_FONT.render("Go Back To Main Menu ?", 1, BLACK)
    WIN.blit(confirmation_surf, (confirmation_window.x + 36, confirmation_window.y + 90))
    button6.draw()
    button7.draw()

def handle_feedback_error():
    error_top = pygame.Rect(203, 197, 506, 306)
    error_window = pygame.Rect(206, 200, 500, 300)
    pygame.draw.rect(WIN, GREEN_CYAN, error_top, 3, border_radius=24)
    pygame.draw.rect(WIN, (220, 220, 220), error_window, border_radius=24)
    error_surf = POP_FONT.render("Oops!", 1, BLACK)
    error1_surf = POP_FONT.render("You made an error in your", 1, BLACK)
    error2_surf = POP_FONT.render("previous feedbacks", 1, BLACK)
    WIN.blit(error_surf, (error_window.x + 200, error_window.y + 35))
    WIN.blit(error1_surf, (error_window.x + 16, error_window.y + 90))
    WIN.blit(error2_surf, (error_window.x + 85, error_window.y + 135))
    button9.draw()

def handle_win():
    finished_top = pygame.Rect(203, 197, 506, 306)
    finished_window = pygame.Rect(206, 200, 500, 300)
    pygame.draw.rect(WIN, GREEN_CYAN, finished_top, 3, border_radius=24)
    pygame.draw.rect(WIN, (220, 220, 220), finished_window, border_radius=24)
    if player_won:
        finished_surf = POP_FONT.render("Congratulations!", 1, BLACK)
        finished1_surf = POP_FONT.render("You successfully managed", 1, BLACK)
        finished2_surf = POP_FONT.render("to crack the computer's", 1, BLACK)
        finished3_surf = POP_FONT.render(f"number in {attempts} "+("attempts..." if attempts > 1 else "attempt..."), 1, BLACK)
    elif computer_won:
        finished_surf = POP_FONT.render("Unfortunately!", 1, BLACK)
        finished1_surf = POP_FONT.render("The computer successfully", 1, BLACK)
        finished2_surf = POP_FONT.render("managed to crack your", 1, BLACK)
        tempo_att = attempts - 1
        finished3_surf = POP_FONT.render(f"number in {tempo_att} "+("attempts..." if tempo_att > 1 else "attempt..."), 1, BLACK)

    WIN.blit(finished_surf, (finished_window.x + 120, finished_window.y + 20))
    WIN.blit(finished1_surf, (finished_window.x + 12, finished_window.y + 70))
    WIN.blit(finished2_surf, (finished_window.x + 12, finished_window.y + 110))
    WIN.blit(finished3_surf, (finished_window.x + 12, finished_window.y + 150))
    button9.draw()


################################################################
################################################################


def display_instructions():
    foo = []
    foo.append(MENU_FONT.render("Welcome to Cipher Dash Game!", 1, BLACK))
    foo.append(TEXT_FONT.render("In this exciting and challenging game, you'll be engaged in a thrilling battle of wits against the computer.", 1, BLACK))
    foo.append(TEXT_FONT.render("Both you and the computer will take turns trying to guess each other's secret 4-digit number.", 1, BLACK))
    foo.append(TEXT_FONT.render("   Here's how it works:", 1, BLACK))
    foo.append(TEXT_FONT.render("You and the computer each select a secret 4-digit number with no repeating digits,", 1, BLACK))
    foo.append(TEXT_FONT.render("choosing from the range of 0-9, ensuring there are no leading zeros.", 1, BLACK))
    foo.append(TEXT_FONT.render("The computer will make its initial guess, and you will make yours as well.", 1, BLACK))
    foo.append(TEXT_FONT.render("After each guess, both you and the computer will provide feedback in the form of '+/-' signs,", 1, BLACK))
    foo.append(TEXT_FONT.render("to indicate how close the guess is to the secret number.", 1, BLACK))
    foo.append(TEXT_FONT.render("A ' + ' means a digit in the guess is correct and in the right position.", 1, BLACK))
    foo.append(TEXT_FONT.render("A ' - ' means a digit in the guess is correct but in the wrong position.", 1, BLACK))
    foo.append(TEXT_FONT.render("A ' / ' means no digit in the guess is correct.", 1, BLACK))
    foo.append(TEXT_FONT.render("Both you and the computer will use this feedback to adjust your future guesses,", 1, BLACK))
    foo.append(TEXT_FONT.render("narrowing down the possibilities with each turn.", 1, BLACK))
    foo.append(TEXT_FONT.render("The game continues until one of you correctly guesses the other's secret number,", 1, BLACK))
    foo.append(TEXT_FONT.render("or until an error in the feedback is uncovered.", 1, BLACK))
    foo.append(TEXT_FONT.render("   Can you outsmart the computer and crack its secret code while keeping your own hidden?", 1, BLACK))
    foo.append(TEXT_FONT.render("Or will the computer's algorithmic logic lead it to uncover your secret, while you struggle to decipher its number?", 1, BLACK))
    foo.append(TEXT_FONT.render("Test your skills in this captivating game of strategy and deduction!", 1, BLACK))
    foo.append(TEXT_FONT.render("Good luck, and may the best codebreaker emerge victorious!", 1, BLACK))

    WIN.blit(foo[0], (WIDTH//2 - foo[0].get_width()//2, 90))
    WIN.blit(foo[1], (60, foo[0].get_height() + 92))
    for i in range(2, len(foo)):
        WIN.blit(foo[i], (60, 85 + sum(5 + foo[k].get_height() for k in range(0, i))))

def display_about():
    about_text = [
        "Hello!",
        "My name is Benbouzid Ahmed Abdennour, a.k.a Shayx. I'm currently",
        "a 2nd-year student at the Higher National School of Computer",
        "Science in Algiers, Algeria.",
        "I have a strong passion for both game development and machine learning.",
        "I'm dedicated to learning and exploring new technologies in these fields,",
        "and I'm excited to combine my knowledge and skills, to create",
        "innovative projects in the future.",
        "Thanks for visiting!"
    ]

    # Display the "About Me" text
    for i, line in enumerate(about_text):
        text_surf = pygame.font.SysFont("georgia", 24).render(line, 1, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (55, 140 + i * (text_surf.get_height() + 20))  # Adjust the position as needed
        WIN.blit(text_surf, text_rect)

def draw_window():
    global computer_won, player_won
    WIN.fill(GRAY)
    signature_surf = SIGNATURE_FONT.render(" Benbouzid Ahmed Abdennour™  ", 1, BLACK)
    WIN.blit(signature_surf, (WIDTH - signature_surf.get_width() - 4, HEIGHT - signature_surf.get_height() - 2))

    # New Game
    if (button1.clicked):
        
        handle_game()
        if button8.clicked:
            resetting()
        if button5.clicked:
            if len(texts) > 1:
                handle_quit()
                if button6.clicked:
                    button1.clicked = False
                    button5.clicked = False
                    resetting()
                    draw_menu()
                elif button7.clicked:
                    button5.clicked = False
            else:
                resetting()
                button1.clicked = False
                button5.clicked = False
                draw_menu()
        else:
            if (fb_error) and (not button9.clicked):
                handle_feedback_error()
            elif (computer_won or player_won) and (not button9.clicked):
                    handle_win()
            else:
                button5.draw()
                button8.draw()

    
    # Instructions
    elif (button2.clicked):
        
        button5.draw()
        draw_text_box()
        display_instructions()
        if (button5.clicked):
            draw_menu()
            button2.clicked = False
            button5.clicked = False

    # About Me
    elif (button3.clicked):
        button5.draw()
        draw_text_box()
        display_about()
        if (button5.clicked):
            draw_menu()
            button3.clicked = False
            button5.clicked = False

    # Exit Game
    elif (button4.clicked):
        return

    # Main Menu
    else:
        draw_menu()


    pygame.display.update()


################################################################
################################################################


def main():

    global possible_numbers, previous_feedback, computer_number, text_boxes
    global L, attempts, scale_factor, computer_number
    global user_guess, user_feedback, done
    global computer_won, player_won, fb_error

    possible_numbers = generate_possible_numbers()
    computer_number = random.choice(possible_numbers)
    clock = pygame.time.Clock()

    run = True
    while run:

        clock.tick(FPS)

        attempts = 1 + (len(texts) // 4) - (0 if done else 1)
        scale_factor = 1.25 + (len(texts) // 4) - (0 if done else 1)

        if button1.clicked and not player_won and not computer_won and not fb_error:
            if (len(text_boxes) < 4 * attempts):
                text_boxes.append(pygame.Rect(36, 100 + (attempts+scale_factor)*30, 150, 40))
                text_boxes.append(pygame.Rect(271, 100 + (attempts+scale_factor)*30, 150, 40))
                text_boxes.append(pygame.Rect(490, 100 + (attempts+scale_factor)*30, 150, 40))
                text_boxes.append(pygame.Rect(736, 100 + (attempts+scale_factor)*30, 150, 40))

        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                
            if button1.clicked:
                if not button5.clicked and not player_won and not computer_won and not fb_error:
                    if event.type == pygame.KEYDOWN:
                        if done:
                            if (len(texts) % 4 == 0):
                                ch = event.unicode
                                if ch in "123456789":
                                    user_guess += ch
                                    temp_surf = DIGITS_FONT.render(user_guess, 1, BLACK)
                                    texts.append(temp_surf)
                            else:
                                ch = event.unicode
                                if len(user_guess) == 0:
                                    if ch in "123456789":
                                        user_guess += ch
                                else:
                                    if ch in "0123456789" and ch not in user_guess and len(user_guess) < 4:
                                        user_guess += ch

                                if event.key == pygame.K_BACKSPACE:
                                    user_guess = user_guess[:-1]

                                temp_surf = DIGITS_FONT.render(user_guess, 1, BLACK)
                                texts[-1] = temp_surf
                            
                                if event.key == pygame.K_RETURN:
                                    if len(user_guess) == 4:
                                        texts[-1] = temp_surf
                                        rr, r = [], ""
                                        for h in range(len(user_guess)):
                                            if (user_guess[h] == computer_number[h]):
                                                rr.append("+")
                                            elif (user_guess[h] in computer_number):
                                                rr.append("-")
                                                
                                        user_guess = ""
                                        if len(rr) == 0:
                                            r = "/ / / /"
                                        else:
                                            random.shuffle(rr)
                                            r = "".join(rr)

                                        temp_surf = DIGITS_FONT.render(r, 1, BLACK)
                                        texts.append(temp_surf)

                                        if r == "++++":
                                            player_won = True
                                            L = 3
                                            break

                                        r = computer_guess_number()
                                        temp_surf = DIGITS_FONT.render(r, 1, BLACK)
                                        texts.append(temp_surf)
                                        L = 1
                                        done = False
                        
                        else:
                            ch = event.unicode
                            if len(user_feedback) < 4:
                                if ch == "+" or ch == "-":
                                    user_feedback += ch
                                elif ch == "/":
                                    user_feedback = "/ / / /"
                            if event.key == pygame.K_BACKSPACE:
                                if "/" in user_feedback:
                                    user_feedback = ""
                                else:
                                    user_feedback = user_feedback[:-1]

                            temp_surf = DIGITS_FONT.render(user_feedback, 1, BLACK)
                            if len(texts) % 4 == 3:
                                texts.append(temp_surf)
                            else:
                                texts[-1] = temp_surf
                            
                            if event.key == pygame.K_RETURN:
                                done = True
                                plus, minus = user_feedback.count("+"), user_feedback.count("-")
                                previous_feedback = (plus, minus)
                                possible_numbers = updated_possible_numbers(possible_numbers, r, plus, minus)
                                user_feedback = ""
                                L = 0
                            if possible_numbers == []:
                                fb_error = True
                                L = 1
                            elif (previous_feedback and previous_feedback[0] == 4):
                                computer_won = True  
                                L = 3

            elif button4.clicked:
                run = False
                pygame.time.wait(40)
                pygame.quit()
                sys.exit()


        draw_window()  
   

################################################################
################################################################


if __name__ == "__main__":
    main()
