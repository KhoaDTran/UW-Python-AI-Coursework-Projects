"""
Khoa Tran
CSE 163 AB

This program performs a test on search_engine.py
and document.py by creating their respective
objects and testing the existing functions in each
class
"""
from cse163_utils import assert_equals

from document import Document
from search_engine import SearchEngine


def test_document():
    """
    Tests the Document class.

    Special Case: Testing the frequency
    for a word that isn't in the document.
    """
    doc1 = Document('/home/testFiles/doc1.txt')
    assert_equals(['hi', 'my', 'name', 'is', 'zach', 'and',
                   'i', 'love', 'food'], doc1.get_words())
    doc2 = Document('/home/testFiles/doc2.txt')
    assert_equals(0, doc2.term_frequency('soccer'))
    doc3 = Document('/home/testFiles/doc3.txt')
    assert_equals(0.16666666666666666, doc3.term_frequency('uber'))


def test_search_engine():
    """
    Tests the SearchEngine class.

    Special Case: Testing a term
    that doesn't exist in the directory.
    """
    test_search = SearchEngine('/home/testFiles')
    assert_equals(None, test_search.search("street"))
    assert_equals(['/home/testFiles/doc4.txt',
                   '/home/testFiles/doc2.txt'],
                  test_search.search("basketball"))
    assert_equals(['/home/testFiles/doc4.txt', '/home/testFiles/doc5.txt',
                   '/home/testFiles/doc3.txt', '/home/testFiles/doc2.txt',
                   '/home/testFiles/doc1.txt'],
                  test_search.search('food'))


def main():
    """
    Operates test functions
    """
    test_document()
    test_search_engine()
    print('Successful')


if __name__ == '__main__':
    main()
