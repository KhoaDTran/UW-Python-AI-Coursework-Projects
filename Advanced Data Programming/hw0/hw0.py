"""
Khoa Tran
CSE 163 AB

Implements the functions funky_sum
and total for HW0
"""


def funky_sum(a, b, mix):
    """
    Function that takes in three number inputs
    and implements linear interpolation by
    taking the last number and based on it, returns either
    the first or second number or a calculated number
    from an equation with all three inputs
    """
    if mix <= 0:
        return a
    elif mix >= 1:
        return b
    else:
        return ((1 - mix) * a) + (mix * b)


def total(n):
    """
    Function that takes in a number input
    and returns None if the number is negative,
    if not, return the sum of the integers
    from 0 to the given integer(inclusive)
    """
    if n < 0:
        return None
    else:
        result = 0
        for i in range(n + 1):
            result += i
        return result


def swip_swap(source, c1, c2):
    """
    Function that takes a string input and
    two different characters and returns
    the string with all occurences of the
    given characters swapped.
    """
    list = []
    for i in range(len(source)):
        if source[i] == c1:
            list.append(c2)
        elif source[i] == c2:
            list.append(c1)
        else:
            list.append(source[i])
    return ''.join(list)
