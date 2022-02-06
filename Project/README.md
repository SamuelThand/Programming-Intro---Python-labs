
# Project - Game of Life

## Environment & Tools

Ubuntu 20.04 LTS, Pycharm 2021.2.1, Python 3.8.10, Git 2.25.1

## Purpose

### Perspective

The student needs to understand the structure of a python project repository, how to run a project as a module, how to handle interaction with a prewritten codebase imported as a module, and how to work with git using multiple branches and .gitignore. The student needs to understand how to follow the execution flow of a program with many interconnected functions.

The assignment aims to help the student understand argument parsing, and how to properly format, cast and validate incoming arguments with error-raising and exception handling, and fallback default values.

It aims to help the student understand how to employ proper conditional execution with nested conditionals and more intermediate-difficulty logical flows. The student also needs to learn about representing tuples as coordinates and how to build a coordinate grid for visual dictionary data representation in a correct way.

The student needs to understand how to calculate the position of neighbouring coordinates using offsets in the imagined coordinate grid. The student must also be able to determine the state of neighbours by comparison against a dictionary.

The assignment helps the student learn how to control the executional ticks of a program using a dedicated function with both iterative and recursive approaches.

The student needs to understand how to coordinate output, line breaks and formatting to produce a correct coordinate grid with correct dimensions and determine a conditional structure for determining the cell states of the next generation, and design a functioning flow for updating the current generation with new states, and passing the new data for output visualisation in the next simulation tick.

The student needs to understand how to load an existing seed of coordinates from both an existing code module with correct formatting, and from files with incorrect formatting. When loading from files, the student needs to be able to fix filenames, create paths and parse incorrect JSON data into a correctly formatted python dictionary.
 
The assignment aims to help the student understand logging, with intermediate knowledge of a logging object's constituents, how to manually configure a lightweight logger with just the right parts and handle logger objects.

The student needs to understand function decoration with functions being passed as parameters and logging.

### Concrete goals

The student needs to write own implementation for all predefined functions, which should result in a functioning program for running the game of life simulation.

For grade E, the functions under "Base implementation" must be defined according to instructions. parse_world_size_arg() needs to handle parsing of command line arguments, populate_world() needs to handle generation of an initial seed generation, calc_neighbour_positions() needs to handle calculation of coordinate neighbour positions, run_simulation() needs to handle execution of generational ticks, update_world() needs to handle the updating of cell states for the next generation as well as the visual output. count_alive_neighbours() needs to handle the counting of alive neighbours for a cell.

For grade D, a recursive version of run simulation must be implemented.

For grades C - B, the functions under "Implementations for higher grades, C - B" must be defined according to instructions. load_seed_from_file() needs to handle loading and parsing of the initial seed and world size from a file. create_logger() needs to handle the creation of a logging object with a file handler. simulation_decorator() needs to handle the execution of generational ticks and logging of generation info to the log file.

For grade A, the functions under "Grade A: Aging of Cells" must be defined according to instructions. populate_world() needs to account for age in the initial seed generation,
update_world() needs to account for the additional cell states and handle cell aging, count_alive_neighbours() also needs to account for the additional cell states and  simulation_decorator() needs to include additional cell states in the logging. A fix also needs to be implemented for the lack of age in seeds loaded from file.  

There also needs to be a higher degree of understanding in terms of program flow, generation numbers and assignment interpretation. There also needs to be a higher degree of testing/validation skills since provided validation data will only point in the right direction, but not fully prove a correct implementation.

## Procedures

The solution can be reproduced by building the functions as follows.

### Base Implementations

#### parse_world_size_arg()

Take the incoming _arg value from -ws argument and .split() it on 'x'. Store in variable size_values. This creates a list of the input values split on 'x'. Use a try clause and test using a compound if conditional if len(size_values) is not 2, and if
both numbers .isnumeric().

This validates if the input argument is exactly two numeric values separated by an x. If this is not true, raise an AssertionError. Then cast both values into integers and assign size_value[0] to width, and size_value[1] to height. Test with an if statement if either width or height is less than 1. If this is not true, raise a ValueError.

The order of these conditionals are important to ensure correct error handling, i first had issues with ValueErrors being raised for bad input, but this was resolved by combining the length test and numeric test into a compound statement.

Write an except clause for AssertionError that prints error messages according to specifications and sets width, height to default values of 80, 40.

Write an except clause for ValueError that prints error messages according to specifications and sets width, height to default values of 80, 40.

Return width, height variables.

#### populate_world()

Set an empty dictionary for the population. Then make lists of all numbers in a range derived from _world_size width and height. This is in order to make a grid using itertools.product(). Test if a seed pattern has been provided as a command line argument by testing if _seed_pattern is not None. If true, use the provided get_pattern function from code_base.py to load the correct pattern based on stated seed and stated world size. Assign to a variable pattern. If false, set the variable pattern to None.

Use itertools.product with world_height and world_width as arguments to make a cartesian product of all possible combinations between height and width. These will be produced as two-tuples which together will work as a coordinate grid. It is important to use the format height, width (y,x) instead of x,y in this function. This is due to how output is handled in the console - output can only be printed on an X axis, and the Y axis can only be incremented with line breaks. Therefore we need to produce "Every X coordinate, for every Y coordinate" and not the other way around. It is not possible to "stack" every Y coordinate upwards or downwards for every X coordinate. The pattern format in code_base.py also accommodates this.

Iterate over each generated coordinate/cell and test if the cell has the list value of xmin/xmax or ymin/ymax using min() and max() functions. If this is true, the cell is added to the population dictionary as a key, and its value is set to None. This means the cell is a rim cell and is to be excluded from mutable cell states and other properties. Then use a continue statement to restart the iteration with the next coordinate/cell.

Test with elif a seed pattern has been provided as a command line argument by testing if _seed_pattern is not None, if True - look if the current cell is included in the loaded seed pattern from cb.get_pattern. If True - use the provided cb.STATE_ALIVE from code_base.py to set its state to alive. Assign value to variable cell_state. If False, set state to cb.STATE_DEAD.

Elif no seed pattern was provided, randomise seed pattern by creating a random integer number between 0, 20 using randint() from random module. If the generated number is > 16, set the cell state to cb.STATE_ALIVE, else - set the cell state to cb.STATE_DEAD. This simulates a 20% chance of a cell being alive in the seed.

Finally create a key in the population dictionary for the current cell, and set an empty dictionary as value to it. Then add the key 'state', with the calculated cell_state variable as value, the key 'neighbours' with the value being returned from a function call to calc_neighbour_positions() with the current cell as argument.

These logical flows and conditionals initially caused issues, with some conditions never being tested and randomisation occuring regardless of loading a seed pattern or not. This was fixed with structured thinking about which conditions can be True at the same time, and if each condition needs to be tested every time. The corner rim cells can be ymin/xmin or ymax/xmax or ymin/xmax or ymax/xmin but each of these doesn't need to be tested, it is enough if one rim cell condition is True to determine it should be a rim cell. The occurrence of the cell in the loaded seed pattern should not be tested for rim cells either since they are excluded from mutability.

#### calc_neighbour_positions()

Make a list with offset values [-1, 1, 0] and assign to the ‘offsets’ variable. These values are the offsets that can be applied to a coordinate to find the neighbouring coordinate. Then create an empty list for the neighbours and use itertools.product with offsets as argument and a repeat = 2 argument to iterate over all possible combinations of offsets. This is equal to stating itertools.product(offsets, offsets).

Sum the  _cell_coord that was passed as an argument with the current offset value to get the correct neighbour coordinate. This can be done by using a generator expression with zip(), which combines the item iterator with the _cell_coord and then summing resulting values using the sum() function. Then cast the generator object into a tuple.

Append the generated neighbour coordinate to the neighbours list.

When all neighbours have been iterated over, remove the _cell_coord from the neighbours list to leave only the neighbours. Return the neighbours list to the function call.

A problem in this function was how to sum tuple indices with each other, and I think using a generator expression in conjunction with zip solved this in a good way.

#### run_simulation()
Iterate over a range derived from the _generations command line argument, and execute the following steps for each generation.

Use cb.clear_console() function provided in code_base.py to clear the console and prepare for output. Then make a function call to update_world() with the _population dictionary provided from populate_world() and _world_size tuple provided from parse_world_size_arg(). Assign the return value with the updated generation to the variable _population, to ensure that the next generational function call will be based on the updated population dictionary returned from update_world().

Use sleep(0.2) from the time module to delay execution of the next iteration with 200ms.

Return None

#### update_world()

Create an empty dictionary for the next generation of cells.

Then iterate over each cell in the _cur_gen, which is the current generation of cells passed from run_simulation() and enumerate it with enumerate() function with argument start = 1. This is to ensure cells are counted with start value 1 for counting purposes. Start by creating an empty dictionary for the next_gen cell.

Test if the cell has a value of None, which means it is a rim cell. If true - use cb.progress in conjunction with cb.get_print_value to print the cell state of cb.STATE_RIM to console. Both functions are provided in code_base.py. Then copy the cur_gen cell value to the next_gen cell value, since the cell will be a rimcell the next generation as well.

Test if the number value from enumerate is evenly divisible with the width value from _world_size. If this is True - it means there should be a line break since the number of cells having been iterated over is either equal to the max width value or a multiple of it. This is why enumerating the loop with start of 1 is important. Execute the line break by using cb.progress with a newline character passed as a string.

If the cell does not have a value of None - the cell state update block needs to be executed. Use cb.progress in conjunction with cb.get_print_value to print the cell state of the cur_gen cell to console. Then copy the neighbours list from the cur_gen cell to the next_gen cell, since the cell will always have the same neighbours because the cells never change location. Call the count_alive_neighbours() function and with the _cur_gen neighbours list and the entire _cur_gen dictionary passed as arguments, and assign the return integer value in neighbours_alive variable.

Then conditional tests to determine the next cell state must be created. If the _cur_gen cell has a state of cb.STATE_ALIVE AND has 2 OR 3 neighbours_alive - assign cb.STATE_ALIVE to the cell_state variable.

Elif the _cur_gen cell has a state of cb.STATE_DEAD AND has exactly 3 neighbours_alive - assign cb.STATE_ALIVE to cell_state variable.

Elif the the _cur_gen cell has a state of cb.STATE_ALIVE and none of the above compound statements have returned True - assign cb.STATE_DEAD to cell_state variable.

Else assign the _cur_gen cell state to cell_state variable.

Finally set the next_gen cell state value to equal the value of the cell_state variable. Return the dictionary for the next generation.

The order you test for rim cells, execute line breaks, print to console and correct enumeration is important to consider, and caused problems for me. I had issues with line breaks being executed too early / too late, or at the wrong line width. I decided to split the function into two branches, one for rim cells and one for normal cells. Since the only place a line break should occur is directly after the last rim cell, I decided on the order of first printing the rim cell, then copying cell state, then testing if this was the rim cell on maximum width, and in that case executing a line break.

#### count_alive_neighbours()

Assign an integer value of 0 to variable neighbours_alive. This is to be used as a counter.

Iterate over all the neighbour cells in the incoming _neighbours list and test if the cell has a value of None in the incoming _cells dictionary, AND if the cell has a state of cb.STATE_ALIVE in the _cells dictionary. If True - increment the neighbours_alive counter by + 1. Return the integer value of neighbours_alive to the function call.

### D implementation

#### run_simulation()

For this grade the run_simulation() function needs to be rewritten to a recursive version.

Define an inner function simulation_tick with _n and _pop as parameter. This will represent the number n from the _nth_generation and the _population. Test if _n is bigger than or equal to 1, if True - Use the same implementation as in the E level, with a few modifications. Use cb.clear_console() function provided in code_base.py to clear the console and prepare for output. Use sleep(0.2) from the time module to delay execution of the next iteration with 200ms.  Then make a function call to update_world() with the _pop dictionary provided from outside function run_simulation() and _world_size tuple provided from parse_world_size_arg(). Assign the return value with the updated generation to the variable _pop, to ensure that the next generational function call will be based on the updated population dictionary returned from update_world().

Then make a recursive call to simulation_tick with (_n - 1, _pop) passed as arguments. This will run the simulation_tick() function until _n is smaller than 1, which is the function base case.

Return None

Call the inner function simulation_tick() from inside run_simulation() after the function definition.

Return None

### Implementations for higher grades, C - B

For these grades, the functions under Implementations for higher grades, C - B must be implemented

#### load_seed_from_file()

Use absolute() method from pathlib module on the predefined RESOURCES variable to set an absolute path to the _Resources/_Project_Files folder and assign it to seeds_path variable.

Test if the file path doesn't exist using an if not statement and the Pathlib Path.exists() function, if True - create the seeds_path path using Pathlib Path.mkdir() function.

Test if the string '.json' is not a substring in the _file_name string from incoming -f argument. If True - append the _file_name string with '.json' using a formatted string, and assign it to the _file_name variable.

Create a Path object that is the seeds_path followed by the _file_name
using a formatted string, and assign it to the file_path variable.

Use a context manager to open the file_path in read mode as f_hand (file handle). Then use json.load with f_hand passed as argument to store the loaded json file as a python dictionary. Assign the dictionary to seed_dict.

Iterate over the keys in seed_dict using .keys() dictionary method. If the key is equal to 'world_size', assign seed_dict[key] to variable world_size_value for readability. Then use the tuple() function to cast the world_size_value into a tuple from its original list format.

Elif the key is equal to 'population', assign seed_dict[key] to variable population_dict for readability, then use the dictionary .copy() method to create a copy of the population_dict, and use keys() to select the keys from the copy. Then iterate over these keys. The reason for using a copied iterator, is to avoid modifying the actual iterator while looping over the cell keys and modifying the original keys. Assign population_dict[cell] to cell_dict variable for readability. If the cell_dict is not None(Not a rim cell), assign cell_dict['neighbours'] to neighbours_list for readability, then iterate over the index and neighbours in the neighbours_list by enumerating it using enumerate(). For each list item by index position, use tuple() to cast it into a tuple from its original list format.

Finally replace each key in the population dictionary with a quote-less key using a one line dictionary pop and replace statement. Replace the key with literal_eval(key), to remove the quotation marks in the json format. LIteral_eval evaluates a Python expression that is contained in a string. Return a tuple with the population dictionary and the world size tuple.

Parsing the dictionary loaded from the JSON file with all its nested dictionaries caused some problems with navigation of the dictionary depth. It is easy to lose the conceptual understanding of what you're doing when a dictionary value is also a dictionary, and these dictionaries in turn contain other data structures. This problem was reduced by using variables with mnemonic names to keep track of the nesting depth, together with incremental programming with testing.   

#### create_logger()

Use the logging.getLogger() function with the argument 'gol_logger' to get a logger object with the name gol_logger. Assign to variable logger_object. Use the .setlevel() method with 'INFO' as argument to to set the logging level to INFO.

Use absolute() method from pathlib module on the predefined RESOURCES variable to set an absolute path to the log file _Resources/gol.log and assign it to the log_path variable. Use logging.FileHandler with arguments filename=log_path, mode='w' to set up a file handler which logs to _Resources/gol.log in write mode.

Call the .addHandler() method on logger_object with file_handler as an argument to add the file handler to the created logger object.

Return logger_object.

#### simulation_decorator()

Define a wrapper() function to use for decorating, and set the same parameters as run_simulation().  

Call create_logger() and store the logger object in variable logger. Then use a list constructor that creates a list of all the .keys() from _population dictionary IF the key is not None. Use len() on the list to determine the length of the list, and assign it to the population_number variable. This variable contains the amount of cells in the population, excluding rim cells.

Iterate over a range derived from the _generations command line argument, and execute the following steps for each generation.

Use cb.clear_console() function provided in code_base.py to clear the console and prepare for output. Assign the integer value 0 to variable cells_alive. This is to be used as a counter for alive cells.

Loop through the keys in _population, if the key is not None (Not a rim cell) AND has a state of cb.STATE_ALIVE, increment cells_alive with + 1.

After looping through all keys in _population, calculate dead cells by subtracting cells_alive from population_number, and assign the result to cells_dead variable.

Use 4 logger.info() statements with a formatted string containing gen, population_number, cells_alive or cells_dead variables together with a title according to the instructions. This will log information about the current generation to _Resources/gol.log.

Then make a function call to func() with the original arguments _generations, _population and _world_size. This results in a function call to the decorated run_simulation() function, which returns a function call to update_world() with the arguments _population and _world size.
The _populatoin dictionary is provided from populate_world() in the 1st gen and the _world_size tuple is provided from parse_world_size_arg().

 Assign the return value from the func() call, with the updated generation, to the variable _population, to ensure that the next generational func() function call will be based on the updated population dictionary returned from update_world().

Use sleep(0.2) from the time module to delay execution of the next iteration with 200ms.

Return None.

Return the wrapper function as a closure.

### Grade A: Aging of Cells

For the grade A, the following functions need to be redesigned to account for an aging mechanism for the cells.

#### load_seed_from_file() - Optional

This function does not necessarily need to be altered, but one can choose to account for the missing 'age' key/value pair in this function. Since this function already serves to parse and correct the slightly broken format derived from the JSON files into a functioning Python dictionary, the 'age' = 0 key/value pair can easily be added to the cell_dict by stating cell_dict['age'] = 0 after defining the neighbours_list.

#### populate_world()

The implementation of this function is identical to the earlier implementations, except for stating population[cell]['age'] = 0 as a final statement when iteration through the cells generated by itertools.product() This adds the key/value pair 'age' = 0 to all the mutable cells dictionaries before returning the population dictionary.

#### update_world()

This needs to be modified to a greater extent. The implementation until the cell state update block is identical. Modified implementation after the else clause:

If the cell does not have a value of None - the cell state update block needs to be executed. Use cb.progress in conjunction with cb.get_print_value to print the cell state of the cur_gen cell to console. Then copy the neighbours list from the cur_gen cell to the next_gen cell, since the cell will always have the same neighbours because the cells never change location. Also copy the value of key 'age' from the cur_gen cell to the next_gen cell, to prepare the integer value for modification.

Call the count_alive_neighbours() function and with the _cur_gen neighbours list and the entire _cur_gen dictionary passed as arguments, and assign the return integer value in neighbours_alive variable.

Then conditional tests to determine the next cell state must be created. These are heavily modified for the A implementation with nested conditional tests.

    If the _cur_gen cell has a state stored in tuple (cb.STATE_ALIVE, cb.STATE_ELDER, cb.STATE_PRIME_ELDER) AND has 2 OR 3 neighbours_alive:
            If the cell has a state of cb.STATE_ALIVE:
                If the cell has an age of 5:
                    Assign cb.STATE_ELDER to cell_state variable
                Else:
                    Assign cb.STATE_ALIVE to cell_state variable
            Elif the cell has a state of cb.STATE_ELDER:
                If the cell has an age of 10:
                    Assign cb.STATE_PRIME_ELDER to cell_state variable
                Else:
                    Assign cb.STATE_ELDER to cell_state variable
            Else:
                Assign cb.STATE_PRIME_ELDER to cell_state variable
        Increment age by + 1 for the cell.
        
    Elif the _cur_gen cell has a state stored of cb.STATE_DEAD AND has exactly 3 neighbours_alive:
        assign cb.STATE_ALIVE to cell_state variable, and increment age by + 1 for the cell.
        
    Elif the _cur_gen cell has a state stored in tuple (cb.STATE_ALIVE, cb.STATE_ELDER, cb.STATE_PRIME_ELDER) and none of the above paths have executed:
        assign cb.STATE_DEAD to cell_state variable, and set age to 0 for the cell.
        
    Else - if none of the above paths have executed:
        Copy cell state of _cur_gen cell to cell_state variable.
    
    Finally, assign the value of cell_state value determined by the above process to the cell_state variable.

Return next_gen dictionary.

The above implementation ensures that the four laws of Conway are applied.

1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by
reproduction.

It also ensures that a cell surviving more than 5 consecutive generations becomes and Elder,
and a cell living until the 11th generation becomes a Prime Elder. The structure of the tests
also ensures that a cell cannot go directly from Alive to Prime Elder.

Problems arose regarding the interpretation of the aging rules in the assignment. It was at the beginning a bit unclear whether -g should be interpreted as generation 0 or generation 1, this was resolved by closely studying the program flow, and determining what generation gets printed for each tick, and how the generations should correlate to age values.

#### count_alive_neighbours()

This implementation is identical to the earlier version, except for including cb.STATE_ELDER and CB.STATE_PRIME_ELDER as living states.

Assign an integer value of 0 to variable neighbours_alive. This is to be used as a counter.

Iterate over all the neighbour cells in the incoming _neighbours list and test if the cell has a value of None in the incoming _cells dictionary, AND if the cell has a state of cb.STATE_ALIVE, cb.STATE_ELDER or CB.STATE_PRIME_ELDER in the _cells dictionary. If True - increment the neighbours_alive counter by + 1. Return the integer value of neighbours_alive to the function call.

#### simulation_decorator

This implementation is similar to the earlier version, except for including cb.STATE_ELDER and CB.STATE_PRIME_ELDER as living states and counting and logging these new states to gol.log

Define a wrapper() function to use for decorating, and set the same parameters as run_simulation().  

Call create_logger() and store the logger object in variable logger. Then use a list constructor that creates a list of all the .keys() from _population dictionary IF the key is not None. Use len() on the list to determine the length of the list, and assign it to the population_number variable. This variable contains the amount of cells in the population, excluding rim cells.

Iterate over a range derived from the _generations command line argument, and execute the following steps for each generation.

Use cb.clear_console() function provided in code_base.py to clear the console and prepare for output. Assign the integer value 0 to variable cells_living. This is to be used as a counter for alive cells, and the new variable name cells_living reflects that it does not reference cells with cb.STATE_ALIVE, but all living cells regardless of state. Also assign integer value 0 to variables cells_state_elder and cells_state_prime_elder. These are to be used as counters for cells with these cell states.

Loop through the cells in _population, if the cell is not None (Not a rim cell), test the following conditions.

If the cell has a state of cb.STATE_ALIVE, increment cells_living with + 1.

Elif the cell has a state of cb.STATE_ELDER, increment cells_living with + 1, and cells_state_elder with + 1.

Elif the cell has a state of cb.STATE_PRIME_ELDER, increment cells_living with + 1, and cells_state_prime_elder with + 1.  

After looping through all keys in _population, calculate dead cells by subtracting cells_alive from population_number, and assign the result to cells_dead variable.

Use 6 logger.info() statements with a formatted string containing one variable - gen, population_number, cells_alive,  cells_state_elder, cells_state_prime_elder or cells_dead together with a title according to the instructions. This will log information about the current generation to _Resources/gol.log.

Then make a function call to func() with the original arguments _generations, _population and _world_size. This results in a function call to the decorated run_simulation() function, which returns a function call to update_world() with the arguments _population and _world size.
The _populatoin dictionary is provided from populate_world() in the 1st gen and the _world_size tuple is provided from parse_world_size_arg().

 Assign the return value from the func() call, with the updated generation, to the variable _population, to ensure that the next generational func() function call will be based on the updated population dictionary returned from update_world().

Use sleep(0.2) from the time module to delay execution of the next iteration with 200ms.

Return None.

Return the wrapper function as a closure.

## Discussion

### Perspective

I think the purpose has been fulfilled. The concrete goals have been completed according to stated requirements. The intended program flow with each function's responsibilities has been kept intact, and the game of life program works as intended.

The project has prompted further solidification of the skills and concepts stated in the "Perspective" section, and a basic toolbox of programming know-how has been displayed. The confidence of handling a small project spanning weeks independently has also been built.

I think the implementation is suitable with regards to the level of knowledge that can be expected from a beginner student. While studying the code, redundant statements or variable uses have been identified and fixed, but one can assume there are more improvements to be made if the code is examined close enough. Further performance measuring and understanding of the different python functions and their different performance metrics could unveil possibilities for optimisation. A few thoughts about how a more object oriented approach could be considered have surfaced, but only on a conceptual level.

Currently I do not think an alternative approach should be considered, but there are some alternative procedures that can be considered.

In the A implementation, I opted for adding the missing 'age' = 0 key value pair in the load_seed_from_file() function instead in the under update_world() function suggested in the assignment. My line of reasoning for this was that adding a missing dictionary item to the seed dictionary loaded from a file is included in the responsibility of parsing and correcting the information loaded from the JSON file. It also made sense to correct this issue as close to the 'source' as possible, instead of doing it further down the line of program flow. Doing it in the function for loading the file also ensures the code will only run once every time the program is run. However, there is surely a good reason for doing it in the update_world() function instead, and there have been hints to side effects connected to my method mentioned in contact with the examiner. Therefore an alternative procedure should be considered.

In load_seed_from_file(), the method of parsing the loaded data can also be discussed. I opted for modifying the loaded dictionary, instead of building a new one. My line of reasoning for this was that it would be less demanding performance wise to modify an already existing dictionary instead of having to allocate additional memory to a new deep copy of the dictionary data structure with more or less duplicate data. However, my use of .copy().keys() shallow copy in line 95 to avoid modifying the actual iterator while looping over the cell keys felt a bit strange. It works, but I'm uncertain whether it is considered good practice. The many levels of nested iteration may also cause unnecessary complexity, although efforts have been made to ensure readability and abstraction. Therefore an alternative procedure should be considered.

### Personal reflections

In this project I got the chance to solidify the knowledge that has been built during the modules covered in the course. The assignment also prompted much further research regarding the inner workings of various python modules and functions. For instance a better understanding of loggers has been acquired through trial and error, and study. The insight in how a basic simulation can be built with different functions having different responsibilities, and how the background logic can be implemented has been built. The project also prompted me to research other simulations and study concepts such as "seed" and how it is used in programming overall.

I found the coding of the logic for the A implementation to be straightforward, however the interpretation of generations and the conditions given for cell aging was difficult. Initially, I tried validating my solution using the provided log data - but then I realised I could get identical generational values that matched the provided log data, even if the aging conditions were changed with several indices. Realising that the provided log data wasn't accurate enough for a 100% validation of my A implementation prompted further testing and validation. I studied the definition:

"The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations."

This led me to conclude that the integer stated as -g argument is **not** to be interpreted as "-g 1 is the generation number being printed" but instead as "-g 1 is the number of simulation ticks to run". Since **the printing to console occurs before calculating the next generation state**, this means that -g 1 outputs generation 0, which is the seed pattern before rules have been applied. Only in -g 2 is generation 1 printed to console, because the first generation is created only when applying the stated rules unto the seed pattern. The age starting value of 0 for the cell pattern created in populate_world() as well as the log output of GENERATION 0 for -g 1 further supported my conclusion.

The resulting age conditions of my interpretation of ['age'] == 5 for Elders and ['age'] == 10 for Prime Elders also made sense, since age is incremented **after** a generation has been printed to console. "Each cell surviving more than 5 consecutive generations will become an elder" = apply state change from Alive to Elder at age of 5, since the new Elder state needs to be applied for the output of the 6th generation. "Should the cell still be alive until the eleventh generation, it becomes a prime elder" = apply state change from Elder to Prime Elder at age of 10, since the new Prime Elder state needs to be applied for the output of the 11th generation. The importance of requirement interpretation and attention to detail is sure to be important in software development.

Overall I found the project to be challenging, exciting and interesting. I find the concept behind the Game of Life to be fascinating, and I have been reading about cellular automation and the Von Neumann universal constructor being designed in the 1940s(!) as a result of being exposed to this assignment. Very fascinating.

I think the modules have prepared us well for the assignment, as long as they have been actually studied properly. Additional research outside the modules have been conducted, but I believe that is more due to forgetting some details already studied in the modules, as well as the convenience of search engines and my own habit of self studying subjects online - rather than a lack of information in the modules. I tend to use sources such as Corey Schafer since he has been selected as a good source for the course.




