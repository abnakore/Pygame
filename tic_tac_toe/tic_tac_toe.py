import random
from tic import Check_win, check_win
from datetime import date
import pygame
import sys, os

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
pygame.display.set_icon(pygame.image.load("icon.png"))
# The length of the squares
length = 120

# Game on variable
game_on = False

# sprite of x and o
class Square(pygame.sprite.Sprite):
    """
        The square sprite
    """

    def __init__(self, column: int, row: int):
        super().__init__()

        # x position of the square
        self.x_pos = (column * (length))

        # y position of the square
        self.y_pos = (row * (length))
        
        # The custume to be displayed
        self.image = empty
        self.rect = self.image.get_rect()

        # Index of the square starting from 1 to 9
        self.num = ((row - 1) * 3) + (column)

    # update
    def update(self):
        self.rect.center = (self.x_pos, self.y_pos)

    def get_pos(self):
        return self.x_pos, self.y_pos

    # diplay the player when clicked
    def click(self, mx, my):
        # Global variable player
        global player
        # Check if the rectangle is clicked
        
        if self.rect.collidepoint(mx, my) and self.image == empty:
            if mode == "multiplayer" or not player == computer_player:
                # Display x if the player is x and change the player to o and vice vercer
                if player == 'x':
                    inputs[self.num - 1] = 'x'
                    self.image = _x
                    x_inputs.append(self.num)
                    pygame.mixer.Sound.play(place_x_sound)
                    winner(inputs)
                    player = 'o'
                    player_text.change()
                else:
                    inputs[self.num - 1] = 'o'
                    self.image = _o
                    o_inputs.append(self.num)
                    pygame.mixer.Sound.play(place_o_sound)
                    winner(inputs)
                    player = 'x'
                    player_text.change()
                return True


class Button(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, img, id):
        super().__init__()
        self.id = id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)

    def clicked(self, mx, my):
        if self.rect.collidepoint(mx, my):
            pygame.mixer.Sound.play(button_sound)
            return self.id

class AboutButton:
    def __init__(self, x, y, width, height, text, onclickfunction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclickfunction = onclickfunction
        self.fillColors = {"normal" : (225, 255, 255), "hover": (125, 125, 125), "pressed": (color)}
        self.Surface = pygame.Surface((self.width, self.height))
        # self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect = self.Surface.get_rect()
        self.rect.center = (self.x, self.y)
        self.font = pygame.font.SysFont("Elephant", 10)
        self.bttnSurf = self.font.render(self.text, True, (20, 20, 20))
        self.pressed = False
        
    def draw(self):
        screen.fill(color, self.rect)
        self.rect = self.Surface.get_rect()
        self.rect.center = (self.x, self.y)
        textRect = self.bttnSurf.get_rect()
        self.Surface.blit(self.bttnSurf, (self.rect.width/2 - textRect.width/2, 
                                          self.rect.height/2 - textRect.height/2))
        screen.blit(self.Surface, self.rect)
    
    def process(self):
        self.Surface = pygame.Surface((self.width, self.height))
        self.Surface.fill(self.fillColors["normal"])
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.Surface = pygame.Surface((self.width + 10, self.height + 10))
            self.Surface.fill(self.fillColors["hover"])
            if pygame.mouse.get_pressed()[0]:
                self.Surface.fill(self.fillColors["pressed"])
                self.draw()
                pygame.time.wait(50)
                if not self.pressed:
                    pygame.mixer.Sound.play(button_sound)
                    self.onclickfunction()
                    self.pressed = True
            else:
                self.pressed = False
        
        self.draw()

        
class ReadMe:
    def __init__(self, surf: pygame.Surface, x, y, prev):
        self.surf = surf
        self.x = x
        self.rect = self.surf.get_rect()
        self.rect.height += 2
        self.rect.width = 500
        self.prev = prev
        self.y = (self.prev + self.rect.height)
        self.rect.left = self.x
        self.rect.bottom = self.y
  
    def get_y(self):
        return self.y

    def draw(self):
        if -10 < self.y < 620:
            # self.rect.width = 500
            screen.fill(color, self.rect)
            screen.blit(self.surf, self.rect)

    def update(self, i, prev):
        if self.y > 0:
            self.y -= 1
        else:
            self.y = (prev + self.rect.height)
        self.rect.bottom = self.y

# current player text
class Player_text(pygame.sprite.Sprite):
    def __init__(self, img, x_pos, y_pos):
        super().__init__()
        self.image = img
        self.x = x_pos
        self.y = y_pos
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def change(self):
        if mode == "multiplayer":
            self.image = x_img if player == 'x' else o_img
        else:
            if computer_player == 'x':
                self.image = xc if player == 'x' else op
            else:
                self.image = oc if player == 'o' else xp
        
# Background color
color = (0, 0, 20)

# the game window
screen = pygame.display.set_mode([500, 500])
screen.fill(color)

# The game title
pygame.display.set_caption("TIC TAC TOE")

# loading sound
place_x_sound = pygame.mixer.Sound("HighWhoosh.wav")
place_o_sound = pygame.mixer.Sound("LowWhoosh.wav")
button_sound = pygame.mixer.Sound("SuctionCup.wav")
win_sound = pygame.mixer.Sound("Tada.wav")
tie_sound = pygame.mixer.Sound("DunDunDun.wav")

# Setting the player to start playing      
player = random.choice(['x', 'o'])

# Loading up the sprite custumes and scaling them
length -= 20
_x = pygame.transform.scale(pygame.image.load("x.png"), (length, length))
_o = pygame.transform.scale(pygame.image.load("o.png"), (length, length))
empty = pygame.transform.scale(pygame.image.load("e1.png"), (length, length))
length += 20

x_img = pygame.transform.scale(pygame.image.load("x.png"), (60, 60))
o_img = pygame.transform.scale(pygame.image.load("o.png"), (60, 60))
xp = pygame.transform.scale(pygame.image.load("xp.png"), (60, 60))
op = pygame.transform.scale(pygame.image.load("op.png"), (60, 60))
xc = pygame.transform.scale(pygame.image.load("xc.png"), (60, 60))
oc = pygame.transform.scale(pygame.image.load("oc.png"), (60, 60))

game_state = None

# List that stores the entries
inputs = ['' for _ in range(9)]
x_inputs = []
o_inputs = []

# exit the game
def exit_game():
    pygame.quit()
    sys.exit()


# Making the sprite group and list
group = pygame.sprite.Group()
squares = []
# Generating the sprites
for y in range(1, 4):
    for x in range(1, 4):
        temp = Square(x, y)
        group.add(temp)
        squares.append(temp)
        
# Make the button group
button_group = pygame.sprite.Group()
def readME():
    global game_state, button_group
    game_state = "readME"
    clear_splash_screen()
    read = []
    i = 0
    prev = 500
    img = ReadMe(pygame.transform.scale(pygame.image.load("sample.png"), (150, 150)), 220, i, prev)
    read.append(img)
    font = pygame.font.SysFont("Bookman Old Style", 15)
    i += 1
    prev = read[-1].get_y()
    text = ReadMe(font.render(f"Copyright © 2022 - {date.today().year}", True, (255, 255, 255)), 20, i, prev)
    read.append(text)
    with open("README.txt") as file:
        i += 1
        prev = read[-1].get_y()
        for line in file:
            
            text = ReadMe(font.render(line.strip(), True, (255, 255, 255)), 20, i, prev)
            read.append(text)
            # text_rect = text.get_rect()
            # text_rect.left = (20)
            # text_rect.centery = (20 * i)
            # screen.blit(text, text_rect)
            i += 1
            prev = read[-1].get_y()


    while game_state == "readME":
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "splash_screen"
                break
        for item in read:
            item.update(i, prev + 500 if item == read[0] else prev)
            item.draw()
            pygame.display.update()
            # Draw screen
            pygame.display.flip()
            prev = item.get_y()
        pygame.time.delay(1)
        # screen.fill(color, pygame.Rect(0, 0, 500, 20))
    screen.fill(color)
    pygame.time.delay(1)
    splash_screen()

# Show the splash screen
def splash_screen():
    global mode, button_group, game_state
    buttons = []
    button_group = pygame.sprite.Group()
    name = "single_player"
    for i in range(1, 3):
        temp = Button(250, 200 + (120 * i), pygame.transform.scale(pygame.image.load(f"{name}.png"), (300, 200)), name)
        button_group.add(temp)
        buttons.append(temp)
        name = "multiplayer"

    # Displaying the TIC TAC TOE text in the splash screen
    font = pygame.font.SysFont("Bradley Hand ITC", 50)
    text = font.render(f"TIC TAC TOE", True, (255, 179, 200))
    text_rect = text.get_rect()
    text_rect.center = (250, 100)
    screen.blit(text, text_rect)

    about = AboutButton(450, 470, 80, 30, "About", readME)
    # Main loop for the splash screen
    running = True
    while running:
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit_game()
            if game_state == "splash_screen":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for s in buttons:
                        if mode:= s.clicked(mx, my):
                            running = False
                            break
        if game_state == "splash_screen":
            about.process()
            if game_state == "splash_screen":
                button_group.update()
                button_group.draw(screen)
                screen.blit(text, text_rect)
            else:
                screen.fill(color, about.rect)
                
        pygame.display.update()
        # Draw screen
        pygame.display.flip()  
    clear_splash_screen()

def clear_splash_screen():
    global button_group
    # temporary surface used for cleaning the buttons
    w = pygame.Surface((500, 500))
    w.fill(color)
    button_group.clear(screen, w)
    screen.fill(color)

def winner(game):
    global screen, game_on, text
    temp = Check_win(game)
    if temp == 1:
        game_on = False
        Update()
        pygame.mixer.Sound.play(win_sound)
        draw_win()
        group.empty()
        text_group.empty()
        screen.fill(color)
        font = pygame.font.SysFont("Elephant", 50)
        text = font.render(f"{player.capitalize()}'s win", True, (255, 255, 255))
    elif temp == 0:
        game_on = False
        Update()
        pygame.mixer.Sound.play(tie_sound)
        pygame.time.wait(2000)
        group.empty()
        text_group.empty()
        screen.fill(color)
        font = pygame.font.SysFont("Elephant", 50)
        text = font.render(f"Tie Game", True, (255, 255, 255))
    if not game_on:
        text_rect = text.get_rect()
        text_rect.center = (250, 250)
        screen.blit(text, text_rect)
        pygame.mixer.music.stop()

# draw the line if win
def draw_win():
    indx = check_win(x_inputs if player == 'x' else o_inputs)
    x1, y1 = squares[indx[0]].get_pos()
    x2, y2 = squares[indx[1]].get_pos()
    x3, y3 = squares[indx[2]].get_pos()
    if x1 == x2 == x3:
        cur = y1 - 50
        for i in range(y1 - 49, y3 + 50):
            pygame.draw.line(screen, (25, 125, 10), (x1, cur), (x1, i), 5)
            pygame.display.flip()
            cur = i
            pygame.time.wait(2)

    elif y1 == y2 == y3:
        cur = x1 - 50
        for i in range(x1 - 49, x3 + 50):
            pygame.draw.line(screen, (25, 125, 10), (cur, y1), (i, y1), 5)
            pygame.display.flip()
            cur = i
            pygame.time.wait(2)

    elif x1 < x3:
        curx = x1 - 50
        cury = y1 - 50
        while cury < y3 + 50:
            pygame.draw.line(screen, (25, 125, 10), (curx, cury), (curx + 1, cury + 1), 5)
            pygame.display.flip()
            curx += 1
            cury += 1
            pygame.time.wait(2)
    else:
        curx = x1 + 50
        cury = y1 - 50
        while cury < y3 + 50:
            pygame.draw.line(screen, (25, 125, 10), (curx, cury), (curx + 1, cury + 1), 5)
            pygame.display.flip()
            curx -= 1
            cury += 1
            pygame.time.wait(2)

    pygame.time.wait(2000)

# Computer player
def computer():
    global player, player_text
    # insert at random position if its the first move 
    if not 'x' in inputs and not 'o' in inputs:
        move = random.randint(0, 8)
    elif '' in inputs:
        move = minimax(inputs, player)[0]
        pygame.time.wait(500)
    else:
        return
        

    
    inputs[move] = computer_player
    o_inputs.append(move + 1) if computer_player == 'o' else x_inputs.append(move + 1)
    squares[move].image = _o if computer_player == 'o' else _x
    pygame.mixer.Sound.play(place_o_sound if computer_player == 'o' else place_x_sound)
    winner(inputs)
    player = 'x' if computer_player == 'o' else 'o'
    player_text.change()

cur_winner = None
def minimax(state, cur_player):
    global player, cur_winner
    num_of_empty = len([c for c in state if c == ''])
    other_player = 'o' if cur_player == 'x' else 'x'
    if cur_winner == 1:
        if not cur_player == computer_player:
            return [None, 1 * (num_of_empty + 1)]
        else:
            return [None, -1 * (num_of_empty + 1)]
    elif num_of_empty == 0:
        return [None, 0]

    if cur_player == computer_player:
        best = [None, -10]
    else:
        best = [None, 10]
    
    for i in range(9):
        if state[i] == '':
            state[i] = cur_player
            cur_winner = Check_win(state)
            temp_best = minimax(state, other_player)
            

            state[i] = ''
            cur_winner = None
            temp_best[0] = i
            
            if cur_player == computer_player:
                if temp_best[1] > best[1]:
                    best = temp_best
                elif temp_best[1] == best[1]:
                    best = random.choice([best, temp_best])
            else:
                if temp_best[1] < best[1]:
                    best = temp_best  
                elif temp_best[1] == best[1]:
                    best = random.choice([best, temp_best])
    
    return best

def update_text():
    global text_group
    if game_on:
        text_group.empty()
        screen.fill(color, player_text.rect)
        text_group.update()
        text_group.draw(screen)
        text_group.add(player_text)
    text_group.update()
    text_group.draw(screen)


def Update():
    update_text()
    group.update()
    group.draw(screen)
    pygame.display.update()



# draw the board
def board():
    x = 180
    for _ in range(2):
        cur = 70
        for i in range(71, 430):
            pygame.draw.line(screen, (125, 125, 125), (x, cur), (x, i), 5)
            pygame.display.flip()
            cur = i
            pygame.time.wait(1)
        
        x = 300

    
    y = 180
    
    for _ in range(2):
        cur = 70
        for i in range(71, 430):
            pygame.draw.line(screen, (125, 125, 125), (cur, y), (i, y), 5)
            pygame.display.flip()
            cur = i
            pygame.time.wait(1)
        y = 300

# Closing the pyi_splashscren
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    pass


# def play():
# global text_group, game_state, player_text, computer_player
# Displaying the splash screen
while True:
    # Setting the player to start playing      
    player = random.choice(['x', 'o'])
    game_state = None

    # List that stores the entries
    inputs = ['' for _ in range(9)]
    x_inputs = []
    o_inputs = []
    # Making the sprite group and list
    group = pygame.sprite.Group()
    squares = []
    # Generating the sprites
    for y in range(1, 4):
        for x in range(1, 4):
            temp = Square(x, y)
            group.add(temp)
            squares.append(temp)

    game_state = "splash_screen"

    screen.fill(color)
    splash_screen()
    # Calling the board function
    board()

    # Setting the computer to random player if playing vs computer
    if mode == "single_player":
        computer_player = random.choice(['x', 'o'])


    player_text = Player_text(empty, 260, 480)
    player_text.change()
    text_group = pygame.sprite.Group()
    text_group.add(player_text)
    text_group.draw(screen)


    pygame.mixer.music.load("DripDrop.wav")
    pygame.mixer.music.play(-1)

    game_on = True
    # Game loop
    running = True
    while running:

        # Handling events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                exit_game()

            if event.type == pygame.MOUSEBUTTONDOWN and game_on:
                mx, my = pygame.mouse.get_pos()
                if mode == "multiplayer" or not player == computer_player:
                    for s in squares:
                        if s.click(mx, my):
                            break

        # Updating game state
        Update()
        # Draw screen
        pygame.display.flip()

        if mode == "single_player" and player == computer_player:
            computer()
            # Updating game state
            Update()
            # Draw screen
            pygame.display.flip()

        if not game_on:
          running = False


# Exiting the programme
exit_game()


# pyinstaller --noconfirm --onefile --windowed --hidden-import=pyi_splash --icon C:\Users\Abdul\Desktop\python_demo\project\Tic_tac_toe\icon.ico --splash C:\Users\Abdul\Desktop\python_demo\project\Tic_tac_toe\icon.png --name 'Tic Tac Toe' --add-data "C:\Users\Abdul\Desktop\python_demo\project\Tic_tac_toe\tic.py;." C:\Users\Abdul\Desktop\python_demo\project\Tic_tac_toe\tic_tac_toe.py
