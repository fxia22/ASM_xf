#!/usr/bin/python

from Crypto.Cipher import AES
import md5

def random():
    fd = file("/dev/random","rb")
    r = fd.read(16)
    return r

def encrypt(key, data):
    digest = md5.new(key).digest()
    data = random() + data
    if (len(data) % 16) != 0:
        data = data + ' '*(16-(len(data)%16))
    a=AES.new(digest,AES.MODE_CBC)
    e = a.encrypt(data)
    out = ""
    for k in e:
        out = out + "%02x" % ord(k)
    return out

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Syntax: python encrypt.py <filename>"
        print sys.argv
        sys.exit(0)
    print "Enter passkey:",
    key = sys.stdin.readline().strip()
    data = file(sys.argv[1],"rb").read()
    e = encrypt(key,data)
    print "Encrypted:"
    print e
