import threading

SaveFile_ThreadLock = threading.Lock()
VariFile_ThreadLock = threading.Lock()



def SaveFileLock():
    SaveFile_ThreadLock.acquire()

def SaveFileUnLock():
    SaveFile_ThreadLock.release()

def VariFileLock():
    VariFile_ThreadLock.acquire()

def VariFileUnLock():
    VariFile_ThreadLock.release()