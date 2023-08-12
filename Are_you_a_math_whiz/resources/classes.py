# importing required libraries
import pygame
import pygame_textinput

# Button
class Button(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, text: str):
        super().__init__()
        # Setting the some class variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        # state variable(stores the state of the button either normal, hover or pressed)
        self.state = "normal"

        # This is a dictionary that stores the colors that the button will be in three diff conditions
        self.fillColors = {
            "normal": (200, 255, 255),
            "hover": (140, 200, 190),
            "pressed": (90, 150, 140),
        }
        # Creating a rectangular surface (the button) to be the image
        self.image = pygame.Surface((self.width, self.height))
        # self.image.fill(self.fillColors[self.state])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Setting a font of a text and setting the font size
        self.font = pygame.font.SysFont("Elephant", (self.width + self.height) // 15)
        # Make a text and setting the text color
        self.bttn_text = self.font.render(self.text, True, self.fillColors["pressed"])
        # getting the bttn_text rect
        self.textRect = self.bttn_text.get_rect()

        # a variable to make sure that the button is pressed once
        self.pressed = False

    # Handling hover and click
    def process(self) -> str:
        # Change the state to normal
        self.state = "normal"
        # fill the button with the current state color
        self.image.fill(self.fillColors[self.state])
        self.display_update()
        # Getting the current mouse position
        mousePos = pygame.mouse.get_pos()
        # Check if the mouse is on the button
        if self.rect.collidepoint(mousePos):
            # self.image = pygame.Surface((self.width + 20, self.height + 20))
            self.rect.height += self.height // 2
            # Change the state to hover
            self.state = "hover"
            # fill the button with the current state color
            self.image.fill(self.fillColors[self.state])
            self.display_update()
            # Check if the button is clicked else set the clicked variable to false
            if pygame.mouse.get_pressed()[0]:
                # Change the state to pressed
                self.state = "pressed"
                # fill the button with the current state color
                self.image.fill(self.fillColors[self.state])
                self.display_update()
                # set the clicked variable to true
                if not self.pressed:
                    self.pressed = True
                    return self.text
            else:
                self.pressed = False

            self.rect.height = self.height

    def display_update(self):
        # Place the text at the center of the button
        self.image.blit(
            self.bttn_text,
            (
                self.rect.width / 2 - self.textRect.width / 2,
                self.rect.height / 2 - self.textRect.height / 2,
            ),
        )
        self.update()


# Text Input
class TextInput(pygame_textinput.TextInputVisualizer):
    def __init__(self, x: float, y: float, width: float, height: float, manager, text=""):
        # Setting some variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.inner_rect = pygame.Rect(self.x, self.y, self.width - 50, self.height - 35)
        self.rect.center = (self.x, self.y)
        self.inner_rect.center = self.rect.center
        self.enter = pygame.Rect(self.inner_rect.x, self.y, self.inner_rect.height - 5, self.inner_rect.height - 5)
        self.enter.centery = self.inner_rect.centery
        self.enter.right = self.inner_rect.right - 5

        # Setting a font of a text and setting the font size
        self.font = pygame.font.SysFont("TimesNewRoman", (self.inner_rect.width + self.height) // 50)

        super().__init__(manager=manager, font_object=self.font)
        # Other customizations:
        self.cursor_width = 2
        self.cursor_blink_interval = 500 # blinking interval in ms
        self.antialias = False
        self.font_color = (0, 0, 0)

        # Fill colors
        self.fillColors = {"active": (0, 0, 255), "inactive": (180, 180, 200)}

        # Setting default to inactive
        self.active = True
        self.color = (
                    self.fillColors["active"] if self.active else self.fillColors["inactive"]
                )
        # Rendering the font
        self.txt_surface = self.font.render(text, True, self.color)
        # text rect
        self.text_rect = self.txt_surface.get_rect()

    # Handling events
    def handle_event(self, event, screen, color):


        # for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check if the tick button is clicked
            if self.enter.collidepoint(event.pos):
                if not self.value == '':
                    value = self.value
                    self.value = ""
                    return value
            # If the user clicked on the input_box rect.
            elif self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (
                self.fillColors["active"] if self.active else self.fillColors["inactive"]
            )
        
        # Check if user pressed return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.value == '':
                value = self.value
                self.value = ""
                return value

        # And the text input is active
        if self.active:
            # Feed it with events every frame
            self.update((event, ))
        else:
            # Handle hover
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.fillColors["active"]
            else:
                self.color = self.fillColors["inactive"]
            self.draw(screen, color)

    def draw(self, screen, color):
        # Cleaning the screen
        self.clear(screen, color)
        # Blit the outer rect.
        # The White background
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)
        # the outline
        pygame.draw.rect(screen, (150, 150, 180), self.rect, 2, 10)
        # blit the shadow rect if focus
        if self.active:
            shadow_rect = pygame.Rect(self.x, self.y, self.inner_rect.width + 3, self.inner_rect.height + 3)
            shadow_rect.center = self.inner_rect.center
            pygame.draw.rect(screen, (150, 150, 255), shadow_rect, 3, 30)
        # Blit the circle for the check button
        pygame.draw.circle(screen, self.fillColors["active"], self.enter.center, self.enter.width/2)
        # Making the mark inside the button
        check = self.font.render("OK", True, (255, 255, 255))#🗸✔↵
        check_rect = check.get_rect()
        check_rect.center = self.enter.center
        screen.blit(check, check_rect)
        pygame.draw.rect(screen, self.color, self.inner_rect, 1, 30)
        # Get its surface(That's the text) to blit onto the screen
        screen.blit(self.surface, (self.inner_rect.x + 10, self.inner_rect.y + (self.surface.get_height() / 2)))

    def clear(self, screen, color):
        '''
            Clean the screen with the given color
        '''
        screen.fill(color, self.rect)
        