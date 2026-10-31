from .gor_importer import GorImporter
from .har_importer import HarImporter

HAR_FORMAT = 'har'
GOR_FORMAT = 'gor'
IMPORT_FORMATS = [HAR_FORMAT, GOR_FORMAT]


def get_importer(format: str):
  if format == HAR_FORMAT:
    return HarImporter()
  if format == GOR_FORMAT:
    return GorImporter()
  raise ValueError(f'Unsupported import format: {format}')
