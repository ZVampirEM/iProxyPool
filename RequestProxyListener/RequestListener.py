import socket
import threading
import re
import time
from Lock import ThreadLock
from conf import ProxyPoolConfig


class Listener(object):
    def __init__(self):
        self.__m_listen_addr = ProxyPoolConfig.config_instance.get_listen_addr
        self.__m_listen_port = ProxyPoolConfig.config_instance.get_listen_port
        self.socket_server = None
        self.__m_send_proxy_list = []
        self.__proxy_vari_file = ''
        self.request_num_pattern = re.compile(r'R_(\d+)')
        self.__m_is_to_exit = False
        self.m_accept_connect_num = 0
        self.m_exit_flag_threadlock = threading.Lock()
        self.m_connect_num_lock = threading.Lock()

    def __del__(self):
        self.socket_server.close()

    def set_is_to_exit(self):
        self.m_exit_flag_threadlock.acquire()
        self.__m_is_to_exit = True
        self.m_exit_flag_threadlock.release()


    def create_socket_server(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SET ADDRESS REUSE
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # BIND
        self.socket_server.bind((self.__m_listen_addr, int(self.__m_listen_port)))
        # LISTEN
        self.socket_server.listen(5)

#        return my_socket_server

    def Join(self):
        while self.m_accept_connect_num != 0:
            time.sleep(1)


    #listen the request
    def listening_request(self):
        while not self.__m_is_to_exit:
            sock, addr = self.socket_server.accept()
            print "A New Connect, address = %s:%s" % (addr)
            #create handle thread
            handle_thread = threading.Thread(target=self.handle_client_request, args=(sock, addr))
            self.m_connect_num_lock.acquire()
            self.m_accept_connect_num += 1
            self.m_connect_num_lock.release()
            handle_thread.start()

        print "need to stop"
        self.Join()


    def handle_client_request(self, socket_obj, client_addr):
        print "A New Thread to Handle the request for client in address = %s:%s"\
              % (client_addr)

        is_finished = False
        while is_finished == False:
            recv_request = socket_obj.recv(4)
            print recv_request

            match_obj = self.request_num_pattern.match(recv_request)

            if match_obj:
                request_proxy_num = int(match_obj.group(1))
                self.__m_send_proxy_list = self.GetProxy(request_proxy_num)
                socket_obj.send(",".join(self.__m_send_proxy_list))
            elif recv_request == 'exit' or not recv_request:
                is_finished = True

            else:
                continue

        socket_obj.close()
        print "close the connect"
        self.m_connect_num_lock.acquire()
        self.m_accept_connect_num -= 1
        self.m_connect_num_lock.release()
            

    def GetProxy(self, request_num):
        proxy_list = []
        today = str(int(time.strftime("%Y%m%d", time.localtime(time.time()))))
        self.__proxy_vari_file = 'VariableProxy' + today + '.txt'
        with ThreadLock.VariFile_ThreadLock:
            try:
                with open(self.__proxy_vari_file, 'r') as proxy_pool_fp:
                    variable_proxy_list = proxy_pool_fp.readlines()
                    if len(variable_proxy_list) < request_num:
                        request_num = len(variable_proxy_list)
                    while len(proxy_list) != request_num:
                        proxy_list.append(variable_proxy_list.pop(0)[0:-1])
                        
            except:
                print "There is not any variable proxy!"
                proxy_list.append("There Is Not Any Variable Proxy!")
                
        return proxy_list



#close listener socket -- > self.socket_server and working socket