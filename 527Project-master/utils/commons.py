"""
This script file consists of all the helper utilities needed in the application
"""


def json_map_generator(columns, data):
    json_map = {}
    for column, value in zip(columns, data):
        # if to handle the describe table record fetch
        if type(column) is bytes:
            column = column.decode("UTF-8")
        if str(value).startswith('b'):
            json_map[column] = str(value)[2:len(str(value))-1]
        else:
            json_map[column] = value
    return json_map