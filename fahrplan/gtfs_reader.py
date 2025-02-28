from math import inf
import os
import json
import csv

class Stop:
    def __init__(self, row):
        self.id = row['stop_id']
        self.name = row['stop_name']
        self.lat = row['stop_lat']
        self.lon = row['stop_lon']
        self.type = row['location_type']
        self.parent = row['parent_station']

def parse_time_to_minutes(str):
    """Returns the HH:mm:ss time in minutes.
       GTFS times may have more than 23 hours if the route extends into the next day, so
       we cannot use the regular datetime parsing.
    """
    ints = str.split(':')
    return int(ints[0])*60 + int(ints[1])

def update_graph(graph, source, destination, minutes):
    """Updates the graph by adding or updating the edge between
       source and destination to the minimum of minutes and an existing edge.
       """
    neighbors = graph.setdefault(source.name, {})
    old_duration = neighbors.setdefault(destination.name, inf)
    neighbors[destination.name] = min(old_duration, minutes)
    # Add destination to graph to ensure all stops are included.
    graph.setdefault(destination.name, {})

def read_stops(path, identity='id'):
    stops = {}
    with open(os.path.join(path, 'stops.txt'), mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stop = Stop(row)
            stops[stop.__getattribute__(identity)] = stop
    return stops

def read_stop_times(path, stops, graph, max_stops=None):
    with open(os.path.join(path, 'stop_times.txt'), mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        trip = None
        departure = None
        origin = None
        count = 0
        for row in reader:
            # Our next stop.
            destination = stops[row['stop_id']]
            current_trip = row['trip_id']

            # If stop is on the same trip as the previous stop, record
            # a direct non-stop edge [previous_stop -> destination]
            if current_trip == trip:
                arrival = parse_time_to_minutes(row['arrival_time'])
                duration_minutes = arrival - departure
                update_graph(graph, origin, destination, duration_minutes)
            
            trip = current_trip
            departure = parse_time_to_minutes(row['departure_time'])
            origin = destination

            count += 1
            if max_stops and count > max_stops: break
    
    return graph

def read_transfers(path, stops, graph):
    with open(os.path.join(path, 'transfers.txt'), mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source = stops[row['from_stop_id']]
            destination = stops[row['to_stop_id']]
            minutes = int(int(row['min_transfer_time']) // 60)
            update_graph(graph, source, destination, minutes)

def read_gtfs(path):
    """Reads GTFS schedule data and returns the stops graph as adjacency list.
       The graph contains the direct non-stop connections between two stops, but 
       does not include trip information or change information."""
    stops = read_stops(path)
    graph = {}
    read_stop_times(path, stops, graph)
    read_transfers(path, stops, graph)
    return graph

def write_schedule(filename, graph):
    with open(filename, mode='w', encoding='utf-8') as out:
        json.dump(graph, out, ensure_ascii=False, indent=4, sort_keys=True)

def read_json_schedule(filename):
    with open(filename, mode='r', encoding='utf-8') as fahrplan:
        graph = json.load(fahrplan)
    return graph

# import sys
# sys.setrecursionlimit(10000)

# print(find_path(graph, 'Romanshorn', 'Romanshorn, Bahnhof'))