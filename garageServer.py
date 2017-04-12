import http.server
import socketserver
import json
from garage_gpio import PiPin

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("do Get") 
        #get path from the url ie: '/close' 
        path = (self.path.lower())
        if path != "/door":
            return
        html = self.html()
        self.set_headers(html)
        self.write_response(html)
 
    def do_POST(self):
        result = self.processRequest(self.path.lower())
        html = self.html('success')
        self.set_headers(html)
        self.write_response(html) 
    
    def set_headers(self, html):
        self.send_response(200)
        self.send_header("Content-type", 'text/html' )
        self.send_header("Content-Length", len(html) ) 
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
    
    def write_response(self, html):
        #send the response:
        #cast output to bytes and write to file
        self.wfile.write(bytes(html, 'UTF-8') )
       
    def html(self, status=''):
        form = '<form action="/door" method="POST"><input type="submit" value="Open Door" style="font-size:30px;"></form>'
        html = "<!DOCTYPE html><html><body><h3>"+status+"</h3><h1>click to open</h1>"+form+"</body></html>"
        return html
        
    def processRequest(self, path):
        print("process request for path: " + path)

        if path == "/door":

            pin = PiPin() 
            pin.send_signal()
            pin.cleanup()

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
    
