# A simple unweighted graph as adjacency matrix.
graph1 = [
    # KSR, Sek, Bahnhofstr, Hafenstrasse, Zelgstrasse, Bahnhof
    [ False, True, False, False, False, False],  # KSR
    [ True, False, True, True, True, False],  # Sek
    [ False, True, False, False, False, True],  # Bahnhofstrasse
    [ False, True, False, False, False, True],  # Hafenstrasse
    [ False, True, False, False, False, True],  # Zelgstrasse
    [ False, False, True, True, True, False],  # Bahnhof
]

# The same graph as adjacency matrix, with weights.
graph2 = [
    # KSR, Sek, Bahnhofstr, Hafenstrasse, Zelgstrasse, Bahnhof
    [ -1, 1, -1, -1, -1, -1],  # KSR
    [ 1, -1, 3, 5, 7, -1],  # Sek
    [ -1, 3, -1, -1, -1, 7],  # Bahnhofstrasse
    [ -1, 5, -1, -1, -1, 6],  # Hafenstrasse
    [ -1, 7, -1, -1, -1, 5],  # Zelgstrasse
    [ -1, -1, 7, 6, 5, -1],  # Bahnhof
]

def has_direct_connection(matrix, n1, n2):
    return matrix[n1][n2] >= 0

# The same directed graph as adjacency list.
graph3 = {
    "ksr": {"sek": 1, "weitenzelgstr": 1},
    "sek": {"bahnhofstr": 3, "hafenstr": 5, "zelgstr": 7},
    "bahnhofstr": {"bahnhof": 7, "ksr": 1},
    "hafenstr": {"bahnhof": 6},
    "zelgstr": {"bahnhof": 5, "sek": 7},
    "bahnhof": {},
    "weitenzelgstr": {},
}

# Matrix version usin numpy instead.
import numpy as np
graph4 = np.array([
    # KSR, Sek, Bahnhofstr, Hafenstrasse, Zelgstrasse, Bahnhof
    [ -1, 1, -1, -1, -1, -1],  # KSR
    [ 1, -1, 3, 5, 7, -1],  # Sek
    [ -1, 3, -1, -1, -1, 7],  # Bahnhofstrasse
    [ -1, 5, -1, -1, -1, 6],  # Hafenstrasse
    [ -1, 7, -1, -1, -1, 5],  # Zelgstrasse
    [ -1, -1, 7, 6, 5, -1]  # Bahnhof
    ]
)

def has_direct_connection(matrix, n1, n2):
    return matrix[n2][n1] >= 0

def has_direct_connection2(matrix, n1, n2):
    return matrix[n2,n1] >= 0

graph5 = {
    "ksr": {"turnhalle": 1, "weitenzelgstr": 1, "sek": 2},
    "turnhalle": {},
    "weitenzelgstr": {"bahnhofstr": 8},
    "sek": {"bahnhofstr": 3, "hafenstr": 5, "zelgstr": 7},
    "bahnhofstr": {"bahnhof": 7, "ksr": 4},
    "hafenstr": {"bahnhof": 4},
    "zelgstr": {"bahnhof": 5},
    "bahnhof": {},
}

