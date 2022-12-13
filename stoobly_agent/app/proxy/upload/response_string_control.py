class ResponseStringControl():
  RESPONSE_TYPE = 2

  def __init__(self):
    self.__response_type = self.RESPONSE_TYPE
    self.__id = None
    self.__timestamp = 0
    self.__latency = 0

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, id: str):
    self.__id = id

  @property
  def latency(self):
    return self.__latency

  @latency.setter
  def latency(self, l: int):
    self.__latency = l

  @property
  def response_type(self):
    return self.__response_type

  @property
  def timestamp(self):
    return self.__timestamp

  @timestamp.setter
  def timestamp(self, t: int):
    self.__timestamp = t

  def parse(self, s: str):
    toks = s.split(' ')
    self.__id = toks[1]
    self.__timestamp = int(toks[2])
    self.__latency = int(toks[3])

  def serialize(self):
    return "{} {} {} {}".format(self.RESPONSE_TYPE, self.__id, self.__timestamp, self.__latency)