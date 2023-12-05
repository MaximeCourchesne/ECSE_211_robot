#===================================================================
# Created by Maxime Courchesne, McGill University
#
# Last modified by Maxime Courchesne on October 29th 11:35
# Reason: cleaned up unnecessary comments, print statements and made
# the code easier to read
#
#
#===================================================================


# function that takes in two blocks and returns the shortest path between the blocks on the grid
def findShortestPath(pos_start, pos_end, blocks_not_to_check, order_check_around=0):
    # we make a copy of blocks_not_to_check so that we don't modify the argument
    blocks_not_to_check = blocks_not_to_check.copy()
    listFinalPath = []
    # Here we keep the parent block of each block while scanning for the shortest path
    dictBlockParents = {}
    # The first block we check_around is pos_start
    blocksToCheckNext = [pos_start]
    if pos_end in blocks_not_to_check:
        blocks_not_to_check.remove(pos_end)

    # functions that takes in a block and adds it's neighbors to blocksToCheckNext. Unless they are in "blocks_not_to_check"
    def checkAround(block, parentBlock, blocksAlreadyVisited, dictBlockParents,
                    blocksToCheckNext, arrivedAtEndBlock):

        if block not in blocksAlreadyVisited and block[0] >= 0 and block[0] <= 3 and block[1] >= 0 and block[1] <= 3:
            dictBlockParents[block] = parentBlock
            blocksAlreadyVisited.add(block)
            blocksToCheckNext.append(block)

    arrivedAtEndBlock = False
    while not arrivedAtEndBlock:
        for block in blocksToCheckNext:
            if block == pos_end:
                arrivedAtEndBlock = True

            elif not arrivedAtEndBlock:
                checkAround(((block[0] + 1), (block[1])), block, blocks_not_to_check, dictBlockParents, blocksToCheckNext, arrivedAtEndBlock)
                checkAround(((block[0] - 1), (block[1])), block, blocks_not_to_check, dictBlockParents, blocksToCheckNext, arrivedAtEndBlock)
                checkAround(((block[0]), (block[1] + 1)), block, blocks_not_to_check, dictBlockParents, blocksToCheckNext, arrivedAtEndBlock)
                checkAround(((block[0]), (block[1] - 1)), block, blocks_not_to_check, dictBlockParents, blocksToCheckNext, arrivedAtEndBlock)

    pathComputed = False
    next_block = pos_end
    while not pathComputed:
        # dictBlockParents will never be 0 so the following if statement could be erased
        if len(dictBlockParents) == 0:
            pathComputed = True
            continue
        listFinalPath.append(dictBlockParents[next_block])
        next_block = dictBlockParents[next_block]
        if next_block == pos_start:
            pathComputed = True

    # So that the returned list is in order and contains start/end blocks
    listFinalPath = list(reversed(listFinalPath))
    listFinalPath.append(pos_end)
    # So that the arguments are not modified
    blocks_not_to_check.add(pos_end)
    return listFinalPath


def findRobotPath(block1_position, block1_color, block2_position, block2_color, block3_position, block3_color):
    # positions where to drop cubes and firestation. Important for pathfinding algorithm
    block_positions = {block1_position, block2_position, block3_position}

    # paths to first block
    path_b0_to_b1 = findShortestPath((0, 0), block1_position, block_positions)
    path_b0_to_b2 = findShortestPath((0, 0), block2_position, block_positions)
    path_b0_to_b3 = findShortestPath((0, 0), block3_position, block_positions)

    # function to calculate a path for a given order
    def findPathForPermutation(path_to_first_block, second_block, third_block, block_positions):
        # the path starts of as the path to the first block
        first_path = path_to_first_block
        # appending the path to block 2
        second_path = findShortestPath(first_path[-2], second_block, block_positions)
        # appending the path to block 3
        third_path = findShortestPath(second_path[-2], third_block, block_positions)
        # adding return to fire station
        fourth_path = findShortestPath(third_path[-2], (0, 0), block_positions)
        return first_path + second_path[1:] + third_path[1:] + fourth_path[1:]

    # cost function for a given path


    possible_paths = []
    # @@@@@@@@@@@@@ appending path for each permutation to list of paths @@@@@@@@@@@@@
    # @@@@@@@@@@@@@ 1, 2, 3 @@@@@@@@@@@@
    # initializing as the path to block 1
    # path_1_2_3 = findPathForPermutation(path_b0_to_b1, block2_position, block3_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b1, block2_position, block3_position, block_positions)))
    # @@@@@@@@@@@@@ 1, 3, 2 @@@@@@@@@@@@@
    # path_1_3_2 = findPathForPermutation(path_b0_to_b1, block3_position, block2_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b1, block3_position, block2_position, block_positions)))

    # @@@@@@@@@@@@@ 2, 1, 3 @@@@@@@@@@@@@
    # path_2_1_3 = findPathForPermutation(path_b0_to_b2, block1_position, block3_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b2, block1_position, block3_position, block_positions)))

    # @@@@@@@@@@@@@ 2, 3, 1 @@@@@@@@@@@@@
    # path_2_3_1 = findPathForPermutation(path_b0_to_b2, block3_position, block1_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b2, block3_position, block1_position, block_positions)))

    # @@@@@@@@@@@@@ 3, 2, 1 @@@@@@@@@@@@@
    # path_3_1_2 = findPathForPermutation(path_b0_to_b3, block2_position, block1_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b3, block2_position, block1_position, block_positions)))

    # @@@@@@@@@@@@@ 3, 1, 2 @@@@@@@@@@@@@
    # path_3_2_1 = findPathForPermutation(path_b0_to_b3, block1_position, block2_position, block_positions)
    possible_paths.append(tuple(findPathForPermutation(path_b0_to_b3, block1_position, block2_position, block_positions)))

    # Determine the "cost" of each path
    def cost_path(path):
        return len(path)

    # returns the smallest path calculated by the cost function
    return min(possible_paths, key=lambda x: cost_path(x))

def calculate_rotations(facing_direction, current_block, next_block):
    # function that takes a current direction, a current block and a next block
    # and outputs the rotation in degrees that the robot has to perform
    movement = (next_block[0]-current_block[0], next_block[1]-current_block[1])
    if movement == (1,0):
        # going east (180 degree)
        direction_in_degrees = 0
    elif movement == (-1, 0):
        # going west (0 degree)
        direction_in_degrees = 180
    elif movement == (0, 1):
        # going north (90 degree)
        direction_in_degrees = 90
    elif movement == (0, -1):
        # going south (270 degree)
        direction_in_degrees = -90
    else:
        raise ArithmeticError("the blocks passed in are more than 1 block apart (manhattan distance)")

    # setting the rotation to be between -180 degrees and 180 degrees
    angle_to_rotate = (facing_direction-direction_in_degrees)
    if -180<=angle_to_rotate<=180:
        return angle_to_rotate
    elif angle_to_rotate>180:
        return angle_to_rotate-360
    elif angle_to_rotate<-180:
        return angle_to_rotate+360

def translate_path_to_movements(path, block1_position, block1_color, block2_position, block2_color, block3_position, block3_color):
    # function that takes in a path and block positions and outputs a list of directions
    list_instructions = []
    drop_off_positions = {block1_position, block2_position, block3_position}
    drop_off_colors = {block1_position: block1_color, block2_position: block2_color, block3_position: block3_color}

    current_facing_angle = 90
    count_dropoff_in_a_row = 0

    for coordinate_index in range(0, len(path)-1):
        current_block = path[coordinate_index - count_dropoff_in_a_row]
        next_block = path[coordinate_index+1]

        # calculate the rotation we need to reach the next block and update the current angle of the robot
        rotation_to_reach_next_block = calculate_rotations(current_facing_angle, current_block, next_block)
        if rotation_to_reach_next_block != 0:
            list_instructions.append(rotation_to_reach_next_block)
        current_facing_angle=(current_facing_angle-rotation_to_reach_next_block)%360
        # appending drop off instruction of foward instruction depending on if the position is a drop off position

        if next_block in drop_off_positions:
            list_instructions.append("drop_" + str(drop_off_colors[next_block]))
            count_dropoff_in_a_row += 1
        else:
            list_instructions.append("forward")
            count_dropoff_in_a_row = 0

    return list_instructions


# function that will be imported by other files
def getRobotMovementList(block1_position, block1_color, block2_position, block2_color, block3_position, block3_color):
    """Find the shortest path visiting each building in target_buildings, returns a list of strings
    containing step by step instructions
    target_buildings: a list of two item tuples containing positions of buildings on fire
    fire_types: a list of strings containing the type of extinguishers needed (in order of target_buildings)
    """
    return translate_path_to_movements(findRobotPath(block1_position, block1_color, block2_position, block2_color, block3_position, block3_color), block1_position, block1_color, block2_position, block2_color, block3_position, block3_color)

# Assuming that the robot starts facing north
# print(getRobotMovementList((1, 0), "purple", (3, 2), "red", (2, 1), "green"))
