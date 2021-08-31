"""
Khoa Tran
CSE 163 AB

Program that implements the solution code for various problems presented
"""


def total(n):
    """
    Returns the sum of the numbers from 0 to n (inclusive).
    If n is negative, returns None.
    """
    if n < 0:
        return None
    else:
        result = 0
        for i in range(n + 1):
            result += i
        return result


def count_divisible_digits(n, m):
    """
    Returns the number of digits in the given number that are divisible
    by the other given number
    """
    result = 0
    if m == 0:
        return 0
    n = abs(n)
    while n != 0:
        temp = n % 10
        if temp % m == 0:
            result += 1
        n = n // 10
    return result


def is_relatively_prime(n, m):
    """
    Returns whether two numbers are prime relative to one another,
    meaning if the only common factor is "1" between the two numbers,
    function returns True
    """
    result = True
    larger = n
    if m > n:
        larger = m
    for i in range(1, larger + 1):
        if n % i == 0 and m % i == 0:
            if i == 1:
                result = True
            else:
                result = False
    return result


def travel(direction, x, y):
    """
    Returns a final coordinate of x and y
    based on given instructions of cardinal directions
    from the given string
    """
    x_new = x
    y_new = y
    for i in range(len(direction)):
        test = direction[i].lower()
        if test == 'n':
            y_new += 1
        elif test == 's':
            y_new -= 1
        elif test == 'e':
            x_new += 1
        elif test == 'w':
            x_new -= 1
    return (x_new, y_new)


def compress(word):
    """
    Returns a string in which each letter is followed by count of
    the same characters adjacent to it from the passed string
    """
    temp = []
    for i in range(len(word)):
        if word[i] in temp and word[i] == word[i - 1]:
            if temp[len(temp) - 2] == word[i]:
                last = int(temp[len(temp) - 1]) + 1
                temp[len(temp) - 1] = str(last)
            else:
                num = temp.index(word[i]) + 1
                val = int(temp[num]) + 1
                temp[num] = str(val)
        else:
            temp.append(word[i])
            temp.append(str(1))
    return ''.join(temp)


def longest_line_length(file_name):
    """
    Returns the length of the longest line in given file.
    Returns None if the file is empty
    """
    result = 0
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > result:
                result = len(line)
    if result <= 1:
        return None
    else:
        return result


def longest_word(file_name):
    """
    Returns the longest word in a file and along with its line number.
    Returns None if the file is empty
    """
    longest = 0
    linenum = 0
    finalnum = 0
    result = ''
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            linenum += 1
            words = line.split()
            for word in words:
                if len(word) > longest:
                    longest = len(word)
                    result = word
                    finalnum = linenum
    if longest == 0:
        return None
    return str(finalnum) + ': ' + result


def get_average_in_range(list, low, high):
    """
    Returns the average of the digits in the given list
    that is in the range between the given low (inclusive)
    and the high (exclusive) integers
    """
    track = 0
    val = 0
    for num in list:
        if num >= low and num < high:
            val += num
            track += 1
    if track == 0:
        return 0
    return val / track


def mode_digit(n):
    """
    Returns the digit that most commonly occur in given integer
    """
    temp = dict()
    result = 0
    most = 0
    n = abs(n)
    while n != 0:
        val = n % 10
        if val in temp:
            temp[val] += 1
        else:
            temp[val] = 1
        n = n // 10
    for k, v in temp.items():
        if v >= most:
            if v == most:
                if k > result:
                    result = k
            else:
                most = v
                result = k
    return result
