# #Frames per second manipulation

# #required 
# import pygame
# pygame.init();

# #create colors
# white = (255,255,255)
# black = (0,0,0)
# red = (255, 0, 0)
# green = (0, 255, 0)
# blue = (0, 0, 255)

# #position vars
# x_pos = 0
# y_pos = 0
# x_delta = 0
# y_delta = 0
# clock = pygame.time.Clock()

# #create a surface
# gameDisplay = pygame.display.set_mode((800,600)) #initialize with a tuple

# #lets add a title, aka "caption"
# pygame.display.set_caption("Frames per second")
# pygame.display.update()		#only updates portion specified




# gameExit = False
# while not gameExit:
# 	gameDisplay.fill(white)

# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			gameExit = True

# 	if event.type == pygame.KEYDOWN:
# 		x_delta=0;
# 		y_delta=0;
# 		if event.key == pygame.K_LEFT:
# 			x_delta -= 10
# 		if event.key == pygame.K_RIGHT:
# 			x_delta += 10
# 		if event.key == pygame.K_UP:
# 			y_delta -= 10
# 		if event.key == pygame.K_DOWN:
# 			y_delta += 10
	
# 	x_pos +=x_delta
# 	y_pos +=y_delta
# 	gameDisplay.fill(blue, rect=[x_pos,y_pos, 20,20])
# 	pygame.display.update()		
# 	clock.tick(30)



# #required
# pygame.quit()
# quit()		




# import library called pygame
import pygame

# initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

# Set the width and height of the screen [width, height]
width = 500
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# List containing all sprites in the program to draw them
all_sprites_list = pygame.sprite.Group()


# Define wall
class Wall(pygame.sprite.Sprite):
    # initialises parameters of a wall
    def __init__(self, corner_x, corner_y, width, height, color):
        super().__init__()  # inherits all parameters of a sprite
        self.width = width
        self.height = height
        self.color = color
        # set the image of the wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()  # finds the rectangle object that has the dimensions of the image
        self.rect.x = corner_x
        self.rect.y = corner_y

    # draws a wall
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])


# Define coins to collect
class coin(pygame.sprite.Sprite):
    # initialses parameters of the coin
    def __init__(self, center_x, center_y, radius, color):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.color = color
        self.radius = radius

        pygame.draw.circle(self.image, self.color, (center_x, center_y), self.radius, 0)

        self.rect = self.image.get_rect()
        self.rect.x = center_x
        self.rect.y = center_y

    def draw(self):
        pygame.draw.circle(self.image, self.color, (center_x, center_y), self.radius, 0)


# this is the list of all walls in the game
wall_list = pygame.sprite.Group()
# this is the list of all coins in the game
coin_list = pygame.sprite.Group()

# Parameters of the map
widthofwalls = 20
heightofwalls = 20
colorofwalls = RED
colorofcoins = BLUE


# Function for adding the map from a given string
def adding_map(mapdescription, heightofwalls, widthofwalls, colorofwalls):
    # For each row, starting from 0
    current_row = 0
    for each_string in mapdescription:
        # For each column
        for i in range(0, len(each_string)):
            # Letter W means wall
            if each_string[i] == "W":
                newWall = Wall(i * widthofwalls, current_row * heightofwalls, widthofwalls, heightofwalls, colorofwalls)
                wall_list.add(newWall)
                all_sprites_list.add(newWall)
            # A . means a coin
            elif each_string[i] == ".":
                newCoin = coin(i * widthofwalls, current_row * heightofwalls, int(widthofwalls / 4), colorofcoins)
                coin_list.add(newCoin)
                all_sprites_list.add(newCoin)
        current_row += 1

        # Declaration of the maze


basicmap = ["WWWWWWWWWWWWWWWWWWWWWWWWW",
            "W    .      W           W",
            "W WWW WWWWW W WWWWW WWW W",
            "W WWW WWWWW W WWWWW WWW W",
            "W.........              W",
            "W WWW W WWWWWWWWW W WWW W",
            "W     W     W     W     W",
            "WWWWW WWWWW W WWWWW WWWWW",
            "    W W           W W    ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "        W       W        ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "    W W           W W    ",
            "WWWWW W WWWWWWWWW W WWWWW",
            "W           W           W",
            "W WWW WWWWW W WWWWW WWW W",
            "W   W               W   W",
            "WWW W W WWWWWWWWW W W WWW",
            "W     W     W     W     W",
            "W WWWWWWWWW W WWWWWWWWW W",
            "W                       W",
            "WWWWWWWWWWWWWWWWWWWWWWWWW"]
adding_map(basicmap, heightofwalls, widthofwalls, colorofwalls)


# Define moving object
class moving_object(pygame.sprite.Sprite):
    # initialises theobject
    def __init__(self, speed, direction, height, width, color):
        super().__init__()
        self.speed = speed
        self.direction = direction
        self.height = height
        self.width = width
        self.color = color
        # set the image of Pacman
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # fetches the rectangle in which the image is enclosed
        self.rect = self.image.get_rect()

    # moves the object
    def move(self):
        # moves upwards
        if self.direction == 1:
            self.rect.y -= self.speed
        # moves right
        if self.direction == 2:
            self.rect.x += self.speed
        # moves down
        if self.direction == 3:
            self.rect.y += self.speed
        # moves left
        if self.direction == 4:
            self.rect.x -= self.speed

    # allows the direction of movement to be changed
    def new_direction(self, newdirection):
        self.direction = newdirection

    # returns direction
    def get_direction(self):
        return self.direction

    # returns speed
    def get_speed(self):
        return self.speed

    # returns coordinates
    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.width, self.height])

    def moving_object_detecting_collisions(self, wall_list):
        # Checks what would happen if the object would be moved as intended
        self.move()
        # If there is a collision, moves the object back in the opposite direction
        # Object ends up in the same position as it was before the collision
        if pygame.sprite.spritecollide(self, wall_list, False):
            if self.get_direction() == 3:
                self.new_direction(1)
                self.move()
                self.new_direction(3)
            if self.get_direction() == 1:
                self.new_direction(3)
                self.move()
                self.new_direction(1)
            if self.get_direction() == 2:
                self.new_direction(4)
                self.move()
                self.new_direction(2)
            if self.get_direction() == 4:
                self.new_direction(2)
                self.move()
                self.new_direction(4)

    def signalfromkeyboard(self, event):
        # find if it was an arrow and adjust the next direction accordingly
        # Pacman now moves right
        if event.key == pygame.K_RIGHT:
            newdirection = 2
            self.new_direction(newdirection)
        # Pacman now moves up
        if event.key == pygame.K_UP:
            newdirection = 1
            self.new_direction(newdirection)
        # Pacman now moves down
        if event.key == pygame.K_DOWN:
            newdirection = 3
            self.new_direction(newdirection)
        # Pacman now moves left
        if event.key == pygame.K_LEFT:
            newdirection = 4
            self.new_direction(newdirection)

    def wouldcollide(self, wall_list):
        self.move()
        if pygame.sprite.spritecollide(self, wall_list, False):
            return True
        else:
            return False


initxPac = 20
inityPac = 20
initspeedPac = 1
initdirectionPac = 2
heightPac = 20
widthPac = 20
colorPac = BLACK

Pacman = moving_object(initspeedPac, initdirectionPac, widthPac, heightPac, colorPac)
Pacman.rect.x = initxPac
Pacman.rect.y = inityPac


# Will be used for implementing changing direction as it is in original Pacman
def createacopyofPacman(Pacman):
    Pacmanexampleforcollisions = moving_object(Pacman.get_speed(), Pacman.get_direction(), widthPac, heightPac,
                                               colorPac)
    Pacmanexampleforcollisions.rect.x = Pacman.rect.x
    Pacmanexampleforcollisions.rect.y = Pacman.rect.y
    return Pacmanexampleforcollisions


Pacmanexampleforcollisions = createacopyofPacman(Pacman)

# Two direction indicators, one for the current, one for the one that is to be the next one
currentdirection = initdirectionPac
newdirection = currentdirection

all_sprites_list.add(Pacman)
# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        # user pressed down on a key
        elif event.type == pygame.KEYDOWN:
            Pacmanexampleforcollisions = createacopyofPacman(Pacman)
            Pacmanexampleforcollisions.signalfromkeyboard(event)
            newdirection = Pacmanexampleforcollisions.get_direction()

    # --- Game logic should go here

    # Pacman moves every step in the game
    # If there was a change of the direction comming from the user
    if currentdirection != newdirection:
        # Then uses the example of Pacman to verify if turn possible
        Pacmanexampleforcollisions.new_direction(newdirection)
        # Moves this example
        Pacmanexampleforcollisions.move()
        # And checks if there would be a collision
        if Pacmanexampleforcollisions.wouldcollide(wall_list):
            # If so, moves Pacman as if there was nothing from the user
            Pacman.moving_object_detecting_collisions(wall_list)
            # And moves the example Pacman as well
            Pacmanexampleforcollisions = createacopyofPacman(Pacman)
        else:
            # If no collision, checks the direction of movement of Pacman
            Pacman.new_direction(newdirection)
            # And moves Pacman
            Pacman.moving_object_detecting_collisions(wall_list)
            # Now the Pacman moves in the direction in which the user wants it to
            currentdirection = newdirection
    # If there is no signal from the user, just moves the Pacman preventing collisions
    else:
        Pacman.moving_object_detecting_collisions(wall_list)
    # screen cleared to white
    screen.fill(WHITE)

    # --- Drawing
    all_sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()