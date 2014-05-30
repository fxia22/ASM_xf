#!d:/usr/djgpp/bin/python/python.exe


# Written by Bram Cohen
# see LICENSE.txt for license information

from os import listdir
from os.path import join, split
from threading import Event
from traceback import print_exc
from sys import argv
from btmakemetafile import calcsize, make_meta_file, ignore

def dummy(x):
    pass

def completedir(dir, url, flag = Event(), vc = dummy, fc = dummy, piece_len_pow2 = None):
    files = listdir(dir)
    files.sort()
    ext = '.torrent'

    togen = []
    for f in files:
        if f[-len(ext):] != ext and (f + ext) not in files:
            togen.append(join(dir, f))
        
    total = 0
    for i in togen:
        total += calcsize(i)

    subtotal = [0]
    def callback(x, subtotal = subtotal, total = total, vc = vc):
        subtotal[0] += x
        vc(float(subtotal[0]) / total)
    for i in togen:
        fc(i)
        try:
            t = split(i)[-1] 
            if t not in ignore and t[0] != '.':
                make_meta_file(i, url, flag = flag, progress = callback, progress_percent=0, piece_len_exp = piece_len_pow2)
        except ValueError:
            print_exc()

def dc(v):
    print v

if __name__ == '__main__':
    completedir(argv[1], argv[2], fc = dc)
