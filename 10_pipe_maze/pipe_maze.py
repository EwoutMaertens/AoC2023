from typing import Callable, List, Any
from time import perf_counter
from abc import ABC
import pdb

# GENERAL

class Pipe(ABC):
    def __init__(self, character: str) -> None:
        self.character = character
        self.south = False
        self.north = False
        self.east = False
        self.west = False

    def navigate(self, starting_direction: str) -> None:
        if starting_direction == 'S':
            if self.north:
                return 'N'
            if self.east:
                return 'E'
            if self.west:
                return 'W'
        if starting_direction == 'N':
            if self.south:
                return 'S'
            if self.east:
                return 'E'
            if self.west:
                return 'W'
        if starting_direction == 'E':
            if self.north:
                return 'N'
            if self.south:
                return 'S'
            if self.west:
                return 'W'
        if starting_direction == 'W':
            if self.north:
                return 'N'
            if self.east:
                return 'E'
            if self.south:
                return 'S'

class VerticalPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.north = True
        self.south = True

class HorizontalPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.east = True
        self.west = True

class FPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.east = True
        self.south = True

class JPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.north = True
        self.west = True

class SevenPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.west = True
        self.south = True

class LPipe(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)
        self.north = True
        self.east = True

class Ground(Pipe):
    def __init__(self, character: str) -> None:
        super().__init__(character)

def determine_which_pipe_for_start(schedule_matrix: List[List[Pipe]], y: str, x: str) -> Pipe:
    pipe = Pipe('S')
    if not y == 0:
        pipe.north = schedule_matrix[y-1][x].south
    if not y == len(schedule_matrix) - 1:
        pipe.south = schedule_matrix[y+1][x].north
    if not x == 0:
        pipe.west = schedule_matrix[y][x-1].east
    if not x == len(schedule_matrix[y]) - 1:
        pipe.east = schedule_matrix[y][x+1].west
    if pipe.north and pipe.south:
        return VerticalPipe('|')
    if pipe.east and pipe.west:
        return HorizontalPipe('-')
    if pipe.west and pipe.south:
        return SevenPipe('7')
    if pipe.south and pipe.east:
        return FPipe('F')
    if pipe.north and pipe.east:
        return LPipe('L')
    if pipe.north and pipe.west:
        return JPipe('J')
    return pipe

def determine_pipe(character: str) -> Pipe:
    if character == '|':
        return VerticalPipe(character)
    if character == '-':
        return HorizontalPipe(character)
    if character == '7':
        return SevenPipe(character)
    if character == 'F':
        return FPipe(character)
    if character == 'L':
        return LPipe(character)
    if character == 'J':
        return JPipe(character)
    if character == '.':
        return Ground(character)
    if character == 'S':
        raise RuntimeError("This should be done at the end.")
    raise RuntimeError(f"{character}")

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

# PART ONE

def reverse_direction(direction: str) -> str:
    if direction == 'S':
        return 'N'
    if direction == 'N':
        return 'S'
    if direction == 'W':
        return 'E'
    if direction == 'E':
        return 'W'

def move_node(y, x, direction):
    if direction == 'S':
        return (y+1, x)
    if direction == 'N':
        return (y-1, x)
    if direction == 'E':
        return (y, x+1)
    if direction == 'W':
        return (y, x-1)

def process_input_line_p1(line: str) -> Any:
    return line

def process_result_list_p1(result_list: List[Any]) -> Any:
    schedule_matrix = []
    starting_node = None
    for y in range(len(result_list)):
        matrix_line = []
        for x in range(len(result_list[y])):
            if result_list[y][x] == 'S':
                starting_node = (y, x)
                matrix_line.append(None)
                continue
            matrix_line.append(determine_pipe(result_list[y][x]))
        schedule_matrix.append(matrix_line)
    schedule_matrix[starting_node[0]][starting_node[1]] = determine_which_pipe_for_start(schedule_matrix, starting_node[0], starting_node[1])

    steps = 0
    if schedule_matrix[starting_node[0]][starting_node[1]].south:
        direction = 'S'
    elif schedule_matrix[starting_node[0]][starting_node[1]].north:
        direction = 'N'
    elif schedule_matrix[starting_node[0]][starting_node[1]].east:
        direction = 'E'

    steps += 1
    current_node = move_node(starting_node[0], starting_node[1], direction)
    direction = schedule_matrix[current_node[0]][current_node[1]].navigate(reverse_direction(direction))
    while starting_node != current_node:
        steps += 1
        current_node = move_node(current_node[0], current_node[1], direction)
        direction = schedule_matrix[current_node[0]][current_node[1]].navigate(reverse_direction(direction))

    return steps/2

# PART TWO

def process_input_line_p2(line: str) -> Any:
    return line

def process_result_list_p2(result_list: List[Any]) -> Any:
    schedule_matrix = []
    starting_node = None
    for y in range(len(result_list)):
        matrix_line = []
        for x in range(len(result_list[y])):
            if result_list[y][x] == 'S':
                starting_node = (y, x)
                matrix_line.append(None)
                continue
            matrix_line.append(determine_pipe(result_list[y][x]))
        schedule_matrix.append(matrix_line)
    schedule_matrix[starting_node[0]][starting_node[1]] = determine_which_pipe_for_start(schedule_matrix, starting_node[0], starting_node[1])

    steps = 0
    if schedule_matrix[starting_node[0]][starting_node[1]].south:
        direction = 'S'
    elif schedule_matrix[starting_node[0]][starting_node[1]].north:
        direction = 'N'
    elif schedule_matrix[starting_node[0]][starting_node[1]].east:
        direction = 'E'

    result_matrix = []
    for y in range(len(result_list)):
        matrix_line = []
        for x in range(len(result_list[y])):
            matrix_line.append(0)
        result_matrix.append(matrix_line)

    steps += 1
    current_node = move_node(starting_node[0], starting_node[1], direction)
    result_matrix[current_node[0]][current_node[1]] = 1
    direction = schedule_matrix[current_node[0]][current_node[1]].navigate(reverse_direction(direction))
    while starting_node != current_node:
        steps += 1
        current_node = move_node(current_node[0], current_node[1], direction)
        result_matrix[current_node[0]][current_node[1]] = 1
        direction = schedule_matrix[current_node[0]][current_node[1]].navigate(reverse_direction(direction))

    for y in range(len(result_matrix)):
        for x in range(len(result_matrix[y])):
            print(f"{schedule_matrix[y][x].character}", end="")
        print()


    enclosed = False
    score = 0

    for y in range(len(result_matrix)):
        for x in range(len(result_matrix[y])):
            if result_matrix[y][x] == 1:
                pipe = True
            else:
                pipe = False

            if not pipe:
                if enclosed:
                    result_matrix[y][x] = 'I'
                    score += 1
                continue

            char = schedule_matrix[y][x].character

            is_starting_corner = char in 'FL'
            is_ending_corner = char in '7J'
            is_vertical_pipe = char == '|'

            if is_vertical_pipe:
                enclosed = not enclosed
            elif is_starting_corner:
                source_direction = 'E' if char == 'L' else 'W'
            elif is_ending_corner:
                target_direction = 'E' if char == 'J' else 'W'
                if target_direction != source_direction:
                    enclosed = not enclosed

    print()
    for y in range(len(result_matrix)):
        for x in range(len(result_matrix[y])):
            print(f"{result_matrix[y][x]}", end="")
        print()
    return score

# MAIN

print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample1.txt', process_input_line_p1))}")
print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample2.txt', process_input_line_p1))}")

time_start = perf_counter()
result = process_result_list_p1(process_input_file('input.txt', process_input_line_p1))
time_stop = perf_counter()
print(f"Part 1 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")

print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample1.txt', process_input_line_p2))}")
print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample2.txt', process_input_line_p2))}")
print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample3.txt', process_input_line_p2))}")
print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample4.txt', process_input_line_p2))}")

time_start = perf_counter()
result = process_result_list_p2(process_input_file('input.txt', process_input_line_p2))
time_stop = perf_counter()
print(f"Part 2 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")
