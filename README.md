# Search API

This API takes an arbitrary string of text as an endpoint, and uses that text as an index to search a file.

It will respond with JSON, and contain the number of occurrences of the string, as well as some details about each occurrence. These details include the line number it is found on, the start and end indexes of the string on the particular line, and the full sentence that it is found in.

The URL is:

> localhost:8000/api/v1/search/enter some text

The current file being searched is a transcript of Martin Luther King Jr's famous "I Have A Dream" speech.

As of now, the search algorithm does not handle phrases that span multiple lines. Only single words or short phrases on a single line will be found.
