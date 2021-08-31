"""
Khoa Tran
CSE 163 AB

A file to test the outputs of the methods in
HW0. Checks if funky_sum() and total() operates
without any issues.
"""


import hw0
from cse163_utils import assert_equals


def test_funky_sum():
    """
    Checks if the function funky_sum in hw0 outputs
    the desired output
    """
    # Spec test
    assert_equals(2, hw0.funky_sum(1, 3, 0.5))
    assert_equals(1, hw0.funky_sum(1, 3, 0))
    assert_equals(3, hw0.funky_sum(1, 3, 1))
    # Addtional test
    assert_equals(3, hw0.funky_sum(2, 6, 0.25))
    assert_equals(4.2, hw0.funky_sum(3, 5, 0.6))
    assert_equals(6.5, hw0.funky_sum(5, 8, 0.5))


def test_total():
    """
    Checks if the function total in hw0 outputs
    the desired output
    """
    # Spec test
    assert_equals(15, hw0.total(5))
    assert_equals(1, hw0.total(1))
    assert_equals(0, hw0.total(0))
    # Additional test
    assert_equals(10, hw0.total(4))
    assert_equals(6, hw0.total(3))
    assert_equals(None, hw0.total(-1))


def test_swip_swap():
    """
    Checks if the function swip_swap in hw0
    outputs the correct string output
    """
    # Spec test
    assert_equals('offbar', hw0.swip_swap('foobar', 'f', 'o'))
    assert_equals('foocar', hw0.swip_swap('foobar', 'b', 'c'))
    assert_equals('foobar', hw0.swip_swap('foobar', 'z', 'c'))
    # Additional test
    assert_equals('baoossn', hw0.swip_swap('bassoon', 'o', 's'))
    assert_equals('bkkooeeper', hw0.swip_swap('bookkeeper', 'o', 'k'))
    assert_equals('avelueta', hw0.swip_swap('evaluate', 'e', 'a'))


def main():
    test_total()
    test_funky_sum()
    test_swip_swap()


if __name__ == '__main__':
    main()
