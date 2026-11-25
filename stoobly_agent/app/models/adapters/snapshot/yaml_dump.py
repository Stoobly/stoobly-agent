import yaml


class YamlLiteralStr(str):
  """str dumped as a YAML literal block scalar (| / |-)."""


def _represent_literal_str(dumper, data):
  return dumper.represent_scalar('tag:yaml.org,2002:str', str(data), style='|')


yaml.add_representer(YamlLiteralStr, _represent_literal_str, Dumper=yaml.SafeDumper)


def _wrap_header_strings(obj):
  """Recursively wrap `headers` string values so dumps use the | block style."""
  if isinstance(obj, dict):
    out = {}
    for key, value in obj.items():
      if key == 'headers' and isinstance(value, str):
        out[key] = YamlLiteralStr(value)
      else:
        out[key] = _wrap_header_strings(value)
    return out
  if isinstance(obj, list):
    return [_wrap_header_strings(item) for item in obj]
  return obj


def dump_snapshot_yaml(data, stream=None, **kwargs):
  """
  Dump snapshot YAML with request/response `headers` as literal block scalars.

  Uses the | / |- style so multiline header blocks stay readable.
  """
  kwargs.setdefault('sort_keys', False)
  kwargs.setdefault('default_flow_style', False)
  return yaml.safe_dump(_wrap_header_strings(data), stream, **kwargs)
