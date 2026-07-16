import atexit
import sys
from typing import Callable, Optional


class _TeeStream:
    """Wraps a text stream, forwarding every write to it unchanged while also
    emitting each complete line to a `sink` callback.

    Used to mirror workflow stdout/stderr into the request log without altering
    what actually reaches the real stream (the .log file locally, `docker logs`
    output in Docker).

    Known limitation: output written directly to the underlying file descriptor
    (bypassing this Python stream object, e.g. os.write(1, ...)) still reaches
    the real stream but is not mirrored. In practice Stoobly's Logger and
    mitmproxy log via Python streams, so coverage is effectively complete.
    """

    def __init__(self, wrapped, sink: Callable[[str], None]):
        self._wrapped = wrapped
        self._sink = sink
        self._buffer = ''

    def write(self, s: str) -> int:
        result = self._wrapped.write(s)

        self._buffer += s
        while '\n' in self._buffer:
            line, self._buffer = self._buffer.split('\n', 1)
            self._emit(line)

        return result

    def _emit(self, line: str) -> None:
        try:
            self._sink(line)
        except Exception:
            # Mirroring must never break real output.
            pass

    def _flush_partial(self) -> None:
        """Emit any buffered partial line (no trailing newline yet)."""
        if self._buffer:
            self._emit(self._buffer)
            self._buffer = ''

    def flush(self) -> None:
        self._wrapped.flush()

    def __getattr__(self, name):
        return getattr(self._wrapped, name)


_stdout_tee: Optional[_TeeStream] = None
_stderr_tee: Optional[_TeeStream] = None
_atexit_registered = False


def install_workflow_log_tee(sink: Callable[[str], None]) -> None:
    """Wrap sys.stdout/sys.stderr so every complete line is also handed to `sink`."""
    global _stdout_tee, _stderr_tee, _atexit_registered

    _stdout_tee = _TeeStream(sys.stdout, sink)
    _stderr_tee = _TeeStream(sys.stderr, sink)
    sys.stdout = _stdout_tee
    sys.stderr = _stderr_tee

    if not _atexit_registered:
        atexit.register(_flush_installed_tees)
        _atexit_registered = True


def _flush_installed_tees() -> None:
    if _stdout_tee is not None:
        _stdout_tee._flush_partial()
    if _stderr_tee is not None:
        _stderr_tee._flush_partial()


def uninstall_workflow_log_tee() -> None:
    """Restore the original sys.stdout/sys.stderr, flushing any trailing partial line."""
    global _stdout_tee, _stderr_tee

    if _stdout_tee is not None:
        _stdout_tee._flush_partial()
        if sys.stdout is _stdout_tee:
            sys.stdout = _stdout_tee._wrapped
        _stdout_tee = None

    if _stderr_tee is not None:
        _stderr_tee._flush_partial()
        if sys.stderr is _stderr_tee:
            sys.stderr = _stderr_tee._wrapped
        _stderr_tee = None
