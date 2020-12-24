import os
import socket 

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def getCurrentIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


userFTPServer = "xxxxxxxxxx"
passwordFTPServer = "xxxxxxxxx"
portFTPServer = 1026
securityDataSheetFolderPath = "/security_datasheet"

authorizer = DummyAuthorizer()
authorizer.add_user(userFTPServer, passwordFTPServer, str(os.path.dirname(os.path.abspath(__file__)))+securityDataSheetFolderPath, perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((getCurrentIP(), portFTPServer), handler)
server.serve_forever()
