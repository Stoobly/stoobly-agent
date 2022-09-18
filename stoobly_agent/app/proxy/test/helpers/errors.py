import pdb

def length_match_error(path_key, expected_value, actual_value):
    if not expected_value:
        return False, f"Key '{path_key}' length did not match: got {len(actual_value)}"
    else:
        return False, f"Key '{path_key}' length did not match: got {len(actual_value)}, expected {len(expected_value)}"

def param_name_exists_error(path_key):
    return False, f"Extra key: expected {path_key} to not exist"

def param_name_missing_error(path_key):
    return False, f"Missing key: expected {path_key} to exist"

def type_match_error(path_key, expected_value, actual_value):
    return False, f"Key '{path_key}' type did not match: got {actual_value}, expected {expected_value}"

def valid_type_error(path_key, value, valid_types):
    valid_types = list(map(lambda t: str(t), valid_types))
    return False, f"Key '{path_key}' type did not match: got {type(value)}, expected valid types {', '.join(valid_types)}"

def value_match_error(path_key, expected_value, actual_value):
    if len(path_key) == 0:
        return False, f"Match error: got {actual_value}, expected {expected_value}"
    else:
        return False, f"Key '{path_key}' did not match: got {actual_value}, expected {expected_value}"