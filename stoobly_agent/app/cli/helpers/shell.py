import os
import subprocess
import sys

from dotenv import load_dotenv

DOTENV_PATH = 'STOOBLY_DOTENV_PATH'

def exec_stream(command):
  dotenv_path = os.environ.get(DOTENV_PATH)

  if dotenv_path and os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
  else:
    load_dotenv()

  # Start the process
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  
  # Stream output line by line
  while True:
      stdout = process.stdout.readline()
      stderr = process.stderr.readline()

      if stdout == '' and stderr == '' and process.poll() is not None:
          break

      if stdout:
          print(stdout, end='')

      if stderr:
          print(stderr, end='', file=sys.stderr)
  
  # Get the remaining output (if any)
  rc = process.poll()
  return rc