import webbrowser
import os
from urllib import pathname2url
from PIL import Image
import math
pixelsreserved=6

passcode = raw_input("Please Enter the Password:")

def write(message, filename):
    copy = open(filename +'.html', 'wb')
    htmlfilepart1="""<!DOCTYPE html>
<html lang="en-us">
  <head>
    <meta charset="UTF-8">
    <title>Message</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="stylesheets/MainCSS.css" media="screen">
    <link href='https://fonts.googleapis.com/css?family=Open+Sans:400,700' rel='stylesheet' type='text/css'>
  </head>
  <body>
    <section class="page-header">
      <h1 class="project-name">Image Steganography</h1>
      <h2 class="project-tagline"></h2>

    </section>

    <section class="main-content"><body bgcolor="#2A4E51">
    <h2> Your Message Is:</h2>
    """ + message +"""
    </body>
        </section>


      </body>
    </html>
    """
    copy.write(htmlfilepart1)
    copy.close


def bin2str(message):
    # print message
    message = ''.join(str(p) for p in message)
    message = chr(int(message, 2))
    return message


def decode(img, passcode):
    img = Image.open(img)
    # the passcode text file shall be stored by user entry when encoding and sent along with image file by server
    passfile = open('passfile.txt', 'r')
    string1 = passfile.read()
    if (passcode != string1):
        print "Unauthorized Access!"
        passfile.close()
        exit(0)
    else:
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False

        message = ""
        checker= True
        todecode = img.copy()
        width, height = img.size
        index = 0
        count = 0
        checker = True
        binaryR = ''
        binaryG = ''
        binaryB = ''
        i = 0
        k = 0
        m = 0
        lengtharray = 0;
        chararray = [0 for x in xrange(9)]
        lenarray = [0 for x in xrange(3*pixelsreserved)]
        for row in range(height):
            if not checker:
                break
            for col in range(width):
                r, g, b = img.getpixel((col, row))
                if row == 0 and col < pixelsreserved:
                    # getting length of message
                    # 2D array of all pixel data from image

                    binr = int(bin(r)[2:])
                    bing = int(bin(g)[2:])
                    binb = int(bin(b)[2:])

                    if binr & 1 != 0:
                        lenarray[i] = 1
                    else:
                        lenarray[i] = 0
                    i += 1

                    if bing & 1 != 0:
                        lenarray[i] = 1

                    else:
                        lenarray[i] = 0
                    i += 1

                    if binb & 1 != 0:
                        lenarray[i] = 1

                    else:
                        lenarray[i] = 0
                    i += 1
                    if col == pixelsreserved-1:
                        lenarray = ''.join(str(p) for p in lenarray)

                        # going back to decimal

                        lengthmsg = int(lenarray, 2)
                        print 'length', lengthmsg

                elif m < lengthmsg * 3:
                    # getting the rest of the bits from the message and putting in array
                    # chararray= [0 for x in xrange(9)]

                    binr = int(bin(r)[2:])
                    bing = int(bin(g)[2:])
                    binb = int(bin(b)[2:])
                    # print binr, bing, binb

                    if binr & 1 != 0:
                        chararray[k] = 1
                    else:
                        chararray[k] = 0
                    k += 1
                    # m+=1
                    if bing & 1 != 0:
                        chararray[k] = 1
                    else:
                        chararray[k] = 0
                    k += 1
                    # m+=1
                    if binb & 1 != 0`
                    k += 1
                    m += 1
                    # print k
                    if k >= 8:
                        message += bin2str(chararray)  # make a function bin2str
                        k = 0
                # print chararray
                else:
                    checker = False

                index += 1

        return message
msg = decode('enc_Message.png','hello')
filename = 'Message'
write(msg,filename)
url = 'file:{}'.format(pathname2url(os.path.abspath(filename + '.html')))
write (msg, 'Message')
webbrowser.open(url, 2)

