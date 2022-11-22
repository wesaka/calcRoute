from queue import PriorityQueue
from typing import NamedTuple
from datetime import datetime, timedelta
import argparse


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight


graph = Graph(315)

# Define line A
graph.add_edge(101, 102, 3)
graph.add_edge(102, 112, 3)
graph.add_edge(112, 111, 3)
graph.add_edge(111, 108, 3)
graph.add_edge(108, 107, 3)
graph.add_edge(107, 106, 3)

# Define line B
graph.add_edge(204, 203, 3)
graph.add_edge(203, 212, 3)
graph.add_edge(212, 211, 3)
graph.add_edge(211, 208, 3)
graph.add_edge(208, 209, 3)

# Define line C
graph.add_edge(314, 313, 3)
graph.add_edge(313, 311, 3)
graph.add_edge(311, 308, 3)
graph.add_edge(308, 305, 3)
graph.add_edge(305, 304, 3)
graph.add_edge(304, 303, 3)
graph.add_edge(303, 302, 3)

# Define station changes
graph.add_edge(302, 102, 4)
graph.add_edge(212, 112, 4)
graph.add_edge(211, 111, 4)
graph.add_edge(111, 311, 4)
graph.add_edge(211, 311, 4)
graph.add_edge(208, 108, 4)
graph.add_edge(208, 308, 4)
graph.add_edge(308, 108, 4)
graph.add_edge(303, 203, 4)
graph.add_edge(304, 204, 4)

valid_stations = [
    101,
    102,
    112,
    111,
    108,
    107,
    106,
    204,
    203,
    212,
    211,
    208,
    209,
    302,
    303,
    304,
    305,
    308,
    311,
    313,
    314
]


def dijkstra(graph, start_vertex):
    # Populate the dictionary - for each vertex, we will have a "distance" and the visited nodes to get that distance
    D = {v: [float('inf'), []] for v in range(graph.v)}
    D[start_vertex][0] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))
    graph.visited = []

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor][0]
                    new_cost = D[current_vertex][0] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor][0] = new_cost  # If the new cost is better, save it
                        D[neighbor][1] = D[current_vertex][1] + [neighbor]  # Also save visited stations for the case
    return D


def prettify_station(station):
    number = station - 100
    letter = 'A'
    while number > 100:
        number = number - 100
        letter = chr(ord(letter) + 1)

    return '{}{}'.format(letter, number)


def prettify_station_list(station_list):
    return [prettify_station(station) for station in station_list]


def detect_line_changes(station_list):
    line_changes = []
    current = station_list[0]
    for station in station_list:
        if station - current <= -100 or station - current >= 100:
            # Line change
            line_changes.append('{} -> {}'.format(prettify_station(current), prettify_station(station)))

        current = station

    return line_changes


def calculate(origin, destination, hour):
    station_letter = 'A'
    station_number = ((int(ord('A') - ord(station_letter)) + 1) * 100) + origin

    station = NamedTuple('Station', [('station_number', int), ('origin', int), ('station_letter', chr)])
    possible_origins = []

    while station_number < 400:
        if station_number in valid_stations:
            possible_origins.append(station(station_number, origin, station_letter))

        station_number = station_number + 100
        station_letter = chr(ord(station_letter) + 1)

    final_result = []
    departure_arrival_station = NamedTuple('DepartureArrivalStation',
                                           [('origin_number', int),
                                            ('origin_letter', chr),
                                            ('destination_number', int),
                                            ('destination_letter', chr),
                                            ('time_to_station', int),
                                            ('path', list)]
                                           )

    for origin_station in possible_origins:
        result = dijkstra(graph, origin_station.station_number)

        for station in range(len(result)):
            if result[station][0] != float('inf'):
                destination_station_number = station - 100
                destination_station_letter = 'A'

                while destination_station_number > 100:
                    destination_station_number = destination_station_number - 100
                    destination_station_letter = chr(ord(destination_station_letter) + 1)

                # Store the results in the final list
                final_result.append(departure_arrival_station(origin_station.origin,
                                                              origin_station.station_letter,
                                                              destination_station_number,
                                                              destination_station_letter,
                                                              result[station][0], result[station][1])
                                    )

    # Find the intended destination station from between all the results
    best_route = final_result[0]
    for final_station in final_result:
        lowest_time = 2000
        if final_station.destination_number == destination and final_station.time_to_station < lowest_time:
            lowest_time = final_station.time_to_station
            best_route = final_station

    end_time = datetime.strptime(hour, '%H:%M') + timedelta(minutes=best_route.time_to_station)

    # Check if end time is within working hours
    if end_time.hour < 6:
        raise Exception('Error - The end-time is outside of the working hours ({} -> {:02d}:{:02d})'.format(
            hour,
            end_time.hour,
            end_time.minute)
        )

    printing_value = '{}{}\n{}{}\n{}\n{}\n{:02d}:{:02d}\n{:02d}:{:02d}\n{}'.format(
        best_route.origin_letter,
        best_route.origin_number,
        best_route.destination_letter,
        best_route.destination_number,
        prettify_station_list(best_route.path),
        hour,
        end_time.hour,
        end_time.minute,
        *divmod(best_route.time_to_station, 60),
        detect_line_changes(best_route.path)
    )

    print(printing_value)


if __name__ == "__main__":
    # Parse the arguments from the command line
    parser = argparse.ArgumentParser(description='Calculating time between metro stations', add_help=False)
    parser.add_argument('-o', default=-1, type=int, help='The origin station (only its number!)')
    parser.add_argument('-d', default=-1, type=int, help='The destination station (only its number!)')
    parser.add_argument('-h', help='The time of departure')

    args = parser.parse_args()

    # Handle the possible input errors
    try:
        # Both origin and destination can only be numbers between 1 and 14 (inclusive)
        # Origin
        origin = args.o
        if type(origin) != int:
            raise ValueError('Error - Origin can only be a number.')

        if origin < 1 or origin > 14:
            raise ValueError('Error - Origin can only be a number between 1 and 14 (inclusive).')

        # Destination
        destination = args.d
        if type(destination) != int:
            raise ValueError('Error - Destination can only be a number.')

        if destination < 1 or destination > 14:
            raise ValueError('Error - Destination can only be a number between 1 and 14 (inclusive).')

        # Time of departure
        hour = args.h
        datetime_hour = datetime.strptime(hour, '%H:%M')
        if datetime_hour.hour < 6:
            raise ValueError('Error - The metro working hours are between 06:00 and 00:00')

        calculate(origin, destination, hour)

    except Exception as e:
        print(e)
        exit()
