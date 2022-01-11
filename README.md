# Simple Echo HTTP Server

Very simple Python echo HTTP server. 
This script will write to an output file inputs as they come. No parsing or handling of any sort.

It is a sequential implementation, not multithreaded. It will be able to handle one request at a time.

# Usage 

```bash
Usage: Creates an http-server that will echo out any GET or POST parameters
Run:

echo_server.py [options]

Options:
  -h, --help            show this help message and exit
  -s HOSTNAME, --server=HOSTNAME
                        hostname for the server to run at.
  -p PORT, --port=PORT  port for the server to listen to.
  -o OUTPUT, --output=OUTPUT
                        File to store the requests data.
```

