import unittest

import json
from peewee import *

import app
import models
import re

from settings import FILEPATH
import resources


class SearchResultTestCase(unittest.TestCase):
    def setUp(self):
        self.new_search_result = models.SearchResult(
            query_text="test text"
        )

    def test_num_of_occurrences(self):
        """Test set_num_of_occurrences() method in SearchResult"""

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

        #Test value of 'number_of_occurrences' attribute
        setattr(self.new_search_result, "occurrences", occurrence_object_list)
        self.new_search_result.set_num_of_occurrences()
        self.assertEqual(self.new_search_result.number_of_occurrences, count)


class OccurrenceListResourceTestCase(unittest.TestCase):
    def setUp(self):
        resources.occurrences.FILEPATH = 'files/test_file.txt'
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_get_success(self):
        """Test status code 200 with arbitrary GET request"""

        res = self.app.get('/api/v1/search/sometext')
        self.assertEqual(res.status_code, 200)

    def test_valid_json_response(self):
        """Test response is valid JSON"""

        query_string = "text"
        res = self.app.get("api/v1/search/{}".format(query_string))
        self.assertEqual(res.content_type, "application/json")

    def test_single_word_query(self):
        """Test a query with a single word"""

        query_string = "interesting"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 14)
        self.assertEqual(data["occurrences"][0]["start"], 64)
        self.assertEqual(data["occurrences"][0]["end"], 75)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "Here is another sentence as an interesting addition."
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])

    def test_multi_word_phrase(self):
        """Test a query with multiple words"""

        query_string = "that span multiple"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 5)
        self.assertEqual(data["occurrences"][0]["start"], 52)
        self.assertEqual(data["occurrences"][0]["end"], 70)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
        "We definitely should check that we can find phrases that span multiple lines."
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])

    def test_correct_preceeding_period_boundary(self):
        """
        Check that the correct preceeding period in lines with more than one
        sentence is used to determine sentence start boundary
        """

        query_string = "determines"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(data["occurrences"][0]["in_sentence"],
    "On the same line to make sure that that the correct period determines the beginning of the sentence."
        )



    def test_exclamation_point_start_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering exclamation points at beginning of sentence.
        """

        query_string = "preceded"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 10)
        self.assertEqual(data["occurrences"][0]["start"], 38)
        self.assertEqual(data["occurrences"][0]["end"], 46)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "This sentence is preceded with different punctuation."
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])

    def test_exclamation_point_end_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering exclamation points at end of sentence.
        """

        query_string = "exclamation"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 10)
        self.assertEqual(data["occurrences"][0]["start"], 1)
        self.assertEqual(data["occurrences"][0]["end"], 12)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "Also, we should test sentences that end in exclamation points!"
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])



    def test_question_mark_start_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering question marks at beginning of sentence.
        """

        query_string = "deal"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 16)
        self.assertEqual(data["occurrences"][0]["start"], 43)
        self.assertEqual(data["occurrences"][0]["end"], 47)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "There is another thing we must deal with."
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])

    def test_question_mark_end_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering question marks at end of sentence.
        """

        query_string = "questions"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)
        self.assertEqual(data["number_of_occurrences"], 1)
        self.assertEqual(data["occurrences"][0]["line"], 16)
        self.assertEqual(data["occurrences"][0]["start"], 1)
        self.assertEqual(data["occurrences"][0]["end"], 10)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "We should also ask: what about questions?"
        )
        self.assertIn(query_string, data["occurrences"][0]["in_sentence"])

    def test_quote_conversion(self):
        """Check that all double quotes in text are converted to singles"""

        query_string = "quotes"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        self.assertNotIn('"', data["occurrences"][0]["in_sentence"])

    def test_abbreviations(self):
        """
        Check that sentence constructor ignores periods used for abbreviations
        """

        query_string = "abbreviations"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "That other thing is abbreviations, like Mr. Smith."
        )

    def test_newline_start_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering a newline at the beginning of a sentence.
        """

        query_string = "sample"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "This is a sample bit of text used for testing this API."
        )

    def test_newline_end_boundary(self):
        """
        Make sure in_sentence attribute is correctly constructed when
        encountering a newline at the end of a sentence.
        """

        query_string = "newline"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "This sentence ends with a newline"
        )

    def test_repeat_matches_on_single_line(self):
        """Check that seperate repeat matches are detected on a single line"""

        query_string = "repeat"
        res = self.app.get("api/v1/search/{}".format(query_string))
        data = res.data.decode('utf-8')
        data = json.loads(data)

        #test first occurrence
        self.assertEqual(data["number_of_occurrences"], 2)
        self.assertEqual(data["occurrences"][0]["line"], 19)
        self.assertEqual(data["occurrences"][0]["start"], 11)
        self.assertEqual(data["occurrences"][0]["end"], 17)
        self.assertEqual(data["occurrences"][0]["in_sentence"],
            "Repeat sentences on same line."
        )
        self.assertRegex(data["occurrences"][0]["in_sentence"],
                                re.escape(query_string) + r"(?i)")

        #test second occurrence
        self.assertEqual(data["occurrences"][1]["line"], 19)
        self.assertEqual(data["occurrences"][1]["start"], 42)
        self.assertEqual(data["occurrences"][1]["end"], 48)
        self.assertEqual(data["occurrences"][1]["in_sentence"],
            "Repeat sentences on same line."
        )
        self.assertRegex(data["occurrences"][1]["in_sentence"],
                                re.escape(query_string) + r"(?i)")


if __name__ == '__main__':
    unittest.main()
