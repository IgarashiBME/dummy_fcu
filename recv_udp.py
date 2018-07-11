from __future__ import print_function
import socket
from contextlib import closing
import binascii

def main():
  host = ''
  port = 14550
  bufsize = 100000

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  with closing(sock):
    sock.bind((host, port))
    #sock.setblocking(0)
    while True:
      mav_protocol = binascii.b2a_hex(sock.recv(bufsize))
      #print(mav_protocol[0:12], int(mav_protocol[10:12],16))
      #print(mav_protocol[10:12], int(mav_protocol[10:12], 16))
      print(mav_protocol)
      
      #if int(mav_protocol[10:12], 16) == 0:
       #   print(mav_protocol)

      if int(mav_protocol[10:12], 16) == 47:
          print(mav_protocol)
  return

if __name__ == '__main__':
  main()
