import os
import shutil
import tempfile

import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.chunk_ref import (
  content_hash,
  is_chunk_ref,
  normalize_chunk_ref,
  read_chunks,
  relative_chunk_ref,
  write_chunks,
)
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class TestChunkRef:
  def test_relative_chunk_ref(self):
    assert relative_chunk_ref('GET-events', 'abc123') == (
      f'{DATA_DIR_NAME}/snapshots/requests/GET-events/chunks/abc123'
    )

  def test_normalize_and_is_chunk_ref(self):
    ref = relative_chunk_ref('GET-events', 'abc123')
    assert is_chunk_ref(ref)
    assert normalize_chunk_ref(ref, slug='GET-events') == ref
    with pytest.raises(ValueError):
      normalize_chunk_ref(ref, slug='other')
    with pytest.raises(ValueError):
      # Directory-style refs (no hash) are no longer valid
      normalize_chunk_ref(f'{DATA_DIR_NAME}/snapshots/requests/GET-events/chunks')

  def test_write_and_read_chunks(self):
    tmp = tempfile.mkdtemp()
    try:
      slug_dir = os.path.join(tmp, 'GET-events')
      os.makedirs(slug_dir)
      refs = write_chunks(slug_dir, [b'a', b'b', b'c'])
      assert len(refs) == 3
      assert all(is_chunk_ref(ref) for ref in refs)
      assert refs[0].endswith(f'/chunks/{content_hash(b"a")}')
      assert read_chunks(slug_dir, refs) == [(0, b'a'), (1, b'b'), (2, b'c')]
    finally:
      shutil.rmtree(tmp, ignore_errors=True)

  def test_same_slug_different_payloads_do_not_collide(self):
    tmp = tempfile.mkdtemp()
    try:
      slug_dir = os.path.join(tmp, 'GET-sse')
      os.makedirs(slug_dir)
      refs_a = write_chunks(slug_dir, [b'data: one\n\n', b'data: two\n\n'])
      refs_b = write_chunks(slug_dir, [b'data: alpha\n\n', b'data: beta\n\n'])
      assert refs_a != refs_b
      assert read_chunks(slug_dir, refs_a) == [(0, b'data: one\n\n'), (1, b'data: two\n\n')]
      assert read_chunks(slug_dir, refs_b) == [(0, b'data: alpha\n\n'), (1, b'data: beta\n\n')]
      # Four distinct content-addressed files under shared chunks/
      names = sorted(os.listdir(os.path.join(slug_dir, 'chunks')))
      assert len(names) == 4
    finally:
      shutil.rmtree(tmp, ignore_errors=True)

  def test_identical_payloads_dedupe(self):
    tmp = tempfile.mkdtemp()
    try:
      slug_dir = os.path.join(tmp, 'GET-sse')
      os.makedirs(slug_dir)
      refs_a = write_chunks(slug_dir, [b'same\n\n'])
      refs_b = write_chunks(slug_dir, [b'same\n\n'])
      assert refs_a == refs_b
      assert os.listdir(os.path.join(slug_dir, 'chunks')) == [content_hash(b'same\n\n')]
    finally:
      shutil.rmtree(tmp, ignore_errors=True)
