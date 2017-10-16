
from peewee import *

class SearchResult(Model):
    query_text = CharField()
    number_of_occurrences = IntegerField(default=0)

    def set_num_of_occurrences(self):
        """Sets number_of_occurrences if 'occurrences' attribute has been set"""
        try:
            self.number_of_occurrences = len(self.occurrences)
        except AttributeError:
            pass


class Occurrence(Model):
    search_result = ForeignKeyField(SearchResult, related_name='occurrence_set')
    line = IntegerField()
    start = IntegerField()
    end = IntegerField()
    in_sentence = TextField()
