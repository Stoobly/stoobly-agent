from stoobly_agent.app.settings import RemoteSettings
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse

from .local_db.replayed_response_adapter import LocalDBReplayedResponseAdapter

class ReplayedResponseAdapterFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBReplayedResponseAdapter:
    return LocalDBReplayedResponseAdapter(ReplayedResponse)  