type_map = {}
type_map[str(list)] = 'Array'
type_map[str(dict)] = 'Hash'
type_map[str(int)] = 'Integer'
type_map[str(float)] = 'Float'
type_map[str(str)] = 'String'
type_map[str(bool)] = 'Boolean'

reverse_type_map = {}
reverse_type_map['Array'] = list()
reverse_type_map['Hash'] = dict()
reverse_type_map['Integer'] = int()
reverse_type_map['Float'] = float()
reverse_type_map['String'] = str()
reverse_type_map['Boolean'] = bool() 

def convert(python_type: str):
  return type_map.get(python_type)

def convert_reverse(ruby_type: str):
  return reverse_type_map.get(ruby_type)

