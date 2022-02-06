#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import ast
import pprint
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep

import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """

    #  Tests if an absolute path exists to the _Resources/_project_files directory, if false - creates the directory.
    #  Then it tests if '.json' file extension is included in _file_name, if false - appends it to the
    #  end of _file_name. Opens the file in a context manager in read mode and loads the json into
    #  the dictionary seed_dict.
    #
    #  The seed_dict dictionary is then parsed from an incompatible format into a correct one using a series of nested
    #  loops.
    #
    #  Loops through seed_dict keys, and formats the world_size value into a tuple. Then it
    #  loops through a copy() of the cells keys in the population dictionary. The reason for using a copy iterator, is
    #  to avoid modifying the actual iterator while looping over the cell keys.
    #
    #  If cell key is not None - it loops through the cell's 'neighbours' list and formats each neighbour to a tuple.
    #  Here it also creates a key-value pair for the cell age with a value of 0. This is to compensate for the fact
    #  that the seed files have no 'age' key-value pair.
    #
    #  Finally it replaces each cell key in the population dictionary with a quote-less key using a one line dictionary
    #  pop and replace statement. The new key is created by using literal_eval() on the previous key, which removes the
    #  quotes.
    #
    #  Returns a tuple (dict(population), tuple(world size))

    seeds_path = RESOURCES.absolute() / '_Project_Files'
    if not seeds_path.exists():
        seeds_path.mkdir()

    if '.json' not in _file_name:
        _file_name = f'{_file_name}.json'

    file_path = Path(f'{seeds_path}/{_file_name}')

    with Path.open(file_path, 'r', encoding='UTF-8') as f_hand:
        seed_dict = json.load(f_hand)

    for key in seed_dict.keys():
        if key == 'world_size':
            world_size_value = seed_dict[key]
            seed_dict[key] = tuple(world_size_value)

        elif key == 'population':
            population_dict = seed_dict[key]

            for cell in population_dict.copy().keys():
                cell_dict = population_dict[cell]

                if cell_dict is not None:
                    neighbours_list = cell_dict['neighbours']
                    cell_dict['age'] = 0

                    for index, neighbour in enumerate(neighbours_list):
                        neighbours_list[index] = tuple(neighbour)

                #  Replaces string key in population dictionary with tuple key
                population_dict[literal_eval(cell)] = population_dict.pop(cell)

    return seed_dict['population'], seed_dict['world_size']


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """

    # Gets a logger object with the name 'gol_logger' and sets the log level to INFO.
    #
    # Sets an absolute path log_path to the log file _Resources/gol.log, then runs
    # logging.FileHandler to set up a file handler to the specified log_path in write mode.
    #
    # Adds the file handler to the 'gol_logger' logger object and returns the logger object.

    logger_object = logging.getLogger('gol_logger')
    logger_object.setLevel("INFO")

    log_path = RESOURCES.absolute() / 'gol.log'
    file_handler = logging.FileHandler(filename=log_path, mode='w')

    logger_object.addHandler(file_handler)

    return logger_object


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """

    # This function decorates run_simulation(). The simulation_decorator() function
    # takes the original function as parameter func. The inner wrapper() function
    # takes the same parameters as original function run_simulation().
    #
    # Calls the create_logger() function to get the logger object, and calculates
    # the number of populated cells. For this a list comprehension is used that makes a list of all the _population keys
    # that is not None. The rim cells are excluded from list in this way. The length of this list is then extracted
    # using len() - which gives the number of populated cells.
    #
    # Loops through the range made from _generations and clears console for each generation, then loops through
    # the keys in _population and increments the cells_living counter by 1 for each cell that is not a rim cell, and has
    # an alive state of either cb.STATE_ALIVE, cb.STATE_ELDER or cb.STATE_PRIME_ELDER. It also increments the counter
    # cells_state_elder by 1 for each cell with state cb.STATE_ELDER, and increments the counter cells_state_prime_elder
    # by 1 for each cell with state cb.STATE_PRIME_ELDER.
    #
    # Calculates the dead cells by subtracting cells_living from population_number.
    #
    # Logs information about current generation to _Resources/gol.log. This includes GENERATION counter with start 0,
    # population number, number of living cells, number of elders, number of prime elders and number of dead cells.
    #
    # Calls the original run_simulation() function as func with the original arguments
    # which returns update_world(_population, _world_size). The updated population states
    # are stored in _population and further execution is delayed 200ms between ticks.

    def wrapper(_generations: int, _population: dict, _world_size: tuple):
        """Controls generation ticks and logs generation info to _Resources/gol.log"""

        logger = create_logger()
        population_number = len([cell for cell in _population.keys() if _population[cell] is not None])

        for gen in (range(_generations)):

            cb.clear_console()

            cells_living = 0
            cells_state_elder = 0
            cells_state_prime_elder = 0
            for cell in _population:
                if _population[cell] is not None:
                    if _population[cell]['state'] == cb.STATE_ALIVE:
                        cells_living += 1
                    elif _population[cell]['state'] == cb.STATE_ELDER:
                        cells_state_elder += 1
                        cells_living += 1
                    elif _population[cell]['state'] == cb.STATE_PRIME_ELDER:
                        cells_state_prime_elder += 1
                        cells_living += 1

            cells_dead = population_number - cells_living

            logger.info(f'GENERATION {gen}')
            logger.info(f'Population: {population_number}')
            logger.info(f'Alive: {cells_living}')
            logger.info(f'Elders: {cells_state_elder}')
            logger.info(f'Prime Elders: {cells_state_prime_elder}')
            logger.info(f'Dead: {cells_dead}')

            _population = func(_generations, _population, _world_size)
            sleep(0.2)

        return None

    return wrapper


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------


def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    #  Takes the stated arguments from -ws and splits it on 'x'.
    #
    #  Inside a try clause it tests if input list size_value consists of exactly two numeric values separated by x,
    #  and if these values are bigger than 1. If any of these two tests return True, it raises Assertion or Value
    #  errors with appropriate error messages and sets the world width and height to default values.
    #
    #  If these tests return False, it returns the width and height that was stated as commandline arguments.
    #
    #  Returns tuple with width, height to populate_world()

    size_values = _arg.split('x')

    try:
        if not len(size_values) == 2 or not size_values[0].isnumeric() or not size_values[1].isnumeric():
            raise AssertionError
        width, height = int(size_values[0]), int(size_values[1])
        if width < 1 or height < 1:
            raise ValueError
    except AssertionError:
        print(f"World size should contain width and height, separated by ‘x’. Ex: ‘80x40'")
        print('Using default world size: 80x40')
        width, height = 80, 40
    except ValueError:
        print('Both width and height needs to have positive values above zero.')
        print('Using default world size: 80x40')
        width, height = 80, 40

    return width, height


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """

    #  Creates an empty dictionary for the population and lists of numbers in a range derived from _world_size
    #  width and height.
    #
    #  Then tests if a seed has been stated in the -s argument, if True the pattern is loaded using cb.get_pattern for
    #  for the actual seed and world size.
    #
    #  If False, sets pattern to None.
    #
    #  Makes a coordinate grid based on the lists of numbers in the range of the world size by a Cartesian product.
    #
    #  The product is made by world height, world_width (Y,X) instead of world_width, world_height (X,Y)
    #  in order to create each "X-coordinate" for every "Y-coordinate" instead of the opposite. This is also
    #  to accommodate the format used for the coordinate patterns in cb.get_pattern.
    #
    #  Iterating through the cells in the Cartesian product, it tests if the cell is a rim cell by testing
    #  if the cell has max or min value for either width or height.
    #
    #  Tests if a seed pattern has been stated as argument. If true - determines cell state from pattern, if
    #  false - randomises cell state using the random.randint() function combined with an if/else clause.
    #
    #  Creates dictionary for initial population based on results of the above steps, and by calling the
    #  calc_neighbour_positions. It also sets the 'age' = 0 key/value pair for each cell, since this is the
    #  initial seed state of the population, generation 0. Returns the population dictionary to run_simulation().

    population = {}

    world_width, world_height = list(range(_world_size[0])), list(range(_world_size[1]))

    if _seed_pattern is not None:
        pattern = cb.get_pattern(_seed_pattern, _world_size)
    else:
        pattern = None

    for cell in itertools.product(world_height, world_width):

        if cell[1] == min(world_width) or cell[1] == max(world_width):
            population[cell] = None
            continue
        elif cell[0] == min(world_height) or cell[0] == max(world_height):
            population[cell] = None
            continue
        elif _seed_pattern is not None:
            if cell in pattern:
                cell_state = cb.STATE_ALIVE
            else:
                cell_state = cb.STATE_DEAD
        else:
            num = random.randint(0, 20)
            if num > 16:
                cell_state = cb.STATE_ALIVE
            else:
                cell_state = cb.STATE_DEAD

        population[cell] = {}
        population[cell]['state'] = cell_state
        population[cell]['neighbours'] = calc_neighbour_positions(cell)
        population[cell]['age'] = 0

    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    #  Creates a list of possible offset values, and an empty neighbours list.
    #
    #  Creates all possible combinations of offsets in tuple format using a cartesian product
    #  then creates a new tuple with the summed values of the itertools generated offset tuple
    #  and the _cell_coord tuple. For this, a generator expression is used with zip(), which combines
    #  the item iterator with the _cell_coord and the resulting values are summed using the sum() function.
    #  The generator object is then casted into a tuple.
    #
    #  Appends each created neighbour tuple to the neighbours list, and then removes the original _cell_coord
    #  which leaves only the neighbours in the list.
    #
    #  Returns the neighbours to function call in populate_world().

    offsets = [-1, 1, 0]
    neighbours = list()

    for item in itertools.product(offsets, repeat=2):
        item = tuple(sum(value) for value in zip(item, _cell_coord))
        neighbours.append(item)
    neighbours.remove(_cell_coord)

    return neighbours


@simulation_decorator
def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """

    # This function only returns a function call to update_world, which returns updated
    # population states. The actual simulation ticks are handled in the simulation_decorator()

    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """

    #  Creates empty dictionary for next generation, then iterates through each cell
    #  in the _cur_gen from run_simulation() with start = 1 to get actual numbers for cells iterated over.
    #
    #  Creates an empty nested dictionary for the cell, then checks if the cell is a
    #  rim cell. If true, it prints the formatted value for rim cells using cb.progress together with cb.get_print_value
    #  and copies the cell state from _cur_gen cell to the next_gen cell. Then tests if the index from enumerate is
    #  evenly divisible with the world width. If True, this means the current cell being iterated over is
    #  located at the maximum world width, and a line break is performed by printing a newline to console.
    #
    #  If the cell is not a rim cell the generational update block is executed. It prints the _cur_gen cell state
    #  and copies the _cur_gen cell neighbours to next_gen cell neighbours since the cell neighbours will always
    #  have the same position. It then copies the _cur_gen cell age key/value pair to prepare it for modification
    #  depending on the game rules. Then it determines the _cur_gen cell alive neighbours using count_alive_neighbours
    #  which is important for determining the next cell state.
    #
    #  The cell states for the next generation are determined as follows.
    #
    #  If the _cur_gen cell is either alive, elder och a prime elder AND it has 2 or 3 living neighbours:
    #
    #  1. An alive cell is updated to an elder if it has survived more than 5 consecutive generations - which means an
    #  age value of 5 since seed generation 0 has an age value of 0. If age is not 5, it remains an alive cell.
    #
    #  2. An elder cell is updated to a prime elder if it has been alive until the 11th generation - which means an age
    #  value of 10 or above since seed generation 0 has an age value of 0 and it should first become a prime elder in
    #  the 11th generation. If age < 10, it remains an elder cell.
    #
    #  3. A prime elder cell remains a prime elder.
    #
    #
    #  Finally the cell age is incremented by + 1 regardless of outcome since it will live on the next generation.
    #
    #
    #  If the _cur_gen cell is dead, AND it has exactly 3 living neighbours:
    #
    #  The cell becomes alive with an age of 0.
    #
    #
    #  If the _cur_gen cell is either alive, elder or a prime elder AND none of the above steps have been run:
    #
    #  The cell becomes dead with an age of 0.
    #
    #
    #  If none of the above steps have been run:
    #
    #  The cell state is unchanged, current state is copied to next state.
    #
    #
    #  Finally the next_gen cell state is set based on the above tests and the next_gen population dictionary is
    #  returned to run_simulation().

    next_gen = {}

    for num, cell in enumerate(_cur_gen, start=1):

        next_gen[cell] = {}

        if _cur_gen[cell] is None:
            cb.progress(cb.get_print_value(cb.STATE_RIM))
            next_gen[cell] = _cur_gen[cell]
            if num % _world_size[0] == 0:
                cb.progress('\n')

        else:
            cb.progress(cb.get_print_value(_cur_gen[cell]['state']))

            next_gen[cell]['neighbours'] = _cur_gen[cell]['neighbours']
            next_gen[cell]['age'] = _cur_gen[cell]['age']
            neighbours_alive = count_alive_neighbours(_cur_gen[cell]['neighbours'], _cur_gen)

            if _cur_gen[cell]['state'] in (cb.STATE_ALIVE, cb.STATE_ELDER, cb.STATE_PRIME_ELDER) \
                    and neighbours_alive in (2, 3):
                if _cur_gen[cell]['state'] == cb.STATE_ALIVE:
                    if _cur_gen[cell]['age'] == 5:
                        cell_state = cb.STATE_ELDER
                    else:
                        cell_state = cb.STATE_ALIVE
                elif _cur_gen[cell]['state'] == cb.STATE_ELDER:
                    if _cur_gen[cell]['age'] == 10:
                        cell_state = cb.STATE_PRIME_ELDER
                    else:
                        cell_state = cb.STATE_ELDER
                else:
                    cell_state = cb.STATE_PRIME_ELDER

                next_gen[cell]['age'] += 1

            elif _cur_gen[cell]['state'] == cb.STATE_DEAD and neighbours_alive == 3:
                cell_state = cb.STATE_ALIVE
                next_gen[cell]['age'] = 0

            elif _cur_gen[cell]['state'] in (cb.STATE_ALIVE, cb.STATE_ELDER, cb.STATE_PRIME_ELDER):
                cell_state = cb.STATE_DEAD
                next_gen[cell]['age'] = 0

            else:
                cell_state = _cur_gen[cell]['state']

            next_gen[cell]['state'] = cell_state

    return next_gen


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """

    #  Sets a neighbours_alive counter to 0
    #
    #  Iterates through each neighbour in the neighbour list and tests if cell neighbours is not None (Not a rim cell)
    #  and if their state either cb.STATE_ALIVE, cb.STATE_ELDER or cb.STATE_PRIME_ELDER by comparing it to the same cell
    #  in the _cells dictionary which is the current generation.
    #
    #  If true, it increments neighbours_alive with + 1.
    #
    #  After checking all neighbours, it returns the neighbours_alive counter.

    neighbours_alive = 0
    for neighbour in _neighbours:
        if _cells[neighbour] is not None and _cells[neighbour]['state'] in \
                (cb.STATE_ALIVE, cb.STATE_ELDER, cb.STATE_PRIME_ELDER):
            neighbours_alive += 1

    return neighbours_alive


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
