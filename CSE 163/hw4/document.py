"""
Khoa Tran
CSE 163 AB

This class creates Document type objects that
can tracks data on a text file. The data includes the
list of unique words and the frequency of each word.
"""
import re


class Document:

    def __init__(self, filename):
        """
        Initialize Document object by mapping each word
        in the given file name to the number of times
        that the word appears in the file
        """
        self._filename = filename
        self._wdict = dict()
        self._wcount = 0
        with open(filename) as file:
            lines = file.readlines()
            for line in lines:
                words = line.split()
                for word in words:
                    word = re.sub(r'\W+', '', word)
                    word = word.lower()
                    self._wcount += 1
                    if word not in self._wdict.keys():
                        self._wdict[word] = 1
                    else:
                        self._wdict[word] = self._wdict[word] + 1

    def get_path(self):
        """
        Returns the path of the file this Document represents
        """
        return str(self._filename)

    def term_frequency(self, term):
        """
        Given a term, returns the
        frequency of the given term in file,
        by taking the times it appears in the file and
        dividing with the the total word count of the file
        """
        term = re.sub(r'\W+', '', term)
        term = term.lower()
        if term in self._wdict.keys():
            tfrequency = (self._wdict[term])/(self._wcount)
            return tfrequency
        else:
            return 0

    def get_words(self):
        """
        Returns a list of unique words in the file
        """
        return (list(self._wdict.keys()))

    def __repr__(self):
        """
        Returns the string representation of
        the document object as document's path
        """
        return self._filename
