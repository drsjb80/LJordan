import logging
from http.server import SimpleHTTPRequestHandler
from http import HTTPStatus
import socketserver
from json import loads, dumps

from .schema import schema
from .config import port

class PostHandler(SimpleHTTPRequestHandler):

    def bad_request_resp(self):
        self.send_response(HTTPStatus.BAD_REQUEST)
        self.send_header('Content-Length', 0)
        self.end_headers()

    def do_POST(self):

        req_content_type = self.headers.get('Content-Type', False)
        if not req_content_type or req_content_type != 'application/json':
            self.bad_request_resp()
            return

        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode()
        
        query = {}
        try:
            query = loads(post_body)['query']
        except (Exception) as ex:
            logging.error(repr(ex))
            self.bad_request_resp()
            return

        result = schema.execute(query).to_dict()
        result = dumps(result)

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(result.encode())

def serve_forever():
    with socketserver.TCPServer(('', port), PostHandler) as httpd:
        try:
            logging.info('Serving at port %s', port)
            httpd.serve_forever()

        except KeyboardInterrupt:
            logging.info('shutting the server down')
            httpd.shutdown()
