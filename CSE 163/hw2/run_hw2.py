import pandas as pd

import cse163_utils
import hw2_manual
import hw2_pandas


DATA = 'pokemon_box.csv'


def part0():
    """
    Calculates various statistics about the Pokemon dataset using
    the implementation in Part 0.
    """
    print('=== Starting Part 0 ===')
    data = cse163_utils.parse(DATA)

    print('Number of species:', hw2_manual.species_count(data))
    print('Highest level pokemon:', hw2_manual.max_level(data))
    print('Low-level Pokemon', hw2_manual.filter_range(data, 1, 9))
    print('Average attack for fire types',
          hw2_manual.mean_attack_for_type(data, 'fire'))
    print('Count of each Pokemon type:')
    print(hw2_manual.count_types(data))
    print('Highest stage for each Pokemon type')
    print(hw2_manual.highest_stage_per_type(data))
    print('Average attack for each Pokemon type')
    print(hw2_manual.mean_attack_per_type(data))


def part1():
    """
    Calculates various statistics about the Pokemon dataset using
    the implementation in Part 1.
    """
    print('=== Starting Part 1 ===')
    data = pd.read_csv(DATA)

    print('Number of species:', hw2_pandas.species_count(data))
    print('Highest level pokemon:', hw2_pandas.max_level(data))
    print('Low-level Pokemon',  hw2_pandas.filter_range(data, 1, 9))
    print('Average attack for fire types',
          hw2_pandas.mean_attack_for_type(data, 'fire'))
    print('Count of each Pokemon type:')
    print(hw2_pandas.count_types(data))
    print('Highest stage for each Pokemon type')
    print(hw2_pandas.highest_stage_per_type(data))
    print('Average attack for each Pokemon type')
    print(hw2_pandas.mean_attack_per_type(data))


def main():
    part0()
    print()
    print()
    part1()


if __name__ == '__main__':
    main()
