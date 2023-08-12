# https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

import pygame
from pygame_textinput import *

pygame.init()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()
def text_input1():
    # No arguments needed to get started
    textinput = TextInputVisualizer()

    # But more customization possible: Pass your own font object
    font = pygame.font.SysFont("Consolas", 55)
    # Create own manager with custom input validator
    manager = TextInputManager(validator = lambda input: len(input) <= 20)
    # Pass these to constructor
    textinput_custom = TextInputVisualizer(manager=manager, font_object=font)
    # Other customizations:
    textinput_custom.cursor_width = 2
    textinput_custom.cursor_blink_interval = 500 # blinking interval in ms
    textinput_custom.antialias = False
    textinput_custom.font_color = (0, 85, 170)


    # Pygame now allows natively to enable key repeat
    # first arg: Time to wait
    # second arg: time btw each keypress
    pygame.key.set_repeat(500, 25)

    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Feed it with events every frame
        textinput.update(events)
        textinput_custom.update(events)

        # Get its surface to blit onto the screen
        screen.blit(textinput.surface, (10, 10))
        screen.blit(textinput_custom.surface, (10, 50))

        # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
        textinput_custom.font_color = [(c+10)%255 for c in textinput_custom.font_color]

        # Check if user pressed return
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            print(f"User pressed enter! Input so far: {textinput_custom.value}")

        pygame.display.update()
        clock.tick(30)

text_input1()