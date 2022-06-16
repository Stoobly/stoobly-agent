import pdb
import email.parser

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, encode_response

multipart_string = b"--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"author\"\r\n\r\nJohn Smith\r\n--ce560532019a77d83195f9e9873e16a1\r\nContent-Disposition: form-data; name=\"file\"; filename=\"example2.txt\"\r\nContent-Type: text/plain\r\nExpires: 0\r\n\r\nHello World\r\n--ce560532019a77d83195f9e9873e16a1--\r\n"
content_type = "multipart/form-data; boundary=ce560532019a77d83195f9e9873e16a1"


params = decode_response(multipart_string, content_type)

print(params.items())

print(multipart_string)
print(encode_response(params, content_type))
