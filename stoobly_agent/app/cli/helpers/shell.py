import subprocess
import sys

DOTENV_PATH = 'STOOBLY_DOTENV_PATH'

def exec_stream(command):
  # Run the command in the foreground so Ctrl+C properly exits
  process = subprocess.run(command, shell=True)
  return process.returncode