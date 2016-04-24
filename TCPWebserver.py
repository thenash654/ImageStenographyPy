from socket import *



def main():
    serverPort = 55555
    sSocket = socket(AF_INET, SOCK_STREAM)
    sSocket.bind(('', serverPort))
    sSocket.listen(1)
    URL = 'nothing'
    print 'The server is running on %s' %serverPort

    while True:
        cSocket, address = sSocket.accept()
        try:
            message = cSocket.recv(1024)
            # print message, '||',message.split()[0], ':' , message.split()[1]
            if URL == 'nothing':
                URL = 'index.html'
            else:
                filename = message.split()[1]
                print filename[1:]
                URL = filename[1:]
            f = open(URL)
            outputdata = f.read()
            print outputdata
            cSocket.send('\nHTTP/1.1 200 OK\n\n')
            cSocket.send(outputdata)
            cSocket.close()

        except IOError:
            print "404 Not Found"
            cSocket.send('\nHTTP/1.1 404 Not Found\n\n')

if __name__=='__main__':
    main()

