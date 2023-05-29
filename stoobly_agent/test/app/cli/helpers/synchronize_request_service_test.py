import copy
import json
import pdb
import pytest
from stoobly_agent.app.cli.helpers.request_synchronize_handler import RequestSynchronizeHandler

from stoobly_agent.app.cli.helpers.synchronize_request_service import synchronize_component
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response

class TestSynchronizeRequestService():

  class TestWhenAdding():
    @pytest.fixture(scope='function')
    def query_param_names_facade(self):
      query_param_names = copy.deepcopy(endpoint_show_response['query_param_names'])
      aliases = copy.deepcopy(endpoint_show_response['aliases'])

      facade = RequestComponentNamesFacade(query_param_names).with_aliases(aliases)
      return facade

    @pytest.fixture(scope='function')
    def response_param_names_facade(self):
      response_param_names = copy.deepcopy(endpoint_show_response['response_param_names'])
      aliases = copy.deepcopy(endpoint_show_response['aliases'])

      facade = RequestComponentNamesFacade(response_param_names).with_aliases(aliases)
      return facade

    def test_array_of_object_one_property(self, response_param_names_facade: RequestComponentNamesFacade):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])
      response = [{}]
      expected_response = [{'id': 934}]
      handler = RequestSynchronizeHandler(request_component.RESPONSE_PARAM)

      result = synchronize_component(response, response_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response)
      assert success == True

    def test_array_of_object_two_property(self, response_param_names_facade: RequestComponentNamesFacade):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])
      self.__decorate_with_values(response_param_names_facade, '[*].category', [1])
      response = [{}]
      expected_response = [{'category': 1, 'id': 934}]
      handler = RequestSynchronizeHandler(request_component.RESPONSE_PARAM)

      result = synchronize_component(response, response_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response)
      assert success == True

    def test_array_of_objects_one_property(self, response_param_names_facade: RequestComponentNamesFacade):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])
      response = [{}, {}]
      expected_response = [{'id': 934}, {'id': 934}]
      handler = RequestSynchronizeHandler(request_component.RESPONSE_PARAM)

      result = synchronize_component(response, response_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response)
      assert success == True

    def __decorate_with_values(self, facade: RequestComponentNamesFacade, query: str, value):
      facade.query_index[query]['values'] = value

    def __equals(self, a, b):
      return json.dumps(a) == json.dumps(b)

  class TestWhenRemoving():
    @pytest.fixture(scope='function')
    def body_param_names_facade(self):
      body_param_names = copy.deepcopy(endpoint_show_response['body_param_names'])
      aliases = copy.deepcopy(endpoint_show_response['aliases'])

      facade = RequestComponentNamesFacade(body_param_names).with_aliases(aliases)
      return facade

    @pytest.fixture(scope='function')
    def response_param_names_facade(self):
      response_param_names = copy.deepcopy(endpoint_show_response['response_param_names'])
      aliases = copy.deepcopy(endpoint_show_response['aliases'])

      facade = RequestComponentNamesFacade(response_param_names).with_aliases(aliases)
      return facade
    
    def test_dict_of_object(self, response_param_names_facade: RequestComponentNamesFacade):
      response = {'to-remove': 1}
      expected_response = {}
      handler = RequestSynchronizeHandler(request_component.RESPONSE_PARAM)

      result = synchronize_component(response, response_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response) 
      assert success == True

    def test_dict_of_objects(self, body_param_names_facade: RequestComponentNamesFacade):
      self.__decorate_with_values(body_param_names_facade, 'name', ['abc'])
      response = {'name': 'abc', 'to-remove': 1}
      expected_response = {'name': 'abc'}
      handler = RequestSynchronizeHandler(request_component.BODY_PARAM)

      result = synchronize_component(response, body_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response)
      assert success == True

    def test_array_of_object_one_property(self, response_param_names_facade: RequestComponentNamesFacade):
      response = [{'to-remove': 1}]
      expected_response = [{}]
      handler = RequestSynchronizeHandler(request_component.RESPONSE_PARAM)

      result = synchronize_component(response, response_param_names_facade, handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response) 
      assert success == True

    def __equals(self, a, b):
      return json.dumps(a) == json.dumps(b)

    def __decorate_with_values(self, facade: RequestComponentNamesFacade, query: str, value):
      facade.query_index[query]['values'] = value

