from typing import Callable, List, Any
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

def is_character_number(character: str) -> bool:
    return ord('0') <= ord(character) <= ord('9')

def process_input_line_p1(line: str) -> str:
    first_num = None
    last_num = None

    for character in line:
        if is_character_number(character):
            first_num = character
            break

    for character in line[::-1]:
        if is_character_number(character):
            last_num = character
            break

    return first_num + last_num

def process_result_list_p1(result_list: List[str]) -> int:
    result_list = [int(res) for res in result_list]
    return sum(result_list)

# PART TWO

charmap = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}
number_string_regex = "|".join(charmap.keys())
reverse_number_string_regex = number_string_regex[::-1]

def process_input_line_p2(line: str) -> str:
    first_num = re.findall(fr"(\d|{number_string_regex}){{1}}", line)[0]
    last_num = re.findall(fr"(\d|{reverse_number_string_regex}){{1}}", line[::-1])[0]

    if first_num in charmap:
        first_num = charmap[first_num]

    if last_num[::-1] in charmap:
        last_num = charmap[last_num[::-1]]

    return first_num + last_num

def process_result_list_p2(result_list: List[str]) -> int:
    result_list = [int(res) for res in result_list]
    return sum(result_list)

# MAIN

print("Part 1 - Answer")
print(process_result_list_p1(process_input_file('input.txt', process_input_line_p1)))
print("-----------------\n")

print("Part 2 - Answer")
print(process_result_list_p2(process_input_file('input.txt', process_input_line_p2)))
print("-----------------\n")
