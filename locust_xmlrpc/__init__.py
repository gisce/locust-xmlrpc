import six
if six.PY2:
    from .transport import LocustXmlRpcTransport2 as LocustXmlRpcTransport
elif six.PY3:
    from .transport import LocustXmlRpcTransport3 as LocustXmlRpcTransport
