"""
Khoa Tran
CSE 163 AB

This program performs analysis on a given Pokemon data file,
giving various information like average attack levels for a particular type
or number of species and much more. This program immplements the panda
library in order to compute the statistics.
"""


def species_count(data):
    """
    Returns the number of unique species in the
    given file
    """
    result = data['name'].unique()
    return len(result)


def max_level(data):
    """
    Returns a tuple with the name and level of the Pokemon
    that has the highest level
    """
    index = data['level'].idxmax()
    result = (data.loc[index, 'name'], data.loc[index, 'level'])
    return result


def filter_range(data, low, high):
    """
    Returns a list of Pokemon names having a level that is
    larger or equal to the lower given range and less than
    the higher given range
    """
    temp = data[(data['level'] >= low) & (data['level'] < high)]
    return list(temp['name'])


def mean_attack_for_type(data, type):
    """
    Returns the average attack for all Pokemon
    in dataset with the given type

    Special Case: If the dataset does not contain the given type,
    returns 'None'
    """
    temp = data.groupby('type')['atk'].mean()
    if type not in temp.index:
        return None
    else:
        return temp[type]


def count_types(data):
    """
    Returns a dictionary of Pokemon with the types
    as the keys and the values as the corresponding
    number of times that the type appears in the dataset
    """
    temp = data.groupby('type')['type'].count()
    return dict(temp)


def highest_stage_per_type(data):
    """
    Returns a dictionary with the key as the type of
    Pokemon and the value as the highest stage reached for
    the corresponding type in the dataset
    """
    temp = data.groupby('type')['stage'].max()
    return dict(temp)


def mean_attack_per_type(data):
    """
    Returns a dictionary with the key as the type of Pokemon
    and the value as the average attack for
    the corresponding Pokemon type in the dataset
    """
    temp = data.groupby('type')['atk'].mean()
    return dict(temp)
