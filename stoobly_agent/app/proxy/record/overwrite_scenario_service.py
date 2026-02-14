import os
import pdb

from filelock import FileLock

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.logger import Logger

LOG_ID = 'OverwriteScenario'

def overwrite_scenario(scenario_key: ScenarioKey):
  settings = Settings.instance()
  scenario_model = ScenarioModel(settings) 
  scenario, status = scenario_model.show(scenario_key.id)

  if status != 200:
    return

  if not scenario.get('overwritable'):
    return

  status = scenario_model.update(scenario_key.id, **{ 'overwritable': False })[1]

  if status != 200:
    return 

  requests_model = RequestModel(settings)
  res, status = requests_model.destroy_all(scenario_id=scenario['id'])

  if status != 200:
    return

  return res

def overwrite_scenario_with_lock(overwrite_id: str, scenario_key: ScenarioKey, scenario_model: ScenarioModel):
    """
    Thread-safe and process-safe scenario overwrite using file-based locking.
    
    Ensures that each unique combination of (scenario_key, overwrite_id) can only
    trigger a scenario overwrite once, even with concurrent requests.
    
    Args:
        overwrite_id: Unique identifier for this overwrite operation.
                     Different IDs allow multiple overwrites of the same scenario.
        scenario_key: The scenario to overwrite
        scenario_model: Model instance for updating scenario state
    
    Behavior:
        - Creates a file lock based on scenario_key.id and overwrite_id
        - First request with a given (scenario_key, overwrite_id) combination will:
          1. Set scenario to overwritable=True
          2. Delete all existing requests in the scenario
          3. Set scenario to overwritable=False
          4. Create a marker file to prevent duplicate processing
        - Subsequent requests with the same combination will detect the marker and skip
        - Different overwrite_ids for the same scenario will each trigger one overwrite
    
    Thread/Process Safety:
        - Uses FileLock for coordination across threads and processes
        - In non-detached Docker mode: works across containers (shared bind mount)
        - In detached Docker mode: only works within a single container (isolated volumes)
    """
    lock_file_name = f'.{scenario_key.id}_{overwrite_id}.overwrite.lock'
    lock_path = os.path.join(DataDir.instance().tmp_dir_path, lock_file_name)
    file_lock = FileLock(lock_path)

    try:
      with file_lock:
        # Check if already processed by checking if marker file exists
        marker_file = lock_path.replace('.lock', '.processed')
        if os.path.exists(marker_file):
          return
        
        res, status = scenario_model.update(scenario_key.id, **{ 'overwritable': True })
        if status != 200:
          Logger.instance(LOG_ID).error(f"Failed to update scenario {scenario_key.id} to overwritable: {res}")
          return
        
        overwrite_scenario(scenario_key)
         
        # Create marker file to indicate processing is complete
        with open(marker_file, 'w') as f:
          f.write('')
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to acquire lock for scenario overwrite: {e}")
      return