from http.server import BaseHTTPRequestHandler, HTTPServer
from pydoc import doc
import sys
from datetime import datetime
from threading import Thread
import time
from urllib.request import Request
import cgi
import jwt
from cryptography.hazmat.primitives import serialization
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from socketserver import ThreadingMixIn

#settings
url = 'https://postman-echo.com/post' # destination URL
keystr='a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf' #JWT secret
usrname="test123" #JWT username
HTTPPort=8020 #server listening port

#global variables
StartZeit=datetime.now() #program start datetime
RequestProcessed = 0 #requests counter
Arr = [] #message queue
jti=0 #nonce

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            
            #status indicator page
            if (self.path=="/status"):
                global StartZeit, RequestProcessed
                td = datetime.now()-StartZeit
                message="<html><head><title></title></head><body>TIME FROM START: " + str(td) + "<br>REQUESTS PROCESSED "+ str(RequestProcessed) +"</body></html>"
                #message ="TIME FROM START: " + str(td) + "  REQUESTS PROCESSED: " + str(RequestProcessed)
                self.wfile.write(bytes(message, "utf8"))

            else:
                #landing page
                message="<html><head><title></title></head><body> STAFFA HOLTMANN POST HANDLER </body></html>"
                #message = "STAFFA HOLTMANN POST HANDLER"
                self.wfile.write(bytes(message, "utf8"))

        
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info())

    def do_POST(self):
        try:
            if (self.path=="/post"):
                print ("post")
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    m = fields.get('message')
                    #adds message to the internal POST queue in position 0 - posts are processed in FIFO order
                    global Arr
                    Arr.insert (0,m) 
                    output= 'POSTED MESSAGE: ' + m[0]
                else:
                    output= 'EMPTY MESSAGE RECEIVED'    

                #sends result to the HTTP client
                self.wfile.write(bytes(output, "utf8"))


        except:
           self.send_error(404, "{}".format(sys.exc_info()[0]))
           print(sys.exc_info())


#queue processor class - FIFO
class Pr(Thread):

   def __init__(self):
       Thread.__init__(self)

   def run(self):
        #processes the array
        while 1==1:
            time.sleep(0.1)
            if len(Arr)>0:
                if Arr [-1] != "":
                    print(Arr [-1])
                    t=CreateJWT()
                    HTTPPost (t,Arr [-1])
                    Arr.remove (Arr [-1])
                    global RequestProcessed
                    RequestProcessed +=1

#Web Token creation
def CreateJWT():


    now = datetime.now() # current date and time

    today = now.strftime("%m/%d/%Y")
    print("date:",today)

    import time    
    epoch_time = int(time.time())
    print (epoch_time)

    global usrname
    payload_data = {
        "user": usrname,
        "date": today
    }

    global jti
    jti+=1


    claims = {
        "iat": epoch_time,
        "jti": jti,
        "payload" : payload_data
    }

    global keystr

    token = jwt.encode(
    payload=claims,
    key=keystr,
    algorithm='HS512'
    )

    print(token)

    return token


#HTTP post
def HTTPPost(tkn,Content):
    
    post_fields = {'message': Content} 

    headers = {
    "x-my-jwt":tkn,
    #"Authorization":"Bearer TOKEN_XYZ"
    }

    global url

    request = Request(url, urlencode(post_fields).encode(), headers)
    json = urlopen(request).read().decode()
    print(json)


#starts the queue processor thread
th=Pr()
th.start()


class HTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    global HTTPPort
    server = HTTPServer(('0.0.0.0', HTTPPort), handler)

    server.serve_forever()


if __name__ == '__main__':
    run()
