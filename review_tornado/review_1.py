import socket

"""
使用socket实现web服务
"""

address = ('0.0.0.0', 8000)
RESP = '''
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
<head>
<title>review_1</title>
<body>
<h1>Hello world!</h1>
</body>
</html>
'''

listen_sock = socket.socket()
listen_sock.bind(address)
listen_sock.listen(50)
print("Server is running:%s:%s",address)
while 1:
    client_sock , client_addr =listen_sock.accept()
    print("Server is running:%s:%s",client_addr)
    request = client_sock.recv(1024)

    http_response = RESP
    client_sock.sendall(http_response.encode('utf8'))
    client_sock.close()
    