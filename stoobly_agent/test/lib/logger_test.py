import logging
import os

import pytest

from stoobly_agent.config.constants.env_vars import LOG_LEVEL
from stoobly_agent.lib.logger import DEBUG, INFO, Logger, WARNING


def _reset_named_logger(name='Mock'):
  named = logging.getLogger(name)
  named.handlers.clear()
  named.setLevel(logging.NOTSET)
  named.disabled = False
  return named


@pytest.fixture(autouse=True)
def reset_logger_state():
  """Reset Logger singletons and root logger so each test starts clean."""
  previous = os.environ.get(LOG_LEVEL)
  os.environ.pop(LOG_LEVEL, None)

  Logger._instance = None
  Logger._instances = {}

  root = logging.getLogger()
  root.handlers.clear()
  root.setLevel(logging.NOTSET)
  _reset_named_logger()

  yield

  Logger._instance = None
  Logger._instances = {}
  root.handlers.clear()
  root.setLevel(logging.NOTSET)
  _reset_named_logger()

  if previous is None:
    os.environ.pop(LOG_LEVEL, None)
  else:
    os.environ[LOG_LEVEL] = previous


class TestLoggerLoad:
  def test_initial_load_honors_log_level_env(self):
    os.environ[LOG_LEVEL] = WARNING

    logger = Logger.instance('Mock')

    assert logger.getEffectiveLevel() == logging.WARNING
    assert not logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)

  def test_reload_updates_existing_named_logger_level(self):
    os.environ[LOG_LEVEL] = INFO
    logger = Logger.instance('Mock')

    assert logger.isEnabledFor(logging.INFO)

    os.environ[LOG_LEVEL] = WARNING
    Logger.reload()

    assert logger.getEffectiveLevel() == logging.WARNING
    assert not logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)

  def test_reload_to_debug_does_not_disable_cached_loggers(self):
    os.environ[LOG_LEVEL] = INFO
    logger = Logger.instance('Mock')

    os.environ[LOG_LEVEL] = DEBUG
    Logger.reload()

    assert not logger.disabled
    assert logger.getEffectiveLevel() == logging.DEBUG
    assert logger.isEnabledFor(logging.DEBUG)
