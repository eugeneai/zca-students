from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from components import Group, load_obj
from interfaces import *


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/5',)

SERVER=("localhost", 8080)

# Create server
server = SimpleXMLRPCServer(
    SERVER,
    requestHandler=RequestHandler)
server.register_introspection_functions()

group=load_obj(5, Group)

server.register_instance(group)

# Run the server's main loop
print ("Server started at {}:{}".format(*SERVER))
server.serve_forever()
