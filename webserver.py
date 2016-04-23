from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 8080
mimetype = ''
def getmimetype(string):
	if string.endswith(".html"):
		mimetype='text/html'
		
	if string.endswith(".jpg"):
		mimetype='image/jpg'
		
	if string.endswith(".gif"):
		mimetype='image/gif'
		
	if string.endswith(".js"):
		mimetype='application/javascript'
		
	if string.endswith(".css"):
		mimetype='text/css'
		
	return True

def OpenFile(endoffile):
		#getmimetype(endoffile)
		f = open(curdir + sep + endoffile.path) 
		endoffile.send_response(200)
		endoffile.send_header('Content-type',mimetype)
		endoffile.end_headers()
		endoffile.wfile.write(f.read())
		f.close()


class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			sendReply = getmimetype(self.path)
			

			if sendReply == True:
				#Open the static file requested and send it
				# f = open(curdir + sep + self.path) 
				# self.send_response(200)
				# self.send_header('Content-type',mimetype)
				# self.end_headers()
				# self.wfile.write(f.read())
				# f.close()
				OpenFile(self)
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/name":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "Your name is: %s" % form["your_name"].value
			self.send_response(200)
			if form["your_name"].value=="nashmia" and form["your_password"].value=="nashmia":
				self.send_response(200)
				self.path="/messages.html"
				self.wfile.write("Thanks %s !" % form["your_name"].value )
				
				self.do_GET()
			else:
				self.wfile.write("Incorrect username or password entered")
			return		

try:
        server = HTTPServer(('', PORT_NUMBER),myHandler)
        print 'started httpserver on port' , PORT_NUMBER

        server.serve_forever()

except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
