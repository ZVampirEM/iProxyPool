# iProxyPool

若想获得代理，需要引入iProxyPool模块

通过ConnectToProxyPool接口连接到代理池

通过ReqProxy接口获取代理，目前支持获取代理数量范围为1-99个，当然视目前数据库中储存的可用代理数量，可能会返回少于请求数量的代理。参数为所要请求的代理数量。

获取到的代理通过链表的形式返回。

获取代理后，调用ReleaseConnect来释放与代理池的连接
