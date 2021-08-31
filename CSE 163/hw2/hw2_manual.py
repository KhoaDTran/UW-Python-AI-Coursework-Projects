"""
Khoa Tran
CSE 163 AB

This program performs analysis on a given Pokemon data file,
giving various information like average attack levels for a particular type
or number of species and much more.
"""


def species_count(data):
    """
    Returns the number of unique species in the
    given file
    """
    result = set()
    for species in data:
        result.add(species['name'])
    return len(result)


def max_level(data):
    """
    Returns a tuple with the name and level of the Pokemon
    that has the highest level
    """
    level = data[0]
    for species in data:
        if species['level'] > level['level']:
            level = species
    return (level['name'], level['level'])


def filter_range(data, low, high):
    """
    Returns a list of Pokemon names having a level that is
    larger or equal to the lower given range and less than
    the higher given range
    """
    result = []
    for species in data:
        if species['level'] >= low and species['level'] < high:
            result.append(species['name'])
    return result


def mean_attack_for_type(data, string):
    """
    Returns the average attack for all Pokemon
    in dataset with the given type

    Special Case: If the dataset does not contain the given type,
    returns 'None'
    """
    count = 0
    attack_total = 0
    for species in data:
        if species['type'] == string:
            attack_total += species['atk']
            count += 1
    if count == 0:
        return None
    else:
        return attack_total / count


def count_types(data):
    """
    Returns a dictionary of Pokemon with the types
    as the keys and the values as the corresponding
    number of times that the type appears in the dataset
    """
    result = dict()
    for species in data:
        if species['type'] in result:
            result[species['type']] += 1
        else:
            result[species['type']] = 1
    return result


def highest_stage_per_type(data):
    """
    Returns a dictionary with the key as the type of
    Pokemon and the value as the highest stage reached for
    the corresponding type in the dataset
    """
    result = dict()
    for species in data:
        if species['type'] in result:
            if result[species['type']] < species['stage']:
                result[species['type']] = species['stage']
        else:
            result[species['type']] = species['stage']
    return result


def mean_attack_per_type(data):
    """
    Returns a dictionary with the key as the type of Pokemon
    and the value as the average attack for
    the corresponding Pokemon type in the dataset
    """
    total_attack = dict()
    result = dict()
    type_count = count_types(data)
    for species in data:
        if species['type'] in total_attack:
            total_attack[species['type']] += species['atk']
        else:
            total_attack[species['type']] = species['atk']
    for pokemon in total_attack.keys():
        result[pokemon] = total_attack[pokemon] / type_count[pokemon]
    return result
