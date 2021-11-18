from random import choice
from itertools import product
from pprint import pprint


def make_variants(dict_tasks, num_of_variants, retake=False):
    # Input data processing:

    if not dict_tasks:
        return -3

    # Finding the number of tasks in a variant
    num_of_tasks_in_var = max(dict_tasks, key=lambda x: x['number'])['number']

    # Exit status -1 in case of invalid number of tasks
    if len(set([_v['number'] for _v in dict_tasks])) != num_of_tasks_in_var:
        return -1

    # Exit status -2 in case of invalid entered number of variants
    if num_of_variants <= 0:
        return -2

    # Packing tasks by number:
    filtered_tasks = []
    for _num in range(num_of_tasks_in_var):
        filtered_tasks.append(list(filter(lambda dict_task: dict_task['number'] == (_num + 1), dict_tasks)))

    # Warning announcement:
    function_warnings = []

    # Finding the number of tasks in each type:
    if not all(len(filtered_tasks[_i]) == len(filtered_tasks[_i + 1]) for _i in range(num_of_tasks_in_var - 1)):
        function_warnings.append('The number of tasks should be equal')

    # Finding the number of all the unique variations:
    num_of_diff_var = 1
    for _t in filtered_tasks:
        num_of_diff_var *= len(_t)

    # Finding the difference between the number of unique variants and the number of entered
    if num_of_variants > num_of_diff_var:
        function_warnings.append(f'The number of variants should be no more than {num_of_diff_var}')

    function_warnings = tuple(function_warnings)

    # Creating unique variants:
    max_num_of_tasks = len(max(filtered_tasks, key=len))  # Finding the maximum number task in all types

    # Creating an original list of different variations by product from itertools for backup in future
    variants_t_original = [_v for _v in product(range(max_num_of_tasks), repeat=num_of_tasks_in_var)]
    variants_t = variants_t_original.copy()  # Copying the original list

    # Packing in dictionaries.
    total_variants = dict()  # Creating a dict for total variants.
    # Packing variants.
    for _num_of_var in range(num_of_variants):
        # Due to deletion values and overuse of the list of combinations, the list may empty.
        # So the program has to check the list before use it.
        try:
            _v = choice(variants_t)
        except IndexError:
            variants_t = variants_t_original.copy()
            _v = choice(variants_t)
        variants_t.remove(_v)  # Removing used variants to minimize repetition of combinations.

        # Creation of a new variant.
        variant = []
        for _i, _n in enumerate(_v):
            # Searching and adding task by a unique combination.
            variant.append(filtered_tasks[_i][_n % len(filtered_tasks[_i])])
        total_variants[_num_of_var + 1] = variant  # Adding the variant to dictionary.

    # Creation of a variant for a retake:
    if retake:
        zero_v = []
        if num_of_variants == 1:
            _v = choice(variants_t) # Choosing a random variant from unused.
            for _i, _n in enumerate(_v):
                # Searching and adding task by a unique combination.
                # [_n % len(filtered_tasks[_i])] saving from an index error if the numbers of the tasks are not equal.
                zero_v.append(filtered_tasks[_i][_n % len(filtered_tasks[_i])])
            total_variants[0] = zero_v
        else:
            for _i in range(num_of_tasks_in_var):
                _v = choice(list(total_variants.keys()))  # Choosing a random task from all of the variants.
                zero_v.append(total_variants[_v][_i])
            total_variants[0] = zero_v
        num_of_variants += 1  # Due ti making one more variant the number was raised

    return {
        'tasks': total_variants,
        'warnings': function_warnings,
        'total_rows': num_of_variants * max_num_of_tasks
    }


if __name__ == '__main__':
    demo_data = [
        {
            'number': 1,
            'task': '1 + 1',
            'answer': '2'
        }, {
            'number': 1,
            'task': '2 + 1',
            'answer': '3'
        }, {
            'number': 1,
            'task': '4 + 1',
            'answer': '5'
        }, {
            'number': 2,
            'task': '1 * 2',
            'answer': '2'
        }, {
            'number': 2,
            'task': '2 * 2',
            'answer': '4'
        }, {
            'number': 2,
            'task': '4 * 4',
            'answer': '16'
        }

    ]
    t = make_variants(demo_data, 1, True)
    pprint(t)
