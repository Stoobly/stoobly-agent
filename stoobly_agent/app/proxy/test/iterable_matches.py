from typing import Tuple

def dict_matches(d1: dict, d2: dict, path_key: str) -> Tuple[bool, str]:
    for key, val in d1.items():
        path_key = '.'.join([path_key, key])

        if key not in d2:
            return False, f"Expected {path_key} to exist"

        if type(val) != type(d2[key]):
            return False, f"Expected type for {path_key} to match, got {type(d2[key])}, expected {type(d1[key])}"

        if type(val) is dict:
            return dict_matches(val, d2[key], path_key)

        if type(val) is list:
            return list_matches(val, d2[key], path_key)

    return True, ''

###
#
# For list matching, look for all types in expected list
# Expect tested list to have a type that exists in expected list
#
# If list value is traversable, traverse
#
def list_matches(l1: list, l2: list, path_key: str) -> Tuple[bool, str]:
    valid_types = []
    type_examples = {}

    for i, val in enumerate(l1):
        valid_types.append(type(val))

        if type(val) is dict and str(dict) not in type_examples:
            type_examples[dict] = val
        elif type(val) is list and str(list) not in type_examples:
            type_examples[list] = val

    for i, val in enumerate(l2):
        path_key = f"{path_key}[{i}]"

        if type(val) not in valid_types:
            return False, f"Expected type for {path_key} to exist, got {type(val)}, expected {valid_types}"

        if type(val) is dict:
            return dict_matches(type_examples[dict], val)

        if type(val) is list:
            return dict_matches(type_examples[list], val)

    return True, ''