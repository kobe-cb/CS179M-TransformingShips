import copy
from queue import PriorityQueue

# -1 means NAN, meaning the space does not exist in the ship
# test_state = (
#     ('*', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 'Dog', -1, -1, -1, -1, -1, -1, -1, -1, -1),
#     (-1, -1, 'Cat', -1, -1, -1, -1, -1, -1, -1, -1, -1)
# )
# test_state = (
#     ('*', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
#     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
# )
actions = [('UNLOAD', 'Ewe')]
f = open('path.txt', 'w')


class Node:
    def __init__(self, ship, container_to_unload, container_to_load):
        self.ship = ship
        self.heuristic = 0  # h(n)
        self.depth = 0  # g(n), would represent the number of moves performed so far
        self.containers_to_unload = container_to_unload
        self.containers_to_load = container_to_load
        self.time = 0

    # Implemented so the priorityqueue can compare objects and automatically precede with the node with the lowest cost
    # https://stackoverflow.com/questions/9292415/i-notice-i-cannot-use-priorityqueue-for-objects
    def __lt__(self, other):
        return (self.depth + self.heuristic) < (other.depth + other.heuristic)


# Driver FUNCTION
def main(actionsQueued, manifestFile, pathOnly):
    # ship = test_state
    ship = get_ship(manifestFile)
    print_ship(ship)
    if pathOnly:
        print_ship(ship)
        balance_path(ship, actionsQueued)
    else:
        containers_to_unload, containers_to_load = get_goal_state(actionsQueued, ship)
        if not containers_to_unload and not containers_to_load:
            print('Empty ship and nothing to load. Closing program!')
            return 0
        search_ship(ship, containers_to_unload, containers_to_load)
    f.close()
    return 0


def search_ship(ship, unloaded, loaded):
    curr_ship = Node(ship, unloaded, loaded)
    if len(curr_ship.containers_to_unload) == 0:
        if len(curr_ship.containers_to_load) != 0:
            load = list(curr_ship.containers_to_load).pop()
        else:
            load = False
        curr_ship.heuristic = a_star_manhattan(curr_ship.ship, False,
                                               curr_ship.containers_to_unload, curr_ship.depth, load)
    else:
        target = get_target(curr_ship)
        curr_ship.heuristic = a_star_manhattan(curr_ship.ship, target,
                                               curr_ship.containers_to_unload, curr_ship.depth, False)

    curr_ship.time = curr_ship.time + curr_ship.heuristic
    working_queue = PriorityQueue()
    repeated_states = set()
    max_queue_size = 0
    expanded_nodes = 0
    working_queue.put(curr_ship)
    repeated_states.add(curr_ship.ship)
    max_queue_size += 1
    while working_queue.qsize() != 0:
        max_queue_size = max(working_queue.qsize(),
                             max_queue_size)
        curr_ship = working_queue.get()
        if len(curr_ship.containers_to_unload) == 0 and len(curr_ship.containers_to_load) == 0 and curr_ship.ship[0][
            0] == '*':
            print("Ship loaded and unloaded! Total time to move containers is " + str(curr_ship.time) + " minutes.")
            f.write('Final time for all moves is: ' + str(curr_ship.time) + ' minutes.' + '\n' + '\n')
            print_ship(curr_ship.ship)
            break
        if curr_ship.depth != 0:
            curr_ship.time += curr_ship.heuristic
        if curr_ship.ship[0][0] == '*' and len(curr_ship.containers_to_unload) == 0:
            curr_ship.time += 4
        expanded_nodes += 1
        print('The best state to expand with a g(n) = ' + str(curr_ship.depth) + ' and h(n) = ' + str(
            curr_ship.heuristic) + ' is...')
        print_ship(curr_ship.ship)
        target = get_target(curr_ship)
        node_expansion(curr_ship, target, repeated_states, working_queue)
    else:
        print('No solution found. Exiting the program.')
        exit(0)


def node_expansion(ship, target, repeated_states, working_queue):
    if len(ship.containers_to_load) == 0:
        load = False
    else:
        load = list(ship.containers_to_load).pop()
    if len(ship.containers_to_unload) == 0:
        target = False
    else:
        load = False
    move_tile(ship, repeated_states, working_queue, target, load)


def move_tile(ship, repeated_states, working_queue, target, load):
    # print(row, column)
    # if ship.depth % 2 != 0:
    #     print("Moving " + str(ship.ship[row][column]))
    child = copy.deepcopy(ship.ship)
    child = convert_to_list(child)
    check = len(ship.containers_to_unload)
    one_check = False
    # Distinguish between loading a container and unloading
    if not target:
        if len(ship.containers_to_load) == 0:
            print('All containers are loaded!')
        else:
            print('Containers to load are: ' + str(ship.containers_to_load))
        valid_load(child, ship.depth, load, False)
        if ship.depth % 2 == 0:
            if len(ship.containers_to_load) != 0:
                ship.containers_to_load.remove(load)
    else:
        print('Containers to unload are: ' + str(ship.containers_to_unload))
        if target not in ship.containers_to_unload:
            child = valid_position(child, target, ship.depth, False)
        else:
            child = move_out(child, target, ship.depth, ship.heuristic)
            if ship.depth % 2 != 0:
                if len(ship.containers_to_unload) != 0:
                    ship.containers_to_unload.remove(target)
            # Edge case to mark in the file an unload after the last container got unloaded
            if len(ship.containers_to_unload) == 0:
                one_check = True
    child = convert_to_tuple(child)
    if child not in repeated_states:
        repeated_states.add(child)
        child_node = Node(child, ship.containers_to_unload, ship.containers_to_load)
        child_node.depth = ship.depth + 1
        # Depth checks done to mark moves for when the container itself is moved to a location rather than the crane
        if target:
            if check != len(ship.containers_to_unload) and ship.depth % 2 != 0:
                # print('Calculating moving crate to the ship itself')
                child_node.time += 4
        target = get_target(child_node)
        child_node.heuristic = a_star_manhattan(child_node.ship, target,
                                                child_node.containers_to_unload, child_node.depth, load)
        child_node.time = ship.time + child_node.time
        print('Current time to move container into the ship is ' + str(child_node.time) + ' minutes.')
        if ship.depth % 2 != 0 and len(ship.containers_to_unload) != 0:
            f.write('Cumulative time for moves so far is: ' + str(child_node.time) + ' minutes.' + '\n' + '\n')
        elif ship.depth % 2 != 0 and len(ship.containers_to_unload) == 0 and one_check:
            f.write('Cumulative time for moves so far is: ' + str(child_node.time) + ' minutes.' + '\n' + '\n')
        elif ship.depth % 2 == 0 and len(child_node.containers_to_unload) == 0:
            f.write('Cumulative time for moves so far is: ' + str(child_node.time) + ' minutes.' + '\n' + '\n')
        working_queue.put(child_node)


# HELPER FUNCTIONS
def convert_to_list(ship):  # Convert tuple to a list for modifying the ship
    temp_list = []
    for row in range(len(ship)):
        temp_list.append(list(ship[row]))
    temp_list = tuple(temp_list)
    return temp_list


def convert_to_tuple(ship):  # Convert back to a tuple
    tuple_list = []
    for row in range(len(ship)):
        temp_tuple = tuple(ship[row])
        tuple_list.append(temp_tuple)
    tuple_list = tuple(tuple_list)
    return tuple_list


def print_ship(ship):
    # Easier to see the ship state when swapping the ship items
    for row in ship:
        row_str = ""
        for element in row:
            row_str += "{:<5}".format(str(element))
        print(row_str)
    print()


def get_ship(manifestName):
    # Interprets the manifest file and converts it to a usable embedded tuple for use
    ship_coordinates = []
    ship_containers = []
    with open(manifestName, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            coords = [0, 0]
            coords[0] = abs(int(parts[0].strip("[")) - 9)
            coords[1] = int(parts[1].strip("]")) - 1
            name = parts[3].strip()
            ship_coordinates.append(coords)
            ship_containers.append(name)

    num_rows = max(coord[0] for coord in ship_coordinates) + 1
    num_cols = max(coord[1] for coord in ship_coordinates) + 1

    nested_list = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    for coord, item in zip(ship_coordinates, ship_containers):
        row, col = coord
        if item == 'UNUSED':
            item = 0
        elif item == 'NAN':
            item = -1
        nested_list[row][col] = item
    nested_list[0][0] = '*'
    final_ship = convert_to_tuple(nested_list)
    return final_ship


def get_goal_state(actionQueue, ship):
    # Calculate goal state by adding the action queue from the UI to the code itself
    # actionQueue = [('UNLOAD', 'Pig'), ('LOAD', 'Tail', '123'), ('UNLOAD', 'Cat'), ('UNLOAD', 'Dog')]
    unloadItems = []
    loadItems = []
    for item in actionQueue:
        if item[0] == 'UNLOAD':
            unloadItems.append(item[1])
        elif item[0] == 'LOAD':
            loadItems.append(item[1])
    curr_ship = Node(ship, unloadItems, loadItems)
    target = get_target(curr_ship)
    if target == 0 and len(unloadItems) != 0 and len(loadItems) == 0:
        return False, False
    elif target == 0 and len(loadItems) != 0:
        return [], loadItems
    else:
        return unloadItems, loadItems


def get_target(ship):
    # Calculate the container that will be unloaded Manhattan Distance
    target = 0
    for row in range(len(ship.ship)):
        for column in range(len(ship.ship)):
            if ship.ship[row][column] in ship.containers_to_unload:
                target = container_above(ship, row, column)
                print("Target is " + str(target))
                print(row, column)
                return target
    return target


def get_crane_pos(ship):
    # Get the position of the crane
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == '*' or ship[row][column] == '**':
                return row, column


def container_above(ship, targetRow, targetCol):
    # Check for containers above so that the target is the one with the shortest Manhattan Distance
    valid = False
    if ship.ship[targetRow - 1][targetCol] == 0:
        return ship.ship[targetRow][targetCol]
    while not valid:
        if ship.ship[targetRow - 1][targetCol] != 0 and ship.ship[targetRow - 1][targetCol] != '*' and \
                ship.ship[targetRow - 1][targetCol] != '**':
            targetRow = targetRow - 1
        else:
            valid = True
    return ship.ship[targetRow][targetCol]


def move_out(ship, target, depth, heuristic):
    goalRow = 0
    goalColumn = 0
    found = False
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == target and not found:
                goalRow = row
                goalColumn = column
                found = True
                break
    # print('Current depth is ' + str(depth))

    if depth % 2 == 0:
        # print("Crane picking up")
        # print('Moving to the target crate')
        craneRow, craneCol = get_crane_pos(ship)
        ship[goalRow - 1][goalColumn] = ship[craneRow][craneCol]
        ship[craneRow][craneCol] = 0
        return ship
    else:
        # Moving the container off the ship
        # print('Moving out of the target crate')
        f.write('Move container ' + str(ship[goalRow][goalColumn]) + ' ' + str(
            [abs(goalRow - 9), goalColumn + 1]) + ' to ' + str([9, 1]) + ' (off the ship)' + '\n')
        craneRow, craneCol = get_crane_pos(ship)
        ship[goalRow][goalColumn] = 0
        ship[craneRow][craneCol] = 0
        ship[0][0] = '*'
        return ship


def balance_path(ship, path_file):
    # Calculate a readable path file for the balance algorithm
    ship_position1 = []
    ship_position2 = []
    count = 0
    with open('Instructions.txt', "r") as file:
        for line in file:
            if count == 0:
                count += 1
                time = line
            else:
                coords = [0, 0]
                coords2 = [0, 0]
                parts = line.strip().split(" to ")
                parts[0] = parts[0].strip('Move ')
                coords_stored = parts[0].strip('()').split(',')
                coords = [int(coords_stored[0]), int(coords_stored[1])]
                coords_stored = parts[1].strip('()').split(',')
                coords2 = [int(coords_stored[0]), int(coords_stored[1])]
                ship_position1.append(coords)
                ship_position2.append(coords2)
    time = time.strip('Estimated cost = ')
    for pos in range(len(ship_position1)):
        print(ship_position1[pos][0])
        validRow = abs(ship_position1[pos][0] - 9)
        validCol = abs(ship_position1[pos][1] - 1)
        goalRow = abs(ship_position2[pos][0] - 9)
        goalColumn = abs(ship_position2[pos][1] - 1)
        f.write('Move container ' + str(ship[validRow][validCol]) + ' ' + str(ship_position1[pos]) + ' to ' + str(
            ship_position2[pos]) + '\n' + '\n')
        ship = convert_to_list(ship)
        temp = ship[goalRow][goalColumn]
        ship[goalRow][goalColumn] = ship[validRow][validCol]
        ship[validRow][validCol] = temp
        ship = convert_to_tuple(ship)
    f.write('Final time for all moves is: ' + str(time))


# HEURISTIC FUNCTIONS


def a_star_manhattan(ship, target, unload, depth, load):
    # Calculate Manhattan Distance based on whether a crane is loading/unloading or moving/picking up a container
    # print(target)
    if not target:
        return valid_load(ship, depth, load, True)
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == target:
                if target in unload:
                    if depth != 0 and depth % 2 == 0:
                        print('Found the unloaded container')
                        return valid_position(ship, target, depth, True)
                    # print('Distance is ' + str(abs(row - 0) + abs(column - 0)))
                    return abs(row - 0) + abs(column - 0) - 1
                elif depth == 0:
                    # print('Distance is ' + str(abs(row - 0) + abs(column - 0) - 1))
                    return abs(row - 0) + abs(column - 0) - 1
                else:
                    # print('Not the unloaded container')
                    return valid_position(ship, target, depth, True)


def valid_position(ship, target, depth, distance):
    # Calculates a proper distance between two coordinates and swaps items to reposition containers after being moved
    goalRow = 0
    goalColumn = 0
    valid_coordinates = []
    shortest_distance = []
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == target:
                goalRow = row
                goalColumn = column
    # print('Current depth is ' + str(depth))
    if depth % 2 == 0:
        # print("Crane picking up")
        craneRow, craneCol = get_crane_pos(ship)
        # print(craneRow)
        # print(craneCol)
        if distance:
            # print('Distance is ' + str(abs((goalRow - 1) - craneRow) + abs(goalColumn - craneCol)))
            return abs((goalRow - 1) - craneRow) + abs(goalColumn - craneCol)
        if goalRow == 1 and goalColumn == 0:
            ship[goalRow - 1][goalColumn] = ship[craneRow][craneCol]
            ship[craneRow][craneCol] = '**'
            return ship
        else:
            ship[goalRow - 1][goalColumn] = ship[craneRow][craneCol]
            ship[craneRow][craneCol] = 0
            return ship
    else:
        # print("Crane moving column")
        for row in range(len(ship)):
            for column in range(len(ship)):
                if ship[row][column] == 0:
                    if row != 0:
                        if row < 7:
                            if ship[row + 1][column] != 0 and ship[row + 1][column] != target and ship[row + 1][
                                column] != \
                                    ship[row + 1][goalColumn]:
                                valid_coordinates.append([row, column])
                            if ship[row + 1][column] == - 1:
                                valid_coordinates.append([row, column])
                        elif row == 7:
                            if ship[row + 1][column] != 0 and ship[row + 1][column] != ship[row + 1][goalColumn]:
                                valid_coordinates.append([row, column])
                            if ship[row + 1][column] == 0 and ship[row + 1][column] != ship[row + 1][goalColumn]:
                                valid_coordinates.append([row + 1, column])
                            if ship[row + 1][column] == - 1:
                                valid_coordinates.append([row, column])
    for coordinates in valid_coordinates:
        shortest_distance.append((abs(goalRow - coordinates[0]) + abs(goalColumn - coordinates[1])))
    if distance:
        # print('Shortest distance is: ' + str(min(shortest_distance)))
        return min(shortest_distance)
    validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
    validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
    craneRow, craneCol = get_crane_pos(ship)

    temp = ship[goalRow][goalColumn]
    ship[goalRow][goalColumn] = ship[validRow][validColumn]
    ship[validRow][validColumn] = temp
    ship[validRow - 1][validColumn] = '*'
    ship[craneRow][craneCol] = 0
    f.write('Move container ' + str(ship[validRow][validColumn]) + ' ' + str(
        [abs(validRow - 9), validColumn + 1]) + ' to ' + str(
        [abs(goalRow - 9), goalColumn + 1]) + '\n')
    return ship


def valid_load(ship, depth, load, distance):
    # Calculates a proper distance between two coordinates and swaps items to reposition containers after being moved for load
    valid_coordinates = []
    shortest_distance = []
    craneRow, craneCol = get_crane_pos(ship)
    invalidColumn = 20
    if depth % 2 != 0:
        if distance:
            return abs(craneRow - 0) + abs(craneCol - 0) - 1
        ship[0][0] = '*'
        ship[craneRow][craneCol] = 0
        return ship
    # print('Getting valid positions')
    for row in range(len(ship)):
        for column in range(len(ship)):
            if row == 1:
                if ship[row][column] != 0 and ship[row][column] != '*' and row != 0 and ship[row][column] != '**':
                    invalidColumn = column
            else:
                if ship[row][column] != 0 and ship[row][column] != '*' and row != 0 and ship[row][
                    column] != '**' and column != invalidColumn and ship[row - 1][column] == 0:
                    valid_coordinates.append([row - 1, column])
                elif ship[row][column] == -1:
                    if ship[row - 1][column] == 0 and row != 1:
                        valid_coordinates.append([row - 1, column])
                elif row == 8:
                    if ship[row][column] == 0:
                        valid_coordinates.append([row, column])
    for coordinates in valid_coordinates:
        shortest_distance.append((abs(craneRow - coordinates[0]) + abs(craneCol - coordinates[1])))
    if distance:
        if len(shortest_distance) == 0:
            return 0
        return min(shortest_distance) - 1
    validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
    validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
    ship[craneRow][craneCol] = 0
    ship[validRow - 1][validColumn] = '*'
    ship[validRow][validColumn] = load
    f.write('Load container ' + str(ship[validRow][validColumn]) + ' to ' + str(
        [abs(validRow - 9), validColumn + 1]) + '\n')
    return ship

main(actions, 'ShipCase4.txt', False)


# MAJORTIY OF THIS ALGORITHM WAS BASED ON THE 8-PUZZLE A* SEARCH FROM CS170: ALL SOURCES BELOW
# Helped with the implementation of a depth for picking up the container, and actually moving the container: https://www.dropbox.com/s/k0eo95kixkyln2p/Thoughts%20on%20N-column%20Container%20Search.pptx?dl=0
# https://raspberrypi.stackexchange.com/questions/15613/stop-program-after-a-period-of-time, Done in case a search depth takes way too long to finish
# Using priority queue for the node frontier: https://docs.python.org/3/library/queue.html
# HEAVILY inspired from psuedocode in: https://www.dropbox.com/sh/cp90q8nlk8od4cw/AADK4L3qOh-OJtFzdi_8Moaka?dl=0&preview=Project_1_The_Eight_Puzzle_CS_170_2022.pdf
# INSPIRED BY https://plainenglish.io/blog/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9f
# Implemented so the priorityqueue can compare objects and automatically preceed with the node with the lowest cost
# https://stackoverflow.com/questions/9292415/i-notice-i-cannot-use-priorityqueue-for-objects
# https://cdn.codespeedy.com/wp-content/uploads/2020/03/manhattan.jpg
# Based off this: https://ai.stackexchange.com/questions/7555/how-do-i-keep-track-of-already-visited-states-in-breadth-first-search
