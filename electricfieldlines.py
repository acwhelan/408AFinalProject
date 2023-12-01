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
        # For each election, it will calculate the square of the distance between the point (x,y) 
        r_squared = (x - electron.x)**2 + (y - electron.y)**2
        # Coulomb's law to calculate the magnitude of the efield 
        magnitude = k * electron.charge / r_squared
        # The direction of the efield due to each electron, calculating the difference between x and y to compute the difference
        # divided by the square root of the distance, which normalizes the magnitude of the vector (making it a unit vector)
        r_hat_x = (x - electron.x) / np.sqrt(r_squared)
        r_hat_y = (y - electron.y) / np.sqrt(r_squared)
        # Adding to the Efield components 
        E_x += magnitude * r_hat_x
        E_y += magnitude * r_hat_y
    return E_x, E_y

# taking in a list of electron objects 
def draw_electric_field_lines(electrons):
       # starting a loop over the x coordinates on the screen, creating a sequence of numbers from 0 to 
       # the width of the window, with a step of 20 (0, 20, 40 and so on)
       for x in range(0, width, 20):
       # starting a loop over the x coordinates on the screen, creating a sequence of numbers from 0 to 
       # the width of the window, with a step of 20 (0, 20, 40 and so on)
        for y in range(0, height, 20):
            # I compute my E_x and E_y components, plugging in an x, y and list of electrons 
            # this computes the electric field vector at every point (x,y) on the grid 
            E_x, E_y = electric_field(x, y, electrons)
            # the length of the electric field vector E is computed using pythagorean theorem of the computed x and y components 
            length = np.sqrt(E_x**2 + E_y**2)
            # this line checks if the calculated length of the electric field is greater than 0
            # if it's zero then there's no electric field at this point so no line drawn 
            if length > 0:
                # normalizing both the x and the y components
                unit_vector_x = E_x / length
                unit_vector_y = E_y / length
                # draws the line on the window, starting from (x, y) and ending at (x + unit_vector_x * 20, y + unit_vector_y * 20)
                # 20 because it extends 20 pixels in the direction of the electric field, with a width of 1 pixel
                pygame.draw.line(window, (0, 0, 0), (x, y), (x + unit_vector_x * 20, y + unit_vector_y * 20), 1)

def main():
    # Allows the prograam to run until variable is later set to false
    running = True
    # initializes an empty list of electrons, that will store instances of the Electron class
    electrons = []

    # starts the execution of the project
    while running:
        # clears the window to white
        window.fill((255, 255, 255))
        # start a loop to process all of the events in the Pygame evvent queue
        for event in pygame.event.get():
            # closing a window, set running to false 
            if event.type == pygame.QUIT:
                running = False
            # if mouse button press, charge is 1 and if 2 buttons charge is -1 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                charge = 1 if event.button == 1 else -1
                electrons.append(Electron(*event.pos, charge))

         #   elif event.type == pygame.MOUSEMOTION:
               # for electron in electrons:
                 #   if electron.dragging:
                     #   electron.x, electron.y = event.pos
            # if the mouse button is up, it sets the dragging of all electrons to false
            # stops all drag motion
            elif event.type == pygame.MOUSEBUTTONUP:
                for electron in electrons:
                    electron.dragging = False

        # draws all the electron field lines
        draw_electric_field_lines(electrons)

        # draw all the point charges 
        for electron in electrons:
            electron.draw()

        # update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
