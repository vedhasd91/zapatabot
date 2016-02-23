#! /usr/bin/python
import time
import threading

eflag=0

#Threading class to invoke networkhandler
class networkThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        networkhandler(self.name, self.counter, 5)
        print "Exiting " + self.name

def networkhandler(param, delay,counter):
	print "In network handler"
	while counter:
		if eflag:
			param.exit()
		time.sleep(delay)
	print "%s %s "%(param, time.ctime(time.time()))
	counter-=1
	return 0

def gpshandler(param, delay):
	print "In gps handler"
	return 0

def classhandler():
	return 0

if __name__ == "__main__":
	print "============================"
	print "		MASTER NODE        "
	print "============================"
	thread1=networkThread(1,"NThread",1)
	thread2=networkThread(2,"GThread",2)
	thread1.start()
	thread2.start()
	print "goodbye"
