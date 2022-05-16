import pdb
import requests
import sys

from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.tests_resource import TestsResource
from stoobly_agent.lib.api.users_resource import UsersResource
from stoobly_agent.lib.api.interfaces import TestCreateParams, TestShowResponse, TestsIndexResponse, UserProfileResponse
from stoobly_agent.lib.api.keys import OrganizationKey, TestKey

class TestFacade():

  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.__api = TestsResource(self.__settings.remote.api_url, self.__settings.remote.api_key)

  def create(self, **kwargs: TestCreateParams) -> TestShowResponse:
    organization_key: str = OrganizationKey(kwargs.get('organization_key')) 

    res: requests.Response =  self.__api.create(
      description=kwargs.get('description') or '',
      name=kwargs.get('name'),
      organization_id=organization_key.id
    )

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def show(self, test_key: str) -> TestShowResponse:
    key = TestKey(test_key)
    res = self.__api.show(key.id)

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def show_with_context(self, context: ReplayContext, project_id: str):
    settings = Settings.instance()
    response = context.response

    test_id = response.headers.get(custom_headers.TEST_ID)
    if test_id:
        test = TestFacade(settings)
        test_key = TestKey.encode({'i': test_id, 'p': project_id})
        return self.show(test_key)