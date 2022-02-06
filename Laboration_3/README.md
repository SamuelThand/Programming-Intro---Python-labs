# Laboration 3

## Environment & Tools
Ubuntu 20.04 LTS, Pycharm 2021.2.1, Python 3.8.10, Git 2.25.1

## Purpose

The purpose of the assignment is to create a functional program for calculating fibonacci sequences of the nth number, and measuring performance of different methods used inside. The results need to be saved in files and printed to console according to specifications.  

The assignment aims to help the student understand imports, file paths, file creation, writing and reading to files and file management using pathlib.

How to measure execution time using the timeit module and default_timer (perf_counter()).

Understanding the function of wraps from the functools module, how argparse handles arguments which are passed when running the script.

How logging can be implemented using the logging module, configuring a custom logger with formatters and handlers manually or from settings imported from a JSON file.

Understanding how global variables are used and their implications.

How functools wraps are used to preserve data from the original function when decorating functions.

Understanding how function decoration works and why it is useful.

How iterative vs recursive vs cached recursive approaches for calculations differ in performance and implementations, which approach is better in different applications.

Understanding string formatting at an intermediate level, and how to justify output in the console.

Understanding how to build scalable solutions instead of hardcoded ones.

## Procedures

The solution can be reproduced by building the functions as follows.

### create_logger()
Use the provided RESOURCES variable together with the pathlib absolute() method to create an absolute path to the _Resources directory and assign to variable 'abs_path_resources'. Use this variable and append it with 'ass3_log_conf.json' to get an absolute path to the logger config file. Assign to variable 'config_path'.

Use with context manager to open the JSON file. Load the JSON to a python dictionary and store it in a variable.

Set an absolute path to the logfile in the dictionary by accessing the value of nested key 'filename' and setting its value to abs_path_resources / 'ass_3.log'

Use config.dictConfig with the modified dictionary passed as an argument to configure the root logger. Then use getLogger from the logging module with 'ass_3_logger' as argument to set up a custom logger named ass_3_logger and return the logger object.

### measurements_decorator()

Set Up an empty list container and assign to variable 'fib_values', use perf_counter which is default_timer imported as timer. Use Timer() to start time measurements and assign to variable 'start_time'.

Log 'Starting measurements...' to console via stdout and to ass_3.log on level = info using LOGGER.

Iterate backwards from nth number to zero using a for loop with nth_nmb as start argument, -1 stop argument and -1 step argument. Enumerate the range with enumerate() to create

a separated counter from the fibonacci iterations range. 

Append fibonacci values to list container fib_values. Values are derived from the original fibonacci calculation functions with the current fibonacci iteration as argument. func(seq_num).

Use an if conditional to determine every fifth iteration of the for loop, by using modulus on the enumerate() counter num. When this condition is true, log a formatted string with the fibonacci iteration number and fibonacci value to file ass_3.log using LOGGER.debug.

Use timer() to end time measurement and assign to variable 'end_time'.

Calculate measured time by end_time - start_time, assign the difference value to variable 'duration'.

Return duration and the list of fib_values as a two-tuple.  

Return wrapper

### fibonacci_memory()

Set up an initial cache as a dictionary with key:value pairs 0: 0, 1: 1 hard coded. Store in variable 'cache'.

Define inner function fib_mem(_n)

Use a if not conditional to determine if the number _n is not stored in cache.

If true, store value _n as key in cache, with the recursive statement fib_mem(_n - 1) + fib_mem(_n - 2) as value. Then return the value for key _n in cache.

If false, return value for key _n in cache. This is the function base case.

Return fib_mem(nth_nmb)

### print_statistics()

Declare 'line_length' variable as integer casted length of the predefined 'line' variable. Declare 'column_width' variable as integer casted line_length divided by five. These two variables define the length of the table and width of the five needed columns.

Declare 'main_header' variable as a formatted string according to assignment specifications.

Declare 'column_headers' variable as a list with an empty element, plus the four specified measurement units.

Print a formatted string with the predefined variable 'line' without a newline passed before and the predefined 'line' variable unmodified after the 'main_header' variable. Center justify the string with length of 'line_length' variable.

Loop through the column_headers list and print a formatted string for each header with the header iterable right justified with width of column_width, and end='' parameter.

Loop through the fib_detail dictionary items and print a formatted string with the key left justified with the width of 'column_width' variable for each key.

Make a nested loop that iterates over the 'column_headers' variable, with the first empty element excluded.

For each header in 'column_headers', print a formatted string with the value[0] formatted with duration_format(), with each header iterable passed as precision argument to the function. Right justify the string with 'column_width' as width and use the end='' parameter for the string. This will print the duration formatted to each precision from the switcher in duration_format() on one line.  

Return None

### write_to_file()

Use the provided RESOURCES variable together with the pathlib absolute() method to create an absolute path to the _Resources directory and assign to variable 'abs_path_resources'.

Loop through the keys of fib_details dictionary. Use a with context manager to open a file stream in write mode based on a formatted string which takes the abs_path_resources, appends the fib_details key with spaces replaced with underscores using .replace() string method and .txt appended to the end of the string. This takes the fib_details key, checks if a correctly named fibonacci file exists for that fibonacci-method, and creates it if necessary.

Inside the context manager, declare the variable 'values' as the tuple- value of the fib_details key with index 1, which is a list of the fibonacci values. Then declare the variable 'sequence_numbers' as a reverse range of the length of the 'values' variable. Arguments for the range are (length of 'values' variable) -1 as start, -1 as stop and -1 as step.

Use a for loop with python zip() function inside the context manager for parallel iteration between 'the sequence_numbers' and 'values' variables. For each sequence and value, write a formatted string to the file with the sequence and value formatted according to assignment specifications.

## Discussion

### Perspective
I think the purpose has been fulfilled. The assignment required proper study of the modules, and understanding of the concepts. Use of incremental development methods and a structured approach was important in this assignment and the assignment provided much exercise for this.

I think the implementation is suitable. The program performs according to specifications and is scaleable. 

What could be considered is further optimisation of the fibonaccy_memory function, for maximised performance. There are evidently many methods for writing functions with memoization or cacheing, and also built in functionality for this in Python.

### Personal reflections

I learned much about function decorators, closures and why it is useful in particular. I found the order of problem solving to be difficult, since the decorator in its undefined state did not allow for easy debugging of the fibonaccy_memory function. As the logger was created, and the decorator returning properly, the problem solving got easier.

I also realised my first implementation for this assignment was too hard coded, and that it would cause problems should additional fibonacci functions be added. It was not scalable.

In terms of printing statistics, the console output was not dynamic in its dimensions and the printing was not automated from the fib_details dictionary. Adding additional functions would cause much unnecessary work both in restructuring the console output manually, both in dimensions and added print statements.

In terms of writing to files, adding additional functions would be tedious to add as well since file checking, creation and writing was not automated from the fib_details dictionary either.

In terms of using the duration_format() function, adding new precisions would also have been tedious since the formatting for each precision was hard coded.  

Because of these realisations I had to make redesigns of much of the program which was a very good learning experience. Scalability will definately be an early consideration in my implementations from now on.

The modules provided sufficient learning for the assignment, however the need for repetition was evident because of much information. Some more exercises in module 5 and 6 would be good, but I got some practice by doing code alongs with Corey Schafer as well.









