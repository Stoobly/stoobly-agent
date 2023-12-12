import json
import pdb

from typing import Callable, List, TypedDict, Union

class JsonPrintOptions(TypedDict):
  filter: list
  print_handler: Union[Callable, None]
  select: list

def json_print(records: List[dict], **kwargs: JsonPrintOptions):
  filter = kwargs.get('filter') or []
  print_handler = kwargs.get('print_handler') or print
  select = kwargs.get('select') or []

  rows = []
  for record in records:
    row = {}
    for key, val in record.items():
      # If exclude list is provided, check if key is excluded
      if key in filter:
        continue
      
      # If include list is provided, check if key is included
      if len(select) > 0 and key not in select:
        continue

      row[key] = str(val) if val != None else None
    
    rows.append(row)

  print_handler(json.dumps(rows, indent=2))