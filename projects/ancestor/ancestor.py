"""
STEPS TO SOLVE (almost) ANY GRAPHS PROBLEM!
* Translate the problem into graph terminology
* Build your graph
* Traverse your graph
"""

import sys
sys.path.insert(0, '../graph')
from util import Stack, Queue  # These may come in handy


# Find the longest path

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_edge(self, v1, v2):
        # seems like for this problem, we're given
        # unidirectional relationships from v2 to v1

        if v1 not in self.vertices:
            self.vertices[v1] = set()

        if v2 not in self.vertices:
            self.vertices[v2] = set([v1])
        else:
            self.vertices[v2].add(v1)

    def find_earliest_ancestor(self, starting_vertex):
        # create an empty set to store visited nodes
        visited = set()
        if (starting_vertex not in self.vertices
        or len(self.vertices[starting_vertex]) == 0):
            return -1

        # create an empty Queue and enqueue a path to the starting vertex
        q = Queue()
        q.enqueue([starting_vertex])

        # keep track of longest path

        longest_path = []
        # while the queue is not empty
        while q.size() > 0:
            #dequeue the first path
            path = q.dequeue()
            # grab the vertex from the end of the path
            v = path[-1]

            # if the vertex has not been visited
            if v not in visited:

                # mark it as visited
                visited.add(v)

                # add a path and all of its neighbors to the back of the queue
                for neighbor in self.vertices[v]:
                    #copy the path
                    path_copy = list(path)

                    # append neighbor to the back of the copy
                    path_copy.append(neighbor)

                    # check that longest path isn't shorter than the new path
                    if len(longest_path) < len(path_copy):
                        longest_path = path_copy

                    # if the new path length is equal to the longest path's length
                    # and the last value is less than the longest_path's last value
                    # then choose the copy
                    if (len(longest_path) == len(path_copy)
                    and longest_path[-1] > path_copy[-1]):
                        longest_path = path_copy

                    # enqueue the copy
                    q.enqueue(path_copy)
        return longest_path[-1]

def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    for a in ancestors:
        g.add_edge(a[0], a[1])
    return g.find_earliest_ancestor(starting_node)

# g = Graph()
# g.add_edge(1,3)
# g.add_edge(2,3)
# g.add_edge(3,6)
# g.add_edge(5,6)
# g.add_edge(5,7)
# g.add_edge(4,5)
# g.add_edge(4,8)
# g.add_edge(8,9)
# g.add_edge(11,8)
# g.add_edge(10,1)
# print(g.vertices)
# print(g.find_earliest_ancestor(6))
