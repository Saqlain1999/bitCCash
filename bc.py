#!/bin/python3
from Wallet import Wallet

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



