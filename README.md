# PythonHTTPHandler
Http post handler with JWT security

Description: its a multithread HTTP server wich handles the POST requests and GET requests. /status indicates the requests handled and the start time. /post handles the requests. Each HTTP request is served by a sepparate server thread.
The POST messages received are added to a queue array.
A queue processor thread processes each message in order: adds de JWT and post each message to the destination address.
For simplicity´s sake , I have only included Content-Type = multipart/form-data. You should post a request like form-data, create a key called message with any value. The value is the message payload. (see post request sample screenshot for Postman GUI)

The sttings beginning at line 16 of the code 
#settings
url = 'https://postman-echo.com/post' # destination URL
HTTPPort=8020 #server listening port
keystr='a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf' #JWT secret
usrname="test123" #JWT username
