import TestLockObjOne
import TestLockObjTwo
import threading
import time


test_share_list = []

def main():
    global test_share_list
    test_obj_1 = TestLockObjOne.TestObjOne(test_share_list)
    test_obj_2 = TestLockObjTwo.TestObjTwo(test_share_list)

    test_thread_1 = threading.Thread(target=test_obj_1.BeginTest)
    test_thread_2 = threading.Thread(target=test_obj_2.BeginTest)

    test_thread_1.start()
    time.sleep(1)
    test_thread_2.start()

    test_thread_1.join()
    test_thread_2.join()

    print "test_share_list is {0}".format(test_share_list)



if __name__ == '__main__':
    main()
