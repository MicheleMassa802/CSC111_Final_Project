""" CSC111 Winter 2021 Course Project: Standard Classes and Simple Algorithm

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the Graph and Vertex classes that are used as the
foundation of our program. These classes are similar to those discussed in lecture,
however they do contain a few differences. As these are unweighted graphs, the path-finding
algorithm used for these is the Breadth First Search Algorithm, which has been implemented
as a method of the Graph Class. This module also contains two functions that create blank
graphs for our program levels 1 and 2.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox.
"""
from __future__ import annotations
from typing import Optional
import csv


###########
# Classes #
###########


class Vertex:
    """ A vertex in a graph, representing a grid position. Similar to _Vertex class introduced
    in lecture, however now maintains a position instead of an item, and has a new instance
    attribute, state.

    Instance Attributes
      - pos: position of the vertex on the grid, stored as a tuple of integers, or the
      coordinates of the vertex
      - neighbours: set of adjacent vertices
      - state: str representing whether a vertex is a start point, end point, blocked, within
      a path, or a general vertex

    Representation Invariants
      - state in {'blocked', 'start', 'end', 'path'} or state is None
    """
    pos: tuple[int, int]
    neighbours: set[Vertex]
    state: Optional[str]  # 'start', 'end', 'blocked', 'path', none means normal

    def __init__(self, position: tuple[int, int], neighbours: set[Vertex],
                 state: Optional[str] = None) -> None:
        """ Initialize a new vertex with the given item and neighbours.
        """
        self.pos = position
        self.neighbours = neighbours
        self.state = state

    def check_connected(self, target_pos: tuple[int, int], visited: set[Vertex]) -> bool:
        """ Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited

        >>> v1 = Vertex((0, 1), set())
        >>> v2 = Vertex((0, 2), set())
        >>> v3 = Vertex((0, 3), set())
        >>> v2.neighbours.add(v3)
        >>> v3.neighbours.add(v2)
        >>> v1.neighbours.add(v2)
        >>> v2.neighbours.add(v1)
        >>> v1.check_connected((0, 3), set())
        True
        >>> v2.state = 'blocked'
        >>> v1.check_connected((0, 3), set())
        False
        """
        if self.pos == target_pos:
            # Our base case: the target_item is the current vertex
            return True
        # In case the stating vertex is a blocked vertex
        else:
            visited.add(self)  # Add self to the set of visited vertices
            for u in self.neighbours:
                # Don't recurse to visited or blocked vertices.
                if u not in visited and u.state != "blocked":
                    if u.check_connected(target_pos, visited):
                        return True

            return False


class Graph:
    """ A class representing a graph. The edges are represented by vertices being
    'neighbours' to each other, i.e are in each others neighbour sets. Each graph is a rectangular
    grid of a certain width and height, with vertices being set at specific co-ordinates.

    Instance Attributes:
      - vertices: A dictionary mapping vertex positions on the screen/grid to their
      vertex objects.
    """
    vertices: dict[tuple[float, float], Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges).
        """
        self.vertices = {}

    def add_vertex(self, position: tuple[int, int], state: Optional[str] = None) -> None:
        """ Add a vertex with the given position to this graph, and a state, which
        is set to None if not specified

        The new vertex is not adjacent to any other vertices.

        Preconditions
          - state in {'blocked', 'start', 'end', 'path'} or state is None
        """
        self.vertices[position] = Vertex(position, set(), state)

    def add_edge(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> None:
        """ Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if pos1 in self.vertices and pos2 in self.vertices:
            v1 = self.vertices[pos1]
            v2 = self.vertices[pos2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def connected(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
        """ Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if pos1 in self.vertices and pos2 in self.vertices:
            v1 = self.vertices[pos1]
            return v1.check_connected(pos2, set())  # Pass in an empty "visited" set
        else:
            return False

    def breadth_first_search(self, start_pos: tuple, end_pos: tuple) -> Optional[list]:
        """ Returns the shortest path between two vertexes, if there exists such a path.
        Return None if no such path exists. This method uses the Breadth First Search
        algorithm to find the shortest path between two vertexes. The returned path contains
        only vertices between start and end, and also does NOT contain any blocked vertices.

        Preconditions
          - self.connected(start_pos, end_pos)
        """
        # Extracting the star and end point vertices
        start = self.vertices[start_pos]
        end = self.vertices[end_pos]

        # explored is a set that keep track of 'visited' vertices
        explored = set()
        que = [[start]]

        # pre-add any blocked vertices to explored, so that we don't call them later on
        for u in self.vertices:
            if self.vertices[u].state == "blocked":
                explored.add(u)

        # Run the breadth first search algorithm, slightly modified to not count blocked vertices
        while que != []:
            path = que.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = self.vertices[node.pos].neighbours

                for neighbour in neighbours:

                    # checking that we don't traverse into any blocked vertices
                    if neighbour.state != "blocked":
                        new_path = list(path)
                        new_path.append(neighbour)
                        que.append(new_path)

                        if neighbour == end:
                            return [v.pos for v in new_path][1:-1]

                explored.add(node)

        # In case the early return has not occurred, meaning that there exists no valid path
        return None

    def get_vertices(self) -> set[Vertex]:
        """ Return the set of vertices in this graph in the form of the
        vertex objects. """
        return {self.vertices[vertex] for vertex in self.vertices}


####################
# Helper Functions #
####################


def load_csv_into_graph(file_name: str) -> Graph:
    """ Given a csv file with map data, converts it to and returns a graph
    Note: the csv file must have a "B" every place there is a blocked vertex and P for a path
    In the csv file, each cell counts as one vertex, and contains a letter which denotes
    the state for which this vertex should be initialized to.
    """
    user_map = Graph()
    row_num = 0
    width_of_map = 0

    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            width_of_map = len(row)
            for i in range(len(row)):
                if row[i] == "B":
                    user_map.add_vertex((i, row_num), "blocked")
                elif row[i] == "S":
                    user_map.add_vertex((i, row_num), "start")
                elif row[i] == "E":
                    user_map.add_vertex((i, row_num), "end")
                else:
                    user_map.add_vertex((i, row_num))
            row_num += 1
    height_of_map = row_num
    # Knowing the dimensions of the graph, connect the graph
    for y in range(height_of_map):
        for x in range(width_of_map):
            if x == width_of_map - 1 and y == height_of_map - 1:
                pass
            elif x == width_of_map - 1:
                user_map.add_edge((x, y), (x, y + 1))
            elif y == height_of_map - 1:
                user_map.add_edge((x, y), (x + 1, y))
            else:
                user_map.add_edge((x, y), (x, y + 1))
                user_map.add_edge((x, y), (x + 1, y))

    return user_map


def create_blank_graph(width: int, height: int) -> Graph:
    """ Given a user specified width and height, returns a grid graph with vertices
    at every co-ordinate, with all starting states set to None so the user can modify these
    later on. Used in our level 1 program, where the user understands the functionality of
    path finding algorithms.

    Preconditions
      - width > 0
      - height > 0
    """
    user_map = Graph()

    for y in range(height):
        for x in range(width):
            user_map.add_vertex((x, y))

    for y in range(height):
        for x in range(width):
            if x == width - 1 and y == height - 1:
                pass
            elif x == width - 1:
                user_map.add_edge((x, y), (x, y + 1))
            elif y == height - 1:
                user_map.add_edge((x, y), (x + 1, y))
            else:
                user_map.add_edge((x, y), (x, y + 1))
                user_map.add_edge((x, y), (x + 1, y))

    return user_map


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136', 'E9999', 'E9998', 'R0913'],
        'extra-imports': [],
        'max-nested-blocks': 5
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
