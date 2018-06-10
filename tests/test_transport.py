import unittest
import thread
from xmlrpclib import ServerProxy
from locust_xmlrpc import LocustXmlRpcTransport
from locust.stats import global_stats


class TestTransport(unittest.TestCase):

    def setUp(self):
        from .server import server, start_server
        self.server = server
        thread.start_new_thread(start_server)
        self.client = ServerProxy(
            'http://localhost:8000/RPC2',
            transport=LocustXmlRpcTransport()
        )
        global_stats.reset_all()

    def test_returns_something(self):
        res = self.client.add(2, 2)
        self.assertEqual(res, 4)
        stats = global_stats.get('/RPC2', 'xmlrpc')
        self.assertEqual(stats.num_requests, 1)

    def test_failure(self):
        self.client.failure('01', 'Test Error')
        stats = global_stats.get('/RPC2', 'xmlrpc')
        self.assertEqual(stats.num_failures, 1)

    def test_failure_not_found(self):
        self.client.method_doesnt_exist()
        stats = global_stats.get('/RPC2', 'xmlrpc')
        self.assertEqual(stats.num_failures, 1)
    
    def test_delay(self):
        delayed_ms = 500
        res = self.client.delayed(delayed_ms)
        stats = global_stats.get('/RPC2', 'xmlrpc')
        self.assertEqual(res, delayed_ms)
        self.assertEqual(stats.num_requests, 1)
        self.assertGreaterEqual(stats.avg_response_time, delayed_ms)
    
    def tearDown(self):
        self.server.shutdown()


if __name__ == '__main__':
    unittest.main()