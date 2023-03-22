import copy
from queue import PriorityQueue

# -1 means NAN, meaning the space does not exist in the ship

containers_to_unload = set()
containers_to_unload.add("Hen")
containers_to_unload.add("Pig")
containers_to_load = set()
containers_to_load.add('Nat')
containers_to_load.add('Rat')



class Node:
    def __init__(self, ship, container_to_unload, container_to_load):
        self.ship = ship
        self.path = []  # Changed to a list as it saves a LOT of time adding to a list than a single long string
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
def main():
    ship = get_ship()
    get_goal_state()
    search_ship(ship)
    return 0


def search_ship(ship):
    curr_ship = Node(ship, containers_to_unload, containers_to_load)
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
    curr_ship.path += [curr_ship.ship]
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
            print_ship(curr_ship.ship)
            break
        if curr_ship.depth != 0:
            curr_ship.time += curr_ship.heuristic
        if curr_ship.ship[0][0] == '*' and len(curr_ship.containers_to_unload) == 0:
            curr_ship.time += 8
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
    if len(containers_to_unload) == 0:
        target = False
    else:
        load = False
    move_tile(ship, repeated_states, working_queue, target, load)


def move_tile(ship, repeated_states, working_queue, target, load):
    # print(row, column)
    # if ship.depth % 2 != 0:
    #     print("Moving " + str(ship.ship[row][column]))
    path = []
    child = copy.deepcopy(ship.ship)
    # path += ['Unloading container ' + str(ship.ship[row][column])]
    child = convert_to_list(child)
    check = len(ship.containers_to_unload)
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
            child = move_out(child, target, ship.depth)
            if ship.depth % 2 != 0:
                if len(ship.containers_to_unload) != 0:
                    ship.containers_to_unload.remove(target)
    child = convert_to_tuple(child)
    if child not in repeated_states:
        repeated_states.add(child)
        child_node = Node(child, ship.containers_to_unload, ship.containers_to_load)
        child_node.path += ship.path
        child_node.path += path
        child_node.depth = ship.depth + 1
        if target:
            if check != len(ship.containers_to_unload) and ship.depth % 2 != 0:
                print('Calculating moving crate to the ship itself')
                child_node.time += 4
        target = get_target(child_node)
        child_node.heuristic = a_star_manhattan(child_node.ship, target,
                                                child_node.containers_to_unload, child_node.depth, load)
        child_node.time = ship.time + child_node.time
        print('Current time to move container into the ship is ' + str(child_node.time) + ' minutes')
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
    for row in ship:
        row_str = ""
        for element in row:
            row_str += "{:<5}".format(str(element))
        print(row_str)
    print()


def get_ship():
    ship_coordinates = []
    ship_containers = []
    with open("ShipCase5.txt", "r") as file:
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


def get_goal_state():
    # Calculate goal state by setting the unloaded containers to 0
    return 0


def get_target(ship):
    # Calculate the container that will be unloaded Manhattan Distance
    target = 0
    for row in range(len(ship.ship)):
        for column in range(len(ship.ship)):
            if ship.ship[row][column] in ship.containers_to_unload:
                target = container_above(ship, row, column)
                # print("Target is " + str(target))
                return target
    return target


def get_crane_pos(ship):
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == '*' or ship[row][column] == '**':
                return row, column


def container_above(ship, targetRow, targetCol):
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


def move_out(ship, target, depth):
    goalRow = 0
    goalColumn = 0
    for row in range(len(ship)):
        for column in range(len(ship)):
            if ship[row][column] == target:
                goalRow = row
                goalColumn = column
    # print('Current depth is ' + str(depth))
    if depth % 2 == 0:
        # print("Crane picking up")
        print('Moving to the target crate')
        path_calculations(ship, goalRow, goalColumn, depth, valid_position(ship, target, depth, True))
        craneRow, craneCol = get_crane_pos(ship)
        ship[goalRow - 1][goalColumn] = ship[craneRow][craneCol]
        ship[craneRow][craneCol] = 0
        return ship
    else:
        print('Moving out of the target crate')
        craneRow, craneCol = get_crane_pos(ship)
        ship[goalRow][goalColumn] = 0
        ship[craneRow][craneCol] = 0
        ship[0][0] = '*'
        path_calculations(ship, goalRow, goalColumn, depth, valid_position(ship, target, depth, True))
        return ship


# HEURISTIC FUNCTIONS


def a_star_manhattan(ship, target, unload, depth, load):
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
                            if ship[row + 1][column] == 0 and ship[row + 1][column] != ship[row + 1][goalColumn]:
                                valid_coordinates.append([row + 1, column])
                            if ship[row + 1][column] == - 1:
                                valid_coordinates.append([row, column])
    for coordinates in valid_coordinates:
        shortest_distance.append((abs(goalRow - coordinates[0]) + abs(goalColumn - coordinates[1])))
    if distance:
        # print('Shortest distance is: ' + str(min(shortest_distance)))
        return min(shortest_distance)
    valid_distance = min(shortest_distance)
    # path_calculations(ship, goalRow, goalColumn, depth, valid_distance)
    validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
    validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
    # print(validRow, validColumn)
    # print(goalRow, goalColumn)
    # print('Shortest distance is: ')
    # print(min(shortest_distance))
    craneRow, craneCol = get_crane_pos(ship)
    temp = ship[goalRow][goalColumn]
    ship[goalRow][goalColumn] = ship[validRow][validColumn]
    ship[validRow][validColumn] = temp
    ship[validRow - 1][validColumn] = '*'
    ship[craneRow][craneCol] = 0
    print('Calculating path for moving the target somewhere else')
    path_calculations(ship, goalRow, goalColumn, depth, valid_distance)
    return ship


def path_calculations(ship, goalRow, goalColumn, depth, distance):
    craneRow, craneCol = get_crane_pos(ship)
    path = []
    path += [[craneRow + 1, craneCol]]
    craneRow += 1
    # print(craneRow + 1, craneCol)
    if depth % 2 != 0:
        # if craneRow != 0 or craneCol != 0:
        #     path += [[craneRow + 1, craneCol]]
        #     path += [[craneRow, craneCol]]
        for position in range(distance):
            valid_coordinates = []
            shortest_distance = []
            if craneRow == 0:
                if craneCol == 0:
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
            elif craneRow == 8:
                if craneCol == 0:
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                if craneCol == 11:
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow, craneCol - 1])
                else:
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol - 1])
            elif craneRow != 0:
                if craneCol == 0:
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                if craneCol == 11:
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow, craneCol - 1])
                else:
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
                    if ship[craneRow - 1][craneCol] == 0:
                        valid_coordinates.append([craneRow - 1, craneCol])
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow, craneCol - 1])
            for coordinates in valid_coordinates:
                shortest_distance.append((abs(goalRow - coordinates[0]) + abs(goalColumn - coordinates[1])))
            validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
            validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
            craneRow, craneCol = validRow, validColumn
            if goalRow != craneRow or goalColumn != craneCol:
                path += [[validRow, validColumn]]
            else:
                path += [[validRow, validColumn]]
                break
    print('The valid path is: ' + str(path))


def load_path_calculations(ship, loadRow, loadColumn, depth, distance):
    craneRow, craneCol = 0, 0
    repeats = []
    path = []
    if depth % 2 == 0:
        for position in range(distance):
            valid_coordinates = []
            shortest_distance = []
            if craneRow == 0:
                if ship[craneRow + 1][craneCol] == 0:
                    valid_coordinates.append([craneRow + 1, craneCol])
            elif craneRow != 0 and craneRow != 8:
                if craneCol == 0:
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
                elif craneCol == 11:
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow, craneCol - 1])
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
                else:
                    if ship[craneRow][craneCol + 1] == 0:
                        valid_coordinates.append([craneRow, craneCol + 1])
                    if ship[craneRow][craneCol - 1] == 0:
                        valid_coordinates.append([craneRow, craneCol - 1])
                    if ship[craneRow + 1][craneCol] == 0:
                        valid_coordinates.append([craneRow + 1, craneCol])
            for coordinates in valid_coordinates:
                shortest_distance.append((abs(loadRow - coordinates[0]) + abs(loadColumn - coordinates[1])))
            validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
            validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
            craneRow, craneCol = validRow, validColumn
            if loadRow != craneRow or loadColumn != craneCol:
                path += [[validRow, validColumn]]
            else:
                path += [[validRow, validColumn]]
                break
    path += [[loadRow, loadColumn]]
    print('The valid path is: ' + str(path))


def valid_load(ship, depth, load, distance):
    valid_coordinates = []
    shortest_distance = []
    craneRow, craneCol = get_crane_pos(ship)
    invalidColumn = 20
    if depth % 2 != 0:
        if distance:
            return abs(craneRow - 0) + abs(craneCol - 0)
        ship[0][0] = '*'
        ship[craneRow][craneCol] = 0
        return ship
    # print('Getting valid positions')
    for row in range(len(ship)):
        for column in range(len(ship)):
            if row == 1:
                if ship[row][column] != 0 and ship[row][column] != '*' and row != 0 and ship[row][column] != '**':
                    # print('Row is completely full, no valid coordinates will be in this row.')
                    invalidColumn = column
            else:
                if ship[row][column] != 0 and ship[row][column] != '*' and row != 0 and ship[row][
                    column] != '**' and column != invalidColumn and ship[row - 1][column] == 0:
                    valid_coordinates.append([row - 1, column])
    # print(valid_coordinates)
    for coordinates in valid_coordinates:
        shortest_distance.append((abs(craneRow - coordinates[0]) + abs(craneCol - coordinates[1])))
    if distance:
        # print(min(shortest_distance))
        return min(shortest_distance) - 1
    valid_distance = min(shortest_distance) - 1
    # print('Loading onto the ship')
    validRow = valid_coordinates[shortest_distance.index(min(shortest_distance))][0]
    validColumn = valid_coordinates[shortest_distance.index(min(shortest_distance))][1]
    load_path_calculations(ship, validRow, validColumn, depth, valid_distance)
    ship[craneRow][craneCol] = 0
    ship[validRow - 1][validColumn] = '*'
    ship[validRow][validColumn] = load
    return ship


main()
