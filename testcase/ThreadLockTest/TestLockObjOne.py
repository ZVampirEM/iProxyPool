from Lock import ThreadLock
import random
import time

class TestObjOne(object):
    def __init__(self, share_list):
        self._list = share_list
        print "TestObjOne Init!"

    def BeginTest(self):
        print "TestObjOne begin to test!"
        ele_num = 10
        ThreadLock.Lock()
        while ele_num != 0:
            rand_num = random.randint(1, 100)
            print "TestObjOne append {0} to share list!".format(rand_num)
            self._list.append(rand_num)
            ele_num -= 1
            time.sleep(2)

        print self._list
        ThreadLock.UnLock()
