
import csv
import sys
import heapq
import time

inf = float('inf')


class Vertex:

    def __init__(self, name=None):
        self.P = None
        self.name = name
        self.key = sys.maxsize


class Graph:
    global time

    def __init__(self, file):
        self.vertices = dict()  # adacency list
        self.vertlist = dict()  # actual vertices objects with name as key
        self.E = dict()
        self.file = file
        self.undirected_adjlist()
        self.distance = dict()

    def addE(self, v1, v2, weight):
        if frozenset({v1, v2}) not in self.E:
            self.E[frozenset({v1, v2})] = weight

    def w(self, v1, v2):
        return self.E.get(frozenset({v1, v2}))

    def undirected_adjlist(self):  # creates adj list
        '''created an adjacency list to keep up with what values
        are neighboring to which vertices'''
        with open(self.file, 'r') as csv_file:  # read in as undirected graph. Not specified in assignment doc
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                line = line[0].split()
                x = int(line[0])
                if len(line) > 1:
                    y = int(line[1])
                    weight = float(line[2])
                    self.addE(x, y, weight)
                    if x not in self.vertices:
                        self.vertices[x] = [y]
                    else:
                        if y not in self.vertices.get(x):
                            self.vertices.get(x).append(y)
                    if y not in self.vertices:
                        self.vertices[y] = [x]
                    else:
                        if x not in self.vertices.get(y):
                            self.vertices.get(y).append(x)
                else:
                    self.vertices[x] = []
        for vertex in self.vertices:
            vertex = Vertex(vertex)
            self.vertlist[vertex.name] = vertex

    def print_adjacency_list(self):
        for key, value in self.vertices.items():
            print(str(key) + ": " + str(value))

    def dijkstra(self, s):
        self.distance = {vertex: inf for vertex in self.vertices}
        self.distance[s] = 0
        Q = [(self.distance[vertex], vertex) for vertex in self.vertices]  # heap of tuples containing (distance, vertex)
        while Q:
            heapq.heapify(Q)
            current_vertex = heapq.heappop(Q)[1]  # pops the tuple with shortest distance and gets just the vertex value from the (distance, vertex) tuple
            for adj_v in self.vertices.get(current_vertex):  # gets adjacent vertex names from adjacency list
                if self.distance[adj_v] > self.distance[current_vertex] + self.w(current_vertex, adj_v):
                    Q.remove((self.distance[adj_v], adj_v))
                    self.distance[adj_v] = self.distance[current_vertex] + self.w(current_vertex, adj_v)
                    self.vertlist.get(adj_v).P = current_vertex
                    Q.append((self.distance[adj_v], adj_v))

    def print_path(self, s):
        try:
            if self.vertlist.get(s) and self.vertlist.get(s).P == 0:
                print(self.vertlist.get(s).P, "-", self.vertlist.get(s).name, ": ", "%.5f" % self.distance[s])
                return
        except AttributeError:
            print("NO PATH")
            return
        try:
            self.print_path(self.vertlist.get(s).P)
        except AttributeError:
            print("NO PATH")
            return
        print(self.vertlist.get(s).P, "-", self.vertlist.get(s).name, ": ", "%.5f" % self.distance[s])

    def print_cost(self, s):
        print("Total cost: %.5f" % self.distance[s])

    def all_short_paths(self, s):
        for x in self.vertlist.values():
            print("Total cost: ", s, "-", x.name, ':', "%.5f" % self.distance[x.name])


def driver():
    print("\t\tDriver\n")
    graphs = []
    tiny_graph = Graph("tinyDG.txt")
    graphs.append(tiny_graph)
    medium_graph = Graph("mediumDG.txt")
    graphs.append(medium_graph)
    large_graph = Graph("largeDG.txt")
    graphs.append(large_graph)
    xlarge_graph = Graph("XtraLargeDG.txt")
    graphs.append(xlarge_graph)
    for graph in graphs:
        start = time.perf_counter_ns()
        graph.dijkstra(0)
        elapsed = (time.perf_counter_ns() - start)
        secondtime = str(elapsed / 1000000000)
        print(graph.file, ":", secondtime, "seconds", str(elapsed), "nanoseconds\n")
        print("-"*75)


driver()

# Change these for specific cases (change file, starting node, ending node)
print("\t\tExample path using medium graph. From node 0 to 249")
graph = Graph("mediumDG.txt")
graph.dijkstra(0)  # starting node 0
# graph.print_adjacency_list()
# graph.all_short_paths(0)  # cost from 0 to all other nodes
#change these two for the ending node (currently 100)
graph.print_path(100)  
graph.print_cost(100)

