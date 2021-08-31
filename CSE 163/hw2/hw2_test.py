"""
Khoa Tran
CSE 163 AB

This program is the client tester for the two imported data anaylsis
classes, in order to test the output from the Pokemon dataset.
This test both the panda library class and non-panda class,
with the two different datasets.
"""
import pandas as pd

# You can call the method using
#    assert_equals(expected, received)
#    parse(file)
from cse163_utils import assert_equals, parse

import hw2_manual
import hw2_pandas

nopanda_data1 = parse('/home/pokemon_test.csv')
panda_data1 = pd.read_csv('/home/pokemon_test.csv')
nopanda_data2 = parse('/home/pokemon_test2.csv')
panda_data2 = pd.read_csv('/home/pokemon_test2.csv')


def test_nopanda_data1():
    """
    Tests the various functions in the non-panda class for
    accurately extracting data from the dataset.
    The input file is a given CSV file called pokemon_test.
    """
    # Given test
    assert_equals(3, hw2_manual.species_count(nopanda_data1))
    assert_equals(('Lapras', 72), hw2_manual.max_level(nopanda_data1))
    assert_equals(['Arcanine', 'Arcanine', 'Starmie'],
                  hw2_manual.filter_range(nopanda_data1, 30, 70))
    assert_equals(47.5, hw2_manual.mean_attack_for_type
                  (nopanda_data1, 'fire'))
    assert_equals({'fire': 2, 'water': 2},
                  hw2_manual.count_types(nopanda_data1))
    assert_equals({'fire': 2, 'water': 2},
                  hw2_manual.highest_stage_per_type(nopanda_data1))
    assert_equals({'fire': 47.5, 'water': 140.5},
                  hw2_manual.mean_attack_per_type(nopanda_data1))


def test_panda_data1():
    """
    Tests the various functions in the panda class for
    accurately extracting data from the dataset.
    The input file is a given CSV file called pokemon_test.
    """
    # Given test
    assert_equals(3, hw2_pandas.species_count(panda_data1))
    assert_equals(('Lapras', 72), hw2_pandas.max_level(panda_data1))
    assert_equals(['Arcanine', 'Arcanine', 'Starmie'],
                  hw2_pandas.filter_range(panda_data1, 30, 70))
    assert_equals(47.5, hw2_pandas.mean_attack_for_type
                  (panda_data1, 'fire'))
    assert_equals({'fire': 2, 'water': 2},
                  hw2_pandas.count_types(panda_data1))
    assert_equals({'fire': 2, 'water': 2},
                  hw2_pandas.highest_stage_per_type(panda_data1))
    assert_equals({'fire': 47.5, 'water': 140.5},
                  hw2_pandas.mean_attack_per_type(panda_data1))


def test_nopanda_data2():
    """
    Tests the various functions in the non-panda class for
    accurately extracting data from the dataset.
    The input file is a create CSV file called pokemon_test2.
    """
    # Additional test
    assert_equals(11, hw2_manual.species_count(nopanda_data2))
    assert_equals(('Magmar', 96), hw2_manual.max_level(nopanda_data2))
    assert_equals(['Persian', 'Magmar', 'Kingler', 'Venusaur'],
                  hw2_manual.filter_range(nopanda_data2, 20, 45))
    assert_equals(None, hw2_manual.mean_attack_for_type
                  (nopanda_data1, 'fighting'))
    assert_equals({'normal': 2, 'fire': 2, 'water': 1, 'grass': 3,
                  'poison': 1, 'bug': 2, 'fairy': 1},
                  hw2_manual.count_types(nopanda_data2))
    assert_equals({'normal': 2, 'fire': 1, 'water': 2, 'grass': 3,
                  'poison': 1, 'bug': 3, 'fairy': 1},
                  hw2_manual.highest_stage_per_type(nopanda_data2))
    assert_equals({'normal': 86.0, 'fire': 79.0, 'water': 110.0,
                  'grass': 105.0, 'poison': 30.0,
                   'bug': 13.5, 'fairy': 33.0},
                  hw2_manual.mean_attack_per_type(nopanda_data2))


def test_panda_data2():
    """
    Tests the various functions in the panda class for
    accurately extracting data from the dataset.
    The input file is a create CSV file called pokemon_test2.
    """
    # Additional test
    assert_equals(11, hw2_pandas.species_count(panda_data2))
    assert_equals(('Magmar', 96), hw2_pandas.max_level(panda_data2))
    assert_equals(['Persian', 'Magmar', 'Kingler', 'Venusaur'],
                  hw2_pandas.filter_range(panda_data2, 20, 45))
    assert_equals(None, hw2_pandas.mean_attack_for_type
                  (panda_data1, 'fighting'))
    assert_equals({'normal': 2, 'fire': 2, 'water': 1, 'grass': 3,
                  'poison': 1, 'bug': 2, 'fairy': 1},
                  hw2_pandas.count_types(panda_data2))
    assert_equals({'normal': 2, 'fire': 1, 'water': 2, 'grass': 3,
                  'poison': 1, 'bug': 3, 'fairy': 1},
                  hw2_pandas.highest_stage_per_type(panda_data2))
    assert_equals({'normal': 86.0, 'fire': 79.0,
                  'water': 110.0, 'grass': 105.0, 'poison': 30.0,
                   'bug': 13.5, 'fairy': 33.0},
                  hw2_pandas.mean_attack_per_type(panda_data2))


def main():
    test_nopanda_data1()
    test_panda_data1()
    test_nopanda_data2()
    test_panda_data2()


if __name__ == '__main__':
    main()
