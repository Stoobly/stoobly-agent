import pdb

from tabulate import tabulate
from typing import List, TypedDict

class TabulatePrintOptions(TypedDict):
  filter: dict
  format: str

def tabulate_print(records: List[dict], **kwargs: TabulatePrintOptions):
  filter = kwargs.get('filter') or {}
  format = kwargs.get('format') or 'orgtbl'

  headers = []
  rows = []
  for record in records:
    build_header = len(headers) == 0

    row = []
    for key, val in record.items():
      if key in filter:
        continue

      if build_header:
        headers.append(key)

      row.append(val)

    rows.append(row)

  print(tabulate(rows, headers=headers, tablefmt=format))