from socket import *
import os
from PIL import Image
import math

pixelsreserved=6    #no of pixels reserved for encoding length
maxsize=int(math.pow(2,pixelsreserved*3)-1) #max number these bits will hold

def string2binary (message):
    binarytext=''
    temp=''
    blength = bin(len(message))[2:]
    for i in range ( len(message)):

        temp=bin(ord(message[i]))[2:]
        for j in range(9 - len(temp)):  # loop for getting the length of the message in binary
            temp= '0' + temp
        binarytext = binarytext + temp

    return (binarytext)

def encode(message,img):
    length=len(message)
    print 'maxsize', length
    if (length>maxsize): #if length of message exceeds the length that can be encoded, set length to maxsize
        length=maxsize
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False

    checker = True
    encoded = img.copy() #use a copy of the image to encode
    width, height = img.size #get width and height of image in pixels
    index = 0
    count=0
    
    countmsg=0
    m2b = string2binary(message) #convert message to binary
    binaryR=''
    binaryG=''
    binaryB=''
    for row in range(height):
        if not checker:
            break
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # first value is length of msg
            if row == 0 and col < pixelsreserved:
                blength=bin(length)[2:]
                for i in range(3*pixelsreserved-len(blength)):  #loop for getting the length of the message in binary
                    blength='0'+blength  #adds leading zeroes to make use of the 18 bits
                binaryR=bin(r)[2:]  #converting RGB values to binary and removing 0 and b
                binaryG=bin(g)[2:]
                binaryB=bin(b)[2:]

                binaryR=binaryR[:len(binaryR)-1]+ blength[count]  #takes the bits after 2nd and before the last bit and adds our encoding length
                binaryG=binaryG[:len(binaryG)-1]+ blength[count+1]
                binaryB=binaryB[:len(binaryB)-1]+ blength[count+2]
                count +=3
                encoded.putpixel((col, row), (int(binaryR,2), int(binaryG,2) , int(binaryB,2))) #replacing the pixels of the original image with our new pixel
                print binaryR,binaryG,binaryB

            elif (countmsg) <9*length :
                binaryR = bin(r)[2:]  # converting RGB values to binary and removing 0 and b
                binaryG = bin(g)[2:]
                binaryB = bin(b)[2:]
               
                binaryR = binaryR[:len(binaryR) - 1] + m2b[countmsg]  # takes the bits after 2nd and before the last bit and adds our encoding length
                binaryG = binaryG[:len(binaryG) - 1] + m2b[countmsg + 1]
                binaryB = binaryB[:len(binaryB) - 1] + m2b[countmsg + 2]
              
                countmsg += 3
                encoded.putpixel((col, row), (int(binaryR, 2), int(binaryG, 2), int(binaryB, 2)))  # replacing the pixels of the original image with our new pixel
            else:
                checker = False

            index+=1
    return encoded


def main():
    serverPort = 55555  #port used to access server
    sSocket = socket(AF_INET, SOCK_STREAM)  #assign socket
    sSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sSocket.bind(('', serverPort))  #bind socket
    sSocket.listen(1)   #passive open to listen for incoming connections
    URL = ''     #global declaration for URL
    print 'The server is running on %s' %serverPort

    while True:
        cSocket, address = sSocket.accept() #accept connection and assign client socket and address
        try:
            data = cSocket.recv(1024)    #receive data from client
            print data
            if len(data.split())>0: #if else inserted because name detection wasn't perfect. Sometimes would go out of index
                fname = data.split()[1]   #split the incoming data from client in order to get file name
                print '::',fname[1:], '||', fname[0:]
                URL = fname[1:] #skip first letter (which is '/') and take the rest of the string (which is the file name)
            else:
                fname = data
                URL = fname     #URL is file name

            f=''    #f declared globally inside def
            if os.path.isfile(URL): #if file exists
                f = open(URL, 'rb')  # open file
                if URL.split('.')[1]=='txt': #if client requests message, encode message, save picture and open it. else file will be sent as it is
                    message = f.read()
                    original_image_file = "Message.png"
                    img = Image.open(original_image_file)
                    encoded_image_file = "enc_" + original_image_file
                    img_encoded = encode(message, img)
                    img_encoded.save(encoded_image_file)

                    f = open (encoded_image_file, 'rb')

                cSocket.send('\HTTP/1.1 200 OK\r\n\r\n')  # send OK message to client
            else: #if file does not exist
                f= open('404.html', 'rb')  #open 404 message html
                cSocket.send('\HTTP/1.1 404.0 Not Found\r\n\r\n')    #Send 404 to client
            print 'OPEN SUCCESSFUL'

            outputdata = f.read()   #read file
            print 'READ SUCCESFUL'
            cSocket.sendall(outputdata)     #Send file to client
            cSocket.close()     #close the connection. HTTP 1.1 is non-persistent.

        except IOError:
            print 'error occured.'  #If an IO Error occurs
            cSocket.send('Unknown error occured')   #send this message to client

if __name__=='__main__':    #Run file directly on server only. Don't run imported file
    main()

