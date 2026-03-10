from typing import List, Union

def normalize_public_dir_path(public_dir_path: Union[str, List[str]]):
  if isinstance(public_dir_path, (list, tuple)):
    return ','.join(public_dir_path)
  else:
    return public_dir_path

def normalize_response_fixtures_path(response_fixtures_path: Union[str, List[str]]):
  if isinstance(response_fixtures_path, (list, tuple)):
    return ','.join(response_fixtures_path)
  else:
    return response_fixtures_path