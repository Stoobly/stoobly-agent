from typing import Union

class RequestStringControl():
  REQUEST_TYPE = 1

  def __init__(self, c: Union[bytes, str] = None):
    if not c:
      self.__request_type = self.REQUEST_TYPE
      self.__id = None
      self.__timestamp = None
    else:
      self.parse(c)

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, id: str):
    self.__id = id

  @property
  def request_type(self):
    return self.__request_type

  @property
  def timestamp(self):
    return self.__timestamp

  @timestamp.setter
  def timestamp(self, t: int):
    self.__timestamp = t

  def parse(self, s: Union[bytes, str]):
    if isinstance(s, bytes):
      s = s.decode()

    toks = s.split(' ')
    self.__id = toks[1]
    self.__timestamp = int(toks[2])

  def serialize(self):
    return "{} {} {}".format(self.REQUEST_TYPE, self.__id, self.__timestamp)