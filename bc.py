#!/bin/python3
import os, binascii, hashlib, base58, random, ecdsa
import qrcode

'''

'''

class Wallet:
  def __init__(self, seed):
    self.seed = seed
    self.priv_key, self.WIF, self.publ_key, self.publ_addr = self.generate_wallet_with_seed(self.seed)

      
  def shex(self ,x):
    return binascii.hexlify(x).decode()

  def b58wchecksum(self ,x):
    checksum = hashlib.sha256(hashlib.sha256(x).digest()).digest()[:4]
    return base58.b58encode(x+checksum)

  def ripemd160(self ,x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d

  def generate_wallet_with_seed(self, seed):
    random.seed(seed)
    priv_key = bytes([random.randint(0, 255) for x in range(32)])

    # priv_key -> WIF
    WIF = self.b58wchecksum(b"\x80" + priv_key)

    # get public key
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = b"\x04" + vk.to_string()
    hash160 = self.ripemd160(hashlib.sha256(publ_key).digest()).digest()
    publ_addr = self.b58wchecksum(b"\x00" + hash160)
  
    return self.shex(priv_key), WIF, self.shex(publ_key), publ_addr
  
  def save_qr_png(self):
    qr = qrcode.make(self.publ_addr)
    qr.save('./qrcode-of-%s.png' % self.seed)

w1 = Wallet(1337)
w2 = Wallet(1338)

print("%s -> %s" % (w1.publ_addr, w2.publ_addr))
# print("Private Key:", w1.priv_key)
# print("WIF:", w1.WIF)
# print("Public Key:", w1.publ_key)
# print("Address:",w1.publ_addr)

# print("\nPrivate Key:", w2.priv_key)
# print("WIF:", w2.WIF)
# print("Public Key:", w2.publ_key)
# print("Address:",w2.publ_addr)



