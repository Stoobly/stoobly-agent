import copy
import json
import pdb
import pytest
from stoobly_agent.app.cli.helpers.request_synchronize_handler import RequestSynchronizeHandler

from stoobly_agent.app.cli.helpers.request_synchronize_handler import RequestSynchronizeHandler
from stoobly_agent.app.cli.helpers.synchronize_request_service import SynchronizeRequestService
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response


@pytest.mark.openapi
class TestSynchronizeRequestService():
  @pytest.fixture(scope='class')
  def synchronize_request_service(self) -> SynchronizeRequestService:
    return SynchronizeRequestService(local_db_request_adapter=None)

  @pytest.fixture(scope='class')
  def query_synchronize_handler(self) -> RequestSynchronizeHandler:
    return RequestSynchronizeHandler(request_component.QUERY_PARAM, {})

  @pytest.fixture(scope='class')
  def body_synchronize_handler(self) -> RequestSynchronizeHandler:
    return RequestSynchronizeHandler(request_component.BODY_PARAM, {})

  @pytest.fixture(scope='class')
  def response_synchronize_handler(self) -> RequestSynchronizeHandler:
    return RequestSynchronizeHandler(request_component.RESPONSE_PARAM, {})
  
  @pytest.fixture(scope='function')
  def query_param_names_facade(self) -> RequestComponentNamesFacade:
    query_param_names = copy.deepcopy(endpoint_show_response['query_param_names'])
    aliases = copy.deepcopy(endpoint_show_response['aliases'])

    facade = RequestComponentNamesFacade(query_param_names).with_aliases(aliases)
    return facade
  
  @pytest.fixture(scope='function')
  def body_param_names_facade(self):
    body_param_names = copy.deepcopy(endpoint_show_response['body_param_names'])
    aliases = copy.deepcopy(endpoint_show_response['aliases'])

    facade = RequestComponentNamesFacade(body_param_names).with_aliases(aliases)
    return facade
  
  @pytest.fixture(scope='function')
  def response_param_names_facade(self) -> RequestComponentNamesFacade:
    response_param_names = copy.deepcopy(endpoint_show_response['response_param_names'])
    aliases = copy.deepcopy(endpoint_show_response['aliases'])

    facade = RequestComponentNamesFacade(response_param_names).with_aliases(aliases)
    return facade


  class TestWhenAdding():
    def test_dict_of_object_one_property(self, synchronize_request_service: SynchronizeRequestService, body_param_names_facade: RequestComponentNamesFacade, body_synchronize_handler: RequestSynchronizeHandler):
      self.__decorate_with_values(body_param_names_facade, 'name', ['abc'])
      body_params = {}
      expected_body_params = {'name': 'abc'}

      result = synchronize_request_service.synchronize_component(body_params, body_param_names_facade, body_synchronize_handler)

      assert self.__equals(body_params, expected_body_params), print(body_params)

      success = result[0]
      assert success == True

    def test_dict_does_not_add_extra_optional_params(self, synchronize_request_service: SynchronizeRequestService, query_param_names_facade: RequestComponentNamesFacade, query_synchronize_handler: RequestSynchronizeHandler):
      query_params = {'limit': 3, 'sort': 'color'}
      expected_query_params = {'limit': 3, 'sort': 'color'}

      result = synchronize_request_service.synchronize_component(query_params, query_param_names_facade, query_synchronize_handler)

      assert self.__equals(query_params, expected_query_params), print(query_params)

      success = result[0]
      assert success == True

    def test_array_of_object_one_property(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler: RequestSynchronizeHandler):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])
      response = [{}]

      result = synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)

      expected_response = [{'id': 934}]
      assert self.__equals(response, expected_response), print(response)

      success = result[0]
      assert success == True

    def test_array_of_object_two_property(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler: RequestSynchronizeHandler):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])
      self.__decorate_with_values(response_param_names_facade, '[*].category', [1])

      response = [{}]
      result = synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)

      expected_response = [{'category': 1, 'id': 934}]
      assert self.__equals(response, expected_response), print(response)

      success = result[0]
      assert success == True

    def test_array_of_objects_one_property(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler: RequestSynchronizeHandler):
      self.__decorate_with_values(response_param_names_facade, '[*].id', [934])

      response = [{}, {}]
      result = synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)

      expected_response = [{'id': 934}, {'id': 934}]
      assert self.__equals(response, expected_response), print(response)

      success = result[0]
      assert success == True

    def __decorate_with_values(self, facade: RequestComponentNamesFacade, query: str, value):
      facade.query_index[query]['values'] = value

    def __equals(self, a, b):
      return json.dumps(a) == json.dumps(b)


  class TestWhenRemoving():
    def test_dict_of_object(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler):
      response = {'to-remove': 1}
      expected_response = {}

      result = synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response) 
      assert success == True

    def test_dict_of_objects(self, synchronize_request_service: SynchronizeRequestService, body_param_names_facade: RequestComponentNamesFacade, body_synchronize_handler: RequestSynchronizeHandler):
      self.__decorate_with_values(body_param_names_facade, 'name', ['abc'])
      response = {'name': 'abc', 'to-remove': 1}
      expected_response = {'name': 'abc'}

      result = synchronize_request_service.synchronize_component(response, body_param_names_facade, body_synchronize_handler)
      success = result[0]

      assert self.__equals(response, expected_response), print(response)
      assert success == True
    
    def test_array_of_object_one_property(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler: RequestSynchronizeHandler):
      response = [{'to-remove': 1}]
      result = synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)

      expected_response = [{}]
      assert self.__equals(response, expected_response), print(response) 

      success = result[0]
      assert success == True

    def test_object_two_properties(self, synchronize_request_service: SynchronizeRequestService, response_param_names_facade: RequestComponentNamesFacade, response_synchronize_handler: RequestSynchronizeHandler):
      response = [{'id': 1, 'remove': 1, 'remove2': 1}]
      synchronize_request_service.synchronize_component(response, response_param_names_facade, response_synchronize_handler)

      assert self.__equals(response, [{'id': 1}]), print(response) 

    def __equals(self, a, b):
      return json.dumps(a) == json.dumps(b)

    def __decorate_with_values(self, facade: RequestComponentNamesFacade, query: str, value):
      facade.query_index[query]['values'] = value

