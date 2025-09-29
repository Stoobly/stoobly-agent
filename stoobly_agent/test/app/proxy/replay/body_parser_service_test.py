import pdb
import pytest
import base64

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, encode_response

@pytest.fixture
def multipart_string():
  return b"--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"author\"\r\n\r\nJohn Smith\r\n--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"file\"; filename=\"example2.txt\"\r\nContent-Type: text/plain\r\nExpires: 0\r\n\r\nHello World\r\n--ce560532019a77d83195f9e9873e16a1--\r\n"

@pytest.fixture
def content_type():
  return "multipart/form-data; boundary=ce560532019a77d83195f9e9873e16a1"

@pytest.fixture
def image_data():
  """A small 1x1 pixel PNG image in base64 format for testing."""
  # This is a minimal 1x1 pixel PNG image
  png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
  return base64.b64decode(png_base64)

@pytest.fixture
def multipart_with_image_string(image_data):
  """Multipart form data containing both text fields and an image file."""
  boundary = "ce560532019a77d83195f9e9873e16a1"
  
  # Create multipart form data with text field and image
  result = f'--{boundary}\r\nContent-Disposition: form-data; name="title"\r\n\r\nTest Image Upload\r\n'.encode('utf-8')
  result += f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="test.png"\r\nContent-Type: image/png\r\n\r\n'.encode('utf-8')
  result += image_data
  result += f'\r\n--{boundary}--\r\n'.encode('utf-8')

  with open('/tmp/multi', 'wb') as fp:
    fp.write(result)

  return result

class TestMultipart():

  def test_decodes_response(self, multipart_string: bytes, content_type: str):
    multidict = decode_response(multipart_string, content_type)

    assert multidict.get('author') == b'John Smith'
    assert multidict.get('file') == b'Hello World'

  def test_encodes_response(self, content_type: str):
    expected_params = { 'author': 'John Smith', 'file': 'Hello World'}
    multipart_string = encode_response(expected_params, content_type)

    multidict = decode_response(multipart_string, content_type)
    for key in expected_params:
      assert multidict.get(key) == expected_params[key].encode('utf-8')

  def test_decodes_multipart_with_image(self, multipart_with_image_string: bytes, content_type: str, image_data: bytes):
    """Test decoding multipart form data that contains both text fields and binary image data."""
    multidict = decode_response(multipart_with_image_string, content_type)

    # Check text field
    assert multidict.get('title') == b'Test Image Upload'
    
    # Check image field - should contain the binary image data
    image_field = multidict.get('image')
    assert image_field is not None
    assert isinstance(image_field, bytes)
    assert image_field == image_data
    assert len(image_field) == len(image_data)

  def test_encodes_multipart_with_image(self, content_type: str, image_data: bytes):
    """Test encoding multipart form data that contains both text fields and binary image data."""
    expected_params = {
      'title': 'Test Image Upload',
      'image': image_data
    }
    
    multipart_string = encode_response(expected_params, content_type)
    multidict = decode_response(multipart_string, content_type)
    
    # Verify text field
    assert multidict.get('title') == b'Test Image Upload'
    
    # Verify image field
    decoded_image = multidict.get('image')
    assert decoded_image is not None
    assert isinstance(decoded_image, bytes)
    assert decoded_image == image_data

  def test_decode_error_handling(self):
    """Test decode function error handling with malformed multipart data."""
    from stoobly_agent.app.proxy.replay.multipart import decode
    
    # Test with invalid content type
    headers = {'content-type': 'invalid/type'}
    result = decode(headers, b'some content')
    assert result == b'some content'  # Should return original content
    
    # Test with missing boundary
    headers = {'content-type': 'multipart/form-data'}
    result = decode(headers, b'some content')
    assert result == b'some content'  # Should return original content
    
    # Test with malformed multipart data
    headers = {'content-type': 'multipart/form-data; boundary=test123'}
    malformed_content = b'--test123\r\nincomplete part'
    result = decode(headers, malformed_content)
    # Should return original content or handle gracefully
    assert result is not None  # Should not crash

  def test_decode_return_type_consistency(self):
    """Test that decode function returns consistent types."""
    from stoobly_agent.app.proxy.replay.multipart import decode
    
    # Test with invalid input types
    headers = {'content-type': 'multipart/form-data; boundary=test123'}
    
    # Should return original content for invalid input
    result = decode(headers, None)
    assert result is None
    
    result = decode(headers, 123)  # int instead of bytes/str
    assert result == 123
