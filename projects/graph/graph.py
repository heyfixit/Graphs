"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            self.vertices[v1] = set([v2])

        if v2 not in self.vertices:
            self.vertices[v2] = set()

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        visited_nodes = set()

        # add starting vertex
        q.enqueue(starting_vertex)

        while q.size() > 0:
            v = q.dequeue()
            if v in visited_nodes:
                continue

            print(v)
            visited_nodes.add(v)
            for vertex in self.vertices[v]:
                q.enqueue(vertex)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        visited_nodes = set()

        # add starting vertex
        s.push(starting_vertex)

        while s.size() > 0:
            v = s.pop()
            if v in visited_nodes:
                continue

            print(v)
            visited_nodes.add(v)
            for vertex in self.vertices[v]:
                s.push(vertex)

    def dft_recursive(self, starting_vertex, visited_nodes = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        if visited_nodes is None:
            visited_nodes = set([starting_vertex])

        print(starting_vertex)

        for vertex in self.vertices[starting_vertex]:
            if vertex not in visited_nodes:
                visited_nodes.add(vertex)
                self.dft_recursive(vertex, visited_nodes)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        visited_nodes = set()
        vertex_data = {}

        # add starting vertex

        q.enqueue(starting_vertex)
        vertex_data[starting_vertex] = {
            'dist': 0,
            'prev': -1
        }

        result = []

        while q.size() > 0:
            v = q.dequeue()
            if v in visited_nodes:
                continue

            if v == destination_vertex:
                # we're at the shortest path
                current_vertex = v
                while vertex_data[current_vertex]['prev'] != -1:
                    result.insert(0, current_vertex)
                    current_vertex = vertex_data[current_vertex]['prev']
                result.insert(0, starting_vertex)
                break

            visited_nodes.add(v)
            for vertex in self.vertices[v]:
                if not vertex in vertex_data:
                    vertex_data[vertex] = {
                        'dist': vertex_data[v]['dist'] + 1,
                        'prev': v
                    }
                q.enqueue(vertex)
        return result

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        visited_nodes = set()
        result = []
        vertex_data = {}

        # add starting vertex
        s.push(starting_vertex)

        vertex_data[starting_vertex] = {
            'dist': 0,
            'prev': -1
        }

        while s.size() > 0:
            v = s.pop()
            if v in visited_nodes:
                continue

            if v == destination_vertex:
                current_vertex = v
                while vertex_data[current_vertex]['prev'] != -1:
                    result.insert(0, current_vertex)
                    current_vertex = vertex_data[current_vertex]['prev']
                result.insert(0, starting_vertex)
                break

            visited_nodes.add(v)
            for vertex in self.vertices[v]:
                if not vertex in vertex_data:
                    vertex_data[vertex] = {
                        'dist': vertex_data[v]['dist'] + 1,
                        'prev': v
                    }
                s.push(vertex)
        return result





if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT recursive paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
