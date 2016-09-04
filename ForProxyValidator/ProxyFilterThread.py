#-*- coding=utf-8 -*-

'''
Created on Aug 23, 2016

@author: enming.zhang
'''

import ProxyFilter
from ThreadBase import ThreadBaseModule

class FilterThread(ThreadBaseModule.OriginalThread):
    def __init__(self):
        self.m_filter_instance = ProxyFilter.Filter()
        ThreadBaseModule.OriginalThread.__init__(self)
        
    def Initialize(self):
        return True
    
    def Run(self):
        self.m_filter_instance.filter_run()
    
    def ExitInstance(self):
        del self.m_filter_instance

    def Stop(self):
        self.m_filter_instance.set_is_to_exit()
        print self.m_filter_instance.m_is_wait
        if self.m_filter_instance.m_is_wait:
            self.m_filter_instance.m_thread_event.set()
            self.m_filter_instance.m_thread_event.clear()
        self.thread_instance.join()
        print "Filter Thread Stop Success!"