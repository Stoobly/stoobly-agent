class ConditionalDecorator():

  def __init__(self, decorator, condition):
    self.__decorator = decorator
    self.__condition = condition

  def __call__(self, f):
    if not self.__condition:
      return f
    
    return self.__decorator(f)