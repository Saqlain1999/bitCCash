#!/bin/python3
from Wallet import Wallet
import socket
import struct
import os, binascii, hashlib, base58, random, ecdsa, qrcode, time, utils
from hexdump import hexdump

MAGIC_CASH = 0xe8f3e1e3

def checksum(x):
  return hashlib.sha256(hashlib.sha256(x).digest()).digest()[0:4]

def makeMessage(magic, command, payload):
  return struct.pack('<L12sL4s', magic, command, len(payload), checksum(payload)) + payload


def getVersionMsg():
  version = 60002
  services = 1
  timestamp = int(time.time())
  addr_me = b"\x00"*26
  addr_you = b"\x00"*26
  nonce = random.getrandbits(64)
  sub_version_num = b"\x00"
  start_height = 0

  payload = struct.pack('<LQQ26s26sQsL', version, services, timestamp, addr_me,
    addr_you, nonce, sub_version_num, start_height)
  return makeMessage(MAGIC_CASH, b'version', payload)

def sock_read(sock, count):
  ret = b''
  while len(ret) < count:
    ret += sock.recv(count+len(ret))
  return ret

def recvMessage(sock):
  magic, command, plen, cksum = struct.unpack('<L12sL4s', sock_read(sock, 24))
  assert magic == MAGIC_CASH 
  payload = sock_read(sock, plen)
  assert checksum(payload) == cksum
  print(command)
  hexdump(payload)
  return command, payload

if __name__ == "__main__":
  peers = socket.gethostbyname_ex('seed.bitcoinabc.org')[2]
  peers = random.choice(peers)
  print(peers)

  vermsg = getVersionMsg()
  hexdump(vermsg)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((peers, 8333))
  sock.send(vermsg)

  cmd, payload = recvMessage(sock)
  cmd, payload = recvMessage(sock)
  cmd, payload = recvMessage(sock)
  # comb = cmd + payload

  # w1 = Wallet(123)
  # w2 = Wallet(456)

  # print("%s -> %s" % (w1.publ_addr, w2.publ_addr))
  # print("Private Key:", w1.priv_key)
  # print("WIF:", w1.WIF)
  # print("Public Key:", w1.publ_key)
  # print("Address:",w1.publ_addr)
  # print("\nPrivate Key:", w2.priv_key)
  # print("WIF:", w2.WIF)
  # print("Public Key:", w2.publ_key)
  # print("Address:",w2.publ_addr)
  exit(0)
  



