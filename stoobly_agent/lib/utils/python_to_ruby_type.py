type_map = {}
type_map[str(list)] = 'Array'
type_map[str(dict)] = 'Hash'
type_map[str(int)] = 'Integer'
type_map[str(float)] = 'Float'
type_map[str(str)] = 'String'
type_map[str(bool)] = 'Boolean'

def convert(python_type: str):
  return type_map.get(python_type)
