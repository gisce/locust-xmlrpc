XML-RPC for locust
==================

A XML-RPC Transport to use with `Locust <https://locust.io/>`_

Usage in your locustfile:

.. code:: python

  from six.moves import xmlrpc_client  # Python2-3 compat
  
  from locust_xmlrpc import LocustXmlRpcTransport
  from locust import Locust
  
  class XmlRpcLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(XmlRpcLocust, self).__init__(*args, **kwargs)

        self.client = xmlrpc_client.ServerProxy(
            '{}/xmlrpc'.format(self.host),
            transport=LocustXmlRpcTransport()
        )
