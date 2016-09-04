from ProxyPoolClient import iProxyPool

def testMain():
    proxy_list = []
    iProxyPool.ConnectToProxyPool()
    proxy_list = iProxyPool.ReqProxy(10)

    print proxy_list
    print len(proxy_list)

    iProxyPool.ReleaseConnect()



if __name__ == '__main__':
    testMain()