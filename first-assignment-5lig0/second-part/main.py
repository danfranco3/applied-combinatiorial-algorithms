#!/usr/bin/env python3
import time
import heapq
from collections import defaultdict, deque

import IPython


def read_config(file="config.txt"):
    f = open(file, "r")
    lines = f.readlines()

    n_Hauler = 1
    n_LP = 0
    n_ULP = 0
    n_SO = 0
    n_CS = 1
    init_haulers = []
    LP_positions = []
    ULP_positions = []
    SO_positions = []
    CS_positions = []
    battery_capacity = 0
    initial_energy = 0

    # for following the line number
    index = 1
    for line in lines:
        # read number of Haulers
        if (index == 1):
            n_Hauler = int(line.split("//")[0])

        # read number of LPs
        elif (index == 2):
            n_LP = int(line.split("//")[0])

        # read number of ULPs
        elif (index == 3):
            n_ULP = int(line.split("//")[0])

        # read number of SOs
        elif (index == 4):
            n_SO = int(line.split("//")[0])

        # read number of CSs
        elif (index == 5):
            n_CS = int(line.split("//")[0])

        # read Initial position of haulers
        elif (index == 6):
            t = line.split("//")[0].split("-")
            for i in range(n_Hauler):
                cordinate = t[i].replace("[", "").replace("]", "")
                x = []
                for j in range(2):
                    x.append(int(cordinate.split(",")[j]))
                init_haulers.append(tuple(x))

        # read position of LPs
        elif (index == 7):
            t = line.split("//")[0].split("-")
            for i in range(n_LP):
                cordinate = t[i].replace("[", "").replace("]", "")
                x = []
                for j in range(2):
                    x.append(int(cordinate.split(",")[j]))
                LP_positions.append(tuple(x))

        # read position of ULPs
        elif (index == 8):
            t = line.split("//")[0].split("-")
            for i in range(n_ULP):
                cordinate = t[i].replace("[", "").replace("]", "")
                x = []
                for j in range(2):
                    x.append(int(cordinate.split(",")[j]))
                ULP_positions.append(tuple(x))

        # read position of SOs
        elif (index == 9):
            t = line.split("//")[0].split("-")
            for i in range(n_SO):
                cordinate = t[i].replace("[", "").replace("]", "")
                x = []
                for j in range(2):
                    x.append(int(cordinate.split(",")[j]))
                SO_positions.append(tuple(x))
        # read position of CSs
        elif (index == 10):
            t = line.split("//")[0].split("-")
            for i in range(n_CS):
                cordinate = t[i].replace("[", "").replace("]", "")
                x = []
                for j in range(2):
                    x.append(int(cordinate.split(",")[j]))
                CS_positions.append(tuple(x))
        # read battery capacity
        elif (index == 11):
            if (line.split("//")[0] != '\t'):
                battery_capacity = int(line.split("//")[0])

        # read initial energy
        elif (index == 12):
            if (line.split("//")[0] != '\t'):
                initial_energy = int(line.split("//")[0])
        index += 1
    return init_haulers, LP_positions, ULP_positions, SO_positions, CS_positions, battery_capacity, initial_energy


def read_mission(file, LP_pos, ULP_pos):
    f = open(file, "r")
    lines = f.readlines()

    mission_strings = []

    mission = []

    for line in lines:
        temp = line.split("\t//")[0].split(",")
        mission_strings.append(temp)
        temp_list = []
        for t in temp:
            if t.startswith('U'):
                tn = t.split('U')
                temp_list.append(ULP_pos[int(tn[1]) - 1])
            else:
                tn = t.split('L')
                temp_list.append(LP_pos[int(tn[1]) - 1])
        mission.append(temp_list)

    return mission, mission_strings


def write_output(makespan, completion_times, exec_time, file, haulers):
    f = open(file, "w")
    f.write("//Quantitative values\n")
    f.write(str(makespan) + "\t//Makespan" + "\n")
    for i, c in enumerate(completion_times):
        f.write(str(c) + "\t//Mission completion time hauler " + str(i + 1) + "\n")
    f.write(str(exec_time) + "\t//Application execution time (in millisecond)" + "\n")
    f.write("//Path to the final points\n")
    print_haulers_history(f, haulers, makespan)
    f.close()


def print_haulers_history(file, haulers, makespan):
    for i in range(makespan + 1):
        file.write(f'{i},')
        for j in range(len(haulers)):
            move = haulers[j].get_move_i(i)
            if j == len(haulers) - 1:
                file.write(f'[{move[0]},{move[1]}]')
            else:
                file.write(f'[{move[0]} ,{move[1]}],')
        file.write('\n')


class Hauler:
    def __init__(self, i, init_pos, mission: list, graph: dict, battery_capacity, initial_energy, charging_stations):
        self.move_q = deque()
        self.history = [init_pos]
        self.cur_pos = init_pos
        self.mission = deque(mission)  # Queue of addresses for the hauler to go to in order
        self.graph = graph
        self.finished = False
        self.finished_at = 0
        self.index = i
        self.charging_tup = (False, 0)
        self.charging_flag = True  # True if can be charged still, else has already charged at the cs
        self.energy = initial_energy
        self.battery_capacity = battery_capacity
        self.cs_list = charging_stations

    def is_charging(self):
        charging, time_charging = self.charging_tup
        if charging:
            return True
        return False

    def charge(self):
        charging, time_charging = self.charging_tup
        if time_charging < 5:
            self.charging_tup = (True, time_charging + 1)
            if self.charging_tup[1] == 5:
                self.energy = self.battery_capacity
                self.charging_tup = (False, 0)
                self.charging_flag = False

    def construct_step_queue(self, prev, end_node):
        v = end_node
        while v is not None:
            self.move_q.appendleft(v)
            v = prev[v]
        self.move_q.popleft()  # because right before v is None we add the current position of the hauler to the queue

    # Returns all steps as the shortest path that passes through a CS (clearly not optimal)
    # Maybe test whether we can reach the next step in the mission without visiting a CS. If not, take the best possible route?

    def move(self, step, important_nodes_shortest_paths, important_nodes_distances):
        if len(self.move_q) > 0:
            if self.cur_pos in self.cs_list:  # If at a CS
                if self.energy <= (0.75 * self.battery_capacity):
                    if self.charging_flag:
                        self.charge()
                        self.history.append(self.cur_pos)
                        return

            cur_move = self.move_q.popleft()
            self.energy -= 50
            self.history.append(cur_move)
            self.cur_pos = cur_move
            self.charging_flag = True

        elif len(self.mission) > 0:
            next_lp_ulp = self.mission.popleft()
            cs = self.find_least_detour_charging_station(next_lp_ulp, important_nodes_shortest_paths,
                                                         important_nodes_distances)
            self.construct_step_queue(important_nodes_shortest_paths[cs], next_lp_ulp)
            self.construct_step_queue(important_nodes_shortest_paths[self.cur_pos], cs)

            self.move(step, important_nodes_shortest_paths, important_nodes_distances)
        else:
            self.finished = True
            self.finished_at = step

    def get_move_i(self, i):
        if i >= len(self.history):
            return self.cur_pos
        return self.history[i]

    def compute_shortest_path(self, start_node=None):
        """
        Uses Dijkstra's algorithm to compute the shortest path from the start_node to all nodes.
        """

        if not start_node:
            start_node = self.cur_pos

        dist = {v: float("inf") for v in self.graph.keys()}
        dist[start_node] = 0
        prev = {v: None for v in self.graph.keys()}

        priority_queue = [(0, start_node)]
        heapq.heapify(priority_queue)
        visited = set()

        while priority_queue:
            cur_dist, v = heapq.heappop(priority_queue)

            if v in visited:
                continue
            visited.add(v)
            for u, w in self.graph[v]:
                test_dist = cur_dist + w
                if test_dist < dist[u]:
                    dist[u] = test_dist
                    prev[u] = v
                    heapq.heappush(priority_queue, (test_dist, u))

        return prev, dist

    def find_least_detour_charging_station(self, end_node, important_nodes_shortest_paths, important_nodes_distances):
        """
        Finds the least detour REACHABLE charging station (the one that minimizes the route to the end node).
        """
        cur_cs = None
        cur_dist = float('inf')
        for cs in self.cs_list:
            prev_1, dist_1, prev_2, dist_2 = (None, ) * 4

            if important_nodes_shortest_paths[self.cur_pos]:
                dist_1 = important_nodes_distances[self.cur_pos]
            else:
                prev_1, dist_1 = self.compute_shortest_path()
                important_nodes_shortest_paths[self.cur_pos] = prev_1
                important_nodes_distances[self.cur_pos] = dist_1

            if important_nodes_shortest_paths[cs]:
                dist_2 = important_nodes_distances[cs]
            else:
                prev_2, dist_2 = self.compute_shortest_path(cs)
                important_nodes_shortest_paths[cs] = prev_2
                important_nodes_distances[cs] = dist_2

            if ((dist_1[cs] + dist_2[end_node]) < cur_dist) and ((self.energy - (dist_1[cs]*50)) > 0):
                cur_cs = cs
                cur_dist = dist_1[cs] + dist_2[end_node]
        return cur_cs


def create_graph(m, n, static_objects: [(int, int)]):
    """
    This function creates a graph to model the problem
    by converting the grid into a graph and
    initializing the adjacency list for each node
    taking into account their weight.

    To follow the notation used by the PDF, we use x for the columns and y for the rows.
    """

    so_pos = set(static_objects)

    rows, cols = m, n

    graph = defaultdict(lambda: [])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for y in range(rows):
        for x in range(cols):
            temp_y, temp_x = y + 1, x + 1  # Correcting with +1 because we start at 1 on PDF
            if (temp_y, temp_x) in so_pos:
                continue
            for dy, dx in directions:
                ny, nx = temp_y + dy, temp_x + dx
                if (1 <= ny < rows + 1) and (
                        1 <= nx < cols + 1):  # This is done so the movement cannot be out of the grid
                    if (ny, nx) not in so_pos:
                        graph[(temp_y, temp_x)].append(
                            ((ny, nx), 1))  # Path from (1,1) to (1,2) is coded as (1,1): {(1, (1,2))}
    return graph


def main():
    """
    Replace your input files location and name.
    You can also use command line argument to get input files name.

    functions:
        read_config     -> input: config file name
                        -> output: all variables in config file

        read_mission    -> input: mission file name
                        -> output: mission for each hauler

        write_output    -> input: scenario makespan, completion time of each hauler, elapsed time of program,
                                     path to the final points, output file name
                        -> output: void

    """
    folder = ''
    config_file = folder + "config.txt"
    mission_file = folder + "mission.txt"
    output_file = folder + "output.txt"

    init_haulers, LP_positions, ULP_positions, SO_positions, CS_positions, battery_capacity, initial_energy = read_config(
        config_file)

    mission, mission_strings = read_mission(mission_file, LP_positions, ULP_positions)

    start = time.time()
    #################################

    n, m = 12, 12

    working_haulers = []
    finished_haulers = []

    # Each LP/ULP may have a path to other LPs or ULPs -- We store this in the dict below
    nodes_shortest_paths = defaultdict(dict)
    nodes_shortest_distances = defaultdict(dict)

    graph = create_graph(m, n, SO_positions)

    for i in range(len(init_haulers)):
        working_haulers.append(Hauler(i, init_haulers[i], mission[i], graph, battery_capacity, initial_energy, CS_positions))

    mission_time = 0

    while working_haulers:
        mission_time += 1
        for h in working_haulers:
            h.move(mission_time, important_nodes_shortest_paths=nodes_shortest_paths, important_nodes_distances=nodes_shortest_distances)
            if h.finished:
                finished_haulers.append(h)
                working_haulers.remove(h)

    final_step = mission_time - 1  # e.g. mission finished at 32 means the final step of the mission was 31

    #################################
    end = time.time()
    elapsed_time = int((end - start) * 1000)

    finished_haulers.sort(key=lambda x: x.index)

    completion_times = [h.finished_at for h in finished_haulers]

    # call the writing function here
    # example:
    write_output(final_step, completion_times, elapsed_time, output_file, finished_haulers)


if __name__ == "__main__":
    main()

