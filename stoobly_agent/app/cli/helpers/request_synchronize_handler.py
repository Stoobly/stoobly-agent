from stoobly_agent.app.proxy.test.matchers.context import MatchContext

class RequestSynchronizeHandler():

  def handle_length_match_error(self, context: MatchContext, value: list):
    return True

  def handle_param_name_missing(self, context: MatchContext, value: dict):
    request_component_name = context.request_component_name

    potential_values = request_component_name.get('values') or []

    if len(potential_values) > 0:
      key = context.current_key
      value[key] = potential_values[0]

    return True

  def handle_param_name_exists(self, context: MatchContext, value: dict):
    key = context.current_key
    del value[key]

    return True

  def handle_type_match_error(self, context: MatchContext, value):
    if isinstance(value, list) or isinstance(value, dict):
      key = context.current_key
      del value[key]

    return True

  def handle_valid_type_error(self, context: MatchContext, value):
    if isinstance(value, list) or isinstance(value, dict):
      key = context.current_key
      del value[key]
      
    return True