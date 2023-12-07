from typing import Callable, List, Any

# GENERAL

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    """"""
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            line
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

# PART ONE

def process_input_line_p1(line: str) -> Any:
    pass

def process_result_list_p1(result_list: List[Any]) -> Any:
    pass

# PART TWO

def process_input_line_p2(line: str) -> Any:
    pass

def process_result_list_p2(result_list: List[Any]) -> Any:
    pass

# MAIN

print("Part 1 - Answer")
print(process_result_list_p1(process_input_file('input.txt', process_input_line_p1)))
print("-----------------\n")

print("Part 2 - Answer")
print(process_result_list_p2(process_input_file('input.txt', process_input_line_p2)))
print("-----------------\n")
