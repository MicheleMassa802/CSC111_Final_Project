""" CSC111 Winter 2021 Course Project: Superficial Manager

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the code needed to start up and run the entire
"EFFICIENT SPACE TRAVERSAL" program, and is in charge of managing the running of the program
until the user clicks the "x" on the corner of the pygame window (GUI).

Instructions:
    - Simply run the program and you will be met with the main menu of the program.
    - From there refer to the "A Manual to Efficient Space Traversal" PDF file, or the
    more superficial instructions that can be found on each pygame menu window or in the
    written report.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox.
"""


###########
# IMPORTS #
###########


import pygame
import program


##########################
# PROGRAM'S RUNNING LOOP #
##########################

def run_sim() -> None:
    """ Function in charge of running the program whenever this file is ran.
    """
    gui = program.Program()  # start the Program class

    while gui.running:
        gui.curr_menu.display_menu()
        gui.program_menu_loop()

    # Quit the pygame window once the running attribute becomes False
    pygame.display.quit()
    pygame.quit()


# Some errors raised were counter-intuitive which is why we have removed them
if __name__ == '__main__':

    # make function call to start program as soon as file is ran
    run_sim()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913', 'E1101'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })
