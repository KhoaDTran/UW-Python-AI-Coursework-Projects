import re
import math

def is_multiple_of_9(n):
    """Return True if n is a multiple of 9; False otherwise."""
    if n % 9 == 0:
        return True
    else:
        return False


def next_prime(m):
    """Return the first prime number p that is greater than m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    temp = False
    while not temp:
        isPrime = True
        m += 1
        for i in range(2, m):
            if m % i == 0:
                isPrime = False
        if isPrime == True:
            temp = True
    return m


def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    if ((b**2) - (4 * a * c)) < 0:
        return "complex"
    x = ((-1*b) + math.sqrt((b**2) - (4 * a * c))) / (2 * a)
    y = ((-1*b) - math.sqrt((b**2) - (4 * a * c))) / (2 * a)
    return (x, y)


def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    For example, [0, 1, 2, 3, 4, 5, 6, 7] => [0, 4, 1, 5, 2, 6, 3, 7]"""
    result = []
    split = len(even_list)//2
    first_part = even_list[0:split]
    second_part = even_list[split:]
    for i in range(len(even_list)):
        if i % 2 == 0:
            result.append(first_part[i//2])
        else:
            result.append(second_part[i//2])
    return result


def triples_list(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 3."""
    return [x * 3 for x in input_list]


def double_consonants(text):
    """Return a new version of text, with all the consonants doubled.
    For example:  "The *BIG BAD* wolf!" => "TThhe *BBIGG BBADD* wwollff!"
    For this exercise assume the consonants are all letters OTHER
    THAN A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    result = ""
    vowels = ["a", "e", "i", "o", "u"]
    for i in text:
        if i.lower() not in vowels and i.isalpha():
            result += i
            result += i
        else:
            result += i
    return result


def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', '*', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ]  ).
    Convert all the letters to lower-case before the counting."""
    text = text.strip()
    result = dict()
    lowText = text.lower()
    words = re.split('\s|\n|]|[|[.,"!$?^><`&;:=_~{}()\\\\]', lowText)
    list = [i for i in words if i]
    for item in list:
        if item not in result.keys():
            result[item] = 1
        else:
            result[item] += 1
    return result

def make_cubic_evaluator(a, b, c, d):
    """When called with 4 numbers, returns a function of one variable (x)
    that evaluates the cubic polynomial
    a x^3 + b x^2 + c x + d.
    For this exercise Your function definition for make_cubic_evaluator
    should contain a lambda expression."""
    return lambda x : (a*(x**3)) + (b * x ** 2) + (c*x) + d

class Polygon:
    """Polygon class."""
    def __init__(self, n_sides, lengths=None, angles=None):
        self._number_sides = n_sides
        self._side_lengths = lengths
        self._angles_list = angles

    def is_rectangle(self):
        if (self._number_sides == 4):
            if self._angles_list == None:
                return None
            else:
                for angle in self._angles_list:
                    if angle != 90:
                        return False
                return True
        else:
            return False

    def is_rhombus(self):
        if (self._number_sides != 4):
            return False
        if(self._number_sides == 4 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._angles_list == None and self._side_lengths == None):
            return None
        elif (self._angles_list == None and self._number_sides == 4 and (self._side_lengths is not None)):
            temp3 = []
            temp3.append(self._side_lengths[0])
            for length in range(1, len(self._side_lengths)):
                if self._side_lengths[length] not in temp3:
                    return False
                temp3.append(self._side_lengths[length])
            return True
        else:
            if (self._side_lengths is not None):
                temp = []
                temp.append(self._side_lengths[0])
                for length in range(1, len(self._side_lengths)):
                    if self._side_lengths[length] not in temp:
                        return False
                    temp.append(self._side_lengths[length])
                return True

    def is_square(self):
        if (self._number_sides != 4):
            return False
        if(self._number_sides == 4 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._angles_list == None and self._side_lengths == None):
            return None
        elif (self._angles_list == None and self._number_sides == 4 and (self._side_lengths is not None)):
            temp = []
            temp.append(self._side_lengths[0])
            for length in range(1, len(self._side_lengths)):
                if self._side_lengths[length] not in temp:
                    return False
                temp.append(self._side_lengths[length])
            return None
        elif (self._angles_list != None and self._number_sides == 4 and self._side_lengths == None):
            temp2 = []
            temp2.append(self._angles_list[0])
            for angle in range(1, len(self._angles_list)):
                if self._angles_list[angle] not in temp2:
                    return False
                temp2.append(self._angles_list[angle])
            return None
        elif ((self._side_lengths is not None) and (self._angles_list is not None)):
            temp = []
            temp.append(self._side_lengths[0])
            for angle in self._angles_list:
                if angle != 90:
                    return False
            for length in range(1, len(self._side_lengths)):
                if self._side_lengths[length] not in temp:
                    return False
                temp.append(self._side_lengths[length])   
            return True

    def is_regular_hexagon(self):
        if (self._number_sides != 6):
            return False
        if(self._number_sides == 6 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._angles_list == None and self._side_lengths == None):
            return None
        elif (self._angles_list == None and self._number_sides == 6 and self._side_lengths != None):
            temp = []
            temp.append(self._side_lengths[0])
            for length in range(1, len(self._side_lengths)):
                if self._side_lengths[length] not in temp:
                    return False
                temp.append(self._side_lengths[length])
            return None
        elif (self._angles_list != None and self._number_sides == 6 and self._side_lengths == None):
            temp2 = []
            temp2.append(self._angles_list[0])
            for angle in range(1, len(self._angles_list)):
                if self._angles_list[angle] not in temp2:
                    return False
                temp2.append(self._angles_list[angle])
            return None
        elif ((self._side_lengths is not None) and (self._angles_list is not None)):
            temp = []
            temp2 = []
            temp.append(self._side_lengths[0])
            temp2.append(self._angles_list[0])
            for angle in range(1, len(self._angles_list)):
                if self._angles_list[angle] not in temp2:
                    return False
                temp2.append(self._angles_list[angle])
            for length in range(1, len(self._side_lengths)):
                if self._side_lengths[length] not in temp:
                    return False
                temp.append(self._side_lengths[length])
            return True

    def is_isosceles_triangle(self):
        if(self._number_sides == 3 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._number_sides != 3):
            return False
        else:
            if (self._angles_list == None):
                temp = dict()
                for length in self._side_lengths:
                    if length not in temp.keys():
                        temp[length] = 1
                    else:
                        temp[length] += 1
                test2 = False
                for value in temp.values():
                    if value >= 2:
                        test2 = True
                return (test2)
            else:
                temp2 = dict()
                for angle in self._angles_list:
                    if angle not in temp2.keys():
                        temp2[angle] = 1
                    else:
                        temp2[angle] += 1
                test = False
                for value2 in temp2.values():
                    if value2 >= 2:
                        test = True
                return (test)
            
    def is_equilateral_triangle(self):
        if(self._number_sides == 3 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._number_sides != 3):
            return False
        else:
            if (self._angles_list == None):
                temp = dict()
                for length in self._side_lengths:
                    if length not in temp.keys():
                        temp[length] = 1
                    else:
                        temp[length] += 1
                test2 = False
                for value in temp.values():
                    if value == 3:
                        test2 = True
                return (test2)
            else:
                temp2 = dict()
                for angle in self._angles_list:
                    if angle not in temp2.keys():
                        temp2[angle] = 1
                    else:
                        temp2[angle] += 1
                test = False
                for value2 in temp2.values():
                    if value2 == 3:
                        test = True
                return (test)
        

    def is_scalene_triangle(self):
        if(self._number_sides == 3 and self._angles_list == None and self._side_lengths == None):
            return None
        if (self._number_sides != 3):
            return False
        return not self.is_isosceles_triangle()
        # else:
        #     temp = dict()
        #     temp2 = dict()
        #     for length in self._side_lengths:
        #         if length not in temp.keys():
        #             temp[length] = 1
        #         else:
        #             temp[length] += 1
        #     for angle in self._angles_list:
        #         if angle not in temp2.keys():
        #             temp2[angle] = 1
        #         else:
        #             temp2[angle] += 1
        #     test = True
        #     test2 = True
        #     for value2 in temp2.values():
        #         if value2 != 1:
        #             test = False
        #     for value in temp.values():
        #         if value != 1:
        #             test2 = False
        #     return (test and test2)