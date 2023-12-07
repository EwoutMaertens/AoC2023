from typing import Callable, Dict, List, Any, Tuple
from concurrent.futures import ProcessPoolExecutor
import time

# GENERAL

def process_input_file(input_file: str) -> Tuple[List[int], List[List[Tuple[int, int, int]]]]:
    map_collection = []

    with open(input_file, 'r') as f:
        line = f.readline()
        seeds = line.split(':')[1].strip().split(' ')
        seeds = [int(seed) for seed in seeds]

        line = f.readline()
        map_index = -1
        while line:
            if 'map' in line:
                map_collection.append([])
                map_index += 1
                line = f.readline()
                continue

            if line.strip():
                dest_start, src_start, range_length = line.strip().split(' ')
                dest_start, src_start, range_length = int(dest_start), int(src_start), int(range_length)
                map_collection[map_index].append((dest_start, src_start, range_length))
            line = f.readline()

    return seeds, map_collection

# PART ONE

def process_result_list_p1(result_list: Tuple[List[int], List[List[Tuple[int, int, int]]]]) -> int:
    seeds, map_collection = result_list[0], result_list[1]
    locations = []
    for seed in seeds:
        value = seed
        for map in map_collection:
            for dest, src, r in map:
                if src <= value < src+r:
                    value = dest + (value - src)
                    break
        locations.append(value)
    locations.sort()
    return locations[0]

# PART TWO

def check_value_in_seed_ranges(value:int , seed_ranges: List[Tuple[int, int]]) -> bool:
    for seed_range in seed_ranges:
        start = seed_range[0]
        r = seed_range[1]
        if start <= value < start+r:
            return True
    return False

def find_seed_from_location_batch(location_start: int, location_range: int,
                                  map_collection: List[List[Tuple[int, int, int]]],
                                  seed_ranges: List[Tuple[int, int]]) -> int:
    loc = location_start
    while loc < location_start + location_range:
        value = loc
        for map in map_collection[::-1]:
            for src, dest, r in map:
                if src <= value < src+r:
                    value = dest + (value - src)
                    break

        if check_value_in_seed_ranges(value, seed_ranges):
            print(loc)
            return loc
        loc += 1
    return 0

def process_result_list_p2(result_list: Tuple[List[int], List[List[Tuple[int, int, int]]]]) -> int:
    seeds, map_collection = result_list[0], result_list[1]
    seed_ranges = []

    for i in range(len(seeds)//2):
        start = seeds[2*i]
        r = seeds[2*i+1]
        seed_ranges.append((start, r))

    location = 0
    with ProcessPoolExecutor(max_workers=50) as pp:
        futures = []
        while True:
            futures.append(pp.submit(find_seed_from_location_batch, location, 100000, map_collection, seed_ranges))
            location += 100000

            fs = [future for future in futures if future.done()]
            time.sleep(0.2)
            for future in fs:
                if future.result():
                    return future.result()

# MAIN

print(f"Part 1 - Sample answer: \t{process_result_list_p1(process_input_file('sample.txt'))}")
print(f"Part 1 - Answer:        \t{process_result_list_p1(process_input_file('input.txt'))}")
print("----------------------------------------------\n")

print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample.txt'))}")
print(f"Part 2 - Answer:        \t{process_result_list_p2(process_input_file('input.txt'))}")
print("----------------------------------------------\n")

