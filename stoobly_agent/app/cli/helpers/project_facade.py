import pdb
import requests

from stoobly_agent.lib.api.projects_resource import ProjectsResource
from stoobly_agent.lib.api.interfaces import ProjectCreateParams, ProjectShowResponse, ProjectsIndexQueryParams, ProjectsIndexResponse
from stoobly_agent.lib.api.keys import OrganizationKey, ProjectKey
from stoobly_agent.app.settings import Settings

class ProjectFacade():

  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.__api = ProjectsResource(self.__settings.remote.api_url, self.__settings.remote.api_key)

  def create(self, **kwargs: ProjectCreateParams) -> ProjectShowResponse:
    organization_key: str = OrganizationKey(kwargs.get('organization_key')) 

    res: requests.Response =  self.__api.create(
      description=kwargs.get('description') or '',
      name=kwargs.get('name'),
      organization_id=organization_key.id
    )

    if not res.ok:
      raise AssertionError('Could not create report')

    return res.json()

  def show(self, project_key: str) -> ProjectShowResponse:
    key = ProjectKey(project_key)
    res = self.__api.show(key.id)
    return res.json()

  def index(self, **kwargs) -> ProjectsIndexResponse:
    organization_key: str = OrganizationKey(kwargs.get('organization_key')) 

    del kwargs['organization_key']

    res = self.__api.index(**{ 'organization_id': organization_key.id,  **kwargs })

    return res.json()

  