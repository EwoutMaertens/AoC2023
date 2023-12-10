from typing import Callable, List, Any, Optional, Tuple
import re

# GENERAL

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

# PART ONE

def process_input_line_p1(line: str) -> Any:
    # Using line as a full matrix line
    return line

def is_character_symbol(character: str) -> bool:
    return character[0] in ['=', '-', '_', '+', '/', '*', '@', '$', '!', '#', '%', '^', '&']

def inspect_coordinates(result_list: List[str], x: int, y: int) -> bool:
    if x < 0 or y < 0 or x >= len(result_list[0]) or y >= len(result_list):
        return False
    return is_character_symbol(result_list[y][x])

def check_part_number_adjacent_to_symbol(result_list: List[str], x: int, y: int) -> bool:
    for coordinates in [(x-1, y-1), (x, y-1), (x+1, y-1),
                        (x-1, y), (x+1, y),
                        (x-1, y+1), (x, y+1), (x+1, y+1)]:
        if inspect_coordinates(result_list, coordinates[0], coordinates[1]):
            return True
    return False

def check_part_adjacent_to_symbol(result_list: List[str], part: re.Match, y: int) -> bool:
    for x in range(part.start(), part.end()):
        if check_part_number_adjacent_to_symbol(result_list, x, y):
            return True
    return False

def process_result_list_p1(result_list: List[Any]) -> Any:
    part_numbers = []
    for y in range(len(result_list)):
        line_part_iterator = re.finditer(r'\d+', result_list[y])
        for part in line_part_iterator:
            if check_part_adjacent_to_symbol(result_list, part, y):
                part_numbers.append(int(part.group()))

    return sum(part_numbers)

# PART TWO

def process_input_line_p2(line: str) -> Any:
    # Using line as a full matrix line
    return line

def is_character_gear(character: str) -> bool:
    return character[0] in ['*']

def inspect_coordinates_gear(result_list: List[str], x: int, y: int) -> bool:
    if x < 0 or y < 0 or x >= len(result_list[0]) or y >= len(result_list):
        return False
    return is_character_gear(result_list[y][x])

def check_part_number_adjacent_to_gear(result_list: List[str], x: int, y: int) -> Optional[Tuple[int]]:
    for coordinates in [(x-1, y-1), (x, y-1), (x+1, y-1),
                        (x-1, y), (x+1, y),
                        (x-1, y+1), (x, y+1), (x+1, y+1)]:
        if inspect_coordinates_gear(result_list, coordinates[0], coordinates[1]):
            return coordinates
    return None

def check_part_adjacent_to_gear(result_list: List[str], part: re.Match, y: int) -> Optional[Tuple[int]]:
    for x in range(part.start(), part.end()):
        coordinates = check_part_number_adjacent_to_gear(result_list, x, y)
        if coordinates:
            return coordinates
    return None

def process_result_list_p2(result_list: List[Any]) -> Any:
    gear_coordination_map = {}
    for y in range(len(result_list)):
        line_part_iterator = re.finditer(r'\d+', result_list[y])
        for part in line_part_iterator:
            gear_coordinates = check_part_adjacent_to_gear(result_list, part, y)
            if gear_coordinates:
                if gear_coordinates not in gear_coordination_map:
                    gear_coordination_map[gear_coordinates] = []
                gear_coordination_map[gear_coordinates].append(int(part.group()))

    gear_score = 0
    for gear in gear_coordination_map.keys():
        # print(f"{gear}: {gear_coordination_map[gear]}")
        if len(gear_coordination_map[gear]) == 2:
            gear_score += (gear_coordination_map[gear][0] * gear_coordination_map[gear][1])
    return gear_score

# MAIN

print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample.txt', process_input_line_p1))}")
print(f"Part 1 - Answer:        \t{process_result_list_p1(process_input_file('input.txt', process_input_line_p1))}")
print("----------------------------------------------\n")

print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample.txt', process_input_line_p2))}")
print(f"Part 2 - Answer:        \t{process_result_list_p2(process_input_file('input.txt', process_input_line_p2))}")
print("----------------------------------------------\n")
