import fractions

import numpy as np

import common

def grid_to_list(grid):
    asteroids = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j]:
                asteroids.append((j, i))

    return asteroids


def get_all_directions(station, asteroids):
    all_directions = []
    for asteroid in asteroids:
        if asteroid == station:
            continue
        direction = (asteroid[0] - station[0], asteroid[1] - station[1])
        if direction[1] == 0:
            rational_direction = ('h', (direction[0]) > 0)
        else:
            rational_direction = (fractions.Fraction(direction[0], direction[1]), (direction[1] > 0))
        if rational_direction in all_directions:
            continue
        else:
            all_directions.append(rational_direction)

    return all_directions


def order_all_asteroids(station, asteroids):
    all_asteroids = []
    for asteroid in asteroids:
        if asteroid == station:
            continue
        direction = (asteroid[0] - station[0], asteroid[1] - station[1])

        angle = np.pi - np.arctan2(direction[0], direction[1])
        range = direction[0] ** 2 + direction[1] ** 2

        all_asteroids.append([range, angle, 0])

    unique_angles = np.unique([a[1] for a in all_asteroids])
    count = 1
    while count < len(asteroids):
        for angle in unique_angles:
            matching_angles = [a for a in all_asteroids if (a[1] == angle) and (a[2] == 0)]
            if len(matching_angles) == 0:
                continue
            else:
                ranges = [a[0] for a in matching_angles]
                index = np.argmin(ranges)
                matching_angles[index][2] = count
                count = count + 1

    return all_asteroids


def count_visible(station, asteroids):
    all_directions = get_all_directions(station, asteroids)
    return len(all_directions)


def find_best_station(asteroids):
    best_count = 0
    best_station = None
    for station in asteroids:
        count = count_visible(station, asteroids)
        if count > best_count:
            best_count = count
            best_station = station

    return best_count, best_station


if __name__ == "__main__":
    text = common.import_file("../input/day10")
    grid = common.convert_string_to_np_array(text, {".": 0, "#": 1})
    asteroids = grid_to_list(grid)
    count, best_station = find_best_station(asteroids)

    print(f"Best station: {best_station}")
    all_asteroids = order_all_asteroids(best_station, asteroids)
    for xy, rtheta in zip(asteroids, all_asteroids):
        if rtheta[2] == 200:
            print(f"200th direction: {xy}")
            break