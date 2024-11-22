#!/usr/bin/env python3
import time
import heapq
from collections import defaultdict, deque


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
    batery_capacity = 0
    initial_energy = 0

    # for following the line number
    index = 1
    for line in lines:
        # read number of Haulers
        if(index == 1):
            n_Hauler = int(line.split("//")[0])

        # read number of LPs
        elif(index == 2):
            n_LP = int(line.split("//")[0])

        # read number of ULPs
        elif(index == 3):
            n_ULP = int(line.split("//")[0])

        # read number of SOs
        elif(index == 4):
            n_SO = int(line.split("//")[0])

        # read number of CSs
        elif(index == 5):
            n_CS = int(line.split("//")[0])

        # read Initial position of haulers
        elif(index == 6):
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
        elif(index == 11):
            if(line.split("//")[0] != '\t'):
                batery_capacity = int(line.split("//")[0])

        # read initial energy
        elif(index == 12):
            if(line.split("//")[0] != '\t'):
                initial_energy = int(line.split("//")[0])
        index += 1
    return init_haulers, LP_positions, ULP_positions, SO_positions, CS_positions, batery_capacity, initial_energy


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
                temp_list.append(ULP_pos[int(tn[1])-1])
            else:
                tn = t.split('L')
                temp_list.append(LP_pos[int(tn[1])-1])
        mission.append(temp_list)

    return mission, mission_strings


def write_output(makespan, completion_times, exec_time, file, haulers):
    f = open(file, "w")
    f.write("//Quantitative values\n")
    f.write(str(makespan)+"\t//Makespan" + "\n")
    for i, c in enumerate(completion_times):
        f.write(str(c)+"\t//Mission completion time hauler " + str(i+1)+"\n")
    f.write(str(exec_time)+"\t//Application execution time (in millisecond)"+"\n")
    f.write("// Position of each hauler for every (discrete) time step\n")
    print_haulers_history(f, haulers, makespan)
    f.close()


def print_haulers_history(file, haulers, makespan):
    for i in range(makespan-1):
        file.write(f'{i} ,')
        for j in range(len(haulers)):
            move = haulers[j].get_move_i(i)
            if j == len(haulers)-1:
                file.write(f'[{move[0]} ,{move[1]}]')
            else:
                file.write(f'[{move[0]} ,{move[1]}] , ')
        file.write('\n')


class Hauler:
    def __init__(self, i, init_pos, mission: list, graph: dict):
        self.move_q = deque()
        self.history = []
        self.cur_pos = init_pos
        self.mission = deque(mission)  # List of addresses for the hauler to go to in order
        self.graph = graph
        self.finished = False
        self.finished_at = 0
        self.index = i

    def construct_step_queue(self, prev, end_node):
        v = end_node
        while v is not None:
            self.move_q.appendleft(v)
            v = prev[v]
        self.move_q.popleft()
        print('new mission:', self.move_q)

    def move(self, step):
        if len(self.move_q) > 0:
            cur_move = self.move_q.popleft()
            self.history.append(cur_move)
            self.cur_pos = cur_move
        elif len(self.mission) > 0:
            # Think about how to keep haulers working while calculating route
            prev, end_node = self.compute_shortest_path(self.mission.popleft())
            self.construct_step_queue(prev, end_node)
            self.move(step)
        else:
            self.finished = True
            self.finished_at = step

    def get_move_i(self, i):
        if i >= len(self.history):
            return self.cur_pos
        return self.history[i]

    def compute_shortest_path(self, end_node: (int, int)):
        """
        Uses Dijkstra's algorithm to compute the shortest path from the start_node to the end_node.
        """

        dist = {v: float("inf") for v in self.graph.keys()}
        dist[self.cur_pos] = 0
        prev = {v: None for v in self.graph.keys()}

        priority_queue = [(0, self.cur_pos)]
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

        return prev, end_node


def get_grid(static_objects, n, m):
    """
    We use this function to create a grid where the SOs have +infinite weight and all others have 1
    """
    grid = []
    for i in range(m):
        grid.append([1]*n)
    return grid


def create_graph(grid, static_objects: [(int, int)]):
    """
    This function creates a graph to model the problem
    by converting the grid into a graph and
    initializing the adjacency list for each node
    taking into account their weight.

    To follow the notation used by the PDF, we use x for the columns and y for the rows.
    """

    rows, cols = len(grid), len(grid[0])

    graph = defaultdict(lambda: [])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for y in range(rows):
        for x in range(cols):
            temp_y, temp_x = y + 1, x + 1  # Correcting with +1 because we start at 1 on PDF
            if (temp_y, temp_x) in static_objects:
                continue
            for dy, dx in directions:
                ny, nx = temp_y+dy, temp_x+dx
                if (1 <= ny < rows+1) and (1 <= nx < cols+1):  # This is done so the movement cannot be out of the grid
                    if (ny, nx) not in static_objects:
                        weight = grid[ny-1][nx-1]  # Correcting only to get weight
                        graph[(temp_y, temp_x)].append(((ny, nx), weight))  # Path from (1,1) to (1,2) is coded as (1,1): {(1, (1,2))}
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
    folder = 'example/'
    config_file = folder + "config.txt"
    mission_file = folder + "mission.txt"
    output_file = folder + "output.txt"

    init_haulers, LP_positions, ULP_positions, SO_positions, CS_positions, battery_capacity, initial_energy = read_config(
        config_file)

    mission, mission_strings = read_mission(mission_file, LP_positions, ULP_positions)

    for m in range(len(mission)):
        for i in range(len(mission[m])):
            print(mission_strings[m][i], mission[m][i])

    start = time.time()
    #################################

    n, m = 12, 12

    grid = get_grid(SO_positions, n, m)

    working_haulers = []
    finished_haulers = []

    graph = create_graph(grid, SO_positions)

    for i in range(len(init_haulers)):
        working_haulers.append(Hauler(i, init_haulers[i], mission[i], graph))

    mission_step = 0

    while working_haulers:
        for h in working_haulers:
            h.move(mission_step)
            if h.finished:
                finished_haulers.append(h)
                working_haulers.remove(h)
        mission_step += 1

    print('time:', mission_step)

    #################################
    end = time.time()
    elapsed_time = int((end - start)*1000)

    finished_haulers.sort(key=lambda x: x.index)

    completion_times = [h.finished_at for h in finished_haulers]
    
    # call the writing function here
    # example: 
    write_output(mission_step, completion_times, elapsed_time, output_file, finished_haulers)



if __name__ == "__main__":
    main()
