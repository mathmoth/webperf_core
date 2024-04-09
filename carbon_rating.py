# -*- coding: utf-8 -*-
import sys
import getopt
import math
import json
from datetime import datetime
from engines.json_engine import read_tests

FIELD_INDEX_DATE = 0
FIELD_INDEX_DATA = 1

def get_percentile(arr, percentile):
    """
    Calculate the percentile of a list of values.

    Parameters:
    arr (list): A list of numerical data.
    percentile (float): The percentile to compute, which must be between 0 and 100 inclusive.

    Returns:
    float: The percentile of the values in the `arr`.

    This function uses linear interpolation between data points if
    the desired percentile lies between two data points `i` and `j`:
        percentile = (1 - fraction) * arr[i] + fraction * arr[j]
    where `fraction` is the fractional part of the index surrounded by `i` and `j`.
    """
    percentile = min(100, max(0, percentile))
    index = (percentile / 100) * (len(arr) - 1)
    fraction_part = index - math.floor(index)
    int_part = math.floor(index)
    percentile = float(arr[int_part])

    if fraction_part > 0:
        percentile += fraction_part * \
            (float(arr[int_part + 1]) - float(arr[int_part]))
    else:
        percentile += 0

    return percentile


def write(output_filename, content):
    """
    Write a string to a file.

    Parameters:
    output_filename (str): The name of the file to write to.
    content (str): The content to write to the file.

    This function will overwrite the existing content of the file.
    """
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def generate_content(co2s, generated_date):
    """
    Generate a Python script that includes the date of generation and percentiles of CO2 data.

    Parameters:
    co2s (list): A list of CO2 data.
    generated_date (str): The date when the data was generated.

    Returns:
    str: A string that represents a Python script. The script includes two functions:
        - get_generated_date(): Returns the date when the data was generated.
        - get_percentiles(): Returns a list of percentiles of the CO2 data.

    The percentiles are calculated for each integer from 1 to 100.
    The percentile values are sorted in ascending order.
    If the percentile position is a multiple of 10,
    a comment indicating the percentile is added before the value.
    """
    output_content = f"# This array was last generated with carbon-rating.py on {generated_date}\n"
    output_content += "def get_generated_date():\n"
    output_content += "    \"\"\"\n"
    output_content += "    Get the date when the data was generated.\n"
    output_content += "\n"
    output_content += "    Returns:\n"
    output_content += "    str: A string that represents the date when the data was generated.\n"
    output_content += "         The date is in the format 'YYYY-MM-DD'.\n"
    output_content += "    \"\"\"\n"
    output_content += f"    return '{generated_date}'\n"
    output_content += "\n"
    output_content += "def get_percentiles():\n"
    output_content += "    \"\"\"\n"
    output_content += "    Get the precomputed percentiles of CO2 data.\n"
    output_content += "\n"
    output_content += "    Returns:\n"
    output_content += "    list: A list of precomputed percentiles of the CO2 data.\n"
    output_content += "         The list contains 100 elements,\n"
    output_content += "         each representing the percentile from 1 to 100.\n"
    output_content += "         The percentiles are sorted in ascending order.\n"
    output_content += "         The percentile values are floats.\n"
    output_content += "    \"\"\"\n"
    output_content += "    return [\n"

    co2s_sorted = sorted(co2s)

    intervals = []

    index = 1
    while index <= 100:
        percentile = get_percentile(co2s_sorted, index)
        intervals.append(percentile)
        position = index - 1
        if index < 100:
            if position % 10 == 0 and position != 0:
                output_content += f"        # {position} percentile\n"

            output_content += f"        {percentile},\n"
        else:
            output_content += f"        {percentile}\n"
        index += 1

    output_content += "    ]\n"
    return output_content


def main(argv):
    """
    WebPerf Core Carbon Percentiles

    Usage:
    * run webperf-core test on all websites you want to
      use for your percentiles (with json as output file)
    * run this file against your output file, for example like this:
      carbon_rating.py
        -i data\\carbon-references-2022.json
        -o tests\\energy_efficiency_carbon_percentiles.py

    Options and arguments:
    -h/--help\t\t\t: Help information on how to use script
    -i/--input <file path>\t: input file path (.json)
    -o/--output <file path>\t: output file path (.py)
    """

    output_filename = ''
    input_filename = ''

    try:
        opts, _ = getopt.getopt(
            argv, "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError:
        print(main.__doc__)
        sys.exit(2)

    if len(opts) == 0:
        print(main.__doc__)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):  # help
            print(main.__doc__)
            sys.exit(2)
        elif opt in ("-i", "--input"):  # input file path
            input_filename = arg
        elif opt in ("-o", "--output"):  # output file path
            output_filename = arg

    tests = read_tests(input_filename, 0, -1)
    generated_date = False
    co2s = []

    for test in tests:
        if not generated_date:
            generated_date = datetime.fromisoformat(
                test[FIELD_INDEX_DATE]).strftime('%Y-%m-%d')

        str_data = test[FIELD_INDEX_DATA].replace('\'', '"')
        data = json.loads(str_data)
        print(str_data)
        co2s.append(data['co2'])

    if not generated_date:
        generated_date = datetime.today().strftime('%Y-%m-%d')

    output_content = generate_content(co2s, generated_date)
    print(output_content)
    if len(output_filename) > 0:
        write(output_filename, output_content)


if __name__ == '__main__':
    main(sys.argv[1:])
