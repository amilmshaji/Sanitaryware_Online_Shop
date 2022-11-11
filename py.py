import sys

import pygame
import time
from pygame.locals import *
clock = pygame.time.Clock()
pygame.init()
WHITE = (255, 255, 255)
WIDTH = 1280
HEIGHT = 800
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
originalImg = pygame.image.load("m10.jpg")
img = pygame.transform.scale(originalImg,(WIDTH,HEIGHT))

while True:
        events = pygame.event.get()
        button_down = pygame.mouse.get_pressed()
        if button_down == (1,0,0):
            #print("Clicked")
            WIDTH = WIDTH+10
            HEIGHT = HEIGHT+10
            img = pygame.transform.scale(originalImg, (WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.fill(WHITE)
        windowSurface.blit(img, (0, 0))
        clock.tick(60)
        pygame.display.flip()