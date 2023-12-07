from typing import Callable, List, Any
import re

# GENERAL

class ScratchCard():
    def __init__(self, card_id: int, winning_numbers: List[int], playing_numbers: List[int]) -> None:
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.playing_numbers = playing_numbers

    def get_matching_numbers(self) -> List[int]:
        return [num for num in self.playing_numbers if num in self.winning_numbers]

    def calculate_score(self) -> int:
        scoring_numbers = self.get_matching_numbers()
        return int(2 ** (len(scoring_numbers)-1))

def process_input_file(input_file: str, line_processor: Callable) -> List[ScratchCard]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

def create_scratchcard_from_line(line: str) -> ScratchCard:
    card_info, game_info = line.split(':')

    card_id = re.findall(r'\d+', card_info)[0]
    winning_info, playing_info = game_info.split('|')
    winning_info = re.sub(r' +', ' ', winning_info)
    playing_info = re.sub(r' +', ' ', playing_info)
    winning_numbers = winning_info.strip().split(' ')
    playing_numbers = playing_info.strip().split(' ')

    return ScratchCard(card_id, winning_numbers, playing_numbers)

# PART ONE

def process_input_line_p1(line: str) -> ScratchCard:
    return create_scratchcard_from_line(line)

def process_result_list_p1(result_list: List[ScratchCard]) -> int:
    total_score = 0
    for scratchcard in result_list:
        total_score += scratchcard.calculate_score()
    return total_score

# PART TWO

def process_input_line_p2(line: str) -> ScratchCard:
    return create_scratchcard_from_line(line)

def process_result_list_p2(result_list: List[ScratchCard]) -> int:
    card_inventory = {}
    for i in range(len(result_list)):
        card_inventory[i+1] = 1

    for card_id in card_inventory.keys():
        matching_numbers = result_list[card_id-1].get_matching_numbers()
        for i in range(1, len(matching_numbers) + 1):
            copy_card_id = card_id + i
            card_inventory[copy_card_id] += card_inventory[card_id]

    return sum(card_inventory.values())

# MAIN

print("Part 1 - Answer")
print(process_result_list_p1(process_input_file('input.txt', process_input_line_p1)))
print("-----------------\n")

print("Part 2 - Answer")
print(process_result_list_p2(process_input_file('input.txt', process_input_line_p2)))
print("-----------------\n")
