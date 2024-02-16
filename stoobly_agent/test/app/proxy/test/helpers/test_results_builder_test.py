import pdb
import pytest

from stoobly_agent.app.proxy.test.helpers.test_results_builder import DownloadTestData, TestResultsBuilder as Builder
from stoobly_agent.config.constants import test_strategy

class TestBuilder():

  class TestWhenValid():
    @pytest.fixture(scope='class')
    def test_results(self) -> DownloadTestData:
      return {
        'expected_response': b'expected',
        'log': 'test',
        'passed': True,
        'request_id': 1,
        'received_response': b'received',
        'skipped': False,
        'status': 200,
        'strategy': test_strategy.FUZZY,
      }

    @pytest.fixture(scope='class')
    def builder(self, test_results) -> Builder:
      _builder = Builder(**test_results)
      builder = Builder()
      builder.deserialize(_builder.serialize())
      return builder

    def test_it_has_expected_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.expected_response == test_results['expected_response']

    def test_it_has_log(self, builder: Builder, test_results: DownloadTestData):
      assert builder.log == test_results['log']

    def test_it_has_passed(self, builder: Builder, test_results: DownloadTestData):
      assert builder.passed == test_results['passed']

    def test_it_has_request_id(self, builder: Builder, test_results: DownloadTestData):
      assert builder.request_id == test_results['request_id']

    def test_it_has_received_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.received_response == test_results['received_response']

    def test_it_has_skipped(self, builder: Builder, test_results: DownloadTestData):
      assert builder.skipped == test_results['skipped']

    def test_it_has_status(self, builder: Builder, test_results: DownloadTestData):
      assert builder.status == test_results['status']

    def test_it_has_strategy(self, builder: Builder, test_results: DownloadTestData):
      assert builder.strategy == test_results['strategy']

  class TestWhenEmptyResponse():
    @pytest.fixture(scope='class')
    def test_results(self) -> DownloadTestData:
      return {
        'expected_response': '',
        'received_response': '',
      }

    @pytest.fixture(scope='class')
    def builder(self, test_results) -> Builder:
      _builder = Builder(**test_results)
      builder = Builder()
      builder.deserialize(_builder.serialize())
      return builder

    def test_it_has_expected_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.expected_response == test_results['expected_response']

    def test_it_has_received_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.received_response == test_results['received_response']

  class TestWhenTraversibleResponse():
    @pytest.fixture(scope='class')
    def test_results(self) -> DownloadTestData:
      return {
        'expected_response': {},
        'received_response': {},
      }

    @pytest.fixture(scope='class')
    def builder(self, test_results) -> Builder:
      _builder = Builder(**test_results)
      builder = Builder()
      builder.deserialize(_builder.serialize())
      return builder

    def test_it_has_expected_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.expected_response == test_results['expected_response']

    def test_it_has_received_response(self, builder: Builder, test_results: DownloadTestData):
      assert builder.received_response == test_results['received_response']