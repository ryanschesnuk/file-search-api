import unittest

import json
from peewee import *

import app
import models
from settings import FILEPATH
import resources


class SearchResultTestCase(unittest.TestCase):
    def setUp(self):
        self.new_search_result = models.SearchResult(
            query_text="test text"
        )

    def test_num_of_occurrences(self):
        count = 3
        occurrence_object_list = []
        for i in range(count):
            new_occurrence = models.Occurrence(
                search_result = self.new_search_result,
                line=i,
                start=i,
                end=i+9,
                in_sentence="This is sentence number {}".format(i)
            )
            occurrence_object_list.append(new_occurrence)

        #Test except block in set_num_of_occurrences()
        self.new_search_result.set_num_of_occurrences()
        self.assertEqual(self.new_search_result.number_of_occurrences, 0)

        #Test length of 'occurrences' attribute
        setattr(self.new_search_result, "occurrences", occurrence_object_list)
        self.new_search_result.set_num_of_occurrences()
        self.assertEqual(self.new_search_result.number_of_occurrences, count)


if __name__ == '__main__':
    unittest.main()
