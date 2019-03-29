

def parse_addr(addr):
  i = addr.find(':')
  host = '' if i<0 else addr[0:i]
  port = int(addr if i<0 else addr[i+1:])
  return (host, port)


class RequestHandler(BaseHTTPRequestHandler):
  def body(self):
    size = int(self.headers.get('Content-Length'))
    return self.rfile.read(size)

  def send(self, code, body=None, headers=None):
    self.send_response(code)
    for k, v in headers.items():
      self.send_header(k, v)
    self.end_headers()
    if body is not None:
      self.wfile.write(body)
  
  def send_json(self, code, body):
    heads = {'Content-Type': 'application/json'}
    self.send(code, bytes(json.dumps(body), 'utf8'), heads)

  def do_GET(self):
    handler = self.server.handler
    self.send_json(200, handler.addrs)

  def do_POST(self):
    handler = self.server.handler
    if self.path.startswith('/service'):
      return handler.handle_service(self)
    return handler.handle_forward(self)
