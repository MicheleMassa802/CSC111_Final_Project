"""CSC111 Winter 2021 Course Project: Main Manager

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the Program class which is in charge of monitoring
the activity in the different pygame menus that we have created, and a couple helper
functions that have more broad purposes. The Program class contains all methods that
are related to the user's interaction with the pygame window

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox.
"""


###########
# IMPORTS #
###########
from typing import Optional

import pygame
from pygame.colordict import THECOLORS
import menu
from algorithm_classes import Graph
from algorithm_classes_v2 import WeightedGraph, world_cities_graph
from api import world_countries_graph

#############
# CONSTANTS #
#############

WIDTH = 35
HEIGHT = 35
WINDOW_SIZE = (800, 810)  # window size is strict
MAX_GRID = (20, 20)
GFS = 8

# Air route data:
AR_DIM = (8, 10)
ARC_DIM = (4, 5)


#################
# Program Class #
#################


class Program:
    """ The class establishing the main connection between the user and the various
    accessible menus within the pygame window.

    Instance Attributes:
        - self.running: bool controlling the state of the pygame window (active or closed).
        - self.in_window: bool controlling the state of the running of the program_menu_loop.
        - self.display_dimensions: the pixel size of the pygame window.
        - self.window: pygame.display where text and other widgets are displayed.
        - self.display: pygame.Surface showing and updating the pygame window and its contents.
        - self.font_name: keeps track of the font used when displaying text.
        - self.main_menu: subclass to class Menu in charge of controlling the main menu.
        - self.simple_program_menu: subclass to class Menu in charge of controlling the
        simple program menu.
        - self.simple_program_run: subclass to class Menu in charge of controlling the
        running of the simple implementation of this program.
        - self.maze_program_menu: subclass to class Menu in charge of controlling the
        maze program menu.
        - self.maze_program_run: subclass to class Menu in charge of controlling the
        running of the maze implementation of this program.
        - self.air_routes_program_menu: subclass to class Menu in charge of controlling the
        air routes program menu.
        - self.air_routes_maze_program_run: subclass to class Menu in charge of controlling the
        running of the air routes implementation of this program.
        - self.air_cost_program_menu: subclass to class Menu in charge of controlling the
        air cost program menu.
        - self.air_cost_maze_program_run: subclass to class Menu in charge of controlling the
        running of the air cost implementation of this program.
        - self.curr_menu: keeps track of the menu the user finds themselves in.
        - self.up_key: keeps track of the interactions with the Up key.
        - self.down_key: keeps track of the interactions with the Down key.
        - self.left_key: keeps track of the interactions with the Left key.
        - self.right_key: keeps track of the interactions with the Right key.
        - self.enter_key: keeps track of the interactions with the Enter key.
        - self.back_key: keeps track of the interactions with the BackSpace key.
        - self.left_key: keeps track of the interactions with the Left Click and
        its pixel position.
        - self.right_key: keeps track of the interactions with the Right Click and
        its pixel position.
        - self.mid_click: keeps track of the interactions with the Middle Click and
        its pixel position.

    Representation Invariants:
        - self.display dimensions == (800, 810)
    """

    running: bool
    in_window: bool
    display_dimensions: tuple[int, int]
    window: pygame.display
    display: pygame.Surface
    font_name: str

    # menus
    main_menu = menu.MainMenu
    simple_program_menu: menu.SpMenu
    simple_program_run: menu.SimpleProgramRun
    maze_program_menu: menu.MazeProgramMenu
    maze_program_run: menu.MazeProgramRun
    air_routes_program_menu: menu.AirProgramMenu
    air_routes_program_run: menu.AirProgramRun
    air_cost_program_menu: menu.AirCostProgramMenu
    air_cost_program_run: menu.AirCostProgramRun

    curr_menu = menu.MainMenu

    # keys and clicks
    up_key: bool
    down_key: bool
    left_key: bool
    right_key: bool
    enter_key: bool
    back_key: bool
    left_click: tuple[bool, Optional[tuple[int, int]]]
    right_click: tuple[bool, Optional[tuple[int, int]]]
    mid_click: tuple[bool, Optional[tuple[int, int]]]

    def __init__(self) -> None:
        """ Initialize the pygame window and control the state of all of its contents
        according to user input.
        """
        pygame.init()
        pygame.display.set_caption("Efficient Space Traversal")
        pygame.display.set_icon(pygame.image.load('media/EST_Logo.png'))

        self.running = True
        self.in_window = False

        self.display_dimensions = WINDOW_SIZE

        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.display = pygame.Surface(WINDOW_SIZE)

        self.font_name = 'comicsansms'

        # key events

        self.up_key, self.down_key, self.left_key, self.right_key = False, False, False, False
        self.enter_key, self.back_key = False, False
        self.left_click, self.right_click, self.mid_click = \
            (False, None), (False, None), (False, None)

        # different windows

        self.main_menu = menu.MainMenu(self)
        self.simple_program_menu = menu.SpMenu(self)
        # this is the default load which is overwritten when user enters the simple program run menu
        self.simple_program_run = menu.SimpleProgramRun(self, (5, 5))
        self.maze_program_menu = menu.MazeProgramMenu(self)
        # this is the default load which is overwritten when user enters the maze program run menu
        self.maze_program_run = menu.MazeProgramRun(self, 'datasets/default_maze.csv', (5, 5))
        self.air_routes_program_menu = menu.AirProgramMenu(self)
        # this is the default load which is overwritten when user enters the air program run menu
        self.air_routes_program_run = menu.AirProgramRun(self, world_cities_graph(AR_DIM[0],
                                                                                  AR_DIM[1]))
        self.air_cost_program_menu = menu.AirCostProgramMenu(self)
        # this is the default load which is overwritten when user enters the air program run menu
        self.air_cost_program_run = menu.AirCostProgramRun(self, world_countries_graph(ARC_DIM[0],
                                                                                       ARC_DIM[1]))

        self.curr_menu = self.main_menu

    def program_menu_loop(self) -> None:
        """ The loop keeping the various program menus running through the attribute curr_menu
        until event.QUIT is executed.
        """
        while self.in_window:
            self.catch_events_menu()  # receive user input
            self.window.blit(self.display, (0, 0))  # align menu display with window
            pygame.display.update()

    def catch_events_menu(self) -> None:
        """ Method in charge of interpreting the user input events in any of the pygame
        menus (this includes arrow keys, mouse input, and more).
        """
        for event in pygame.event.get():  # detect an input

            # Quitting game
            if event.type == pygame.QUIT:
                self.running, self.in_window = False, False
                self.curr_menu.run_display = False

            # Traversing menu through keyboard input

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.left_key = True  # register changes
                elif event.key == pygame.K_RIGHT:
                    self.right_key = True  # register changes
                elif event.key == pygame.K_UP:
                    self.up_key = True  # register changes
                elif event.key == pygame.K_DOWN:
                    self.down_key = True  # register changes
                elif event.key == pygame.K_RETURN:
                    self.enter_key = True  # register changes
                elif event.key == pygame.K_BACKSPACE:
                    self.back_key = True  # register changes

            # Releasing key actions related to keyboard input

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_key = False  # register changes
                elif event.key == pygame.K_RIGHT:
                    self.right_key = False  # register changes
                elif event.key == pygame.K_UP:
                    self.up_key = False  # register changes
                elif event.key == pygame.K_DOWN:
                    self.down_key = False  # register changes
                elif event.key == pygame.K_RETURN:
                    self.enter_key = False  # register changes
                elif event.key == pygame.K_BACKSPACE:
                    self.back_key = False  # register changes

            # Input through mouse

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    self.left_click = (True, pos)  # register changes
                elif event.button == 3:
                    self.right_click = (True, pos)  # register changes
                elif event.button == 2:
                    self.mid_click = (True, pos)  # register changes

            # Releasing click actions related to mouse input

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    self.left_click = (False, pos)  # register changes
                elif event.button == 3:
                    self.right_click = (False, pos)  # register changes
                elif event.button == 2:
                    self.mid_click = (False, pos)  # register changes

    def reset_keys(self) -> None:
        """ Method in charge of setting all the keyboard keys to their original False state
        after being pressed once, to avoid multiple inputs with one click.
        """
        self.up_key, self.down_key, self.left_key, self.right_key = False, False, False, False
        self.enter_key, self.back_key = False, False

    def draw_title_text(self, t_size: int, ttd: str, pos: tuple[int, int],
                        colour: str = 'black') -> None:
        """ Method in charge of drawing the input text on the pygame screen at the
        input position, according to the other input characteristics.

        - ttd: the text to be displayed

        Preconditions:
            - len(ttd) <= 60
        """
        font = pygame.font.SysFont(self.font_name, t_size)
        text_surface = font.render(ttd, True, THECOLORS[colour])
        text_rect = text_surface.get_rect()
        text_rect.center = (pos[0], pos[1])
        self.display.blit(text_surface, text_rect)

    ##################################################################
    # methods specific to open sandbox implementation SIMPLE PROGRAM #
    ##################################################################

    def draw_grid(self, grid_dim: tuple[int, int], graph: Graph, show_text: bool = False) -> None:
        """ The method in charge of drawing an empty grid of squares to represent
        the a standard graph based on the coordinates of the vertices and the overall
        size of the grid.

        Preconditions:
            - 5 <= grid_dim[0] <= 20
            - 5 <= grid_dim[1] <= 20
        """
        local_width = int((WINDOW_SIZE[0] - 100) / grid_dim[0])
        local_height = int((WINDOW_SIZE[1] - 110) / grid_dim[1])

        for vertex in graph.get_vertices():
            ttd = str(vertex.pos)
            grid_coords = (int((vertex.pos[0] * local_width) + 50),
                           int((vertex.pos[1] * local_height) + 100))
            colour = get_state_colour(vertex.state)

            self.draw_cell(ttd, grid_coords, colour, grid_dim, 3, show_text)

    ################################################################
    # methods specific to open sandbox implementation MAZE PROGRAM #
    ################################################################

    def draw_invis_grid(self, grid_dim: tuple[int, int], graph: Graph) -> None:
        """ The method in charge of drawing a empty grid of somewhat transparent squares to
        specifically represent the graph for the MAP4 option in the maze menu.

        Preconditions:
            - grid_dim[0] == 18
            - grid_dim[1] == 14
        """
        local_width = int((WINDOW_SIZE[0] - 100) / grid_dim[0])
        local_height = int((WINDOW_SIZE[1] - 110) / grid_dim[1])

        for vertex in graph.get_vertices():
            grid_coords = (int((vertex.pos[0] * local_width) + 50),
                           int((vertex.pos[1] * local_height) + 100))
            colour = get_state_colour(vertex.state)

            self.draw_invis_cell(grid_coords, colour, grid_dim)

    def draw_invis_cell(self, pos: tuple[int, int], colour: str,
                        grid_dim: tuple[int, int]) -> None:
        """ Draw a somewhat transparent cell on the correct window at the given position with the
        given colour. Each cell represents a vertex in the graph.

        Preconditions:
            - 0 <= pos[0] <= 800
            - 0 <= pos[1] <= 810
        """
        local_width = int((WINDOW_SIZE[0] - 100) / grid_dim[0])
        local_height = int((WINDOW_SIZE[1] - 100) / grid_dim[1])

        # draw rectangle where node is contained
        rect = pygame.Surface((local_width - 3, local_height - 3))
        # - 3 difference is specific to this graph, spacing the cells of the grid

        rect.set_alpha(55)  # changes opacity
        rect.fill(colour)

        self.display.blit(rect, pos)

    #################################################################
    # methods specific to strict implementations AIR ROUTES PROGRAM #
    #################################################################

    def draw_air_grid(self, grid_dim: tuple[int, int], graph: WeightedGraph,
                      show_text: bool = True) -> None:
        """ The method in charge of drawing the grid displayed in the menu that sets up
        the air routes graph. This is very similar to the other grids the user will see.

        Preconditions:
            - grid_dim[0] == 8 or grid_dim[0] == 4
            - grid_dim[1] == 10 or grid_dim[1] == 5
        """
        local_width = int((800 - 100) / grid_dim[0])
        local_height = int((810 - 110) / grid_dim[1])
        for vertex in graph.get_vertices():
            if len(str(vertex.name)) > 8:
                ttd = str(vertex.name)[0: 8] + '.'
            else:  # vertex name fits in box size for the standard 8 by 10 grid (and 4 by 5)
                ttd = str(vertex.name)

            # can no longer use vertex.pos since vertex positions represent pixel position now
            grid_coords = (int((vertex.menu_pos[0] * local_width) + 50),
                           int((vertex.menu_pos[1] * local_height) + 100))
            colour = get_state_colour(vertex.state)
            self.draw_cell(ttd, grid_coords, colour, grid_dim, 5, show_text)

    def draw_air_graph(self, graph: WeightedGraph) -> None:
        """ The method in charge of drawing the vertices and edges between the connected
        countries in this graph (the countries that have an air route between them),
        displaying the correct colours and edge and vertex states according to the
        input graph (as modified in the menu window by the user for this specific
        implementation).
        """
        for vertex in graph.get_vertices():
            colour1 = get_state_colour(vertex.state)
            pygame.draw.circle(self.display, colour1, vertex.pos, 8)

            for neighbour in vertex.neighbours:
                colour2 = get_state_colour(neighbour.state)

                # standard edge colour for two connected vertices
                edge_colour = 'black'

                # if any of the two vertices is blocked we block the edge
                if colour1 == 'red' or colour2 == 'red':
                    edge_colour = 'red'

                # draw the line connecting the two, these lines are sometimes overwritten since
                # edges are symmetric, but this doesn't affect the program
                pygame.draw.line(self.display, edge_colour, vertex.pos, neighbour.pos)

    #################################################
    # methods shared across various implementations #
    ##################################################

    def draw_cell(self, text: str, pos: tuple[int, int], colour: str,
                  grid_dim: tuple[int, int], offset: int, show_text: bool) -> None:
        """ Draw a cell on the correct window at the input position with all other
        input characteristics. Each cell represents a vertex in the standard graphs
        being used in the simple_program and maze implementations, or just a cell in
        a non-graph-related grid like the one for the air program menu.

        Preconditions:
            - 0 <= pos[0] <= 800
            - 0 <= pos[1] <= 810
        """
        local_width = int((WINDOW_SIZE[0] - 100) / grid_dim[0])
        local_height = int((WINDOW_SIZE[1] - 110) / grid_dim[1])

        text_size = get_grid_text_size(grid_dim)

        # draw rectangle where node is contained
        pygame.draw.rect(self.display, colour,
                         pygame.Rect(pos, (local_width - offset, local_height - offset)))
        if show_text:
            # draw text on the rectangle's position
            text_pos = (pos[0] + 5, pos[1] + 10)
            self.draw_grid_text(text_size, text, text_pos, grid_dim)

    def draw_grid_text(self, text_size: int, ttd: str, pos: tuple[int, int],
                       grid_dim: tuple[int, int]) -> None:
        """Draw the given text on the pygame screen at the given position (inside grids).
        Unlike with title text, the colour of this text is not open to customization since
        the grid text always needs good contrast with the regular cell colours, and must
        vanish once a vertex is set to be blocked (black-on-black).

        - ttd: the text to be displayed

        Preconditions:
            - 0 <= pos[0] <= 800
            - 0 <= pos[1] <= 810
        """
        local_width = int((WINDOW_SIZE[0] - 100) / grid_dim[0])
        local_height = int((WINDOW_SIZE[1] - 100) / grid_dim[1])

        font = pygame.font.SysFont(self.font_name, text_size)
        text_surface = font.render(ttd, True, THECOLORS['antiquewhite'])
        self.display.blit(text_surface,
                          pygame.Rect(pos, (pos[0] + local_width, pos[1] + local_height)))


###################
# Other functions #
###################

def get_state_colour(state: str) -> str:
    """" Returns the colour name (which forms part of the THECOLORS list) to represent
    a vertex's colour in a grid.

    Preconditions:
        - state in ['start', 'end', 'blocked'] or state is None
    """
    if state == 'start':
        return 'green'
    elif state == 'end':
        return 'blue'
    elif state == 'blocked':
        return 'red'
    elif state == 'path':
        return 'cyan'
    else:  # state is None
        return 'gray24'


def get_grid_text_size(grid_dim: tuple[int, int]) -> int:
    """ Helper performing calculations to determine the font size for the grid cells
    based on the dimensions of the grid (and with respect to the constant window size
    (800, 810). GFS is the smallest possible font size.
    """
    if grid_dim[0] > grid_dim[1]:
        text_size = int((MAX_GRID[0] / grid_dim[0]) * GFS)
    else:  # grid_dim[0] < grid_dim[1]
        text_size = int((MAX_GRID[1] / grid_dim[1]) * GFS)

    return text_size


# Some errors raised were counter-intuitive which is why we have removed them
if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913', 'R0902', 'R0912', 'E9972', 'E1101'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
