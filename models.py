
from peewee import *

class SearchResult(Model):
    query_text = CharField()
    number_of_occurrences = IntegerField(default=0)

    def set_num_of_occurrences(self):
        try:
            self.number_of_occurrences = len(self.occurrences)
        except AttributeError:
            return None



class Occurrence(Model):
    search_result = ForeignKeyField(SearchResult, related_name='occurrence_set')
    line = IntegerField()
    start = IntegerField()
    end = IntegerField()
    in_sentence = TextField()
