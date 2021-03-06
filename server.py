#Import socket, itertools, GPIO and time
import socket
import itertools
import RPi.GPIO as GPIO
from time import gmtime, strftime

#Create control binaries
binaries1 = list(itertools.product(range(2), repeat = 8))

#Setup GPIO and control values
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
lsb = 33
rsb = 8
xbb = 10
bl = 31
Ab = 15
Bb = 13
Xb = 3
Yb = 7
du = 16
dd = 22
dl = 18
dr = 19
st = 5
ba = 12
las = 23
ras = 21
#rtr1 = 35
#rtr2 = 36
#ltr1 = 11
#ltr2 = 12
lasl = 37
lasr = 35
lasu = 38
lasd = 40
lasn = 36
#rasl = 35
#rasr = 36
#rasu = 37
#rasd = 38
buttonset1 = (ras, las, ba, st, dr, dl, dd, du)
buttonset2 = (Yb, Xb, Bb, Ab, bl, xbb, rsb, lsb)
#lefttrigger = (ltr1, ltr2)
#righttrigger = (rtr1, rtr2)
leftanalogue = (lasl, lasr, lasu, lasd, lasn)
#rightanalogue = (rasl, rasr, rasu, rasd)

#Allows multiple connects/disconnects
while True:
 #Setup TCP server
 bindIP = '192.168.1.70'
 bindport = 9235
 connectIP = '192.168.1.66'
 connectport = 9234
 packetsize = 70
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.bind((bindIP, bindport))
 #s.connect((connectIP, connectport))
 s.listen(1)

 #Receive and acknowledge remote connection
 conn, addr = s.accept()
 print(addr , 'connected', strftime("%a, %d, %b %Y %H:%M:%S", gmtime()))
 ackn = conn.recv(packetsize)
 conn.send(ackn)

 #Control input loop
 while True:
  try:
   data = conn.recv(packetsize)
   conn.send(data)
   #Translate into callable list
   decoded = data.decode()
   listed = data.split()
   if len(listed) == 8:
    for x in range(0,256):
     #Start, back, d-pad and analogue clicks
     if listed[0].decode() == str(x):
      GPIO.setup(buttonset1, GPIO.OUT)
      GPIO.output(buttonset1, binaries1[255-x])
     #Xbox button, shoulder buttons, A, B, X and Y
     if listed[1].decode() == str(x):
      GPIO.setup(buttonset2, GPIO.OUT)
      GPIO.output(buttonset2, binaries1[255-x])
    #Left trigger
    #GPIO.setup(lefttrigger, GPIO.OUT)
    #GPIO.output(lefttrigger, 1)
    #if int(listed[2].decode()) >= 150:
     #GPIO.output(lefttrigger, 0)
    #Right trigger
    #GPIO.setup(righttrigger, GPIO.OUT)
    #GPIO.output(righttrigger, 1)
    #if int(listed[3].decode()) >= 150:
     #GPIO.output(righttrigger, 0)
    #DP setup
    #Left analogue stick
    GPIO.setup(leftanalogue, GPIO.OUT)
    #GPIO.output(lasn, 1)
    if int(listed[4].decode()) >= 65000:
     GPIO.output((lasl, lasr), (1,0))
    if int(listed[4].decode()) <= 500:
     GPIO.output((lasl, lasr), (0,1))
    if 10000< int(listed[5].decode()) > 50000:
     GPIO.output((lasu, lasd, lasn), (0,0,1))
    if int(listed[5].decode()) >= 65000:
     GPIO.output((lasu, lasd, lasn), (1,0,0))
    if int(listed[5].decode()) <= 500:
     GPIO.output((lasu, lasd, lasn), (0,1,0))
    #Right analogue stick
    #GPIO.setup(rightanalogue, GPIO.OUT)
    #GPIO.output(rightanalogue, 1)
    #if int(listed[6].decode()) >= 65000:
     #GPIO.output((rasl, rasr), (0,1))
    #if int(listed[6].decode()) <= 500:
     #GPIO.output((rasl, rasr), (1,0))
    #if int(listed[7].decode()) >= 65000:
     #GPIO.output((rasu, rasd), (0,1))
    #if int(listed[7].decode()) <= 500:
     #GPIO.output((rasu, rasd), (1,0))
  #Handles disconnect by peer error
  except socket.error as e:
   if e.errno == 104:
    GPIO.cleanup()
    print(addr , 'disconnected', strftime("%a, %d, %b %Y %H:%M:%S", gmtime()))
    break
