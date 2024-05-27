from .constants import DOCKER_NAMESPACE

class Command():

  def __init__(self, **kwargs):

    self.__namespace = kwargs.get('namespace') or ''

  @property
  def namespace(self):
    return self.__namespace

  def as_docker(self):
    self.__namespace = DOCKER_NAMESPACE
    return self