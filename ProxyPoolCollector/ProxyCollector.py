#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''
import requests
import re
import os
import time
import datetime
import threading
from bs4 import BeautifulSoup
from Lock import ThreadLock
from conf import ProxyPoolConfig

class Collector(object):
    def __init__(self, is_ok_event):
        self.__m_target_url = ProxyPoolConfig.config_instance.get_url
        self.__m_heads = ProxyPoolConfig.config_instance.get_headers
        self.__m_proxy_pool = []
        self.__m_get_proxy_time_stamp = ProxyPoolConfig.config_instance.get_time_stamp
        self.__is_to_exit = False
        self.__file_name = ProxyPoolConfig.config_instance.get_savefile_name
        self.__m_event = is_ok_event
        self.m_exit_flag_threadlock = threading.Lock()

    def __del__(self):
        self.__m_proxy_pool = []

    def get_is_to_exit_flag(self):
        return self.__is_to_exit

    def set_is_to_exit_flag(self, value):
        self.m_exit_flag_threadlock.acquire()
        self.__is_to_exit = value
        self.m_exit_flag_threadlock.release()


    #Parse the url xicidaili.com
    def parse_xici_com(self):
        # the regular expression which is used to abstract the ip of proxy
        proxy_ip_re_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        # the regular expression which is used to abstract the verification time of proxy
        proxy_verf_time_pattern2 = re.compile(r'\d+\-\d+\-\d+')
        # get the local time
#        local_time = int(time.strftime('%Y%m%d', time.localtime(time.time())))
        tmp_today_date = datetime.date.today()
        tmp_yesterday_date = tmp_today_date - datetime.timedelta(days=1)

        today_date = int(''.join(str(tmp_today_date).split('-')))
        yesterday_date = int(''.join(str(tmp_yesterday_date).split('-')))

        is_last_two_days_flag = True
        page_number = 1
        visit_page_url = self.__m_target_url + str(page_number)
        
        m_session = requests.session()
        while is_last_two_days_flag:
            req = m_session.get(visit_page_url, headers = self.__m_heads)
            # use beautifulsoup to parse html
            bs = BeautifulSoup(req.text, 'lxml')

            for item in bs.select('body #wrapper #body #ip_list tr')[1:]:
                # get the verification time of proxy from html
                orig_verf_time = item.find(text = proxy_verf_time_pattern2)
                # handle the verification time for campare with local time
                handled_veri_time = int('20' + ''.join(orig_verf_time.split(' ')[0].split('-')))
                # just abstract the proxy ip which is verified in the last two days
                if (handled_veri_time == today_date) or (handled_veri_time == yesterday_date):
                    # abstract the ip and port of proxy from html
                    proxy_ip = item.find(text = proxy_ip_re_pattern)
                    proxy_port = item.find_all('td')[2].string
                    proxy = proxy_ip + ":" + proxy_port
            
                    self.__m_proxy_pool.append(proxy)
                
                else:
                    is_last_two_days_flag = False
                    print 'get the last page %d' % (page_number)
                    break
                
            if is_last_two_days_flag:
                print 'get page %d' % (page_number)
                page_number += 1
                visit_page_url = self.__m_target_url + str(page_number)
        
        print len(self.__m_proxy_pool)
        return

    def save_proxy(self):
        # txt file is shared by collect thread and listen thread
        # so it should lock for the thread safe of data
        with ThreadLock.SaveFile_ThreadLock:
            if os.path.isfile(self.__file_name):
                os.remove(self.__file_name)
            for item in self.__m_proxy_pool:
                need_to_save_proxy = "http://" + item + os.linesep
                with open(self.__file_name, "a") as fp:
                    fp.write(need_to_save_proxy)
#                fp.close()

        print "Save Proxy Pool Success!"
        self.__m_proxy_pool = []

    def get_proxy_pool(self):
        self.parse_xici_com()
        self.save_proxy()
        self.__m_event.set()
        self.__m_event.clear()

        while 1:
            current_time = int(time.strftime("%H%M%S", time.localtime(time.time())))
            find_key = str(int(time.strftime("%H%M", time.localtime(time.time()))))

            if find_key in self.__m_get_proxy_time_stamp:
                if (current_time - int(self.__m_get_proxy_time_stamp[find_key])) in range(-5, 6):
                    self.parse_xici_com()
                    self.save_proxy()

            self.m_exit_flag_threadlock.acquire()
            if self.__is_to_exit:
                break
            self.m_exit_flag_threadlock.release()

            time.sleep(10)

'''
    #Verify the proxy is available or not, and save the available proxy in a txt file
    def abstract_proxy_available(self):
        fail_num = 0
        success_num = 0
        if os.path.isfile("ProxyPool.txt"):
            os.remove("ProxyPool.txt")
#       m_session = requests.session()
        verify_url = "http://icanhazip.com/"
        for item in self.__m_proxy_pool:
            proxies = dict(http = "http://" + item)

            req = requests.get(verify_url, headers = self.__m_heads, proxies = proxies)


            except:
                print req.status_code
                print "proxy %s is not available" % (item)
                self.__m_proxy_pool.pop(self.__m_proxy_pool.index(item))
                fail_num += 1
                print "now fail_num = %d" % (fail_num)
                continue

            else:
                print req.status_code
                available_proxy = proxies['http'] + os.linesep

                fp = open("ProxyPool.txt", "a")
                fp.write(available_proxy)
                fp.close()
                success_num += 1
                print "now success_num = %d" % (success_num)

        print "success_num = %d, fail_num = %d" % (success_num, fail_num)

'''



