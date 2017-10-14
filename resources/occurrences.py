from flask import Blueprint, jsonify

from flask_restful import Resource, Api, fields, marshal
from playhouse.shortcuts import model_to_dict

import re

import models

FILEPATH = 'files/king-i-150.txt'


occurrence_fields = {
    'line': fields.Integer,
    'start': fields.Integer,
    'end': fields.Integer,
    'in_sentence': fields.String
}

search_fields = {
    'query_text': fields.String,
    'number_of_occurrences': fields.Integer,
    'occurrences': fields.Nested(occurrence_fields)
}

class OccurrenceList(Resource):

    def get(self, query_text):
        with open(FILEPATH, encoding='utf-8') as new_file:
            lines = new_file.readlines()

        new_search_result = models.SearchResult(query_text=query_text)

        occurrence_object_list = []

        for line in lines:
            line_index = lines.index(line)

            for m in re.finditer(re.escape(query_text), line.replace('"', "'"), re.M|re.I):

                text_start = m.start()
                text_end = m.end()

                second_part = ''
                dot_index = None
                line_count = 1
                search_line = line[text_start:].replace('"', "'")

                first_part = ''
                dot_index_rev = None
                line_count_rev = -1
                search_line_rev = line[:text_start].replace('"', "'")

                while dot_index == None or dot_index_rev == None:
                    # Forward Scan of QUERY_TEXT sentence until period
                    if dot_index == None:
                        if "." not in search_line:
                            second_part += search_line
                            search_line = lines[line_index + line_count].replace('"', "'")
                            line_count += 1
                        else:
                            dot_index = search_line.index(".")
                            if search_line[dot_index + 1] == "'":
                                add_quote_index = 2
                            else:
                                add_quote_index = 1
                            second_part += search_line[:dot_index + add_quote_index]

                    # Backwards Scan of QUERY_TEXT sentence until period
                    if dot_index_rev == None:
                        if "." not in search_line_rev:
                            first_part = search_line_rev + first_part
                            search_line_rev = lines[line_index + line_count_rev].replace('"', "'")
                            line_count_rev -= 1
                        else:
                            dot_index_rev = search_line_rev.rindex(".")
                            first_part = (search_line_rev[dot_index_rev+1:]
                                            + first_part)



                sentence = (first_part + second_part).replace('\n', ' ').strip()

                occurrence_object_list.append(
                    models.Occurrence(
                        search_result = new_search_result,
                        line = line_index + 1,
                        start = text_start + 1,
                        end = text_end + 1,
                        in_sentence = sentence
                    )
                )

        setattr(new_search_result, 'occurrences', occurrence_object_list)
        new_search_result.set_num_of_occurrences()
        response = marshal(new_search_result, search_fields)
        return jsonify(response)

occurrences_api = Blueprint('resources.occurrences', __name__)
api = Api(occurrences_api)

api.add_resource(
    OccurrenceList,
    '/<query_text>',
    endpoint='occurrences'
)
