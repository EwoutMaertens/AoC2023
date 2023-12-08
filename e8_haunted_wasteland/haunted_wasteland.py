from typing import Callable, List, Any, Iterator
from time import perf_counter
import re
import math

# GENERAL

class Node():
    def __init__(self, current: str, left: str, right: str) -> None:
        self.current = current
        self.left = left
        self.right = right

    def ends_with_A(self) -> bool:
        return self.current[-1] == 'A'

    def ends_with_Z(self) -> bool:
        return self.current[-1] == 'Z'

def create_directions_iterator(directions: str) -> Iterator[str]:
    while True:
        for direction in directions:
            yield direction

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    result_list = {}

    with open(input_file, 'r') as f:
        line = f.readline()
        directions = line.strip()
        line = f.readline()
        line = f.readline()
        while line:
            node = line_processor(line.strip())
            result_list[node.current] = node
            line = f.readline()
    return (directions, result_list)

# PART ONE

def process_input_line_p1(line: str) -> Any:
    split_line = [part.strip() for part in line.split('=')]
    current = split_line[0]
    left, right = re.findall(r'(\w{3})', split_line[1])
    return Node(current, left, right)


def process_result_list_p1(result_tuple) -> Any:
    directions, result_list = result_tuple[0], result_tuple[1]
    directions_iterator = create_directions_iterator(directions)

    node = result_list['AAA']
    step_amount = 0
    while node.current != 'ZZZ':
        direction = next(directions_iterator)
        step_amount += 1
        if direction == 'L':
            node = result_list[node.left]
        elif direction == 'R':
            node = result_list[node.right]
        else:
            raise RuntimeError(f"{direction}")

    return step_amount

# PART TWO

def process_input_line_p2(line: str) -> Any:
    split_line = [part.strip() for part in line.split('=')]
    current = split_line[0]
    left, right = re.findall(r'(\w{3})', split_line[1])
    return Node(current, left, right)

def check_all_nodes_end_with_Z(node_names, result_list) -> bool:
    nodes_ending_with_z = [node_name for node_name in node_names if result_list[node_name].ends_with_Z()]
    if len(nodes_ending_with_z):
        print(nodes_ending_with_z)
    return len(node_names) == len(nodes_ending_with_z)

def process_result_list_p2(result_tuple: List[Any]) -> Any:
    directions, result_list = result_tuple[0], result_tuple[1]

    node_names = [node_name for node_name in result_list.keys() if result_list[node_name].ends_with_A()]
    iterations_needed_for_node = []
    for node_name in node_names:
        step_amount = 0
        directions_iterator = create_directions_iterator(directions)
        while not check_all_nodes_end_with_Z([node_name], result_list):
            direction = next(directions_iterator)
            step_amount += 1
            if direction == 'L':
                node_name = result_list[node_name].left
            elif direction == 'R':
                node_name = result_list[node_name].right
            else:
                raise RuntimeError(f"{direction}")
        iterations_needed_for_node.append(step_amount)

    print(iterations_needed_for_node)


    # step_amount = 0
    # directions_iterator = create_directions_iterator(directions)
    # while not check_all_nodes_end_with_Z(node_names, result_list):
    #     direction = next(directions_iterator)
    #     step_amount += 1
    #     if direction == 'L':
    #         new_node_names = [result_list[node_name].left for node_name in node_names]
    #         node_names = new_node_names
    #     elif direction == 'R':
    #         new_node_names = [result_list[node_name].right for node_name in node_names]
    #         node_names = new_node_names
    #     else:
    #         raise RuntimeError(f"{direction}")

    return math.lcm(*iterations_needed_for_node)

# MAIN

print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample.txt', process_input_line_p1))}")
print(f"Part 1 - Sample 2 answer: \t{process_result_list_p1(process_input_file('sample2.txt', process_input_line_p1))}")

time_start = perf_counter()
result = process_result_list_p1(process_input_file('input.txt', process_input_line_p1))
time_stop = perf_counter()
print(f"Part 1 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")

print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample3.txt', process_input_line_p2))}")

time_start = perf_counter()
result = process_result_list_p2(process_input_file('input.txt', process_input_line_p2))
time_stop = perf_counter()
print(f"Part 2 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
print("----------------------------------------------\n")
