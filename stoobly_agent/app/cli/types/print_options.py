from typing import Callable, TypedDict, Union

class PrintOptions(TypedDict):
  filter: list
  print_handler: Union[Callable, None]
  select: list

class TabulatePrintOptions(PrintOptions):
  format: str
  headers: bool