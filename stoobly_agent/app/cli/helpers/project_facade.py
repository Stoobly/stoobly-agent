import pdb
import requests

from stoobly_agent.lib.api.projects_resource import ProjectsResource
from stoobly_agent.lib.api.users_resource import UsersResource
from stoobly_agent.lib.api.interfaces import ProjectDetails, ProjectShowResponse, ProjectsIndexResponse, UserProfileResponse
from stoobly_agent.lib.api.keys import OrganizationKey, ProjectKey
from stoobly_agent.app.settings import Settings

class ProjectFacade():

  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.__api = ProjectsResource(self.__settings.remote.api_url, self.__settings.remote.api_key)

  def user_profile(self) -> UserProfileResponse:
    resource = UsersResource(self.__settings.remote.api_url, self.__settings.remote.api_key)
    res = resource.profile()

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def create(self, **kwargs: ProjectDetails) -> ProjectShowResponse:
    organization_key: OrganizationKey = OrganizationKey(kwargs.get('organization_key')) 

    res: requests.Response =  self.__api.create(
      project={
        "description": kwargs.get('description') or '',
        "name": kwargs.get('name'),
        "organization_id": organization_key.id
      },
      organization_id=organization_key.id
    )

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def show(self, project_key: str) -> ProjectShowResponse:
    key = ProjectKey(project_key)
    res = self.__api.show(key.id)

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

  def index(self, kwargs) -> ProjectsIndexResponse:
    organization_key: str = OrganizationKey(kwargs.get('organization_key')) 

    del kwargs['organization_key']

    res = self.__api.index(**{ 'organization_id': organization_key.id,  **kwargs })

    if not res.ok:
      raise AssertionError(res.content)

    return res.json()

