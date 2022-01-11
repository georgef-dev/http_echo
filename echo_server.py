#!/usr/bin/env python

import os
import logging
import functools
import http.client
import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, output=None, **kwargs):
        self.output = output
        super().__init__(*args, **kwargs)

    def do_GET(self):
        request_path = self.path
        
        logging.info("----- Request Start ----->")
        logging.info(request_path)
        logging.info(self.headers)
        logging.info("<----- Request End -----")
        
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()

    def do_POST(self):
        
        request_path = self.path
        
        logging.info("----- Request Start ----->")
        logging.info("Request path: %s" % request_path)
        
        print("self: \n %s" % dir(self))
        print("headers: \n %s" % self.headers)
        request_headers = self.headers
        content_length = request_headers.get("Content-Length")
        length = int(content_length) if content_length else 0
        
        logging.info("Headers: %s" % request_headers)

        request_data = self.rfile.read(int(length)).decode('utf-8')

        '''
        If the intent is to parse a JSON input, the following code is helpful:
            
            data = urllib.parse.parse_qs(request_data)
        
        For an input such as:
            curl -d "user=user1&pass=abcd" -X POST -H 'Content-Type: application/json' localhost:8080

        It outputs;
            {'user': ['user1'], 'pass': ['abcd']}

        Which means that 'user1' can be retrieved as:
            data["user"]
        '''
       
        with open(self.output, "a") as f:
            f.write("%s \n" % request_data) 
        
        logging.info("Request data: \n %s" % request_data)
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
    
    do_PUT = do_POST
    do_DELETE = do_GET

class Http_Server:
    def __init__(self, hostname, port, output):
        logging.info("Listening on %s:%s" % (hostname,port))
        handler_partial = functools.partial(RequestHandler, output=output)
        server = HTTPServer((hostname, port), handler_partial)
        server.serve_forever()

def main(hostname, port, output):
    port = port 
    server = Http_Server(hostname, port, output)
        
if __name__ == "__main__":
    logging.basicConfig(filename="echo_server.log", encoding="utf-8", level=logging.DEBUG)

    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "%s [options]" % os.path.basename(__file__))

    parser.add_option("-s", "--server", dest="hostname", help="hostname for the server to run at.", default="localhost")
    parser.add_option("-p", "--port", dest="port", help="port for the server to listen to.", default=8080)
    parser.add_option("-o", "--output", dest="output", help="File to store the requests data.", default="output.txt")

    (options, args) = parser.parse_args()
    
    main(options.hostname, options.port, options.output)
