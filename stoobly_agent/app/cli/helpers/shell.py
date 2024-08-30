import subprocess
import sys

from dotenv import load_dotenv

def exec_stream(command):
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