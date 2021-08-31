"""
Khoa Tran
CSE 163 AB

This class creates a SearchEngine type object
that creates an inverse index from a given directory,
in order track the word and the files it appears in.
This allows for complete search of the directory
from a given phrase to understand the files each word appears in.
"""
import math
import os
import re
from document import Document


class SearchEngine:

    def __init__(self, directory):
        """
        Initialize SearchEngine by creating the object
        from a given directory name, which has an inverse index
        that maps each word to the documents in which the word
        appears.
        """
        self._inverse_index = dict()
        self._dcount = 0
        for file in os.listdir(directory):
            self._dcount += 1
            file = Document(directory + '/' + file)
            word_list = file.get_words()
            for word in word_list:
                if word not in self._inverse_index.keys():
                    self._inverse_index[word] = [file]
                else:
                    self._inverse_index[word].append(file)

    def _calculate_idf(self, term):
        """
        From the given term, function returns the
        Inverse Document Frequency for the term over all the
        documents in the respective SearchEngine directory
        of documents.
        """
        if term not in self._inverse_index.keys():
            return 0
        else:
            num_tdoc = len(self._inverse_index[term])
            result = math.log((self._dcount)/(num_tdoc))
            return result

    def search(self, word):
        """
        From given word or phrase, function returns a list of
        documents that the word or phrases appears in and in the
        order of the word or phrase's Term Frequency-Inverse
        Document Frequency ranking.

        Special Case: If the term is not in any of the documents,
        returns None.
        """
        result_list = []
        docu_dict = dict()
        word = re.sub(r'\W+', ' ', (word))
        word = word.lower()
        word_list = word.split()
        for word in word_list:
            if word in self._inverse_index.keys():
                for docu in self._inverse_index[word]:
                    tf = docu.term_frequency(word)
                    idf = self._calculate_idf(word)
                    tf_idf = tf * idf
                    if docu not in docu_dict.keys():
                        docu_dict[docu] = tf_idf
                    else:
                        docu_dict[docu] += tf_idf
        docu_list = list(docu_dict.items())
        if len(docu_list) == 0:
            return None
        else:
            docu_list.sort(key=lambda t: t[1], reverse=True)
            for doc in docu_list:
                result_list.append(str(doc[0]))
            return result_list
