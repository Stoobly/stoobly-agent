import sys

from stoobly_agent.config.constants import (
  mode,
  mock_policy,
  develop_policy,
  record_order,
  record_policy,
  record_strategy,
  test_policy,
  test_strategy,
)


def get_order_options(active_mode: str) -> list[str]:
  if active_mode == mode.RECORD:
    return [record_order.APPEND, record_order.OVERWRITE]
  return []


def get_policy_options(active_mode: str) -> list[str]:
  if active_mode == mode.MOCK:
    return [mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE]
  if active_mode == mode.RECORD:
    return [record_policy.ALL, record_policy.API, record_policy.FOUND, record_policy.NOT_FOUND]
  if active_mode == mode.DEVELOP:
    return [develop_policy.ALL]
  if active_mode == mode.TEST:
    return [test_policy.FOUND, test_policy.NONE]
  return []


def get_strategy_options(active_mode: str) -> list[str]:
  if active_mode == mode.RECORD:
    return [record_strategy.FULL, record_strategy.MINIMAL]
  if active_mode == mode.TEST:
    return [test_strategy.CONTRACT, test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]
  return []


ORDER_OPTIONS = [record_order.APPEND, record_order.OVERWRITE]

POLICY_OPTIONS = sorted({
  mock_policy.ALL,
  mock_policy.FOUND,
  mock_policy.NONE,
  record_policy.ALL,
  record_policy.API,
  record_policy.FOUND,
  record_policy.NOT_FOUND,
  develop_policy.ALL,
  test_policy.FOUND,
  test_policy.NONE,
})

STRATEGY_OPTIONS = sorted({
  record_strategy.FULL,
  record_strategy.MINIMAL,
  test_strategy.CONTRACT,
  test_strategy.CUSTOM,
  test_strategy.DIFF,
  test_strategy.FUZZY,
})


def validate_options_for_mode(kwargs: dict, active_mode: str = None) -> None:
  """Validate order/policy/strategy against an intercept mode.

  active_mode defaults to kwargs.get('mode') when not provided.
  """
  mode_value = active_mode if active_mode is not None else kwargs.get('mode')

  if kwargs.get('order'):
    valid_orders = get_order_options(mode_value or '')
    if not valid_orders:
      print("Error: set --mode to an intercept mode that supports the order option", file=sys.stderr)
      sys.exit(1)
    if kwargs['order'] not in valid_orders:
      print(f"Error: Valid orders for {mode_value} are {valid_orders}", file=sys.stderr)
      sys.exit(1)

  if kwargs.get('policy'):
    if not mode_value:
      print("Error: set --mode to an intercept mode that supports the policy option", file=sys.stderr)
      sys.exit(1)

    valid_policies = get_policy_options(mode_value)
    if kwargs['policy'] not in valid_policies:
      print(f"Error: Valid policies for {mode_value} are {valid_policies}", file=sys.stderr)
      sys.exit(1)

  if kwargs.get('strategy'):
    valid_strategies = get_strategy_options(mode_value or '')
    if not valid_strategies:
      print("Error: set --mode to an intercept mode that supports the strategy option", file=sys.stderr)
      sys.exit(1)
    if kwargs['strategy'] not in valid_strategies:
      print(f"Error: Valid strategies for {mode_value} are {valid_strategies}", file=sys.stderr)
      sys.exit(1)
