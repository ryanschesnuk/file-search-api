from flask import Blueprint, jsonify

from flask_restful import Resource, Api

import re

FILEPATH = 'files/king-i-150.txt'

class OccurrenceList(Resource):

    def get(self, query_text):
        with open(FILEPATH, encoding='utf-8') as new_file:
            lines = new_file.readlines()

        occurrences_list = []

        for line in lines:
            for m in re.finditer(re.escape(query_text), line, re.M|re.I):

                line_index = lines.index(line)
                text_start = m.start()
                text_end = m.end()

                second_part = ''
                dot_index = None
                line_count = 1
                search_line = line[text_start:]

                first_part = ''
                dot_index_rev = None
                line_count_rev = -1
                search_line_rev = line[:text_start]

                while dot_index == None or dot_index_rev == None:
                    # Forward Scan of QUERY_TEXT sentence until period
                    if dot_index == None:
                        if "." not in search_line:
                            second_part += search_line
                            search_line = lines[line_index + line_count]
                            line_count += 1
                        else:
                            dot_index = search_line.index(".")
                            second_part += search_line[:dot_index + 1]

                    # Backwards Scan of QUERY_TEXT sentence until period
                    if dot_index_rev == None:
                        if "." not in search_line_rev:
                            first_part = search_line_rev + first_part
                            search_line_rev = lines[line_index + line_count_rev]
                            line_count_rev -= 1
                        else:
                            dot_index_rev = search_line_rev.index(".")
                            first_part = (search_line_rev[dot_index_rev+1:]
                                            + first_part)


                sentence = (first_part + second_part).replace('\n', ' ').strip()
                occurrences_list.append(
                    {
                        "line": line_index + 1,
                        "start": text_start + 1,
                        "end": text_end + 1,
                        "in_sentence": sentence
                    }
                )

        return jsonify(
            {
                "query_text": query_text,
                "number_of_occurrences": len(occurrences_list),
                "occurrences": occurrences_list
            }
        )

occurrences_api = Blueprint('resources.occurrences', __name__)
api = Api(occurrences_api)

api.add_resource(
    OccurrenceList,
    '/<query_text>',
    endpoint='occurrences'
)
