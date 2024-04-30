import abc

from mitmproxy.http import Request
from typing import Union

from stoobly_agent.app.proxy.test.helpers.endpoint_facade import EndpointFacade
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.orm.trace import Trace

from .context_response import TestContextResponse

FuzzyContent = Union[dict, list, str]

class TestContextABC(abc.ABC):

  @abc.abstractmethod
  def with_endpoints_resource(self, resource: EndpointShowResponse):
    pass

  @property
  @abc.abstractmethod
  def cached_rewritten_expected_response_content(self) -> FuzzyContent:
    pass

  @property
  @abc.abstractmethod
  def decoded_response_content(self) -> FuzzyContent:
    pass

  @property
  @abc.abstractmethod
  def decoded_expected_response_content(self) -> FuzzyContent:
    pass

  @property
  @abc.abstractmethod
  def endpoint(self) -> EndpointFacade:
    pass

  @property
  @abc.abstractmethod
  def end_time(self):
    pass

  @property
  @abc.abstractmethod
  def expected_latency(self) -> int:
    pass

  @property
  @abc.abstractmethod
  def expected_response(self) -> TestContextResponse:
    pass

  @property
  @abc.abstractmethod
  def expected_status_code(self) -> int:
    pass

  @property
  @abc.abstractmethod
  def filter(self):
    pass

  @property
  @abc.abstractmethod
  def flow(self):
    pass

  @property
  @abc.abstractmethod
  def intercept_settings(self) -> InterceptSettings:
    pass

  @property
  @abc.abstractmethod
  def lifecycle_hooks(self):
    pass

  @property
  @abc.abstractmethod
  def lifecycle_hooks_path(self):
    pass

  @property
  @abc.abstractmethod
  def log(self):
    pass

  @log.setter
  @abc.abstractmethod
  def log(self, v: str):
    pass

  @property
  @abc.abstractmethod
  def mock_context(self):
    pass

  @property
  @abc.abstractmethod
  def mock_request_id(self) -> Union[str, None]:
    pass

  @property
  @abc.abstractmethod
  def mock_request_endpoint_id(self) -> Union[str, None]:
    pass

  @property
  @abc.abstractmethod
  def passed(self):
    pass

  @passed.setter
  @abc.abstractmethod
  def passed(self, v):
    pass

  @property
  @abc.abstractmethod
  def public_directory_path(self):
    pass

  @property
  @abc.abstractmethod
  def replay_context(self):
    pass

  @property
  @abc.abstractmethod
  def request(self) -> Request:
    pass

  @property
  @abc.abstractmethod
  def request_key(self) -> str:
    pass

  @property
  @abc.abstractmethod
  def request_headers(self):
    pass

  @property
  @abc.abstractmethod
  def response(self) -> TestContextResponse:
    pass

  @property
  @abc.abstractmethod
  def response_fixtures(self):
    pass

  @property
  @abc.abstractmethod
  def response_fixtures_path(self):
    pass

  @property
  @abc.abstractmethod
  def response_param_names(self) -> RequestComponentNamesFacade: 
    pass

  @property
  @abc.abstractmethod
  def rewritten_expected_response_content(self):
    pass

  @property
  @abc.abstractmethod
  def skipped(self):
    pass

  @skipped.setter
  @abc.abstractmethod
  def skipped(self, v: bool):
    pass

  @property
  @abc.abstractmethod
  def start_time(self):
    pass

  @property
  @abc.abstractmethod
  def save(self):
    pass

  @property
  @abc.abstractmethod
  def strategy(self):
    pass

  @property
  @abc.abstractmethod
  def trace(self) -> Union[Trace, None]:
    pass
