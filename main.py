# Import pandas
import pandas as pd
import math
import json
from pprint import pprint
from collections import Counter
from numpyencoder import NumpyEncoder
from datetime import datetime


# Todo: occurances should not be global
def index(element):
    global types
    return types[element] if isinstance(element, type) else element

def is_datetime(string):
    try:
        datetime.fromisoformat(string)
        datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%fZ')
        return True
    except ValueError:
        return False

# Given a string, what does the string probably contain?
def analyze_string_type(element, occurrences):
    supported_strings = {"datetime": is_datetime}

    for type in supported_strings:
        if supported_strings[type](element):
            if type not in occurrences:
                occurrences[type] = 0
            occurrences[type] += 1

    return occurrences


def analyze_most_common(column_data):
    common_elements = []

    # Get inforation about the most occuring elements
    c = Counter(column_data)
    most_common_element = c.most_common(5)  # get the nr. 5 most occuring elements

    for el in most_common_element:
        occurance = {"element": el[0], "occurances": el[1] / column_data.size}
        common_elements.append(occurance)

    return common_elements


def predict_seperator(filename):
    file = open(filename, "r")
    first_row = file.readline()

    possible_seperators = [';', '\t', ',']
    current_seperator = ''
    occurances = 0

    for sep in possible_seperators:
        count = first_row.count(sep)
        if count > occurances:
            occurances = count
            current_seperator = sep

    return current_seperator


def make_dict_relative(dictionary, size):
    for type in dictionary:
        idx = index(type)
        if isinstance(dictionary[idx], dict):
            dictionary[idx] = make_dict_relative(dictionary[idx], size)
        else:
            dictionary[idx] = dictionary[idx] / column_data.size
    return dictionary


def count_type_occurances(column_data):
    occurrences["empty"] = 0
    occurrences["str-data"] = dict()

    global types
    for type in types:
        occurrences[index(type)] = 0

    for element in column_data:
        # float check because math.isnan() only works on real numbers
        if isinstance(element, float) and math.isnan(element):
            # Empty cells get converted to NaN by pandas
            occurrences["empty"] += 1
            occurrences[index("float")] -= 1  # Because it's actually not a float, but empty

        if isinstance(element, str):
            occurrences["str-data"] = analyze_string_type(element, occurrences["str-data"])

        for type in types:
            if isinstance(element, type):
                occurrences[index(type)] += 1

    # Make the absolute values relative
    occurences = make_dict_relative(occurrences, column_data.size)

    return occurrences


def export_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True,
                  separators=(', ', ': '), ensure_ascii=False,
                  cls=NumpyEncoder)
    # with open(filename, 'w') as fp:
    #     json.dump(data, fp)


# input_file = "dwca-est_grey_seals_00-16-v1.1/event.txt"
input_file = "data.csv"

# reading csv file
data = pd.read_csv(input_file, sep=predict_seperator(input_file))
data_info = dict()  # Contains the info about each column

types = {bool: "bool", int: "int", float: "float", str: "str"}

# finding the type of each column
for column in data:
    occurrences = dict()
    column_data = data[column]
    stats = dict()

    stats["type-occurrences"] = count_type_occurances(column_data)

    # There is nothing useful to say about most common nan's in an empty column
    if not stats["type-occurrences"]["empty"] == 1.0:
        stats["most_common"] = analyze_most_common(column_data)

    if stats["type-occurrences"][index(bool)] or \
            stats["type-occurrences"][index(int)] or \
            stats["type-occurrences"][index(float)]:
        stats["avg"] = column_data.mean()
        stats["min"] = column_data.min()
        stats["max"] = column_data.max()
        stats["sd"] = column_data.std()  # Standard deviation

    if stats["type-occurrences"][index(str)]:
        str_lengths = [len(el) for el in column_data]
        stats["avg-length"] = 0 if len(str_lengths) == 0 else (float(sum(str_lengths)) / len(str_lengths))
        stats["min-length"] = min(str_lengths)
        stats["max-length"] = max(str_lengths)

    # Add a timestamp for when the last update was
    stats["timestamp"] = str(datetime.now())

    data_info[column] = stats

pprint(data_info)
export_json("report.json", data_info)
