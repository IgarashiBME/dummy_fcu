from __future__ import print_function
import socket
import time
from contextlib import closing
import binascii

mav_header = "fe"
length = "09"
sys_id = "00"
com_id = "00"
msg_id = "00"
heartbeat_crckey = "32"
mission_count_crckey = "dd"

def checksum():
    sums = int("ffff", 16)
    for i in range(len(message)/2 -1):
        tmp = int(message[2+i*2:4+i*2],16) ^ (sums&0xFF)
        tmp ^= (tmp<<4)&0xFF
        sums = (sums>>8) ^(tmp<<8) ^(tmp<<3) ^(tmp>>4)    

def main():
  #init
  bufsize = 2041
  recv_addr=['127.0.0.1', 14551]
  send_addr=['127.0.0.1', 14540]
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.bind((recv_addr[0], recv_addr[1]))
  
  seq = 0
  sums = int("ffff", 16)
  with closing(sock):
    while True:
      # send mavlink
      seq_str = hex(seq)[2:4].zfill(2)
      message = "fe09" +seq_str +"01010000000405020c1d0303" +heartbeat_crckey
      sums = int("ffff", 16)
      for i in range(len(message)/2 -1):
          tmp = int(message[2+i*2:4+i*2],16) ^ (sums&0xFF)
          tmp ^= (tmp<<4)&0xFF
          sums = (sums>>8) ^(tmp<<8) ^(tmp<<3) ^(tmp>>4)

      #print(message, hex(sums&0xFF)[2:4].zfill(2), hex(sums>>8)[2:4].zfill(2))
      checksum = hex(sums&0xFF)[2:4].zfill(2) + hex(sums>>8)[2:4].zfill(2)
      mav_protocol = binascii.a2b_hex(message[0:30] + checksum)
      sock.sendto(mav_protocol, (send_addr[0], send_addr[1]))

      seq = seq + 1

      # receive section
      recv = binascii.b2a_hex(sock.recv(bufsize))
      #recv, addr = sock.recvfrom(bufsize)
      #recv = sock.recv(bufsize)
      #print(recv)
      #print(recv[14:16])

      if recv[14:16] == "2b":
          seq_str = hex(seq)[2:4].zfill(2)
          message = "fe04" +seq_str +"01012c00000000" +mission_count_crckey
          sums = int("ffff", 16)
          for i in range(len(message)/2 -1):
              tmp = int(message[2+i*2:4+i*2],16) ^ (sums&0xFF)
              tmp ^= (tmp<<4)&0xFF
              sums = (sums>>8) ^(tmp<<8) ^(tmp<<3) ^(tmp>>4)

          checksum = hex(sums&0xFF)[2:4].zfill(2) + hex(sums>>8)[2:4].zfill(2)
          mav_protocol = binascii.a2b_hex(message[0:20] + checksum)
          sock.sendto(mav_protocol, (send_addr[0], send_addr[1]))
          seq = seq + 1
          #print(message[0:30] + checksum, recv)

      if recv[14:16] != "6f" and recv[14:16] != "02" and recv[14:16] != "00":
          print(recv)

      if seq == 256:
          seq = 0
  return

if __name__ == '__main__':
  main()
