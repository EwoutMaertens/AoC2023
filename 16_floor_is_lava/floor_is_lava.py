from typing import Callable, List, Any, Tuple
from time import perf_counter
from abc import ABC
from enum import Enum
from queue import Queue

# GENERAL


class Direction(Enum):
    E = 0
    S = 1
    W = 2
    N = 3

DIRECTION_DELTA_VALUES = ((0, 1), (1, 0), (0, -1), (-1, 0))


class Tile():
    def __init__(self) -> None:
        super().__init__()
        self._is_energized = False
        self._directions_traversed = []

    def is_energized(self) -> bool:
        return self._is_energized

    def set_energized(self, value=True) -> None:
        self._is_energized = value

    def set_direction_traversed(self, direction: Direction) -> None:
        self._directions_traversed.append(direction)

    def clear_direction_traversed(self) -> None:
        self._directions_traversed = []

    def get_direction_is_traversed(self, direction: Direction) -> bool:
        return direction in self._directions_traversed

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        raise RuntimeError("You have to implement this.")


class VerticalMirror(Tile):
    def __init__(self) -> None:
        super().__init__()

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        if direction in [Direction.E, Direction.W]:
            return tuple([Direction.N, Direction.S])
        return tuple([direction])
        

class HorizontalMirror(Tile):
    def __init__(self) -> None:
        super().__init__()

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        if direction in [Direction.N, Direction.S]:
            return tuple([Direction.W, Direction.E])
        return tuple([direction])

class ForwardDiagonalMirror(Tile):
    def __init__(self) -> None:
        super().__init__()

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        if direction == Direction.E:
            return tuple([Direction.N])
        if direction == Direction.N:
            return tuple([Direction.E])
        if direction == Direction.S:
            return tuple([Direction.W])
        if direction == Direction.W:
            return tuple([Direction.S])

class BackwardDiagonalMirror(Tile):
    def __init__(self) -> None:
        super().__init__()

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        if direction == Direction.E:
            return tuple([Direction.S])
        if direction == Direction.N:
            return tuple([Direction.W])
        if direction == Direction.S:
            return tuple([Direction.E])
        if direction == Direction.W:
            return tuple([Direction.N])

class EmptyTile(Tile):
    def __init__(self) -> None:
        super().__init__()

    def get_resulting_beams_from_direction(self, direction) -> Tuple[Direction]:
        return tuple([direction])


def create_tile(character: str) -> Tile:
    if character == '.':
        return EmptyTile()
    if character == '|':
        return VerticalMirror()
    if character == '-':
        return HorizontalMirror()
    if character == '/':
        return ForwardDiagonalMirror()
    if character == '\\':
        return BackwardDiagonalMirror()
    raise RuntimeError(f"Unknown character {character}.")


def process_input_file(input_file: str, line_processor: Callable) -> Tuple[Any]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return tuple(result_list)

# PART ONE

def next_tile_in_bounds(tile_board, row, col) -> bool:
    if 0 <= row < len(tile_board) and 0 <= col < len(tile_board[0]):
        return True
    return False

def traverse_tile_board(tile_board, tile_queue):
    while not tile_queue.empty():
        row, col, direction = tile_queue.get()
        if not tile_board[row][col].get_direction_is_traversed(direction):
            tile_board[row][col].set_direction_traversed(direction)
            tile_board[row][col].set_energized()

            for new_dir in tile_board[row][col].get_resulting_beams_from_direction(direction):
                drow, dcol = DIRECTION_DELTA_VALUES[new_dir.value]
                new_row = row + drow
                new_col = col + dcol

                if next_tile_in_bounds(tile_board, new_row, new_col):
                    tile_queue.put((new_row, new_col, new_dir))

def calculate_tiles_energized(tile_board):
    score = 0
    for row in range(len(tile_board)):
        for col in range(len(tile_board[row])):
            if tile_board[row][col].is_energized():
                print('#', end='')
                score += 1
            else:
                print('.', end='')
        print()
    print()
    return score

def process_input_line_p1(line: str) -> Tuple[Tile]:
    tile_line = []
    for character in line:
        tile_line.append(create_tile(character))
    return tuple(tile_line)

def process_result_list_p1(tile_board: Tuple[Tuple[Tile]]) -> int:
    start_row = 0 # Starting pos
    start_col = 0 # Starting pos
    direction = Direction.E # Starts off by facing East
    tile_queue = Queue()
    tile_queue.put((start_row, start_col, direction))

    traverse_tile_board(tile_board, tile_queue)

    return calculate_tiles_energized(tile_board)

# PART TWO

def clear_board(tile_board):
    for row in range(len(tile_board)):
        for col in range(len(tile_board[row])):
            tile_board[row][col].set_energized(value=False)
            tile_board[row][col].clear_direction_traversed()

def process_input_line_p2(line: str) -> Any:
    return process_input_line_p1(line)

def process_result_list_p2(tile_board: Tuple[Tuple[Tile]]) -> Any:
    max_score = 0
    for i in range(len(tile_board)):
        start_row = i
        start_col = 0
        tile_queue = Queue()
        tile_queue.put((start_row, start_col, Direction.E))

        traverse_tile_board(tile_board, tile_queue)
        score = calculate_tiles_energized(tile_board)

        if max_score < score:
            max_score = score

        clear_board(tile_board)

        start_row = i
        start_col = len(tile_board[0]) - 1
        tile_queue = Queue()
        tile_queue.put((start_row, start_col, Direction.W))

        traverse_tile_board(tile_board, tile_queue)
        score = calculate_tiles_energized(tile_board)

        if max_score < score:
            max_score = score

        clear_board(tile_board)

    for i in range(len(tile_board[0])):
        start_row = 0
        start_col = i
        tile_queue = Queue()
        tile_queue.put((start_row, start_col, Direction.S))

        traverse_tile_board(tile_board, tile_queue)
        score = calculate_tiles_energized(tile_board)

        if max_score < score:
            max_score = score

        clear_board(tile_board)

        start_row = len(tile_board) - 1
        start_col = i
        tile_queue = Queue()
        tile_queue.put((start_row, start_col, Direction.N))

        traverse_tile_board(tile_board, tile_queue)
        score = calculate_tiles_energized(tile_board)

        if max_score < score:
            max_score = score

        clear_board(tile_board)

    return max_score

# MAIN

print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample.txt', process_input_line_p1))}")

time_start = perf_counter()
result = process_result_list_p1(process_input_file('input.txt', process_input_line_p1))
time_stop = perf_counter()
print(f"Part 1 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")

print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample.txt', process_input_line_p2))}")

time_start = perf_counter()
result = process_result_list_p2(process_input_file('input.txt', process_input_line_p2))
time_stop = perf_counter()
print(f"Part 2 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")
