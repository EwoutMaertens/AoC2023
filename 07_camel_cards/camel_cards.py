from collections import defaultdict
from typing import Callable, List, Any
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

# PART ONE

card_scores = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

class Hand():
    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.card_map = defaultdict(lambda: 0)
        self.highest_amount = 0

        for card in cards:
            self.card_map[card] += 1
            if self.card_map[card] > self.highest_amount:
                self.highest_amount = self.card_map[card]

    def __lt__(self, other):
        # four-of-a-kind wins vs (three-of-a-kind and full house) vs (two pair and one pair) vs high card
        if self.highest_amount < other.highest_amount:
            return True
        if self.highest_amount > other.highest_amount:
            return False

        # full house wins vs three-of-a-kind and two pair wins vs one pair
        if len(self.card_map) < len(other.card_map):
            return False
        if len(self.card_map) > len(other.card_map):
            return True

        # outcome is the same, check first cards to see which hand is highest
        for i in range(len(self.cards)):
            if self.cards[i] == other.cards[i]:
                continue
            if card_scores[self.cards[i]] < card_scores[other.cards[i]]:
                return True
            return False
        return False

def process_input_line_p1(line: str) -> Any:
    cards, bid = line.strip().split(' ')
    return Hand(cards, bid)

def process_result_list_p1(result_list: List[Any]) -> Any:
    result_list.sort()

    total_score = 0
    for i in range(len(result_list)):
        total_score += (result_list[i].bid * (i + 1))
    return total_score

# PART TWO

part2_card_scores = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 12,
    'K': 13,
    'A': 14
}

class HandP2():
    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.card_map = defaultdict(lambda: 0)
        self.highest_amount = 0
        self.highest_card = None

        # Keep track of card occurences, and the highest amount (which is not 'J')
        for card in cards:
            self.card_map[card] += 1
            if self.card_map[card] > self.highest_amount and card != 'J':
                self.highest_amount = self.card_map[card]
                self.highest_card = card

        # Now add the amount of J's to the highest amount
        self.highest_amount += self.card_map['J']

        # J's can take any form, so remove them from the card map
        # EXCEPT FOR edge case JJJJJ, this should be smaller than ALL other five-of-a-kinds
        # should you remove it here, it would have the highest score, which is incorrect
        if not self.cards == 'JJJJJ':
            self.card_map.pop('J')

    def __lt__(self, other):
        # four-of-a-kind wins vs (three-of-a-kind and full house) vs (two pair and one pair) vs high card
        if self.highest_amount < other.highest_amount:
            return True
        if self.highest_amount > other.highest_amount:
            return False

        # full house wins vs three-of-a-kind and two pair wins vs one pair
        if len(self.card_map) < len(other.card_map):
            return False
        if len(self.card_map) > len(other.card_map):
            return True

        # outcome is the same, check first cards to see which hand is highest
        for i in range(len(self.cards)):
            if self.cards[i] == other.cards[i]:
                continue
            if part2_card_scores[self.cards[i]] < part2_card_scores[other.cards[i]]:
                return True
            return False
        return False

def process_input_line_p2(line: str) -> Any:
    cards, bid = line.strip().split(' ')
    return HandP2(cards, bid)

def process_result_list_p2(result_list: List[Any]) -> Any:
    result_list.sort()

    total_score = 0
    for i in range(len(result_list)):
        total_score += (result_list[i].bid * (i + 1))
    return total_score

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
