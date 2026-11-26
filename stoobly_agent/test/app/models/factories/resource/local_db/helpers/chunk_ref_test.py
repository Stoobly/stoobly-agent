import os
import shutil
import tempfile

import pytest

from stoobly_agent.app.models.factories.resource.local_db.helpers.chunk_ref import (
  is_chunk_ref,
  normalize_chunk_ref,
  read_chunks,
  relative_chunk_ref,
  write_chunks,
)
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class TestChunkRef:
  def test_relative_chunk_ref(self):
    assert relative_chunk_ref('GET-events') == f'{DATA_DIR_NAME}/snapshots/requests/GET-events/chunks'

  def test_normalize_and_is_chunk_ref(self):
    ref = relative_chunk_ref('GET-events')
    assert is_chunk_ref(ref)
    assert normalize_chunk_ref(ref, slug='GET-events') == ref
    with pytest.raises(ValueError):
      normalize_chunk_ref(ref, slug='other')

  def test_write_and_read_chunks(self):
    tmp = tempfile.mkdtemp()
    try:
      slug_dir = os.path.join(tmp, 'GET-events')
      os.makedirs(slug_dir)
      ref = write_chunks(slug_dir, [b'a', b'b', b'c'])
      assert is_chunk_ref(ref)
      assert read_chunks(slug_dir, ref) == [(0, b'a'), (1, b'b'), (2, b'c')]
    finally:
      shutil.rmtree(tmp, ignore_errors=True)
