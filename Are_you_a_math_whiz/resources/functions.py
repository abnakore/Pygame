"""
    Other Functions
"""

import pygame
from random import random, randint
import sys

# Function that handle addition
def addition(difficulty: str):
    "Easy", "Normal", "Hard", "Extreme"
    if difficulty == "Easy":
        return randint(1, 9), randint(1, 9)
    elif difficulty == "Normal":
        return randint(10, 30), randint(10, 20)
    elif difficulty == "Hard":
        return float(f"{random()*randint(50, 100):.2f}"), float(f"{random()*randint(50, 100):.2f}")

# Function that handle Subtraction
def subtraction(difficulty: str):
    "Easy", "Normal", "Hard", "Extreme"
    if difficulty == "Easy":
        return randint(8, 15), randint(1, 8)
    elif difficulty == "Normal":
        return randint(30, 80), randint(15, 40)
    elif difficulty == "Hard":
        return float(f"{random()*randint(-50, 100):.2f}"), float(f"{random()*randint(-50, 100):.2f}")

# Function that handle Subtraction
def multiplication(difficulty: str):
    "Easy", "Normal", "Hard", "Extreme"
    if difficulty == "Easy":
        return randint(1, 12), randint(1, 12)
    elif difficulty == "Normal":
        return randint(10, 20), randint(13, 20)
    elif difficulty == "Hard":
        return float(f"{random()*randint(-50, 100):.2f}"), float(f"{random()*randint(-50, 100):.2f}")

# Function that handle Subtraction
def division(difficulty: str):
    "Easy", "Normal", "Hard", "Extreme"
    if difficulty == "Easy":
        return randint(1, 12), randint(1, 12)
    elif difficulty == "Normal":
        return randint(10, 20), randint(13, 20)
    elif difficulty == "Hard":
        return float(f"{random()*randint(-50, 100):.2f}"), float(f"{random()*randint(-50, 100):.2f}")

# Function that give the difference btw 2 numbers
def diff(fn: float, sn: float) -> float:
    return fn - sn
# Function that multiply the given numbers
def product(*args : float) -> float:
    ans = 1
    for i in args:
        ans *= i
    return ans
# Function that devide two numbers
def div(fn:float, sn:float) -> float:
    return fn / sn

# Check if the input isfloat
def isfloat(input) -> bool:
    '''
        Return True if the input is a float
        else False
    '''
    try:
        float(input)
    except ValueError:
        return False
    return True

# Function that wait until mouse is released(mouse is not pressed)
def wait_until_mouseUp():
    down = True
    while down:
        # looping trough the events
        for _ in pygame.event.get():
            pass

        # Exit if the mouse is released
        if not pygame.mouse.get_pressed(3)[0]:
            down = False

def wait_until_clicked():
    up = True
    while up:
        # looping trough the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Exit if the mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                up = False
                break
    
    wait_until_mouseUp()

# Functin that makes a text object and display it on screen
def display_text( text: str, color, font_name, size:int, pos, align:str, surf: pygame.Surface):
    '''
        Place text on the given surface and return the rect for future use
        # Can also display multiline text
    '''
    if color == 'small':
        color = (50, 60, 50)
    # Creating the font object
    font = pygame.font.SysFont(font_name, size)
    # Check if the text is multiline
    if '\n' in text:
        left, top = pos
        # Stores the max width among the rects
        max_width = 0
        # Setting the minimum x to be left of the text
        min_x = left
        # Splitting the text line by line
        lines = text.split("\n")
        # Looping trough the lines and displaying them
        for line in lines:
            text_obj = font.render(line, True, color)
            text_rect = text_obj.get_rect()

            if align == "topleft":
                text_rect.topleft = (left, top)
            elif align == "topcenter":
                text_rect.top = top
                text_rect.centerx = left
            elif align == "center":
                text_rect.center = (left, top)
            else:
                text_rect.topright = (left, top)

            surf.blit(text_obj, text_rect)
            # Getting the minimum x
            min_x = min(min_x, text_rect.left)
            # Getting the max rect with
            max_width = max(max_width, text_rect.width)
            # Set the next text's top to be the bottom of the prev text
            top = text_rect.bottom

        # Making the final text rect for the whole text
        text_rect = pygame.Rect(
            min_x,
            pos[1],
            max_width,
            # The height is the last text rect bottom - first text rect top
            text_rect.bottom - pos[1]
        )
    else:
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if align == "center":
            text_rect.center = pos
        elif align == "topcenter":
            text_rect.top = pos[1]
            text_rect.centerx = pos[0]
        elif align == "topleft":
            text_rect.topleft = pos
        elif align == "topright":
            text_rect.topright = pos
        surf.blit(text_obj, text_rect)
    return text_rect

# Display page
def display_page(page, pos, surf):

    left, top = pos
    # Stores the max width among the rects
    max_width = 0
    bottom = 0
    for q in page.split("\n\n"):
        
        if top > 600:
            top = pos[1]
            left = (result_rect.left + max_width + 20 if result_rect else left)
            max_width = 0
            
        result_rect = display_text(
            f"\n{q}",
            (0, 0, 0),
            "Helvetica",
            20,
            (left, top),
            "topleft",
            surf
        )

        # Getting the max rect width
        max_width = max(max_width, result_rect.width)
        bottom = max(bottom, result_rect.bottom)
        # Resetting the top
        top = result_rect.bottom

    # Making the final text rect for the whole page
    text_rect = pygame.Rect(
        pos[0],
        pos[1],
        (result_rect.left + max_width) - pos[0],
        # The height is the last text rect bottom - first text rect top
        bottom - pos[1]
    )
    return text_rect

# Exit the game
def exit_game():
    pygame.quit()
    sys.exit(0)
