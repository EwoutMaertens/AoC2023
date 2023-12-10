from typing import Callable, List, Any
import math
from functools import reduce
from time import perf_counter

# GENERAL

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

def calculate_distance_travelled(time_waited: int, total_time: int) -> int:
    return (total_time - time_waited) * time_waited

# PART ONE

def process_input_line_p1(line: str) -> Any:
    return [int(val) for val in line.split(':')[1].strip().split()]

def process_result_list_p1(result_list: List[Any]) -> Any:
    times = result_list[0]
    distances = result_list[1]
    scores = []
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]
        time_middle = math.ceil(time/2)

        right_boundary = time
        left_boundary = time_middle
        scoring_value = time_middle

        while left_boundary + 1 != right_boundary:
            middle_element = left_boundary + math.floor((right_boundary - left_boundary + 1) / 2)
            
            if calculate_distance_travelled(middle_element, time) > distance:
                left_boundary = middle_element
                scoring_value = middle_element
            else:
                right_boundary = middle_element

        non_scoring_values = time - scoring_value
        scoring_values = scoring_value - non_scoring_values + 1
        scores.append(scoring_values)

    return reduce(lambda x, y: x*y, scores)

# PART TWO

def process_input_line_p2(line: str) -> Any:
    return [int("".join([val for val in line.split(':')[1].strip().split()]))]

def process_result_list_p2(result_list: List[Any]) -> Any:
    return process_result_list_p1(result_list)

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
