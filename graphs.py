def find_path_dfs(graph, start=None, end=None, visited=None):
    """Returns the list of adjacent nodes from 'start' to 'end' if it exists,
       returns False otherwise.

       If start is None, the first node in graph is chosen.
       If end is None, the last node in graph is chosen.
    """
    # Choose first and last nodes in graph if not given.
    if start == None:
        start = next(iter(graph))
    if end == None:
        end = list(graph)[-1]
    if visited == None:
        visited = set()

    # If start has already been visited, we closed a cycle - return false.
    if start in visited:
        return False

    # Local check: if start and end are the same, we have a trivial solution.    
    if start == end:
        return [end]

    # Record the current node as visited so that we break cycles should we return to it
    # in the recursion.
    visited.add(start)

    # Recursion: If we find a path p from any of our neighbors n to end, there obviously is
    # a path from 'start' to end that consists of start + p.
    edges = graph[start]
    for neighbor in edges:
        path = find_path_dfs(graph, neighbor, end, visited)
        if path:
            # We have found a path from neighbor to end
            # -> the path from start to end is the same path, with start prepended.
            return [start] + path
    # None of our neighbors has a path to 'end' -> give up.
    return False

def build_path_from_parents(graph, parents, start, end):
    """Given a parents dictionary, builds the path from start to end and records edge weights."""
    path = []
    node = end
    total = 0
    while node != start:
        parent = parents[node]
        edge = graph[parent][node]
        total += edge
        path.insert(0, (node, edge))
        node = parent
    path.insert(0, (start, 'start'))
    result = {
        'path': path,
        'length': total
    }
    return result

from collections import deque
def find_path_bfs(graph, start, end):
    """Finds the shortest path from start to end using BFS."""
    # Deque: a double-ended list with efficient modifications at either end.
    candidates = deque()
    candidates.append(start)
    # Dictionary containing the parent through which each node was visited.
    parents = {}
    while candidates:
        # print(candidates)
        # input()
        node = candidates.popleft()
        for neighbor in graph[node]:
            if neighbor not in parents:
                parents[neighbor] = node
                candidates.append(neighbor)
                if neighbor == end:
                    return build_path_from_parents(graph, parents, start, end)
    return None  # No path found

from math import inf
from queue import PriorityQueue
def shortest_path(graph, start, end):
    """Dijkstra shortest path."""
    # Candidates to process next, ordered by increasing distance.
    # The head of the queue is guaranteed to be the next node to be visited,
    # while the order of subsequent nodes could still be reordered if and preceding
    # node offers a shorter path to them.
    candidates = PriorityQueue()
    candidates.put((0, start))
    parents = {}
    # In addition to BFS, we record for each discovered node the currently known shortest
    # distance from start.
    distances = {start: 0}
    while candidates:
        # print(distances)
        # print(candidates.queue)
        # input()
        
        # The first candidate node is guaranteed to be the closest one of the candidates.
        distance, node = candidates.get()
        if node == end:  # We're done.
            return build_path_from_parents(graph, parents, start, end)
        if distances.get(node, inf) < distance:
            continue  # Node already processed with smaller distance. See comment below.

        for neighbor, edge in graph[node].items():
            new_distance = distance + edge
            old_distance = distances.get(neighbor, inf)
            if old_distance <= new_distance:
                continue  # Neighbor already filled via some shorter path
            # Otherwise: we found a shorter (or new) path to neighbor - record it
            # and add to candidates.
            distances[neighbor] = new_distance

            # To be correct, we'd need to remove any old record (old_distance, neighbor) 
            # in the candidates, but that is expensive. Instead, we leave it in and
            # check above if distances has a shorter path recorded (line 101).
            candidates.put((new_distance, neighbor))
            parents[neighbor] = node
    return None  # No path found

def find_cycles(graph):
    """Returns all cycles in graph."""
    # Record visited nodes in a set, which gives us constant-time lookup of
    # nodes.
    visited = set()
    cycles = []
    for node in graph:
        if node in visited:
            continue  # already been here
        find_cycles_from_node(graph, node, visited, cycles)
    return cycles

def find_cycles_from_node(graph, node, visited, cycles, path=[]):
    if node in path:
        # We have found a cycle from the first occurrence of node
        # to here.
        # Remove prefix up to the first occurrence:
        index = path.index(node)
        cycle = path[index:]
        cycles.append(cycle)
        return

    visited.add(node)
    path.append(node)
    length = len(path)
    for neighbor in graph[node]:
        # Find cycles forward in graph.
        find_cycles_from_node(graph, neighbor, visited, cycles, path)
        # Crop path to prefix up to current node.
        path = path[:length]

def traversierung_dfs(graph, node, sequence=None):
    """Traverses the graph and returns the sequence of visited nodes in depth-first order."""
    sequence = sequence or []
    if node in sequence:
        return
    sequence.append(node)
    for neighbor in graph[node]:
        traversierung_dfs(graph, neighbor, sequence)
    return sequence

def traversierung_bfs(graph, start):
    """Traverses the graph and returns the sequence of visited nodes in breadth-first order."""
    sequence=[]
    candidates = [start]
    while candidates:
        node = candidates.pop(0)
        if node in sequence:
            continue
        sequence.append(node)
        for neighbor in graph[node]:
            candidates.append(neighbor)
    return sequence

def dfs(graph, node, visited=None):
    """ A generator of all nodes in graph, in depth-first order. """
    visited = visited or set()
    if node in visited:
        return
    yield node
    visited.add(node)
    for neighbor in graph[node]:
        yield from dfs(graph, neighbor, visited)

def bfs(graph, start):
    """ A generator of all nodes in graph, in breadth-first order. """
    candidates = {start}
    visited = {start}
    while candidates:
        next = candidates.pop()
        yield next
        for neighbor in graph[next]:
            if neighbor not in visited:
                visited.add(neighbor)
                candidates.add(neighbor)

