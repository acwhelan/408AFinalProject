# Credit to grx6741 github repository here: https://github.com/grx6741/ElectricFieldVisualizing/blob/main/main.py

import pygame
from numpy import interp
from math import cos, sin, atan2, pi

# Set the dimensions of the window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))

# Constant for electric field calculation
k = 10000

# Set up the frames per second clock
fps = pygame.time.Clock()
FPS = 120

# Function to calculate squared distance between two points (a, b) and (c, d)
def distSquared(a, b, c, d):
    return (a-c)**2 + (b-d)**2

# Function to calculate angle between two points (a, b) and (c, d)
def angleBetween(a, b, c, d):
    return atan2((d - b), (c - a))

# Class representing marks on the screen
class Mark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 5           # Initial radius
        self.stretch = 0     # Initial stretch (for electric field lines)
        self.angle = 0       # Initial angle

    # Function to draw a circle at the mark's position
    def show_circle(self):
        pygame.draw.circle(window, (255, 0, 0), (self.x, self.y), self.r)

    # Function to draw a line representing the electric field at the mark's position
    def show_line(self):
        pygame.draw.line(window, (0, 0, 0), (self.x, self.y), (self.x + self.stretch * cos(self.angle), self.y + self.stretch * sin(self.angle)))

# Class representing a charge
class Charge:
    def __init__(self, charge):
        self.q = charge      # The magnitude of the charge
        self.values = []     # Placeholder for future use

    # Function to calculate the electric field at a mark's position
    def electricField1(self, mark):
        self.pos = pygame.mouse.get_pos()
        dist = distSquared(self.pos[0], self.pos[1], mark.x, mark.y)
        if dist != 0:
            fieldStrength = k * abs(self.q) / dist
            strength = interp(fieldStrength, [0, 200], [1, 30])
            mark.r = strength
            mark.stretch = strength
            ang = angleBetween(self.pos[0], self.pos[1], mark.x, mark.y)
            if self.q > 0:
                mark.angle = ang
            else:
                mark.angle = pi + ang

    # Function to draw electric field lines (currently unused)
    def drawField(self):
        for value in self.values:
            pygame.draw.line(window, (value[0], value[0], value[0]), (value[1], value[2]), (value[1], value[2]))

# Number of marks on the screen
n = 50
# Create marks on the screen in a grid pattern
marks = [Mark(width * x // n, height * y // n) for x in range(0, n+1) for y in range(0, n+1)]

# Create a charge
electron = Charge(30)

# Function to update the screen every frame
def update():
    window.fill((255, 255, 255))
    for mark in marks:
        mark.show_line()
        electron.electricField1(mark)
    pygame.display.update()
    fps.tick(FPS)

# Main loop to keep the program running
def loop():
    while True:
        update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Start the loop
loop()
