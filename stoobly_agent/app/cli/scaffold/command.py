class Command():

  def __init__(self, **kwargs):
    self.__namespace = kwargs.get('namespace') or ''

  @property
  def namespace(self):
    return self.__namespace