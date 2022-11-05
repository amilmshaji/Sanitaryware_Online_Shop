# Python program to move the image
# with the mouse

# Import the library pygame
import pygame
from pygame.locals import *

# Take colors input
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Construct the GUI game
pygame.init()

# Set dimensions of game GUI
w, h = 600, 600
screen = pygame.display.set_mode((w, h))

# Take image as input
img = pygame.image.load('a3.png')
img.convert()

# Draw rectangle around the image
rect = img.get_rect()
rect.center = w // 2, h // 2

# Set running and moving values
running = True
moving = False

# Setting what happens when game
# is in running state
while running:

    for event in pygame.event.get():

        # Close if the user quits the
        # game
        if event.type == QUIT:
            running = False

        # Making the image move
        elif event.type == MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                moving = True

        # Set moving as False if you want
        # to move the image only with the
        # mouse click
        # Set moving as True if you want
        # to move the image without the
        # mouse click
        elif event.type == MOUSEBUTTONUP:
            moving = False

        # Make your image move continuously
        elif event.type == MOUSEMOTION and moving:
            rect.move_ip(event.rel)

    # Set screen color and image on screen
    screen.fill(YELLOW)
    screen.blit(img, rect)

    # Construct the border to the image
    pygame.draw.rect(screen, BLUE, rect, 2)

    # Update the GUI pygame
    pygame.display.update()

# Quit the GUI game
pygame.quit()
