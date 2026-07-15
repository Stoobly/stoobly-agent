import io
import sys

import pytest

from stoobly_agent.lib.intercepted_requests.tee_stream import (
    _TeeStream,
    install_workflow_log_tee,
    uninstall_workflow_log_tee,
)


class TestTeeStream:
    def test_buffers_partial_writes_until_newline(self):
        buf = io.StringIO()
        lines = []
        tee = _TeeStream(buf, lines.append)

        tee.write('hello')          # no newline -> nothing emitted yet
        assert lines == []
        tee.write(' world\n')       # newline completes the line
        assert lines == ['hello world']
        # passthrough is byte-faithful
        assert buf.getvalue() == 'hello world\n'

    def test_multiple_lines_in_one_write(self):
        buf = io.StringIO()
        lines = []
        tee = _TeeStream(buf, lines.append)

        tee.write('a\nb\nc')        # two complete lines, 'c' buffered
        assert lines == ['a', 'b']
        assert buf.getvalue() == 'a\nb\nc'

    def test_line_has_no_trailing_newline(self):
        buf = io.StringIO()
        lines = []
        _TeeStream(buf, lines.append).write('x\n')
        assert lines == ['x']

    def test_flush_forwards_to_wrapped(self):
        buf = io.StringIO()
        flushed = {'n': 0}
        orig_flush = buf.flush
        buf.flush = lambda: (flushed.__setitem__('n', flushed['n'] + 1), orig_flush())
        tee = _TeeStream(buf, lambda line: None)
        tee.flush()
        assert flushed['n'] == 1

    def test_sink_exception_never_breaks_output(self):
        buf = io.StringIO()

        def bad_sink(line):
            raise RuntimeError('boom')

        tee = _TeeStream(buf, bad_sink)
        tee.write('x\n')            # must not raise
        assert buf.getvalue() == 'x\n'

    def test_getattr_delegates_to_wrapped(self):
        buf = io.StringIO()
        tee = _TeeStream(buf, lambda line: None)
        assert tee.isatty() is False   # delegated to StringIO


class TestInstallTee:
    def test_install_tees_stdout_then_uninstall_restores(self):
        lines = []
        original_stdout = sys.stdout
        try:
            install_workflow_log_tee(lines.append)
            assert sys.stdout is not original_stdout
            print('teed line')
        finally:
            uninstall_workflow_log_tee()
        assert sys.stdout is original_stdout
        assert 'teed line' in lines

        print('not teed')
        assert 'not teed' not in lines
