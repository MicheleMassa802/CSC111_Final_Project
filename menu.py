""" CSC111 Winter 2021 Course Project: Menu Manager

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the code needed to run the various menus that can be accessed
through the Program class. It controls the interactions between consecutive menus and most of
the displaying that is done on the user's pygame window.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox.
"""

###########
# IMPORTS #
###########

from typing import Optional
import csv
import pygame
from pygame.colordict import THECOLORS
from algorithm_classes import create_blank_graph, load_csv_into_graph, Graph
from algorithm_classes_v2 import world_cities_graph, WeightedGraph
from api import world_countries_graph


#############
# CONSTANTS #
#############

# general data
WINDOW_SIZE = (800, 810)

# maze data
MAZE1 = ('datasets/MAP1_csv.csv', (9, 9))
MAZE2 = ('datasets/MAP2_csv.csv', (20, 20))
MAZE3 = ('datasets/MAP3_csv.csv', (13, 9))
MAZE4 = ('datasets/MAP4_csv.csv', (18, 14))

# Air route data:
AR_DIM = (8, 10)
ARC_DIM = (4, 5)


#####################
# Menu Parent Class #
#####################


class Menu:
    """ The class controlling the direct interactions between an user and a menu being
    displayed on a pygame window.

    Instance Attributes:
        - self.program: display module connecting a menu to the Program class and its methods.
        - self.run_display: bool determining the current state of a menu object (active
        or inactive).
        - self.mid_coords: tuple of ints representing the pixel position of the center of
        the pygame window.
        - self.user_pos: the '->' str showing the user the position of their cursor in arrow
        key oriented menus.
        - self.offset: int representing the distance between the cursor and the center of the
        text it highlights (so that it is put to the left of this text).

    Representation Invariants:
        - self.mid_coords[0] == 400 and self.mid_coords[1] == 405
        - 0 <= self.user_pos.x <= 800
        - 0 <= self.user_pos.y <= 810
        """

    program: pygame.display
    run_display: bool
    mid_coords: tuple[int, int]
    user_pos: pygame.Rect
    offset: int

    def __init__(self, menu_program: pygame.display) -> None:
        """ Initialize a Menu object and its attributes along with the given
        program.
        """
        self.program = menu_program
        self.run_display = True
        self.mid_coords = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)  # width-height
        self.user_pos = pygame.Rect(0, 0, 50, 50)  # user's '->'
        self.offset = -200

    def draw_cursor(self) -> None:
        """ The function in charge of displaying the user's cursor in arrow key
        oriented movement menus, highlighting the option the user is currently
        pointing at.
        """
        self.program.draw_title_text(25, '->', (self.user_pos.x, self.user_pos.y))

    def blit_screen(self) -> None:
        """ Function in charge of loading and updating the text and other widgets being
        displayed on the current pygame window.
        """
        # align program.display to program.window
        self.program.window.blit(self.program.display, (0, 0))
        pygame.display.update()  # update any changes the pygame window has undergone
        self.program.reset_keys()  # reset all keyboard keys state to not active (False)


###################
# Menu Subclasses #
###################


class MainMenu(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the main menu of this program (the first thing to pop up when this project is
    run).

    Instance Attributes:
        - self.state: str representing the current state of the user's position (which
        option is being currently hovered).
        - self.sp_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the simple program menu.
        - self.mazep_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the maze program menu.
        - self.ar_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the air routes program menu.
        - self.arc_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the air costs program menu.

    Representation Invariants:
        - self.state in {'simple', 'maze', 'air', 'air_cost'}
        - 0 <= self.sp_coords[0] <= 800 and 0 <= self.sp_coords[1] <= 810
        - 0 <= self.mazep_coords[0] <= 800 and 0 <= self.mazep_coords[1] <= 810
        - 0 <= self.ar_coords[0] <= 800 and 0 <= self.ar_coords[1] <= 810
        - 0 <= self.arc_coords[0] <= 800 and 0 <= self.arc_coords[1] <= 810
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    state: str
    sp_coords: tuple[int, int]
    mazep_coords: tuple[int, int]
    ar_coords: tuple[int, int]
    arc_coords: tuple[int, int]

    def __init__(self, program: pygame.display) -> None:
        """ Initialize a MainMenu object and its attributes along with the given
        program, displaying all the contents of this menu according to the display_menu
        method loop.
        """
        Menu.__init__(self, program)

        # attributes for the possible states:
        self.state = 'simple'
        self.sp_coords = (self.mid_coords[0], self.mid_coords[1] - 75)
        self.mazep_coords = (self.mid_coords[0], self.mid_coords[1])
        self.ar_coords = (self.mid_coords[0], self.mid_coords[1] + 75)
        self.arc_coords = (self.mid_coords[0], self.mid_coords[1] + 150)
        # update of Menu class self.user_pos to align text with position of indicator '->'
        self.user_pos.midtop = (self.sp_coords[0] + self.offset, self.sp_coords[1])

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the MainMenu screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background color

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 60])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 60])
            self.program.draw_title_text(20, "Main Menu", (70, 30), 'white')
            self.program.draw_title_text(32, "EFFICIENT SPACE TRAVERSAL PROGRAM",
                                         (self.mid_coords[0], 125))
            authors = 'A project developed by: Michele, Nathan, Nischal'
            self.program.draw_title_text(20, authors, (self.mid_coords[0], 165))
            instructions1 = "1) Use arrow keys to move around the menu, and press ENTER to enter " \
                            "one of the sub-menus"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0],
                                                             self.mid_coords[1] - 150))
            instructions2 = "2) At any point in time, you can press BACKSPACE to go to the" \
                            " previous menu you were in"
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0],
                                                             self.mid_coords[1] + 225))
            instructions2 = "This action doesn't save any changes made to graphs"
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0],
                                                             self.mid_coords[1] + 250))
            self.program.draw_title_text(20, "SIMPLE PROGRAM BFS INPUT (LVL 1)", self.sp_coords)
            self.program.draw_title_text(20, "PRESET MAZE PROGRAM (LVL 2)", self.mazep_coords)
            self.program.draw_title_text(20, "AIR ROUTES CONNECTIONS (LVL 3)", self.ar_coords)
            self.program.draw_title_text(20, "AIR COST CONNECTIONS (LVL 4)", self.arc_coords)
            self.draw_cursor()

            # update screen
            self.blit_screen()

    def move_user_cursor(self) -> None:
        """ Method handling the way the user's "cursor" ('->') is to move according to
        the user's arrow key input in this menu.
        """
        # control movement when user presses the down key
        if self.program.down_key:
            if self.state == 'simple':
                self.user_pos.midtop = (self.mazep_coords[0] + self.offset,
                                        self.mazep_coords[1])
                self.state = 'maze'

            elif self.state == 'maze':
                self.user_pos.midtop = (self.ar_coords[0] + self.offset,
                                        self.ar_coords[1])
                self.state = 'air'

            elif self.state == 'air':
                # going down when you are at the last option takes you to the top
                self.user_pos.midtop = (self.arc_coords[0] + self.offset,
                                        self.arc_coords[1])
                self.state = 'airc'
            elif self.state == 'airc':
                # going down when you are at the last option takes you to the top
                self.user_pos.midtop = (self.sp_coords[0] + self.offset,
                                        self.sp_coords[1])
                self.state = 'simple'

        # control movement when user presses the up key
        elif self.program.up_key:
            if self.state == 'simple':
                # going up when you are at the first option takes you to the bottom
                self.user_pos.midtop = (self.arc_coords[0] + self.offset,
                                        self.arc_coords[1])
                self.state = 'airc'

            elif self.state == 'airc':
                self.user_pos.midtop = (self.ar_coords[0] + self.offset,
                                        self.ar_coords[1])
                self.state = 'air'

            elif self.state == 'air':
                self.user_pos.midtop = (self.mazep_coords[0] + self.offset,
                                        self.mazep_coords[1])
                self.state = 'maze'

            elif self.state == 'maze':
                self.user_pos.midtop = (self.sp_coords[0] + self.offset,
                                        self.sp_coords[1])
                self.state = 'simple'

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the MainMenu, these inputs are
        independent from arrow key movement and consist of executing the commands to
        go into one of the selected sub-menus by pressing ENTER.
        """
        self.move_user_cursor()

        if self.program.enter_key:
            if self.state == 'simple':
                self.program.curr_menu = self.program.simple_program_menu
            elif self.state == 'maze':
                self.program.curr_menu = self.program.maze_program_menu
            elif self.state == 'air':
                self.program.curr_menu = self.program.air_routes_program_menu
            elif self.state == 'airc':
                self.program.curr_menu = self.program.air_cost_program_menu

            self.run_display = False


class SpMenu(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the simple program's menu of this program (accessed by selecting the Simple
    Program option on the main menu).

    Instance Attributes:
        - self.state: str representing the current state of the user's position (which
        option is being currently hovered).
        - self.input_hor_dimension: the int keeping track of the horizontal dimension of the
        grid (graph) presented to the user when this program is run.
        - self.input_ver_dimension: the int keeping track of the vertical dimension of the
        grid (graph) presented to the user when this program is run.
        - self.hd_coords: tuple of ints representing the position of the text used to signal
        the widget taking inputs to update self.input_hor_dimension.
        - self.vd_coords: tuple of ints representing the position of the text used to signal
        the widget taking inputs to update self.input_ver_dimension.
        - self.next_win_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the simple program implementation window.

    Representation Invariants:
        - self.state in {'hd', 'vd', 'next_win'}
        - 5 <= self.input_hor_dimension <= 20
        - 5 <= self.input_ver_dimension <= 20
        - 0 <= self.hd_coords[0] <= 800 and 0 <= self.hd_coords[1] <= 810
        - 0 <= self.vd_coords[0] <= 800 and 0 <= self.vd_coords[1] <= 810
        - 0 <= self.next_win_coords[0] <= 800 and 0 <= self.next_win_coords[1] <= 810
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    state: str
    input_hor_dimension: int
    input_ver_dimension: int
    hd_coords: tuple[int, int]
    vd_coords: tuple[int, int]
    next_win_coords: tuple[int, int]

    def __init__(self, program: pygame.display) -> None:
        """ Initialize a SpMenu object and its attributes along with the given
        program, displaying all the contents of this menu according to the display_menu
        method loop.
        """
        Menu.__init__(self, program)

        self.state = 'hd'
        self.input_hor_dimension = 5
        self.input_ver_dimension = 5
        self.hd_coords = (self.mid_coords[0], self.mid_coords[1] - 100)
        self.vd_coords = (self.mid_coords[0], self.mid_coords[1])
        self.next_win_coords = (self.mid_coords[0], self.mid_coords[1] + 100)
        # update of Menu class self.user_pos to align text with position of indicator '->'
        self.user_pos.midtop = (self.hd_coords[0] + self.offset, self.hd_coords[1])

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the SpMenu screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background color

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 60])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 60])
            self.program.draw_title_text(20, "Simple Program Menu", (120, 30), 'white')

            instructions1 = "1) Use vertical arrow keys to move around the options to modify the" \
                            " dimensions of the desired graph"
            instructions2 = "2) Use horizontal arrow keys to modify the current selected dimension"
            instructions3 = "3) Scroll down to START and press ENTER to start running " \
                            "this program"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 100))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 140))
            self.program.draw_title_text(16, instructions3, (self.mid_coords[0], 180))

            self.program.draw_title_text(20, "HORIZONTAL DIMENSION", self.hd_coords)
            self.program.draw_title_text(20, "VERTICAL DIMENSION", self.vd_coords)
            self.program.draw_title_text(20, "START", self.next_win_coords)

            # changing values
            self.program.draw_title_text(24, str(self.input_hor_dimension),
                                         (self.hd_coords[0] + 270, self.hd_coords[1]))
            self.program.draw_title_text(24, str(self.input_ver_dimension),
                                         (self.vd_coords[0] + 270, self.vd_coords[1]))

            self.draw_cursor()

            # update screen
            self.blit_screen()

    def move_user_cursor(self) -> None:
        """ Method handling the way the user's "cursor" ('->') is to move according to
        the user's arrow key input in this menu.
        """
        if self.program.down_key:
            if self.state == 'hd':
                self.user_pos.midtop = (self.vd_coords[0] + self.offset,
                                        self.vd_coords[1])
                self.state = 'vd'
            elif self.state == 'vd':
                self.user_pos.midtop = (self.next_win_coords[0] + self.offset,
                                        self.next_win_coords[1])
                self.state = 'next_win'
            elif self.state == 'next_win':
                # going down when you are at the last option takes you to the top
                self.user_pos.midtop = (self.hd_coords[0] + self.offset,
                                        self.hd_coords[1])
                self.state = 'hd'

        elif self.program.up_key:
            if self.state == 'hd':
                # going up when you are at the first option takes you to the bottom
                self.user_pos.midtop = (self.next_win_coords[0] + self.offset,
                                        self.next_win_coords[1])
                self.state = 'next_win'
            elif self.state == 'next_win':
                self.user_pos.midtop = (self.vd_coords[0] + self.offset,
                                        self.vd_coords[1])
                self.state = 'vd'
            elif self.state == 'vd':
                self.user_pos.midtop = (self.hd_coords[0] + self.offset,
                                        self.hd_coords[1])
                self.state = 'hd'

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them (passing the correct data onto th next window's class).
        In this case, this method works along move_user_cursor to detect arrow key movement,
        and also executes commands to go to the previous window or to proceed to the next
        one.
        """
        self.move_user_cursor()

        if self.program.back_key:
            self.program.curr_menu = self.program.main_menu
            self.run_display = False

        # left key decreases dimension
        elif self.program.left_key and self.state == 'hd':
            if self.input_hor_dimension <= 5:
                pass
            else:
                self.input_hor_dimension -= 1

        elif self.program.left_key and self.state == 'vd':
            if self.input_ver_dimension <= 5:
                pass
            else:
                self.input_ver_dimension -= 1

        # right key increase dimension
        elif self.program.right_key and self.state == 'hd':
            if self.input_hor_dimension >= 20:
                pass
            else:
                self.input_hor_dimension += 1

        elif self.program.right_key and self.state == 'vd':
            if self.input_ver_dimension >= 20:
                pass
            else:
                self.input_ver_dimension += 1

        # ENTER starts simulation for user
        elif self.program.enter_key:
            if self.state == 'next_win':
                # self.update_real_dimensions()
                new_dimensions = (self.input_hor_dimension, self.input_ver_dimension)
                self.program.simple_program_run = SimpleProgramRun(self.program, new_dimensions)
                self.program.curr_menu = self.program.simple_program_run
            else:
                pass

            self.run_display = False


class SimpleProgramRun(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the simple program's simulation.

    Instance Attributes:
        - self.graph: the standard graph object representing a space to be traversed.
        - self.grid_dimensions: the tuple of ints keeping track of the dimension of the grid
        to be drawn on the user's screen based on the input from the previous menu window.
        - self.start_pos: the tuple of ints representing the starting position of the user on
        the grid representing the graph.
        - self.end_pos: the tuple of ints representing the end position of the user on
        the grid representing the graph.
        - self.show_message: bool keeping track of whether or not the user has tried to make
        and invalid shortest path computation (unable to go from self.start_pos to
        self.end_pos), triggering the showing of an alert notifying user of the invalid input.

    Representation Invariants:
        - 5 <= self.grid_dimensions[0] <= 20
        - 5 <= self.grid_dimensions[1] <= 20
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: Graph
    grid_dimensions: tuple[int, int]
    start_pos = Optional[tuple[int, int]]
    end_pos = Optional[tuple[int, int]]
    show_message: bool

    def __init__(self, program: pygame.display, grid_dimensions: tuple[int, int]) -> None:
        """ Initialize a SimpleProgramRun object and its attributes along with the given
        program, displaying all the contents of this simulation menu according to the
        display_menu method loop.
        """
        Menu.__init__(self, program)
        self.graph = create_blank_graph(grid_dimensions[0],
                                        grid_dimensions[1])
        self.grid_dimensions = grid_dimensions
        self.start_pos = None
        self.end_pos = None

        self.show_message = False

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the SimpleProgramRun screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background colour

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 40])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 40])
            self.program.draw_title_text(20, "Simple Program Run", (120, 20), 'white')

            instructions1 = "1) Click on cells to modify this graph, press ENTER to find the best" \
                            " BFS path from start to end"
            instructions2 = "2) Left click: block cell; Right click: start vertex," \
                            " Middle click: end vertex"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 55))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 80))

            self.program.draw_grid(self.grid_dimensions, self.graph)

            if self.show_message is True:
                ttd = 'NO VALID PATH'
                self.program.draw_title_text(14, ttd, (650, 20), 'red')

            # update screen
            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the SimpleProgramRun window, these
        inputs consist of mouse clicks allowing the user to mutate the graph and customize
        the space to be traversed, and keyboard inputs executing commands to go to the previous
        window or to make the call to the function that calculates and displays the shortest
        path between the user's selected self.start_pos and self.end_pos positions.
        """
        if self.program.back_key:
            self.program.curr_menu = self.program.simple_program_menu
            self.run_display = False

        # handle mouse input

        if self.program.left_click[0]:
            pos = self.program.left_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.grid_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.grid_dimensions[1])))
            coord_number = find_coord(self.grid_dimensions, cell_num)
            number_of_cells = self.grid_dimensions[0] * self.grid_dimensions[1]

            # if number_of_cells >= coord_number:
            if valid_cell(self.grid_dimensions, cell_num, coord_number, number_of_cells):
                # change vertex state to 'blocked'
                self.graph.vertices[cell_num].state = 'blocked'

        elif self.program.right_click[0]:
            pos = self.program.right_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.grid_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.grid_dimensions[1])))
            coord_number = find_coord(self.grid_dimensions, cell_num)
            number_of_cells = self.grid_dimensions[0] * self.grid_dimensions[1]

            if valid_cell(self.grid_dimensions, cell_num, coord_number, number_of_cells) \
                    and self.start_pos is None:
                # change vertex state to 'start'
                self.graph.vertices[cell_num].state = 'start'
                self.start_pos = self.graph.vertices[cell_num].pos

        elif self.program.mid_click[0]:
            pos = self.program.mid_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.grid_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.grid_dimensions[1])))
            coord_number = find_coord(self.grid_dimensions, cell_num)
            number_of_cells = self.grid_dimensions[0] * self.grid_dimensions[1]
            # see how coord_number works
            if valid_cell(self.grid_dimensions, cell_num, coord_number, number_of_cells) \
                    and self.end_pos is None:
                # change vertex state to 'end'
                self.graph.vertices[cell_num].state = 'end'
                self.end_pos = self.graph.vertices[cell_num].pos

        if self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                self.draw_path()

    def draw_path(self) -> None:
        """ Method in charge of making the call to the Breadth First Search algorithm
        which calculates the path to be followed by the user, and displaying this path on
        the SimpleProgramRun screen by mutating the user's graph.
        """
        path_to_follow = self.graph.breadth_first_search(self.start_pos, self.end_pos)

        if path_to_follow is None:
            self.show_message = True
        else:  # path_to_follow is a valid path
            for vertex in path_to_follow:
                self.graph.vertices[vertex].state = 'path'


class MazeProgramMenu(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the maze program's menu of this program (accessed by selecting the Maze
    Program option on the main menu).

    Instance Attributes:
        - self.state: str representing the current state of the user's position (which
        option is being currently hovered).
        - self.selected_maze: str keeping track of the user's current pick out the 4 preset
        mazes (and cities) to access in the next window.
        - self.small_offset: int representing the distance between the cursor and the center
        of the text it highlights (so that it is put to the left of this text).
        - self.map1_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to select map1 as the preset graph to visualize.
        - self.map2_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to select map2 as the preset graph to visualize.
        - self.map3_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to select map3 as the preset graph to visualize.
        - self.map4_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to select map4 as the preset graph to visualize.
        - self.next_win_coords: tuple of ints representing the position of the text used to signal
        the "button" to be "pressed" to enter the simple program implementation window.

    Representation Invariants:
        - self.state in {'map1', 'map2', 'map3', 'map4', 'next_win', 'none'}
        - 0 <= self.map1_coords[0] <= 800 and 0 <= self.map1_coords[1] <= 810
        - 0 <= self.map2_coords[0] <= 800 and 0 <= self.map1_coords[1] <= 810
        - 0 <= self.map3_coords[0] <= 800 and 0 <= self.map1_coords[1] <= 810
        - 0 <= self.map4_coords[0] <= 800 and 0 <= self.map1_coords[1] <= 810
        - 0 <= self.next_win_coords[0] <= 800 and 0 <= self.next_win_coords[1] <= 810
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    state: str
    selected_maze: str
    small_offset: int
    map1_coords: tuple[int, int]
    map2_coords: tuple[int, int]
    map3_coords: tuple[int, int]
    map4_coords: tuple[int, int]
    next_win_coords: tuple[int, int]

    def __init__(self, program: pygame.display) -> None:
        """ Initialize a MazeProgramMenu object and its attributes along with the given
        program, displaying all the contents of this menu according to the display_menu
        method loop.
        """
        Menu.__init__(self, program)

        self.state = 'map1'
        self.selected_maze = 'None'
        self.small_offset = -40
        self.map1_coords = (self.mid_coords[0] - 150, 200)
        self.map2_coords = (self.mid_coords[0] - 150, self.map1_coords[1] + 150)
        self.map3_coords = (self.mid_coords[0] - 150, self.map2_coords[1] + 150)
        self.map4_coords = (self.mid_coords[0] - 150, self.map3_coords[1] + 150)
        self.next_win_coords = (self.mid_coords[0], 750)

        self.user_pos.midtop = (self.map1_coords[0] + self.small_offset, self.map1_coords[1])

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the MazeProgramMEnu screen being shown to the user.
        """
        # load images
        map_1_img = pygame.image.load('media/MAP1_pic.png')
        map_2_img = pygame.image.load('media/MAP2_pic.png')
        map_3_img = pygame.image.load('media/MAP3_pic.png')
        map_4_img = pygame.image.load('media/MAP4_pic.png')

        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background color

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 60])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 60])
            self.program.draw_title_text(20, "Maze Menu", (70, 30), 'white')

            instructions1 = "1) Use arrow keys to move around the menu, and press ENTER to " \
                            "select a preset graph"
            instructions2 = "2) Scroll down to START and press ENTER to run program"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 80))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 120))

            self.program.draw_title_text(20, "MAP 1", self.map1_coords)
            self.program.display.blit(map_1_img, (self.map1_coords[0] + 200,
                                                  self.map1_coords[1] - 50))
            self.program.draw_title_text(20, "MAP 2", self.map2_coords)
            self.program.display.blit(map_2_img, (self.map2_coords[0] + 200,
                                                  self.map2_coords[1] - 50))
            self.program.draw_title_text(20, "MAP 3", self.map3_coords)
            self.program.display.blit(map_3_img, (self.map3_coords[0] + 200,
                                                  self.map3_coords[1] - 50))
            self.program.draw_title_text(20, "MAP 4", self.map4_coords)
            self.program.display.blit(map_4_img, (self.map4_coords[0] + 200,
                                                  self.map4_coords[1] - 50))

            self.program.draw_title_text(20, "START", self.next_win_coords)
            self.draw_cursor()

            # update screen
            self.blit_screen()

    def move_user_cursor(self) -> None:
        """ Method handling the way the user's "cursor" ('->') is to move according to
        the user's arrow key input in this menu.
        """
        if self.program.down_key:
            if self.state == 'map1':
                self.user_pos.midtop = (self.map2_coords[0] + self.small_offset,
                                        self.map2_coords[1])
                self.state = 'map2'
            elif self.state == 'map2':
                self.user_pos.midtop = (self.map3_coords[0] + self.small_offset,
                                        self.map3_coords[1])
                self.state = 'map3'
            elif self.state == 'map3':
                self.user_pos.midtop = (self.map4_coords[0] + self.small_offset,
                                        self.map4_coords[1])
                self.state = 'map4'
            elif self.state == 'map4':
                self.user_pos.midtop = (self.next_win_coords[0] + self.small_offset,
                                        self.next_win_coords[1])
                self.state = 'next_win'
            elif self.state == 'next_win':
                # going down when you are at the last option takes you to the top
                self.user_pos.midtop = (self.map1_coords[0] + self.small_offset,
                                        self.map1_coords[1])
                self.state = 'map1'

        elif self.program.up_key:
            if self.state == 'map1':
                # going up when you are at the first option takes you to the bottom
                self.user_pos.midtop = (self.next_win_coords[0] + self.small_offset,
                                        self.next_win_coords[1])
                self.state = 'next_win'
            elif self.state == 'map2':
                self.user_pos.midtop = (self.map1_coords[0] + self.small_offset,
                                        self.map1_coords[1])
                self.state = 'map1'
            elif self.state == 'map3':
                self.user_pos.midtop = (self.map2_coords[0] + self.small_offset,
                                        self.map2_coords[1])
                self.state = 'map2'
            elif self.state == 'map4':
                self.user_pos.midtop = (self.map3_coords[0] + self.small_offset,
                                        self.map3_coords[1])
                self.state = 'map3'
            elif self.state == 'next_win':
                # going down when you are at the last option takes you to the top
                self.user_pos.midtop = (self.map4_coords[0] + self.small_offset,
                                        self.map4_coords[1])
                self.state = 'map4'

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them (passing the correct data onto th next window's class).
        In this case, for the MazeProgramMenu, these inputs independent from arrow key
        movement consist of selecting a preset graph to customize and going into one of
        these selected preset's simulations, or going back to the previous window.
        """
        self.move_user_cursor()

        if self.program.back_key:
            self.program.curr_menu = self.program.main_menu
            self.run_display = False

        # ENTER starts simulation for user
        elif self.program.enter_key:
            if self.state != 'next_win':
                self.selected_maze = self.state
            else:  # if self.state == 'next_window'
                maze_info = get_maze_details(self.selected_maze)
                self.program.maze_program_run = MazeProgramRun(self.program, maze_info[0],
                                                               maze_info[1])
                if self.selected_maze == 'map4':
                    self.program.maze_program_run.map_4 = True
                self.program.curr_menu = self.program.maze_program_run

            self.run_display = False


class MazeProgramRun(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the maze program's simulation.

    Instance Attributes:
        - self.graph: the standard graph object representing a space to be traversed.
        - self.maze_dimensions: the tuple of ints keeping track of the dimension of the grid
        to be drawn on the user's screen based on the user's selected preset graph.
        - self.start_pos: the tuple of ints representing the starting position of the user on
        the grid representing the graph.
        - self.end_pos: the tuple of ints representing the end position of the user on
        the grid representing the graph.
        - self.show_message: bool keeping track of whether or not the user has tried to make
        and invalid shortest path computation (unable to go from self.start_pos to
        self.end_pos), triggering the showing of an alert notifying user of the invalid input.
        - self.map_4: bool representing the case of the user selecting the Map 4 preset in the
        previous window. If this attribute is True, special characteristics are given to the
        simulation.

    Representation Invariants:
        - 5 <= self.maze_dimensions[0] <= 20
        - 5 <= self.maze_dimensions[1] <= 20
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: Graph
    maze_dimensions: tuple[int, int]
    start_pos: Optional[tuple[int, int]]
    end_pos: Optional[tuple[int, int]]
    show_message: bool
    map_4: bool

    def __init__(self, program: pygame.display, maze_file: str, maze_dim: tuple[int, int]) -> None:
        """ Initialize a MazeProgramRun object and its attributes along with the given
        program, displaying all the contents of this simulation menu according to the
        display_menu method loop.
        """
        Menu.__init__(self, program)

        self.graph = load_csv_into_graph(maze_file)
        self.maze_dimensions = maze_dim

        self.start_pos = None
        self.end_pos = None

        self.show_message = False
        self.map_4 = False

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the MazeProgramRun screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background colour

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 40])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 40])
            self.program.draw_title_text(20, "Maze Program Run", (110, 20), 'white')

            instructions1 = "1) Click on cells to modify this graph, press ENTER to find the best" \
                            " BFS path from start to end"
            instructions2 = "2) Left click: block vertex; Right click: start vertex," \
                            " Middle click: end vertex"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 55))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 80))

            # recognize special case MAP4
            if self.map_4:
                bg = pygame.image.load('media/MAP4_BG_pic.png')
                self.program.display.blit(bg, (50, 100))
                self.program.draw_invis_grid(self.maze_dimensions, self.graph)
                if self.program.enter_key:
                    if self.start_pos is not None and self.end_pos is not None:
                        self.draw_path()

            # proceed with any of the normal cases
            else:
                self.program.draw_grid(self.maze_dimensions, self.graph)

            if self.show_message is True:
                ttd = 'NO VALID PATH'
                self.program.draw_title_text(14, ttd, (650, 20), 'red')

            # update screen
            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the MazeProgramRun window, these
        inputs consist of mouse clicks allowing the user to mutate the graph and customize
        the space to be traversed, and keyboard inputs executing commands to go to the previous
        window or to make the call to the function that calculates and displays the shortest
        path between the user's selected self.start_pos and self.end_pos positions.
        """
        if self.program.back_key:
            self.program.curr_menu = self.program.maze_program_menu
            self.run_display = False

        # handle mouse input

        if self.program.left_click[0]:
            pos = self.program.left_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.maze_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.maze_dimensions[1])))
            coord_number = find_coord(self.maze_dimensions, cell_num)
            number_of_cells = self.maze_dimensions[0] * self.maze_dimensions[1]

            if valid_cell(self.maze_dimensions, cell_num, coord_number, number_of_cells):
                # change vertex state to 'blocked'
                self.graph.vertices[cell_num].state = 'blocked'

        elif self.program.right_click[0]:
            pos = self.program.right_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.maze_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.maze_dimensions[1])))
            coord_number = find_coord(self.maze_dimensions, cell_num)
            number_of_cells = self.maze_dimensions[0] * self.maze_dimensions[1]

            if valid_cell(self.maze_dimensions, cell_num, coord_number, number_of_cells) \
                    and self.start_pos is None:
                # change vertex state to 'start'
                self.graph.vertices[cell_num].state = 'start'
                self.start_pos = self.graph.vertices[cell_num].pos

        elif self.program.mid_click[0]:
            pos = self.program.mid_click[1]
            cell_num = ((pos[0] - 50) // (700 // self.maze_dimensions[0]),
                        ((pos[1] - 90) // (700 // self.maze_dimensions[1])))
            coord_number = find_coord(self.maze_dimensions, cell_num)
            number_of_cells = self.maze_dimensions[0] * self.maze_dimensions[1]
            # see how coord_number works
            if valid_cell(self.maze_dimensions, cell_num, coord_number, number_of_cells) \
                    and self.end_pos is None:
                # change vertex state to 'end'
                self.graph.vertices[cell_num].state = 'end'
                self.end_pos = self.graph.vertices[cell_num].pos

        if self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                self.draw_path()

    def draw_path(self) -> None:
        """ Method in charge of making the call to the Breadth First Search algorithm
        which calculates the path to be followed by the user, and displaying this path on
        the MazeProgramRun screen by mutating the user's graph.
        """
        path_to_follow = self.graph.breadth_first_search(self.start_pos, self.end_pos)

        if path_to_follow is None:
            self.show_message = True
        else:  # path_to_follow is a valid path
            for vertex in path_to_follow:
                self.graph.vertices[vertex].state = 'path'


class AirProgramMenu(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the air program's menu of this program (accessed by selecting the Air Routes
    Program option on the main menu).

    Instance Attributes:
        - self.graph: the weighted graph object representing a space to be traversed
        in the next window. At this stage, in this menu, the graph is there to allow the user
        to input information before proceeding to the simulation of this space.
        - self.ar_grid_dimensions: the tuple of ints keeping track of the dimension of the grid
        to be drawn on the user's screen.
        - self.start_pos: the tuple of floats representing the starting position of the user on
        the grid representing the vertices of the graph.
        - self.end_pos: the tuple of floats representing the end position of the user on
        the grid representing the vertices of the graph.

    Representation Invariants:
        - self.ar_grid_dimensions[0] == 8
        - self.ar_grid_dimensions[1] == 10
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: WeightedGraph
    ar_grid_dimensions: tuple[int, int]
    start_pos: Optional[tuple[float, float]]
    end_pos: Optional[tuple[float, float]]

    def __init__(self, program: pygame.display) -> None:
        """ Initialize an AirProgramMenu object and its attributes along with the given
        program, displaying all the contents of this menu according to the display_menu
        method loop.
        """
        Menu.__init__(self, program)
        # the default weighted graph we start this program with
        self.graph = world_cities_graph(AR_DIM[0], AR_DIM[1])
        self.ar_grid_dimensions = AR_DIM

        self.start_pos = None
        self.end_pos = None

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the AirProgramMenu screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background color

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 40])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 40])
            self.program.draw_title_text(20, "Air Routes Program Menu", (135, 20), 'white')

            instructions1 = "1) Click on cells to modify this graph, press ENTER to run program"
            instructions2 = "2) Left click: block vertex; Right click: start vertex," \
                            " Middle click: end vertex"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 55))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 80))

            self.program.draw_air_grid(self.ar_grid_dimensions, self.graph)

            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the AirProgramMenu window, these
        inputs consist of mouse clicks allowing the user to mutate the weighted graph and
        customize the space to be traversed in the next window, and keyboard inputs
        executing commands to go to the previous window or proceed to the next one.
        """
        if self.program.back_key:
            # reset graph
            self.graph = world_cities_graph(AR_DIM[0], AR_DIM[1])
            self.start_pos = None
            self.end_pos = None

            self.program.curr_menu = self.program.main_menu
            self.run_display = False

        # handle mouse input

        if self.program.left_click[0]:
            pos = self.program.left_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.ar_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.ar_grid_dimensions[1])))
            pixel_pos = get_air_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.ar_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.ar_grid_dimensions[0] * self.ar_grid_dimensions[1]

            if valid_cell(self.ar_grid_dimensions, in_grid_cell_num, coord_number, number_of_cells):
                # change vertex state to 'blocked'
                self.graph.vertices[pixel_pos].state = 'blocked'

        elif self.program.right_click[0]:
            pos = self.program.right_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.ar_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.ar_grid_dimensions[1])))
            pixel_pos = get_air_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.ar_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.ar_grid_dimensions[0] * self.ar_grid_dimensions[1]

            if valid_cell(self.ar_grid_dimensions, in_grid_cell_num, coord_number,
                          number_of_cells) and self.start_pos is None:
                # change vertex state to 'start'
                self.graph.vertices[pixel_pos].state = 'start'
                self.start_pos = self.graph.vertices[pixel_pos].pos

        elif self.program.mid_click[0]:
            pos = self.program.mid_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.ar_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.ar_grid_dimensions[1])))
            pixel_pos = get_air_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.ar_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.ar_grid_dimensions[0] * self.ar_grid_dimensions[1]
            # see how coord_number works
            if valid_cell(self.ar_grid_dimensions, in_grid_cell_num, coord_number,
                          number_of_cells) and self.end_pos is None:
                # change vertex state to 'end'
                self.graph.vertices[pixel_pos].state = 'end'
                self.end_pos = self.graph.vertices[pixel_pos].pos

        # ENTER starts simulation for user
        elif self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                # set up the AirProgramRun class with the necessary updated attributes
                self.program.air_routes_program_run = AirProgramRun(self.program, self.graph)
                self.program.air_routes_program_run.start_pos = self.start_pos
                self.program.air_routes_program_run.end_pos = self.end_pos
                self.program.curr_menu = self.program.air_routes_program_run

                self.run_display = False


class AirProgramRun(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the air routes program's simulation of this program.

    Instance Attributes:
        - self.graph: the weighted graph object representing a space to be traversed
        in this window (world air routes of an airline).
        - self.start_pos: the tuple of ints representing the starting position of the user on
        the representing the graph.
        - self.end_pos: the tuple of ints representing the end position of the user on
        the grid representing the graph.
        - self.message_coords: tuple of ints representing the position of the text used to give
        information to the user about the path computed based on their input.
         - self.show_message1: bool keeping track of whether or not the user has tried to make
        and invalid shortest path computation (unable to go from self.start_pos to
        self.end_pos), triggering the showing of an alert notifying user of the invalid input.
        - self.show_message2: bool keeping track of whether or not the user has made a
        valid shortest path computation, triggering the showing of an str describing the
        cities the user will have to traverse to go from self.start_pos to self.end_pos.
        - self.show_path: bool keeping track of whether or not the user has performed the
        action (pressing ENTER key) to trigger the displaying of the path calculated using
        Dijkstra's algorithm from self.start_pos to self.end_pos.
        - self.show_distance: bool keeping track of whether or not the user has made a
        valid shortest path computation, triggering the showing of an str describing the
        total distance the user will have to travel to go from self.start_pos to
        self.end_pos. Distance is a key of this part of the program as it is the weight that
        is being given to edges when calculating the best path.
        - self.distance: float representing the total distance to be traveled to go from the
        user's self.start_pos to self.end_pos.
        - self.cities: str representing the cities to be traversed to go from the
        user's self.start_pos to self.end_pos.

    Representation Invariants:
        - 0 <= self.message_coords[0] <= 800 and 0 <= self.message_coords[1] <= 810
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: WeightedGraph
    start_pos: Optional[tuple[int, int]]
    end_pos: Optional[tuple[int, int]]
    message_coords: tuple[int, int]
    show_message1: bool
    show_message2: bool
    show_path: bool
    show_distance: bool
    distance: float
    cities: str

    def __init__(self, program: pygame.display, graph: WeightedGraph) -> None:
        """ Initialize a AirProgramRun object and its attributes along with the given
        program, displaying all the contents of this simulation menu according to the
        display_menu method loop.
        """
        Menu.__init__(self, program)

        self.graph = graph

        self.start_pos = None
        self.end_pos = None

        self.message_coords = (self.mid_coords[0], 600)
        self.show_message1 = False
        self.show_message2 = False
        self.show_path = False
        self.show_distance = False

        self.distance = 0.00  # default to 0, no points chosen as start or finish
        self.cities = ''  # string represented traversed countries default to an empty str

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the AirProgramRun screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 60])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 60])
            self.program.draw_title_text(20, "Air Routes Run", (90, 30), 'white')

            instructions = "Press Enter to run program and draw the path connecting start and end" \
                           " (using DIJKSTRA'S)"
            self.program.draw_title_text(16, instructions, (self.mid_coords[0], 80))

            self.program.display.blit(pygame.image.load('media/BG_world_map.png'), (0, 100))
            self.program.draw_air_graph(self.graph)

            if self.show_path is True:
                self.draw_path()

            if self.show_message1 is True:
                ttd = 'NO VALID PATH'
                self.program.draw_title_text(14, ttd, (650, 30), 'red')
            if self.show_distance is True:
                ttd1 = 'The minimum distance that can be travelled to get from your start position'
                ttd2 = 'to your end position is ' + str(self.distance) + ' Km'
                self.program.draw_title_text(18, ttd1, (self.message_coords[0],
                                                        self.message_coords[1]))
                self.program.draw_title_text(18, ttd2, (self.message_coords[0],
                                                        self.message_coords[1] + 25))
            if self.show_message2 is True:
                ttd1 = 'The cities you will traverse through this path are: '
                ttd2 = self.cities

                self.program.draw_title_text(18, ttd1, (self.message_coords[0],
                                                        self.message_coords[1] + 90))

                if len(ttd2) > 70:  # str too long for a single line
                    ttd2_1 = ttd2[:70]
                    ttd2_2 = ttd2[70:]
                    self.program.draw_title_text(18, ttd2_1 + ' -', (self.message_coords[0],
                                                                     self.message_coords[1] + 115))
                    self.program.draw_title_text(18, ttd2_2, (self.message_coords[0],
                                                              self.message_coords[1] + 140))
                else:  # str fits in one line
                    self.program.draw_title_text(18, ttd2, (self.message_coords[0],
                                                            self.message_coords[1] + 115))
            # update screen
            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the AirProgramRun window, these
        inputs consist keyboard key presses independent from arrow keys, executing commands
        to go to the previous window or to make the call to the function that calculates
        and displays the shortest path between the user's selected self.start_pos and
        self.end_pos positions.
        """
        if self.program.back_key:
            # reset the graph the user just used
            self.program.air_routes_program_menu.graph = world_cities_graph(8, 10)
            self.program.air_routes_program_menu.start_pos = None
            self.program.air_routes_program_menu.end_pos = None

            # go to previous
            self.program.curr_menu = self.program.air_routes_program_menu
            self.run_display = False

        if self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                self.show_path = True

    def draw_path(self) -> None:
        """ Method in charge of making the call to Dijkstra's algorithm which calculates
        the path to be followed by the user, and displaying this path on the
        AirProgramRun screen by mutating the user's graph.
        """
        if self.graph.connected(self.start_pos, self.end_pos):
            path_to_follow = self.graph.dijkstra_search(self.start_pos, self.end_pos)
            for i in range(0, len(path_to_follow[self.end_pos][1]) - 1):
                # highlight edges
                local_start = path_to_follow[self.end_pos][1][i]
                local_end = path_to_follow[self.end_pos][1][i + 1]
                pygame.draw.line(self.program.display, 'cyan', local_start, local_end, 2)

            for vertex_pos in path_to_follow[self.end_pos][1][1:-1]:
                # highlight vertices in path (not the ends)
                self.graph.vertices[vertex_pos].state = 'path'

            self.show_distance = True
            self.distance = round(path_to_follow[self.end_pos][0], 2)
            self.show_message2 = True
            self.cities = self.cities_traversed(path_to_follow, self.end_pos)
        else:  # the two selected vertices are not connected (distance between them is inf)
            self.show_message1 = True

    def cities_traversed(self, path: dict[tuple[float, float], list],
                         destination_coord: tuple[int, int]) -> str:
        """ Method in charge of returning a string containing of all the countries
        traversed throughout the path calculated and displayed to the user, based on
        the pixel positions resulting from the Dijkstra's algorithm function.
        """
        traversed_coords_lst = path[destination_coord][1]

        countries_so_far = ''
        for i in range(0, len(traversed_coords_lst)):
            if i < len(traversed_coords_lst) - 1:
                countries_so_far += str(self.graph.vertices[traversed_coords_lst[i]].name) + ', '
            else:  # i == len(traversed_coords_lst)
                # concatenate second last country with a comma and last one without one
                countries_so_far += str(self.graph.vertices[traversed_coords_lst[i]].name)

        return countries_so_far + '.'


class AirCostProgramMenu(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the air cost program's menu of this program (accessed by selecting the Air Routes
    Program option on the main menu).

    Instance Attributes:
        - self.graph: the weighted graph object representing a space to be traversed
        in the next window. At this stage, in this menu, the graph is there to allow the user
        to input information before proceeding to the simulation of this space.
        - self.arc_grid_dimensions: the tuple of ints keeping track of the dimension of the grid
        to be drawn on the user's screen.
        - self.start_pos: the tuple of floats representing the starting position of the user on
        the grid representing the vertices of the graph.
        - self.end_pos: the tuple of floats representing the end position of the user on
        the grid representing the vertices of the graph.

    Representation Invariants:
        - self.arc_grid_dimensions[0] == 4
        - self.arc_grid_dimensions[1] == 5
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: WeightedGraph
    arc_grid_dimensions: tuple[int, int]
    start_pos: Optional[tuple[float, float]]
    end_pos: Optional[tuple[float, float]]

    def __init__(self, program: pygame.display) -> None:
        """ Initialize an AirCostProgramMenu object and its attributes along with the given
        program, displaying all the contents of this menu according to the display_menu
        method loop.
        """
        Menu.__init__(self, program)
        # the default weighted graph we start this program with
        self.graph = world_countries_graph(ARC_DIM[0], AR_DIM[1])
        self.arc_grid_dimensions = ARC_DIM

        self.start_pos = None
        self.end_pos = None

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the AirCostProgramMenu screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])  # fill background color

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 40])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 40])
            self.program.draw_title_text(20, "Air Cost Program Menu", (130, 20), 'white')

            instructions1 = "1) Click on cells to modify this graph, press ENTER to run program"
            instructions2 = "2) Left click: block vertex; Right click: start vertex," \
                            " Middle click: end vertex"
            self.program.draw_title_text(16, instructions1, (self.mid_coords[0], 55))
            self.program.draw_title_text(16, instructions2, (self.mid_coords[0], 80))

            self.program.draw_air_grid(self.arc_grid_dimensions, self.graph)

            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the AirCostProgramMenu window, these
        inputs consist of mouse clicks allowing the user to mutate the weighted graph and
        customize the space to be traversed in the next window, and keyboard inputs
        executing commands to go to the previous window or proceed to the next one.
        """
        if self.program.back_key:
            # reset graph
            self.graph = world_countries_graph(ARC_DIM[0], ARC_DIM[1])
            self.start_pos = None
            self.end_pos = None

            self.program.curr_menu = self.program.main_menu
            self.run_display = False

        # handle mouse input

        if self.program.left_click[0]:
            pos = self.program.left_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.arc_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.arc_grid_dimensions[1])))
            pixel_pos = get_air_cost_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.arc_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.arc_grid_dimensions[0] * self.arc_grid_dimensions[1]

            if valid_cell(self.arc_grid_dimensions, in_grid_cell_num, coord_number,
                          number_of_cells):
                # change vertex state to 'blocked'
                self.graph.vertices[pixel_pos].state = 'blocked'

        elif self.program.right_click[0]:
            pos = self.program.right_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.arc_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.arc_grid_dimensions[1])))
            pixel_pos = get_air_cost_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.arc_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.arc_grid_dimensions[0] * self.arc_grid_dimensions[1]

            if valid_cell(self.arc_grid_dimensions, in_grid_cell_num, coord_number,
                          number_of_cells) and self.start_pos is None:
                # change vertex state to 'start'
                self.graph.vertices[pixel_pos].state = 'start'
                self.start_pos = self.graph.vertices[pixel_pos].pos

        elif self.program.mid_click[0]:
            pos = self.program.mid_click[1]
            in_grid_cell_num = ((pos[0] - 50) // (700 // self.arc_grid_dimensions[0]),
                                ((pos[1] - 100) // (700 // self.arc_grid_dimensions[1])))
            pixel_pos = get_air_cost_file_pos(in_grid_cell_num[0], in_grid_cell_num[1])
            coord_number = find_coord(self.arc_grid_dimensions, in_grid_cell_num)
            number_of_cells = self.arc_grid_dimensions[0] * self.arc_grid_dimensions[1]
            # see how coord_number works
            if valid_cell(self.arc_grid_dimensions, in_grid_cell_num, coord_number,
                          number_of_cells) and self.end_pos is None:
                # change vertex state to 'end'
                self.graph.vertices[pixel_pos].state = 'end'
                self.end_pos = self.graph.vertices[pixel_pos].pos

        # ENTER starts simulation for user
        elif self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                # set up the AirCostRun class with the necessary updated attributes
                self.program.air_cost_program_run = AirCostProgramRun(self.program, self.graph)
                self.program.air_cost_program_run.start_pos = self.start_pos
                self.program.air_cost_program_run.end_pos = self.end_pos
                self.program.curr_menu = self.program.air_cost_program_run

                self.run_display = False


class AirCostProgramRun(Menu):
    """ The class controlling the interactions and overall connection between the user
    and the air cost program's simulation of this program.

    Instance Attributes:
        - self.graph: the weighted graph object representing a space to be traversed
        in this window (world air routes of an airline).
        - self.start_pos: the tuple of ints representing the starting position of the user on
        the grid representing the graph.
        - self.end_pos: the tuple of ints representing the end position of the user on
        the grid representing the graph.
        - self.message_coords: tuple of ints representing the position of the text used to give
        information to the user about the path computed based on their input.
         - self.show_message1: bool keeping track of whether or not the user has tried to make
        and invalid shortest path computation (unable to go from self.start_pos to
        self.end_pos), triggering the showing of an alert notifying user of the invalid input.
        - self.show_message2: bool keeping track of whether or not the user has made a
        valid shortest path computation, triggering the showing of an str describing the
        cities the user will have to traverse to go from self.start_pos to self.end_pos.
        - self.show_path: bool keeping track of whether or not the user has performed the
        action (pressing ENTER key) to trigger the displaying of the path calculated using
        Dijkstra's algorithm from self.start_pos to self.end_pos.
        - self.show_cost: bool keeping track of whether or not the user has made a
        valid shortest path computation, triggering the showing of an str describing the
        total cost the user would have to pay to go from self.start_pos to
        self.end_pos. Cost is a key of this part of the program as it is the weight that
        is being given to edges when calculating the best path.
        - self.cost: float representing the total cost to be paid to go from the
        user's self.start_pos to self.end_pos.
        - self.countries: str representing the cities to be traversed to go from the
        user's self.start_pos to self.end_pos.

    Representation Invariants:
        - 0 <= self.message_coords[0] <= 800 and 0 <= self.message_coords[1] <= 810
        - self.cost >= 0
    """
    # All attributes imported from the Menu parent class are inherited by this class
    # with no change in purpose, refer to Menu class docstring to understand those basic
    # Menu class attributes.
    graph: WeightedGraph
    start_pos: Optional[tuple[int, int]]
    end_pos: Optional[tuple[int, int]]
    message_coords: tuple[int, int]
    show_message1: bool
    show_message2: bool
    show_path: bool
    show_cost: bool
    cost: float
    countries: str

    def __init__(self, program: pygame.display, graph: WeightedGraph) -> None:
        """ Initialize a AirCostProgramRun object and its attributes along with the given
        program, displaying all the contents of this simulation menu according to the
        display_menu method loop.
        """
        Menu.__init__(self, program)

        self.graph = graph

        self.start_pos = None
        self.end_pos = None

        self.message_coords = (self.mid_coords[0], 600)
        self.show_message1 = False
        self.show_message2 = False
        self.show_path = False
        self.show_cost = False

        self.cost = 0.00  # default to 0, no points chosen as start or finish
        self.countries = ''  # string represented traversed countries default to an empty str

    def display_menu(self) -> None:
        """ Function controlling the main loop in charge of displaying and updating
        the AirCostProgramRun screen being shown to the user.
        """
        self.run_display = True
        while self.run_display:
            self.program.catch_events_menu()  # detect events
            self.check_input()  # receive user input
            self.program.display.fill(THECOLORS['lightgrey'])

            # draw text and widgets
            pygame.draw.rect(self.program.display, THECOLORS['gray11'], [0, 0, 800, 60])
            pygame.draw.rect(self.program.display, THECOLORS['cyan'], [740, 0, 60, 60])
            self.program.draw_title_text(20, "Air Cost Run", (100, 30), 'white')

            instructions = "Press Enter to run program and draw the path connecting start and end" \
                           " (using DIJKSTRA'S)"
            self.program.draw_title_text(16, instructions, (self.mid_coords[0], 80))

            self.program.display.blit(pygame.image.load('media/BG_world_map.png'), (0, 100))
            self.program.draw_air_graph(self.graph)

            if self.show_path is True:
                self.draw_path()

            if self.show_message1 is True:
                ttd = 'NO VALID PATH'
                self.program.draw_title_text(14, ttd, (650, 30), 'red')
            if self.show_cost is True:
                ttd1 = 'The minimum cost that can be paid to get from your start position'
                ttd2 = 'to your end position is ' + str(self.cost) + ' $(cad)'
                self.program.draw_title_text(18, ttd1, (self.message_coords[0],
                                                        self.message_coords[1]))
                self.program.draw_title_text(18, ttd2, (self.message_coords[0],
                                                        self.message_coords[1] + 25))
            if self.show_message2 is True:
                ttd1 = 'The cities you will traverse through this path are: '
                ttd2 = self.countries

                self.program.draw_title_text(18, ttd1, (self.message_coords[0],
                                                        self.message_coords[1] + 90))

                if len(ttd2) > 70:  # str too long for a single line
                    ttd2_1 = ttd2[:70]
                    ttd2_2 = ttd2[70:]
                    self.program.draw_title_text(18, ttd2_1 + ' -', (self.message_coords[0],
                                                                     self.message_coords[1] + 115))
                    self.program.draw_title_text(18, ttd2_2, (self.message_coords[0],
                                                              self.message_coords[1] + 140))
                else:  # str fits in one line
                    self.program.draw_title_text(18, ttd2, (self.message_coords[0],
                                                            self.message_coords[1] + 115))
            # update screen
            self.blit_screen()

    def check_input(self) -> None:
        """ Method in charge of recognizing user input and executing the necessary
        actions according to them. In this case, for the AirCostProgramRun window, these
        inputs consist keyboard key presses independent from arrow keys, executing commands
        to go to the previous window or to make the call to the function that calculates
        and displays the shortest path between the user's selected self.start_pos and
        self.end_pos positions.
        """
        if self.program.back_key:
            # reset the graph the user just used
            self.program.air_cost_program_menu.graph = world_countries_graph(ARC_DIM[0], ARC_DIM[1])
            self.program.air_cost_program_menu.start_pos = None
            self.program.air_cost_program_menu.end_pos = None

            # go to previous
            self.program.curr_menu = self.program.air_cost_program_menu
            self.run_display = False

        if self.program.enter_key:
            if self.start_pos is not None and self.end_pos is not None:
                self.show_path = True

    def draw_path(self) -> None:
        """ Method in charge of making the call to Dijkstra's algorithm which calculates
        the path to be followed by the user, and displaying this path on the
        AirCostProgramRun screen by mutating the user's graph.
        """
        if self.graph.connected(self.start_pos, self.end_pos):
            path_to_follow = self.graph.dijkstra_search(self.start_pos, self.end_pos)
            for i in range(0, len(path_to_follow[self.end_pos][1]) - 1):
                # highlight edges
                local_start = path_to_follow[self.end_pos][1][i]
                local_end = path_to_follow[self.end_pos][1][i + 1]
                pygame.draw.line(self.program.display, 'cyan', local_start, local_end, 2)

            for vertex_pos in path_to_follow[self.end_pos][1][1:-1]:
                # highlight vertices in path (not the ends)
                self.graph.vertices[vertex_pos].state = 'path'

            self.show_cost = True
            self.cost = round(path_to_follow[self.end_pos][0], 2)
            self.show_message2 = True
            self.countries = self.countries_traversed(path_to_follow, self.end_pos)
        else:  # the two selected vertices are not connected (distance between them is inf)
            self.show_message1 = True

    def countries_traversed(self, path: dict[tuple[float, float], list],
                            destination_coord: tuple[int, int]) -> str:
        """ Method in charge of returning a string containing of all the countries
        traversed throughout the path calculated and displayed to the user, based on
        the pixel positions resulting from the Dijkstra's algorithm function.
        """
        traversed_coords_lst = path[destination_coord][1]

        countries_so_far = ''
        for i in range(0, len(traversed_coords_lst)):
            if i < len(traversed_coords_lst) - 1:
                countries_so_far += str(self.graph.vertices[traversed_coords_lst[i]].name) + ', '
            else:  # i == len(traversed_coords_lst)
                # concatenate second last country with a comma and last one without one
                countries_so_far += str(self.graph.vertices[traversed_coords_lst[i]].name)

        return countries_so_far + '.'


####################
# Helper Functions #
####################


def get_maze_details(maze: Optional[str]) -> tuple[str, tuple[int, int]]:
    """ Helper function for the MazeProgramMenu class, extracting information about the
    dimensions of the chosen maze (input) according to the constants, that is to be
    turned into a graph.

    Preconditions:
        - maze in {'map1', 'map2', 'map3', 'map4'} or maze is None

    """
    if maze == 'map4':
        return MAZE4
    elif maze == 'map3':
        return MAZE3
    elif maze == 'map2':
        return MAZE2
    else:  # maze == 'map1'
        # this is the default case even if the input is None
        return MAZE1


def find_coord(dimensions: tuple[int, int], cell: tuple[int, int]) -> int:
    """ Helper to mouse position detection methods returning the position number
     of a vertex (cell) in a graph based on the cell pressed on the pygame window.

    Preconditions:
        - 5 <= dimensions[0] <= 20 and 5 <= dimensions[1] <= 20
        - cell[0] >= 0 and cell[1] >= 0
        """
    coord_num = 1 + (cell[1] * dimensions[0])
    return int(coord_num)


def valid_cell(dimensions: tuple[int, int], cell_number: tuple[int, int], coord_number: int,
               num_of_cells: int) -> bool:
    """ Helper to mouse position detection methods determining whether the position where
    the user is clicking is a valid cell on the graph.

    Preconditions:
        - 5 <= dimensions[0] <= 20 and 5 <= dimensions[1] <= 20
    """

    x_bounded = 0 <= cell_number[0] < dimensions[0]
    y_bounded = 0 <= cell_number[1] < dimensions[1]

    if num_of_cells >= coord_number:
        return x_bounded and y_bounded
    else:
        return False


def get_air_file_pos(grid_column: int, grid_row: int) -> tuple[float, float]:
    """ Helper fetching the pixel pos (tuple of two floats) of a vertex from
    the 'datasets/cities.csv' file based on the row number on the csv file which is
    determined using the menu_pos attribute of the vertex of interest.

    Preconditions:
        - 0 <= grid_column <= 7
        - 0 <= grid_row <= 9

    # position of Panama on the pygame window
    >>> get_air_file_pos(5, 1)
    (203.0, 391.0)
    >>> get_air_file_pos(5, 6)
    (538.0, 344.0)
    """
    row_num = (grid_row * 8) + grid_column + 1

    with open('datasets/cities.csv') as csv_file:
        reader = csv.reader(csv_file)

        i = 1
        for row in reader:
            if i == row_num:
                return (float(row[1]), float(row[2]))
            else:
                i += 1

    raise ValueError  # as long as preconditions are followed, this error is not raised


def get_air_cost_file_pos(grid_column: int, grid_row: int) -> tuple[float, float]:
    """ Helper fetching the pixel pos (tuple of two floats) of a vertex from
    the 'datasets/cities.csv' file based on the row number on the csv file which is
    determined using the menu_pos attribute of the vertex of interest.

    Preconditions:
        - 0 <= grid_column <= 3
        - 0 <= grid_row <= 4

    # position of Panama on the pygame window
    >>> get_air_cost_file_pos(1, 4)
    (511.0, 348.0)
    >>> get_air_cost_file_pos(2, 3)
    (648.0, 498.0)
    """
    row_num = (grid_row * 4) + grid_column + 1

    with open('datasets/countries.csv') as csv_file:
        reader = csv.reader(csv_file)

        i = 1
        for row in reader:
            if i == row_num:
                return (float(row[1]), float(row[2]))
            else:
                i += 1

    raise ValueError  # as long as preconditions are followed, this error is not raised


# Some errors raised were counter-intuitive which is why we have removed them
if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913', 'R0912', 'R0902', 'E9959', 'E9972'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })
