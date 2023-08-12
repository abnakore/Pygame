# importing required libraries
import pygame
import pygame_textinput
import os, sys

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# initialize pygame
pygame.init()

# ------------------------------- CLASSES(OBJECTS) ------------------------------- #

from resources.classes import *

# ----------------------------------- VARIABLES ---------------------------------- #

# Background color
color = (100, 160, 150)

# the game window
WINDOW_SIZE = (1000, 700)
window = pygame.display.set_mode(WINDOW_SIZE)
# Fill the window with the color
window.fill(color)

# The game title
pygame.display.set_caption("Are You A Math Whiz?")
# Setting the game icon
pygame.display.set_icon(pygame.image.load(resource_path(f"datas/icon.png")))

# Scores
scores = 0
# Questions asked
questions = []

# Timer
Timer = pygame.time.Clock()

# Exit button
exit_button = pygame.transform.scale(pygame.image.load(resource_path("datas/exit_button.png")), (90, 60))

# ------------------------------- FUNCTIONS -------------------------------#

from resources.functions import *

# Displaying a Splash screen
def splash_screen():
    """Display Splash Screen"""
    # Loading the splash screen image and scaling it to the size of the window
    splash_screen = pygame.transform.scale(
        pygame.image.load(resource_path(f"datas/icon.png")), WINDOW_SIZE
    )
    # Getting the splash screeen rect
    splash_screen_rect = splash_screen.get_rect()
    # Making the splash screen to display at the center of the screen
    splash_screen_rect.center = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)
    # Placing the splash screen on the window
    window.blit(splash_screen, splash_screen_rect)
    # Draw screen
    pygame.display.flip()
    # Wait 1 second  and hide splash screen
    pygame.time.wait(1000)
    window.fill(color)

# Instructions
def instruction():
    # Display a header 'How To Play'
    header_rect = display_text(
        "How To Play",
        (0, 0, 0),
        "Helvetica",
        30,
        (10, 10),
        "topleft",
        window
    )

    # How to play(the instructions)
    with open(resource_path("datas/README.txt")) as readme:
        text = readme.read()

    # Display the instructions
    display_text(
        text,
        (0, 0, 0),
        "Helvetica",
        20,
        (10, header_rect.bottom),
        "topleft",
        window
    )

    # Instruction for leaving the page
    display_text(
        'Click anywhere to leave',
        'small',
        "Helvetica",
        20,
        (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]-30),
        "topcenter",
        window
    )

    pygame.display.flip()

    wait_until_clicked()
    
    window.fill(color)

# Home Screen
def Home_screen():
    play_button = Button(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, 180, 80, "PLAY")
    instruction_button = Button(WINDOW_SIZE[0] / 2, (play_button.rect.bottom + 50), 250, 80, "Instructions")

    running = True

    while running:
        # Handling events
        for event in pygame.event.get():
            # Handling the quit event
            if event.type == pygame.QUIT:
                exit_game()

        # Update the buttons thereby checking if they where clicked
        output = play_button.process()
        instruction_button.process()
        # If it is pressed(Found output) exit loop
        if output:
            running = False

        # Updating the buttons and drawing them on screen
        play_button.update()
        instruction_button.update()
        window.blit(play_button.image, play_button.rect)
        window.blit(instruction_button.image, instruction_button.rect)

        # displaying the screen
        pygame.display.flip()

    window.fill(color, play_button)
    window.fill(color, instruction_button)

    wait_until_mouseUp()

# Select
def select(*items) -> str:
    """
        Make buttons with the given inputs
        and return the value of the selected button
    """
    # Making the sprite group and list for buttons
    button_group = pygame.sprite.Group()
    buttons = []
    # Number of items, height of each bttn
    num_of_items = len(items)
    height = WINDOW_SIZE[1] // (num_of_items + 3)
    # Space btw the y of each bttn
    space = height * 1.2
    available_space = WINDOW_SIZE[1] - (space * num_of_items)
    # Y position of the first bttn
    y = available_space / 2 + space
    # Generating the bttn sprites
    for item in items:
        temp = Button(WINDOW_SIZE[0] / 2, y, WINDOW_SIZE[0] // 2, height, str(item))
        button_group.add(temp)
        buttons.append(temp)
        y += space

    # Looping to get the selected item
    running = True
    while running:
        # Handling events
        for event in pygame.event.get():
            # Handling the quit event
            if event.type == pygame.QUIT:
                exit_game()

        # Looping trough the buttons
        for button in buttons:
            # Update the button thereby checking if they are pressed
            output = button.process()
            # If one is pressed(Found output) exit loop and dont check the rest
            if output:
                running = False
                break

        # Updating the buttons and drawing them on screen
        button_group.update()
        button_group.draw(window)

        # displaying the screen
        pygame.display.flip()

    # Wait until mouse up before it continue
    wait_until_mouseUp()

    # temporary surface used for cleaning the buttons
    w = pygame.Surface(WINDOW_SIZE)
    w.fill(color)
    # Using w to clean the buttons in the group
    button_group.clear(window, w)

    # Return the output
    return output

# Get float
def get_float(exit_rect: pygame.Rect) -> float:
    """
        Display a text box and get user input(float)
    """
    # Setting the USEREVENT gor the count down timer
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    # Setting the timer's time
    timer = 10

    # Pygame now allows natively to enable key repeat
    # first arg: Time to wait
    # second arg: time btw each keypress
    pygame.key.set_repeat(500, 25)

    # Create own manager with custom input validator
    # Take input only if the length of the input < number mentioned
    # And the input is float OR empty
    manager = pygame_textinput.TextInputManager(
        validator=lambda input: len(input) <= 10
        and (isfloat(input) or input == "" or input == "-")
    )

    # Create TextInput-object
    textinput = TextInput(500, 660, WINDOW_SIZE[0] - 100, 70, manager)

    # Value entered
    value = None

    # Keep the loop running
    running = True

    while running:
        # Handling events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the exit button is clicked
                if exit_rect.collidepoint(event.pos):
                    value = "exit"
                    running = False
                    break 
            if event.type == pygame.USEREVENT:
                if timer > 1:
                    timer -= 1
                else:
                    running = False

            # Check if the exit button is not pressed
            if not value:
                # Handling the text input event
                value = textinput.handle_event(event, window, color)

        # exit the loop if the user inserted a value
        if value:
            running = False

        # Displaying the timer text
        timer_rect = display_text(
            f"Timer: {timer}",
            (0, 0, 0),
            "Helvetica",
            50,
            (WINDOW_SIZE[0] - 10, 20),
            "topright",
            window
        )

        # check if the exit button is not already pressed
        # textinput.update
        textinput.draw(window, color)
        pygame.display.update()
        # Draw screen
        pygame.display.flip()
        window.fill(color, timer_rect)
        Timer.tick(60)

    # cleaning the text input and timer
    textinput.clear(window, color)
    window.fill(color, timer_rect)
    pygame.display.update()
    # Draw screen
    pygame.display.flip()
    return value

# Ask
def ask(topic: str, difficulty: str):
    global scores, questions, exit_button
    if topic == "Addition":
        function = addition
    elif topic == "Subtraction":
        function = subtraction
    elif topic == "Multiplication":
        function = multiplication
    elif topic == "Division":
        function = division

    # Signs and functions
    data = {
        "Addition": {"sign": "+", "function": sum},
        "Subtraction": {"sign": "-", "function": diff},
        "Multiplication": {"sign": "*", "function": product},
        "Division": {"sign": "/", "function": div},
    }

    # Displaying the scores
    score_rect = display_text(
        f"scores: {scores}",
        (0, 0, 0),
        "Helvetica",
        50,
        (10, 20),
        "topleft",
        window,
    )

    # Display the exit button
    exit_rect = exit_button.get_rect()
    exit_rect.center = (WINDOW_SIZE[0] / 2, 40)
    window.blit(exit_button, exit_rect)

    answer = 0
    myanswer = 0
    while True:
        # getting the first and the second number
        fn, sn = function(difficulty)
        # The question to be asked
        question = f"{fn} {data[topic]['sign']} {sn} = ?"

        # Displaying the text on the screen
        # displaying the previous question
        if questions:
            prev_rect = display_text(
                questions[-1]["question"],
                (0, 0, 0),
                "Helvetica",
                50,
                (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] // 3),
                "center",
                window,
            )

        # displaying the question
        text_rect = display_text(
            question,
            (0, 0, 0),
            "Helvetica",
            50,
            (prev_rect.centerx, prev_rect.bottom)
            if questions
            else (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] // 3),
            "topcenter",
            window,
        )

        # Get the answer
        answer = get_float(exit_rect)

        # Exitting to home screen if exit button is clicked
        if answer == "exit":
            break

        # Clean the current question for the next one
        window.fill(color, text_rect)
        
        # Setting the variable myanswer to the correct answer
        myanswer = data[topic]["function"]((fn, sn)) if topic in ["Addition"] else data[topic]["function"](fn, sn)
        
        if f"{myanswer}{answer}".isdigit():
            myanswer, answer = f"{int(myanswer)}", f"{int(answer)}"
        elif answer:
            myanswer, answer = f"{float(myanswer):.2f}", f"{float(answer):.2f}"
        else:
            myanswer = f"{float(myanswer):.2f}"

        # Check if the user provide the answer before time is up
        if answer:
            # Increment the score if the answer is correct
            if answer == myanswer:
                scores += 1
                info = "Correct Answer"
            else:
                info = f"Wrong Answer\nThe correct answer is {myanswer}"

            question = question.replace("?", answer)# + " ✔"
        else:
            info = f"Time's Up\nThe correct answer is {myanswer}"

        # Cleaning the previous score and writing a new one
        window.fill(color, score_rect)
        # Displaying the scores
        score_rect = display_text(
            f"scores: {scores}",
            (0, 0, 0),
            "Helvetica",
            50,
            (10, 20),
            "topleft",
            window,
        )
        
        # cleaning the previous question
        if questions:
            window.fill(color, prev_rect)

        # Draw screen
        pygame.display.flip()

        # Displaying the question
        text_rect = display_text(
            f"{question}",
            (0, 0, 0),
            "Helvetica",
            50,
            (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] // 3),
            "center",
            window,
        )

        # displaying the info
        info_rect = display_text(
            f"{info}",
            (0, 0, 0),
            "Helvetica",
            50,
            (text_rect.centerx, text_rect.bottom),
            "topcenter",
            window,
        )

        # Instruction for leaving the page
        display_text(
            'Click anywhere to continue',
            'small',
            "Helvetica",
            20,
            (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]-30),
            "topcenter",
            window
        )

        # rect that joins the text rect and the info rect
        rect = pygame.Rect(
            min(text_rect.left, info_rect.left),
            text_rect.top,
            max(text_rect.width, info_rect.width),
            (text_rect.height + info_rect.height),
        )

        # Draw screen
        pygame.display.flip()

        wait_until_clicked()

        # Clean the current question and info for the next one
        window.fill(color, rect)

        questions.append(
            {
                "question": question,
                "scored": True,
                "answer": answer,
                "info": info
            }
        )

    # Clear the whole screen
    window.fill(color)

# Show the final result
def show_result():
    """
        Shows the final result of the game
        including percentage score and details for each question
    """
    global scores, questions
    # The total number of questions attempted
    no_of_questions = len(questions)

    # Return to main and not display anything if no question attempted
    if no_of_questions == 0:
        return
    
    # Printing the total scores
    display_text(
        f"Total score: {scores}/{no_of_questions}",
        (0, 0, 0),
        "Helvetica",
        30,
        (100, 50),
        "topleft",
        window
    )

    # printing the percentage score
    p_rect = display_text(
        f"{((scores / no_of_questions) if questions else 1) * 100:.2f}%",
        (0, 0, 0),
        "Helvetica",
        30,
        (400, 50),
        "topleft",
        window
    )
    
    # Instruction for leaving the page
    display_text(
        'Click anywhere to leave',
        'small',
        "Helvetica",
        20,
        (WINDOW_SIZE[0]/2, WINDOW_SIZE[1] - 30),
        "topcenter",
        window
    )
    
    # Print a header "Detail:"
    result_rect = display_text(
        f"Detail:",
        (0, 0, 0),
        "Helvetica",
        25,
        (100, p_rect.bottom + 50),
        "topleft",
        window
    )

    # variables used for extracting the pages
    res = ''
    pages = []
    i = 0
    # Looping through the questions
    while i < no_of_questions:
        question = questions[i]
        res = f"\n{question['question']}\n{question['info']}\n"
        
        # This divide the questions to 20 q/page
        if i % 20 == 0:
            pages.append(res)
            res = ''
        else:
            pages[-1] += res
        
        # Increment i
        i += 1

    # Current page
    cur_page = 0
    pos = (100, result_rect.bottom)
    # Displaying page 0 as the default
    page_rect = display_page(pages[cur_page][1:-1], pos, window)
    
    # Draw the screen
    pygame.display.flip()


    if len(pages) > 1:
        # Number of pages
        no_of_pages = len(pages)

        # Loading the arrow image and scaling it to (50, 50)
        arrow_image = pygame.transform.scale(pygame.image.load(resource_path("datas/arrow.png")), (50, 50))

        # Button for navigating to the next page
        nav_right = arrow_image
        nav_right_rect = nav_right.get_rect()
        nav_right_rect.bottomright = WINDOW_SIZE[0], WINDOW_SIZE[1] - 10
        window.blit(nav_right, nav_right_rect)
        
        # Button for navigating to the previous page 
         # Flipping the arrow image
        nav_left = pygame.transform.flip(arrow_image, True, True)
        nav_left_rect = nav_left.get_rect()
        nav_left_rect.bottomleft = 0, WINDOW_SIZE[1]
        window.blit(nav_left, nav_left_rect)
  
        running = True
        while running:
            # Handling events
            for event in pygame.event.get():
                # Handling the quit event 
                if event.type == pygame.QUIT:
                    exit_game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the nav right button is clicked
                    if nav_right_rect.collidepoint(event.pos):
                        # Change to the next page if it is not already the last page
                        if not cur_page == no_of_pages - 1:
                            cur_page += 1
                            window.fill(color, page_rect)
                            page_rect = display_page(pages[cur_page][1:-1], pos, window)
                    
                    # Check if the nav left button is clicked
                    elif nav_left_rect.collidepoint(event.pos):
                        # Change to previous page if it is not the first page
                        if not cur_page == 0:
                            cur_page -= 1
                            window.fill(color, page_rect)
                            page_rect = display_page(pages[cur_page][1:-1], pos, window)
                    
                    # Exit the loop if other places on the screen where clicked
                    else:
                        running = False
                        break
                
                # Handling key press events
                if event.type == pygame.KEYDOWN:
                    # Check if the nav right button is clicked
                    if event.key == pygame.K_RIGHT:
                        # Change to the next page if it is not already the last page
                        if not cur_page == no_of_pages - 1:
                            cur_page += 1
                            window.fill(color, page_rect)
                            page_rect = display_page(pages[cur_page][1:-1], pos, window)
                    
                    # Check if the nav left button is clicked
                    elif event.key == pygame.K_LEFT:
                        # Change to previous page if it is not the first page
                        if not cur_page == 0:
                            cur_page -= 1
                            window.fill(color, page_rect)
                            page_rect = display_page(pages[cur_page][1:-1], pos, window)

            # clean the nav right button if the current page is the last page else display it
            window.fill(color, nav_right_rect) if cur_page == no_of_pages - 1 else window.blit(nav_right, nav_right_rect)
                
            # clean the nav left button if the current page is the first page else display it
            window.fill(color, nav_left_rect) if cur_page == 0 else window.blit(nav_left, nav_left_rect)

            # Draw the screen
            pygame.display.flip()

    # Wait until mouse button clicked
    wait_until_mouseUp if len(pages) > 1 else wait_until_clicked()

    # Clear the screen
    window.fill(color)

# !!! ../project/Tic_tac_toe/pygame/Scripts/activate !!!
# Main game
def play():
    # Global variables
    global selected_difficulty, selected_topic, scores, questions

    # variables
    selected_topic = None
    selected_difficulty = None
    difficulties = ["Easy", "Normal", "Hard"]
    topics = ["Addition", "Subtraction", "Multiplication", "Division"]

    # Game loop
    running = True
    while running:
        # Reset the scores and the questions at each game
        scores = 0
        questions = list()
        # Handling events
        for event in pygame.event.get():
            # Handling the quit event
            if event.type == pygame.QUIT:
                exit_game()

        # Displaying the home screen
        # home_screen()
        move_to = select("Play", "Instructions")
        if move_to == "Play":
            # Return to select topic screen
            selected_topic = select(*topics)
            # Return to select difficulty screen
            selected_difficulty = select(*difficulties)
            # Ask Questions based on topic and difficulty
            ask(selected_topic, selected_difficulty)
            # Show the result when the game is exitted
            wait_until_mouseUp()
            show_result()
        elif move_to == "Instructions":
            # The instruction page
            instruction()

        # Draw screen
        pygame.display.flip()

# Donda name equals donda main
if __name__ == "__main__":
    # splash_screen()
    # import pathlib
    # pathlib.Path(__file__).parent.absolute()
    try:
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass

    play()

# pyinstaller --noconfirm --onefile --windowed --hidden-import=pyi_splash --icon C:\Users\Abdul\Desktop\python_demo\Are_you_a_math_whiz\package_datas\icon1.ico --splash C:\Users\Abdul\Desktop\python_demo\Are_you_a_math_whiz\package_datas\splash_screen.png --name 'Are You A Math Whiz' --add-data "C:\Users\Abdul\Desktop\python_demo\Are_you_a_math_whiz\datas;datas/" C:\Users\Abdul\Desktop\python_demo\Are_you_a_math_whiz\main.py
