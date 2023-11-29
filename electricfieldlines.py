# Credit to grx6741 github repository here: https://github.com/grx6741/ElectricFieldVisualizing/blob/main/main.py

import pygame
import numpy as np

# Set the dimensions of the window
width, height = 1000, 800
window = pygame.display.set_mode((width, height))

# Constant for electric field calculation
k = 8.9875517873681764e9

# Defining our electron class, which takes its own instance as a parameter, a point (x,y), and a charge value 
class Electron:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        self.dragging = False

    # In this function, the electron is drawn, red if the charge is greater than 0 or blue if it is less than 0 
    def draw(self):
        color = (255, 0, 0) if self.charge > 0 else (0, 0, 255)
        pygame.draw.circle(window, color, (self.x, self.y), 5)

# Defining our electric field, which takes a point (x,y) and a list of electrons
def electric_field(x, y, electrons):
    # Initializes E_x and E_y, and used to accumulate the components of the efield at the point (x, y)
    E_x, E_y = 0, 0

    # Iterating through each electron in the list of electrons 
    for electron in electrons:
        # The square of the distance between the point (x,y) and the electron 
        r_squared = (x - electron.x)**2 + (y - electron.y)**2
        # Coulomb's law to calculate the magnitude of the efield 
        magnitude = k * electron.charge / r_squared
        # The direction of the efield due to each electron 
        r_hat_x = (x - electron.x) / np.sqrt(r_squared)
        r_hat_y = (y - electron.y) / np.sqrt(r_squared)
        # Adding to the Efield components 
        E_x += magnitude * r_hat_x
        E_y += magnitude * r_hat_y
    return E_x, E_y

def draw_electric_field_lines(electrons):
       for x in range(0, width, 20):
        for y in range(0, height, 20):
            E_x, E_y = electric_field(x, y, electrons)
            length = np.sqrt(E_x**2 + E_y**2)
            if length > 0:
                unit_vector_x = E_x / length
                unit_vector_y = E_y / length
                pygame.draw.line(window, (0, 0, 0), (x, y), (x + unit_vector_x * 20, y + unit_vector_y * 20), 1)

def initialize_electric_field_lines(electrons):
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            E_x, E_y = electric_field(x, y, electrons)
            length = np.sqrt(E_x**2 + E_y**2)
            if length > 0:
                unit_vector_x = E_x / length
                unit_vector_y = E_y / length
                pygame.draw.line(window, (0, 0, 0), (x, y), (x + unit_vector_x * 20, y + unit_vector_y * 20), 1)

def main():
    running = True
    electrons = []

    while running:
        window.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                charge = 1 if event.button == 1 else -1
                electrons.append(Electron(*event.pos, charge))
            elif event.type == pygame.MOUSEMOTION:
                for electron in electrons:
                    if electron.dragging:
                        electron.x, electron.y = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                for electron in electrons:
                    electron.dragging = False

        draw_electric_field_lines(electrons)

        for electron in electrons:
            electron.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
