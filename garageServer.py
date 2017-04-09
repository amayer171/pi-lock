import http.server
import socketserver
import json
from garage_gpio import PiPin

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("do Get") 
        #get path from the url ie: '/close' 
        path = (self.path.lower())

        result = self.processRequest(path) 
        print("processed request") 
        
        #send the response:
        self.send_response(result['response'])
        self.send_header("Content-type", 'application/json' )
        self.send_header("Content-Length", len( json.dumps(result ) )  )
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        
        #cast output to bytes and write to file
        self.wfile.write(bytes(json.dumps(result), 'UTF-8') )
    
    def processRequest(self, path):
        print("process request for path: " + path)

        if path == "/door":

            pin = PiPin() 
            pin.send_signal()

            result = self.success(path) 
            return result
        else:
            return self.unknownEndpoint(path)

    def success(self, action):
        return { 'response': 200, 'action': action, 'result': 'success' }

    def unknownEndpoint(self, action):
        return { 'response': 404, 'action': action, 'result': 'unknown endpoint' } 
    
PORT = 8001
try:
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()

except:
    PiPin().cleanup()
    print("Application has ended and cleaned up successfully")
    
