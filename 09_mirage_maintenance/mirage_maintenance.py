from typing import Callable, List, Any
from time import perf_counter

# GENERAL

class NumberSequence():
    def __init__(self, sequence) -> None:
        self.sequence = sequence
        self.difference_number_sequence = None

        if [num for num in self.sequence if num != 0]:
            sequence_difference = []
            for i in range(len(self.sequence) - 1):
                sequence_difference.append(self.sequence[i+1] - self.sequence[i])
            self.difference_number_sequence = NumberSequence(sequence_difference)

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
    sequence = [int(val) for val in line.strip().split()]
    return NumberSequence(sequence)

def calculate_next_number(number_sequence: NumberSequence) -> int:
    if number_sequence.difference_number_sequence:
        next_number = calculate_next_number(number_sequence.difference_number_sequence)
    else:
        next_number = 0

    return number_sequence.sequence[-1] + next_number

def process_result_list_p1(result_list: List[Any]) -> Any:
    score = 0
    for number_sequence in result_list:
        score += calculate_next_number(number_sequence)
    return score

# PART TWO

def process_input_line_p2(line: str) -> Any:
    sequence = [int(val) for val in line.strip().split()]
    return NumberSequence(sequence[::-1])

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
