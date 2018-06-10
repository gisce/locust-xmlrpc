from __future__ import division
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
from threading import Thread

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler,
                            allow_none=True)
server.register_introspection_functions()
server.logRequests = False

# Register a function under a different name
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')


def failure_function(code, message):
    raise xmlrpclib.Fault(code, message)
server.register_function(failure_function, 'failure')


def delayed_response(delay_ms):
    import time
    time.sleep(delay_ms/1000)
    return delay_ms
server.register_function(delayed_response, 'delayed')


def start_server():
    server.serve_forever()