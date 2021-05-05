"""CSC111 Winter 2021 Course Project: Weighted Classes and Dijkstra's Algorithm

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the WeightedGraph and WeightedVertex classes that are
used as the foundation of our program. These classes are similar to those used in assignment 3,
however they do contain a few differences. As these are weighted graphs, the path-finding
algorithm used for these is the Dijkstra Algorithm, which has been implemented
as a method of the WeightedGraph Class. This module also contains two functions that create
blank weighted graphs for our program level 3 and 4, which focuses on finding shortest and
least costliest flight paths, with the same blocking functionality as levels 1 and 2.

This file is copyright (c) 2021 Michele Massa, Nischal Nair and Nathan Zavys-Cox.
"""
from __future__ import annotations
from typing import Optional, Union
import math
import csv


###########
# Classes #
###########


class WeightedVertex:
    """ A weighted vertex in a graph, representing a location. Similar to Vertex class from
    level 2, however has new instance attributes. A weight assigned to any edge is either the
    physical distance between two locations, or the cost of a flight ticket between two locations

    Instance Attributes
        - pos: position of the vertex on the map, stored as a tuple of integers, or the
        coordinates of the vertex in the Pygame window
        - neighbours: dictionary mapping adjacent vertices to their assigned edge weights
        - name: the name of the location
        - menu_pos: the (x,y) coordinates of the city on the selection menu, where the user
        selects start, end and blocked points.
        - state: str representing whether a vertex is a start point, end point, blocked, within
        a path, or a general vertex

    Representation Invariants
        - state in {'blocked', 'start', 'end', 'path'} or state is None
    """
    pos: tuple[float, float]
    neighbours: dict[WeightedVertex, Union[int, float]]
    name: str  # city name
    menu_pos: Optional[tuple[int, int]]  # the position of each country in the customizing grid
    state: Optional[str]  # 'start', 'end', 'blocked', none means normal

    def __init__(self, position: tuple[float, float],
                 neighbours: dict[WeightedVertex, Union[int, float]],
                 name: str, menu_pos: tuple[int, int] = None, state: Optional[str] = None) -> None:
        """ Initialize a new vertex with the given item and neighbours.
        """
        self.pos = position
        self.neighbours = neighbours
        self.state = state
        self.name = name
        self.menu_pos = menu_pos

    def check_connected(self, target_pos: tuple[float, float],
                        visited: set[WeightedVertex]) -> bool:
        """ Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.

        Preconditions:
            - self not in visited
        """
        if self.pos == target_pos:
            # Our base case: the target_item is the current vertex
            return True
        # In case the stating vertex is a blocked vertex
        elif self.state == "blocked":
            return False
        else:
            visited.add(self)  # Add self to the set of visited vertices
            for u in self.neighbours:
                # Don't recurse to visited or blocked vertices.
                if u not in visited and u.state != "blocked":
                    if u.check_connected(target_pos, visited):
                        return True

            return False


class WeightedGraph:
    """ A class representing a world map, either containing vertices representing cities
    or countries. Similar to graph, however with changes in certain methods to accommodate
    for WeightedVertex. Also now uses Dijkstra Algorithm to find the shortest possible paths
    between two locations, since this algorithm uses weighted edges.
    """
    vertices: dict[tuple[float, float], WeightedVertex]

    def __init__(self) -> None:
        """ Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, position: tuple[float, float], name: str,
                   menu_pos: Optional[tuple[int, int]] = None, state: Optional[str] = None) -> None:
        """ Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self.vertices[position] = WeightedVertex(position, {}, name, menu_pos, state)

    def add_edge(self, pos1: tuple[float, float], pos2: tuple[float, float], distance: float = 1) \
            -> None:
        """ Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if pos1 in self.vertices and pos2 in self.vertices:
            v1, v2 = self.vertices[pos1], self.vertices[pos2]
            v1.neighbours[v2], v2.neighbours[v1] = distance, distance
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def connected(self, pos1: tuple[float, float], pos2: tuple[float, float]) -> bool:
        """ Return whether item1 and item2 are connected vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if pos1 in self.vertices and pos2 in self.vertices:
            v1 = self.vertices[pos1]
            return v1.check_connected(pos2, set())  # Pass in an empty "visited" set
        else:
            return False

    def dijkstra_search(self, start_pos: tuple[float, float], end_pos: tuple[float, float]) -> dict:
        """ Returns the shortest possible distance between start and end points using the Dijkstra
        Algorithm, which uses a greedy implementation to first calculate the shortest paths from
        the start vertex to every other vertex in the graph, and then identifies the shortest
        path for start to end, excluding any blocked vertices, either in terms of physical distance
        or flight cost, depending on level 3 or level 4 implementations

        Returns this as a dictionary in the form
        {end_pos: [distance/cost of start_pos to end_pos, [path from start to end]]}

        Preconditions
          - self.connected(start_pos, end_pos)
        """
        # Extracting the start and end vertices
        start_vertex = self.vertices[start_pos]
        end_vertex = self.vertices[end_pos]

        # initialising distances from the start vertex to infinity, except the start vertex itself
        dist = {start_vertex: [0, [start_vertex.pos]]}
        for v in self.vertices.values():
            if v != start_vertex:
                dist[v] = [math.inf, [start_vertex.pos]]

        # Greedy implementation of the Dijkstra algorithm
        all_vertices = set(self.vertices.values())
        while all_vertices:
            min_distance = min([dist[vert][0] for vert in all_vertices])
            min_vertex = [vert for vert in all_vertices if dist[vert][0] == min_distance][0]
            all_vertices.remove(min_vertex)

            for u in min_vertex.neighbours:
                if dist[u][0] > dist[min_vertex][0] + min_vertex.neighbours[u] \
                        and u.state != 'blocked':
                    dist[u][0] = dist[min_vertex][0] + min_vertex.neighbours[u]
                    dist[u][1] = dist[min_vertex][1] + [u.pos]

        return {vert.pos: dist[vert] for vert in dist if vert == end_vertex}

    def get_vertices(self) -> set[WeightedVertex]:
        """ Return the set of vertices in this graph in the form of the
        vertex objects.
        """
        return {self.vertices[vertex] for vertex in self.vertices}


############################
# Graph creation functions #
############################


def world_cities_graph(width: int, height: int) -> WeightedGraph:
    """ Returns a WeightedGraph that represents the world map, containing vertices as cities
    as given in the file containing a list of cities, and edges as given on our source map
    as stored in edges. The function arguments are there to define the menu grid positions
    in the selection screen, where the use chooses start, end and blocked locations for
    levels 3 and 4.
    """
    menu_positions = [(x, y) for y in range(0, height) for x in range(0, width)]

    g = WeightedGraph()

    with open('datasets/cities.csv') as csv_file:
        reader = csv.reader(csv_file)
        i = 0
        for row in reader:
            pos = menu_positions[i]
            g.add_vertex((float(row[1]), float(row[2])), row[0], pos)
            i += 1

    with open('datasets/city_edges.csv') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            city1 = [v for v in g.vertices if g.vertices[v].name == row[0]][0]
            city2 = [v for v in g.vertices if g.vertices[v].name == row[1]][0]
            distance = float(row[2])
            g.add_edge(city2, city1, distance)

    return g


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
