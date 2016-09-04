from Lock import ThreadLock
import random

class TestObjTwo(object):
    def __init__(self, share_list):
        self._list = share_list
        print "TestObjTwo Init"

    def BeginTest(self):
        print "TestObjTwo begin to test!"
        ThreadLock.Lock()
        for i in range(5):
            rand_loc = random.randint(0, 9 - i)
            print "TestObjTwo pop the list[{0}]".format(rand_loc)
            print self._list.pop(rand_loc)

        print self._list
        ThreadLock.UnLock()
