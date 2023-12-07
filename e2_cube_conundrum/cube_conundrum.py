from typing import Callable, List, Any
import re

# GENERAL

class CubeGameSet():
    def __init__(self, red_cube_amount: int, green_cube_amount: int, blue_cube_amount: int) -> None:
        self.red_cubes = red_cube_amount
        self.green_cubes = green_cube_amount
        self.blue_cubes = blue_cube_amount

    def check_game_set_valid(self, red_cubes, green_cubes, blue_cubes) -> bool:
        if self.red_cubes > red_cubes:
            return False

        if self.green_cubes > green_cubes:
            return False

        if self.blue_cubes > blue_cubes:
            return False

        return True

class CubeGame():
    def __init__(self, game_id: int) -> None:
        self.game_id = game_id
        self.sets = []

    def add_game_set(self, gameset: CubeGameSet) -> None:
        self.sets.append(gameset)

    def check_game_sets_valid_by_configuration(self, red_cubes, green_cubes, blue_cubes) -> bool:
        for set in self.sets:
            if not set.check_game_set_valid(red_cubes, green_cubes, blue_cubes):
                return False
        return True

    # PART TWO - addition
    def calculate_fewest_cubes_score_valid_game(self) -> int:
        if not self.sets:
            raise RuntimeError("This game has no sets available")

        red_cubes = self.sets[0].red_cubes
        green_cubes = self.sets[0].green_cubes
        blue_cubes = self.sets[0].blue_cubes

        for i in range(1, len(self.sets)):
            if self.sets[i].red_cubes > red_cubes:
                red_cubes = self.sets[i].red_cubes

            if self.sets[i].green_cubes > green_cubes:
                green_cubes = self.sets[i].green_cubes

            if self.sets[i].blue_cubes > blue_cubes:
                blue_cubes = self.sets[i].blue_cubes

        return red_cubes * green_cubes * blue_cubes

def process_input_file(input_file: str, line_processor: Callable) -> List[Any]:
    result_list = []

    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            line
            result_list.append(line_processor(line.strip()))
            line = f.readline()
    return result_list

def get_cube_amount_from_set_string(colour: str, set_string: str) -> int:
    res = re.search(f'(\d+) {colour}', set_string)
    if res:
        return int(res.groups()[0])
    return 0

def convert_line_into_cube_game(line: str) -> CubeGame:
    game_string, set_strings = line.split(':')

    game_id = re.findall(r'\d+', game_string)[0]
    cube_game = CubeGame(int(game_id))
    set_strings = set_strings.split(';')

    for set_string in set_strings:
        red_cubes = get_cube_amount_from_set_string('red', set_string)
        green_cubes = get_cube_amount_from_set_string('green', set_string)
        blue_cubes = get_cube_amount_from_set_string('blue', set_string)
        cube_game_set = CubeGameSet(red_cube_amount=red_cubes, green_cube_amount=green_cubes, blue_cube_amount=blue_cubes)
        cube_game.add_game_set(cube_game_set)

    return cube_game

# PART ONE

CUBE_CONFIGURATION = {
    'red': 12,
    'green': 13,
    'blue': 14
}

def process_input_line_p1(line: str) -> Any:
    return convert_line_into_cube_game(line)

def process_result_list_p1(result_list: List[CubeGame]) -> int:
    game_ids = []
    for cube_game in result_list:
        if cube_game.check_game_sets_valid_by_configuration(
            CUBE_CONFIGURATION['red'], CUBE_CONFIGURATION['green'], CUBE_CONFIGURATION['blue']):
            game_ids.append(cube_game.game_id)

    return sum(game_ids)

# PART TWO

def process_input_line_p2(line: str) -> Any:
    return convert_line_into_cube_game(line)

def process_result_list_p2(result_list: List[Any]) -> Any:
    minimal_game_scores = []
    for cube_game in result_list:
        minimal_game_scores.append(cube_game.calculate_fewest_cubes_score_valid_game())

    return sum(minimal_game_scores)

# MAIN

print("Part 1 - Answer")
print(process_result_list_p1(process_input_file('input.txt', process_input_line_p1)))
print("-----------------\n")

print("Part 2 - Answer")
print(process_result_list_p2(process_input_file('input.txt', process_input_line_p2)))
print("-----------------\n")
