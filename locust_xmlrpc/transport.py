import time
from six.moves import xmlrpc_client

from locust import Locust, events


class LocustXmlRpcTransport(xmlrpc_client.Transport, object):
    def single_request(self, host, handler, request_body, verbose=0):
        start_time = time.time()
        try:
            result = None
            h = self.make_connection(host)
            if verbose:
                h.set_debuglevel(1)

            try:
                self.send_request(h, handler, request_body)
                self.send_host(h, host)
                self.send_user_agent(h)
                self.send_content(h, request_body)

                response = h.getresponse(buffering=True)
                if response.status == 200:
                    self.verbose = verbose
                    result = self.parse_response(response)
            except xmlrpc_client.Fault:
                raise
            except Exception:
                # All unexpected errors leave connection in
                # a strange state, so we clear it.
                self.close()
                raise

            if result is None:
                #discard any response data and raise exception
                if (response.getheader("content-length", 0)):
                    response.read()
                raise xmlrpc_client.ProtocolError(
                    host + handler,
                    response.status, response.reason,
                    response.msg,
                    )
        except xmlrpc_client.Fault as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="xmlrpc",
                name=handler,
                response_time=total_time,
                exception=e
            )
            return ""
        else:
            total_time = int((time.time() - start_time) * 1000)
            response_length = int(response.getheader("content-length", 0))
            events.request_success.fire(
                request_type="xmlrpc",
                name=handler,
                response_time=total_time,
                response_length=response_length
            )
            return result
