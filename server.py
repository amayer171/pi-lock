import http.server
import socketserver
import json
from servo import PiServo 

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        #get path from the url ie: '/close' 
        path = (self.path.lower())

        result = self.processRequest(path) 
       
        #send the response:
        self.send_response(result['response'])
        self.send_header("Content-type", 'application/json' )
        self.send_header("Content-Length", len( json.dumps(result ) )  )
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        
        #cast output to bytes and write to file
        self.wfile.write(bytes(json.dumps(result), 'UTF-8') )
    
    def processRequest(self, path):
        servo = PiServo() 
        result = self.success(path) 
        if path == "/close" or path == "/lock":
            servo.lock()
        elif path == "/open" or path == "/unlock":
            servo.unlock()
        else:
            print ("Unknown url: '" + path + "'")
            result = self.unknownEndpoint(path)
        return result

    def success(self, action):
        return { 'response': 200, 'action': action, 'result': 'success' }

    def unknownEndpoint(self, action):
        return { 'response': 404, 'action': action, 'result': 'unknown endpoint' } 

PORT = 8000

myHandler = Handler

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), myHandler)
print("serving at port", PORT)
httpd.serve_forever()
