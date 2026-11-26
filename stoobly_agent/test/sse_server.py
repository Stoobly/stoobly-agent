"""
Local Server-Sent Events (SSE) upstream for tests and manual checks.

Usage:
  python -m stoobly_agent.test.sse_server [--port 8765] [--interval 0.5]
  curl -N http://127.0.0.1:8765/events
"""

from __future__ import annotations

import argparse
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional, Sequence, Tuple
from urllib.parse import urlparse

DEFAULT_EVENTS: Tuple[bytes, ...] = (
  b'data: hello\n\n',
  b'data: world\n\n',
  b'data: done\n\n',
)

DEFAULT_PATH = '/events'


class _SseHTTPRequestHandler(BaseHTTPRequestHandler):
  protocol_version = 'HTTP/1.1'

  def do_GET(self):
    path = urlparse(self.path).path
    if path != self.server.sse_path:
      self.send_error(404, 'Not Found')
      return

    self.send_response(200)
    self.send_header('Content-Type', 'text/event-stream')
    self.send_header('Cache-Control', 'no-cache')
    self.send_header('Connection', 'close')
    self.end_headers()

    try:
      while True:
        for event in self.server.sse_events:
          self.wfile.write(event)
          self.wfile.flush()
          if self.server.sse_interval > 0:
            time.sleep(self.server.sse_interval)
        if not self.server.sse_repeat:
          break
    except (BrokenPipeError, ConnectionResetError):
      pass

  def log_message(self, format, *args):
    # Quiet in tests; CLI prints bind address instead.
    pass


class SseServer:
  """Threading HTTP server that streams ``text/event-stream`` bodies."""

  def __init__(
    self,
    events: Optional[Sequence[bytes]] = None,
    interval: float = 0.0,
    path: str = DEFAULT_PATH,
    host: str = '127.0.0.1',
    port: int = 0,
    repeat: bool = False,
  ):
    self._events = tuple(events) if events is not None else DEFAULT_EVENTS
    self._interval = interval
    self._path = path
    self._host = host
    self._port = port
    self._repeat = repeat
    self._httpd: Optional[ThreadingHTTPServer] = None
    self._thread: Optional[threading.Thread] = None

  @property
  def events(self) -> Tuple[bytes, ...]:
    return self._events

  @property
  def path(self) -> str:
    return self._path

  @property
  def port(self) -> int:
    if not self._httpd:
      raise RuntimeError('SSE server is not running')
    return self._httpd.server_address[1]

  @property
  def base_url(self) -> str:
    if not self._httpd:
      raise RuntimeError('SSE server is not running')
    host, port = self._httpd.server_address[:2]
    return f'http://{host}:{port}'

  @property
  def url(self) -> str:
    return f'{self.base_url}{self._path}'

  def start(self) -> 'SseServer':
    if self._httpd:
      return self

    httpd = ThreadingHTTPServer((self._host, self._port), _SseHTTPRequestHandler)
    httpd.sse_events = self._events
    httpd.sse_interval = self._interval
    httpd.sse_path = self._path
    httpd.sse_repeat = self._repeat
    self._httpd = httpd
    self._thread = threading.Thread(target=httpd.serve_forever, name='sse-server', daemon=True)
    self._thread.start()
    return self

  def stop(self) -> None:
    if self._httpd:
      self._httpd.shutdown()
      self._httpd.server_close()
      self._httpd = None
    if self._thread:
      self._thread.join(timeout=2.0)
      self._thread = None

  def __enter__(self) -> 'SseServer':
    return self.start()

  def __exit__(self, exc_type, exc, tb) -> None:
    self.stop()


def main(argv: Optional[Sequence[str]] = None) -> None:
  parser = argparse.ArgumentParser(description='Serve test Server-Sent Events')
  parser.add_argument('--host', default='127.0.0.1')
  parser.add_argument('--port', type=int, default=8765)
  parser.add_argument('--path', default=DEFAULT_PATH)
  parser.add_argument(
    '--interval',
    type=float,
    default=0.5,
    help='Delay between events in seconds (default: 0.5)',
  )
  parser.add_argument(
    '--repeat',
    action='store_true',
    help='Loop the event list forever (Ctrl+C to stop)',
  )
  args = parser.parse_args(argv)

  server = SseServer(
    host=args.host,
    port=args.port,
    path=args.path,
    interval=args.interval,
    repeat=args.repeat,
  )
  server.start()
  print(f'SSE server listening at {server.url}')
  try:
    while True:
      time.sleep(3600)
  except KeyboardInterrupt:
    print('\nShutting down')
  finally:
    server.stop()


if __name__ == '__main__':
  main()
