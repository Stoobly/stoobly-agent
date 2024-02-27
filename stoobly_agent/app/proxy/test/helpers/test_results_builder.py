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
    self.__expected_latency = test_data.get('expected_latency')
    self.__expected_response = test_data.get('expected_response')
    self.__expected_status_code = test_data.get('expected_status_code')
    self.__log = test_data.get('log')
    self.__passed = test_data.get('passed')
    self.__request_id = test_data.get('request_id')
    self.__received_response = test_data.get('received_response')
    self.__skipped = test_data.get('skipped')
    self.__status = test_data.get('status')
    self.__strategy = test_data.get('strategy')

  @property
  def expected_latency(self):
    return self.__expected_latency

  @property
  def expected_response(self):
    return self.__expected_response

  @property
  def expected_status_code(self):
    return self.__expected_status_code

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
  def skipped(self):
    return self.__skipped

  @property
  def status(self):
    return self.__status

  @property
  def strategy(self):
    return self.__strategy

  def with_expected_latency(self, latency: int):
    self.__expected_latency = latency
    return self

  def with_expected_response(self, response: bytes):
    self.__expected_response = response
    return self

  def with_expected_status_code(self, status_code: int):
    self.__expected_status_code = status_code
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
      'expected_latency': self.__expected_latency, 
      'expected_status_code': self.__expected_status_code, 
      'log': self.__log,
      'passed': self.__passed,
      'request_id': self.__request_id,
      'skipped': self.__skipped,
      'status': self.__status,
      'strategy': self.__strategy, 
    }

    received, received_format = self.__serialize_response(self.__received_response)
    expected, expected_format = self.__serialize_response(self.__expected_response)
    return REQUEST_DELIMITTER.join([
      received_format,
      received,
      expected_format,
      expected,
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
    
    self.__expected_latency = test_data.get('expected_latency')
    self.__expected_status_code = test_data.get('expected_status_code')
    self.__log = test_data.get('log')
    self.__passed = test_data.get('passed')
    self.__request_id = test_data.get('request_id')
    self.__skipped = test_data.get('skipped')
    self.__status = test_data.get('status')
    self.__strategy = test_data.get('strategy')

  def __serialize_response(self, data):
    if data == None:
      return b'', TEXT_DATA

    if isinstance(data, bytes):
      return data, TEXT_DATA 
      
    return json.dumps(data).encode(), JSON_DATA