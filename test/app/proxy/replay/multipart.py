import pdb

from stoobly_agent.app.proxy.replay.multipart import decode, encode

fp = open('./multipart.txt', 'r')
contents = fp.read()

headers = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryJh4Bf4Xzy3mQewAl'}

print(contents)
decoded = decode(headers, contents.encode())
print(decoded)

print(encode(headers, decoded).decode())