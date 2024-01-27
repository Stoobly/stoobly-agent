import json
import pdb

from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER

from .upload_test_service import UploadTestData

JSON_DATA = b'json'
TEXT_DATA = b'text'

class DownloadTestData(UploadTestData):
  received_response: bytes

class TestResultsBuilder():

  def __init__(self, **test_data: DownloadTestData):
    self.__expected_response = test_data.get('expected_response')
    self.__log = test_data.get('log')
    self.__passed = test_data.get('passed')
    self.__request_id = test_data.get('request_id')
    self.__received_response = test_data.get('received_response')
    self.__status = test_data.get('status')
    self.__strategy = test_data.get('strategy')

  @property
  def expected_response(self):
    return self.__expected_response

  @property
  def log(self):
    return self.__log

  @property
  def passed(self):
    return self.__passed

  @property
  def request_id(self):
    return self.__request_id

  @property
  def received_response(self):
    return self.__received_response

  @property
  def status(self):
    return self.__status

  @property
  def strategy(self):
    return self.__strategy

  def with_expected_response(self, response: bytes):
    self.__expected_response = response
    return self

  def with_log(self, log):
    self.__log = log
    return self

  def with_passed(self, passed: bool):
    self.__passed = passed
    return self

  def with_received(self, response: bytes):
    self.__received_response = response
    return self

  def with_request_id(self, request_id):
    self.__request_id = request_id
    return self

  def with_status(self, status):
    self.__status = status
    return self

  def with_strategy(self, strategy):
    self.__strategy = strategy
    return self

  def serialize(self) -> bytes:
    metadata = {
      'log': self.__log,
      'passed': self.__passed,
      'request_id': self.__request_id,
      'status': self.__status,
      'strategy': self.__strategy, 
    }

    return REQUEST_DELIMITTER.join([
      TEXT_DATA if isinstance(self.__received_response, bytes) else JSON_DATA,
      self.__serialize_response(self.__received_response),
      TEXT_DATA if isinstance(self.__expected_response, bytes) else JSON_DATA,
      self.__serialize_response(self.__expected_response),
      json.dumps(metadata).encode()
    ])

  def deserialize(self, data: bytes):
    toks = data.split(REQUEST_DELIMITTER)

    toks_length = len(toks)

    self.__received_response_header = toks[toks_length - 5]
    self.__received_response = toks[toks_length - 4]
    if self.__received_response_header == JSON_DATA:
      self.__received_response = json.loads(self.__received_response.decode())

    self.__expected_response_header = toks[toks_length - 3]
    self.__expected_response = toks[toks_length - 2]
    if self.__expected_response_header == JSON_DATA:
      self.__expected_response = json.loads(self.__expected_response.decode())

    test_data = {} 
    try: 
      test_data = json.loads(toks[toks_length - 1].decode())
    except:
      pass

    self.__log = test_data.get('log')
    self.__passed = test_data.get('passed')
    self.__request_id = test_data.get('request_id')
    self.__status = test_data.get('status')
    self.__strategy = test_data.get('strategy')

  def __serialize_response(self, data):
    if not data:
      return b''
    return data if isinstance(data, bytes) else json.dumps(data).encode()