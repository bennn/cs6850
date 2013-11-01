"""
    Question!
    Can we have one program read a file while another writes to it?
"""
import hashlib
import threading
import time

class Reader(threading.Thread):
    
    def __init__(self, fname):
        threading.Thread.__init__(self)
        self.filename = fname

    def run(self):
        print "HELLO READER"
        with open(self.filename, "r") as f:
            while (True):
                time.sleep(.5)
                print( "i just read: %s" % next(f))

class Writer(threading.Thread):
    
    def __init__(self, fname):
        threading.Thread.__init__(self)
        self.filename = fname
        
    def run(self):
        print "HELLO WRITER"
        with open(self.filename, "w") as f:
            while (True):
                f.write("hai hai hai\n")
                f.flush()
                time.sleep(0.2)

Writer("fun.txt").start()
time.sleep(1)
Reader("fun.txt").start()

# That does work. Dangerous, but works
