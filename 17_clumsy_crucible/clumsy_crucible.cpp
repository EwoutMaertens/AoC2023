#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
#include <vector>
#include <queue>

enum Direction {
    E = 0,
    S = 1,
    W = 2,
    N = 3,
    Last
};
const int DIRECTION_VECTORS[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

class CityBlock {
    public:
        int heat_reduce;
        int distance;
        bool visited;
        CityBlock(int heat_reduce): heat_reduce(heat_reduce), visited(false), distance(-1) {};
};

class WorkItem {
    public:
        int row;
        int col;
        Direction direction;
        int straight;
        int distance;
        WorkItem(int row, int col, Direction direction, int straight, int distance) :
            row(row), col(col), direction(direction), straight(straight), distance(distance) {};
};

void print_2d_cityblock_matrix(std::vector<std::vector<CityBlock>> &matrix) {
    for (int y = 0; y < matrix.size(); y++) {
        for (int x = 0; x < matrix[y].size(); x++) {
            std::cout << std::setw(4) << std::setfill(' ') << matrix[y][x].heat_reduce;
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void print_2d_cityblock_matrix_scores(std::vector<std::vector<CityBlock>> &matrix) {
    for (int y = 0; y < matrix.size(); y++) {
        for (int x = 0; x < matrix[y].size(); x++) {
            std::cout << std::setw(4) << std::setfill(' ') << matrix[y][x].distance;
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

std::vector<std::vector<CityBlock>> process_input_file(const std::string &input_file) {
    std::ifstream input_stream(input_file);
    if (! input_stream) {
        std::cout << "Error, file couldn't be opened" << std::endl;
    }

    std::vector<std::vector<CityBlock>> city_map;
    std::string line;
    int y = 0;
    while (std::getline(input_stream, line)) {
        std::vector<CityBlock> city_map_line;
        for (int x = 0; x < line.length(); x++) {
            city_map_line.push_back(CityBlock(int(line[x]) - int('0')));
        }
        city_map.push_back(city_map_line);
        y++;
    }

    print_2d_cityblock_matrix(city_map);

    return city_map;
}

/* PART 1 */

bool check_element_in_grid(const std::vector<std::vector<CityBlock>> &city_map, int row, int col) {
    if (0 <= row and row < city_map.size() and 0 <= col and col < city_map[row].size()) {
        return true;
    }
    return false;
}

int solve_part_1(std::vector<std::vector<CityBlock>> &city_map) {
    std::queue<WorkItem> city_blocks_to_check;

    int start_row = 0;
    int start_col = 0;
    city_blocks_to_check.push(WorkItem(start_row, start_row, N, 0, 0));

    while (!city_blocks_to_check.empty()) {
        WorkItem work_item = city_blocks_to_check.front();
        city_blocks_to_check.pop();

        std::cout << "Checking: " << work_item.row << " , " << work_item.col << std::endl;
        if (city_map[work_item.row][work_item.col].distance == -1 and work_item.straight < 3 or
                city_map[work_item.row][work_item.col].distance > work_item.distance and
                work_item.straight < 3) {
            std::cout << "Node distance vs current route distance: " << city_map[work_item.row][work_item.col].distance << " - " << work_item.distance << std::endl;
            city_map[work_item.row][work_item.col].distance = work_item.distance;
            for (int dir = E; dir != Last; dir++) {
                int drow = DIRECTION_VECTORS[dir][0];
                int dcol = DIRECTION_VECTORS[dir][1];
                int new_row = work_item.row + drow;
                int new_col = work_item.col + dcol;

                if (check_element_in_grid(city_map, new_row, new_col)) {
                    int next_heat = city_map[new_row][new_col].heat_reduce;
                    int new_straight = work_item.direction == static_cast<Direction>(dir) ? work_item.straight + 1 : 0;
                    std::cout << new_straight << std::endl;
                    city_blocks_to_check.push(WorkItem(new_row, new_col, static_cast<Direction>(dir), new_straight, work_item.distance + next_heat));
                }
            }
        }
    }

    return city_map[city_map.size()-1][city_map[0].size()-1].distance;
}

int main() {
    std::vector<std::vector<CityBlock>> city_map = process_input_file("sample.txt");
    int score = solve_part_1(city_map);

    std::cout << "Score for Sample 1 is " << score << std::endl;

    print_2d_cityblock_matrix(city_map);
    print_2d_cityblock_matrix_scores(city_map);


    // city_map = process_input_file("input.txt");
    // score = solve_part_1(city_map);

    // std::cout << "Score for Input 1 is " << score << std::endl;

    return 0;
}