from ThreadBase import ThreadBaseModule
import RequestListener
import socket

class RequestListenerThread(ThreadBaseModule.OriginalThread):
    def __init__(self):
        self.request_listener = RequestListener.Listener()
        ThreadBaseModule.OriginalThread.__init__(self)

    def Initialize(self):
        self.request_listener.create_socket_server()
        return True

    def Run(self):
        self.request_listener.listening_request()

    def ExitInstance(self):
        del self.request_listener

    def Stop(self):
        # close the listener socket and worker socket
        self.request_listener.set_is_to_exit()
        close_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_socket.connect(('127.0.0.1', 7777))
        close_socket.send('exit')
        close_socket.close()

        self.thread_instance.join()
        print "Listener Thread Stop Success!"


