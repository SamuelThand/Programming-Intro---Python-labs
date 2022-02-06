#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""

from pathlib import Path
from timeit import default_timer as timer
from functools import wraps
import argparse
import logging
import logging.config
import json

__version__ = '1.1'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

RESOURCES = Path(__file__).parent / "../_Resources/"


def create_logger() -> logging.Logger:
    """Create and return logger object."""

    # Absolute path to _Resources dir
    abs_path_resources = RESOURCES.absolute()

    # Absolute path to JSON-file used for logger config
    config_path = abs_path_resources / 'ass3_log_conf.json'

    with Path.open(config_path, 'r', encoding='UTF-8') as f_hand:
        config_fromjson = json.load(f_hand)

        # Setting absolute path to logfile in dictionary for logger config
        config_fromjson['handlers']['file_handler']['filename'] = abs_path_resources / 'ass_3.log'

        logging.config.dictConfig(config_fromjson)

    # Logger returned to LOGGER which is a global variable set in main().
    return logging.getLogger('ass_3_logger')


def measurements_decorator(func):
    """Function decorator, used for time measurements."""

    @wraps(func)
    # Takes argument nth_nmb from fib original fib functions
    def wrapper(nth_nmb: int) -> tuple:
        fib_values = []
        start_time = timer()
        LOGGER.info('Starting measurements...')

        for num, seq_num in enumerate(range(nth_nmb, -1, -1)):

            # Append fibonacci value to list for current number
            fib_values.append(func(seq_num))

            # Log every fifth iteration: 'number: fib value'
            if num % 5 == 0:
                LOGGER.debug(f'{seq_num}: {func(seq_num)}')

        end_time = timer()

        # Measured calculation time of the fibonacci function
        duration = end_time - start_time

        # Returning duration and fib_values as (float, list)
        return duration, fib_values
    return wrapper


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new
    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)
    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""

    # Initial cache is set, hardcoded values make up the numbers for the base case
    cache = {0: 0, 1: 1}

    def fib_mem(_n):
        if _n not in cache:

            # Add fibonacci values to cache as recursion depth increases.
            cache[_n] = fib_mem(_n - 1) + fib_mem(_n - 2)
            return cache[_n]
        else:

            # Base case, returns the initial cache values of key 0 and 1
            return cache[_n]

    return fib_mem(nth_nmb)


def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument
    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""

    line = '\n' + ("---------------" * 5)
    line_length = int(len(line))
    column_width = int(line_length / 5)
    main_header = f'DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0'
    column_headers = ['', 'Seconds', 'Milliseconds', 'Microseconds', 'Nanoseconds']

    # Prints main header to console center justified.
    print(f'{("---------------" * 5)}\n{main_header:^{line_length}}{line}')

    # Prints the column headers to console with proper justification.
    for header in column_headers:
        print(f'{header:>{column_width}}', end='')
    else:
        print()

    # Prints the method names and duration values to console with proper justification.
    # Uses duration_format() for formatting to each precision.
    for key, value in fib_details.items():
        print(f"{key:<{column_width}}", end='')
        for header in column_headers[1::]:
            print(f"{duration_format(value[0],f'{header}'):>{column_width}}", end='')
        print()

    return None


def write_to_file(fib_details: dict):
    """Function to write information to file."""

    abs_path_resources = RESOURCES.absolute()

    # Writes a formatted string with sequence and value to each file for each fib method.
    # Iterates over keys in fib_details dictionary, and uses a context manager to open a
    # file for each key in write mode. The file path is specified using a formatted string
    # with the absolute path to resources appended with the key, where the blank space is replaced
    # with an underscore using the .replace() string method. If the path doesn't exist, it is created.
    # The list of fibonacci values from the dictionary key value is assigned to values variable.
    # The variable 'sequence_numbers' is a reverse range of the length of the 'values' variable.
    # Arguments for the range are (length of 'values' variable) -1 as start, -1 as stop and -1 as step.
    # Values and sequence_numbers are iterated over using zip() function inside the context manager for
    # parallel iteration between iterables. For each sequence and value, a formatted string is written to
    # the file with the sequence and value formatted using a formatted string.

    for key in fib_details:
        with open(f"{abs_path_resources}/{key.replace(' ', '_')}.txt", 'w', encoding='UTF-8') as f_hand:
            values = fib_details[key][1]
            sequence_numbers = range(len(values) - 1, - 1, - 1)
            for sequence, value in zip(sequence_numbers, values):
                f_hand.write(f'{sequence}: {value}\n')

    return None


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)    # print information in console
    write_to_file(fib_details)                  # write data files


if __name__ == "__main__":
    main()
