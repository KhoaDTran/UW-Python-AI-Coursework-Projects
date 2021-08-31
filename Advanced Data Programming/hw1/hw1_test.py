"""
Khoa Tran
CSE 163 AB

Tests the functions in the program hw1
"""


import hw1

from cse163_utils import assert_equals


def test_total():
    """
    Tests the total method in hw1
    """
    # The regular case
    assert_equals(15, hw1.total(5))
    # Seems likely we could mess up 0 or 1
    assert_equals(1, hw1.total(1))
    assert_equals(0, hw1.total(0))
    # Test the None case
    assert_equals(None, hw1.total(-1))


def test_count_divisible_digits():
    """
    Tests the count_divisible_digits method in hw1
    """
    # Spec test
    assert_equals(4, hw1.count_divisible_digits(650899, 3))
    assert_equals(1, hw1.count_divisible_digits(-204, 5))
    assert_equals(0, hw1.count_divisible_digits(24, 5))
    assert_equals(0, hw1.count_divisible_digits(1, 0))
    # Addtional test
    assert_equals(3, hw1.count_divisible_digits(123456, 2))
    assert_equals(6, hw1.count_divisible_digits(765853, 1))


def test_is_relatively_prime():
    """
    Tests the is_relatively_prime method in hw1
    """
    # Spec test
    assert_equals(True, hw1.is_relatively_prime(12, 13))
    assert_equals(False, hw1.is_relatively_prime(12, 14))
    assert_equals(True, hw1.is_relatively_prime(5, 9))
    assert_equals(True, hw1.is_relatively_prime(8, 9))
    assert_equals(True, hw1.is_relatively_prime(8, 1))
    # Addtional test
    assert_equals(True, hw1.is_relatively_prime(17, 15))
    assert_equals(False, hw1.is_relatively_prime(8, 4))


def test_travel():
    """
    Tests the travel method in hw1
    """
    # Spec test
    assert_equals((-1, 4), hw1.travel('NW!ewnW', 1, 2))
    # Addtional test
    assert_equals((3, 2), hw1.travel('senW..N', 3, 1))
    assert_equals((-3, 3), hw1.travel('NnnwwW', 0, 0))


def test_compress():
    """
    Tests the compress method in hw1
    """
    # Spec test
    assert_equals('c1o17l1k1a1n1g1a1r1o3',
                  hw1.compress('cooooooooooooooooolkangarooo'))
    assert_equals('a3', hw1.compress('aaa'))
    assert_equals('', hw1.compress(''))
    # Addtional test
    assert_equals('c1a1b2a1g1e1', hw1.compress('cabbage'))
    assert_equals('b4a2o1r1o3', hw1.compress('bbbbaaorooo'))


def test_longest_line_length():
    """
    Tests the longest_line_length method in hw1
    """
    # Spec test
    assert_equals(35, hw1.longest_line_length('/home/song.txt'))
    # Addtional test
    assert_equals(None, hw1.longest_line_length('/home/empty.txt'))
    assert_equals(15, hw1.longest_line_length('/home/oneliner.txt'))


def test_longest_word():
    """
    Tests the longest_word method in hw1
    """
    # Spec test
    assert_equals('3: Merrily,', hw1.longest_word('/home/song.txt'))
    # Addtional test
    assert_equals(None, hw1.longest_word('/home/empty.txt'))
    assert_equals('1: everyone', hw1.longest_word('/home/oneliner.txt'))


def test_get_average_in_range():
    """
    Tests the get_average_in_range method in hw1
    """
    # Spec test
    assert_equals(5.5, hw1.get_average_in_range([1, 5, 6, 7, 9], 5, 7))
    assert_equals(2.0, hw1.get_average_in_range([1, 2, 3], -1, 10))
    # Addtional test
    assert_equals(2, hw1.get_average_in_range([1, 3, 4, 2], 1, 4))
    assert_equals(5, hw1.get_average_in_range([4, 3, 5, 6, 7, 9], 3, 8))
    assert_equals(0, hw1.get_average_in_range([], 3, 8))
    assert_equals(0, hw1.get_average_in_range([4, 3, 5, 6, 7, 9], 8, 2))


def test_mode_digit():
    """
    Tests the mode_digit method in hw1
    """
    # Spec test
    assert_equals(1, hw1.mode_digit(12121))
    assert_equals(0, hw1.mode_digit(0))
    assert_equals(2, hw1.mode_digit(-122))
    assert_equals(2, hw1.mode_digit(1211232231))
    # Addtional test
    assert_equals(6, hw1.mode_digit(-32566))
    assert_equals(3, hw1.mode_digit(222333))


def main():
    test_total()
    test_count_divisible_digits()
    test_is_relatively_prime()
    test_travel()
    test_compress()
    test_longest_line_length()
    test_longest_word()
    test_get_average_in_range()
    test_mode_digit()


if __name__ == '__main__':
    main()
